# python standard imports
import re
from typing import Iterable
from copy import copy
from pathlib import Path

# third-party imports
from yaml import safe_load, safe_dump

# internal imports
from .tokens import TokenType, StringBuilder
from .defaults import TEMPLATE_YAMLS, BASIC_ID_REGEX

_DEFAULT_CITATOR = None

class Citation:
    """
    A legal reference found in text.
    
    Attributes:
        tokens: dictionary of the values that define this citation, such
            as its volume and page number, or its title, section, and
            subsection, etc.
        template: the template whose regexes detected/created this
            citation
        name: a uniform, canonical representation of this citation,
            made by the template's name_builder.
        URL: the location, if any, where this citation can be found
            online. Created by the template's URL_builder.
        match: the regex match object from which the citation was
            created
        raw_tokens: dictionary of tokens as captured in the original
            match object, prior to being normalized. Note that for child
            citations, raw_tokens will include any raw_tokens inferred
            from the parent citation.
        idform_regexes: list of regex pattern objects to find child
            citations later in the text, valid until the next different
            citation appears.
        shortform_regexes: list of regex pattern objects to find
            child citations anywhere in the subsequent text
        parent: the earlier citation, if any, that this citation is a
            shortform or idform child of
    """
    
    def __init__(
        self,
        match: re.match,
        template,
        parent = None,
    ):
        self.match = match
        self.span = match.span()
        self.template = template
        self.parent = parent
        self.tokens = {}
        self.raw_tokens = match.groupdict()
        
        # copy raw_tokens (in order) from the parent citation, but
        # stop at the first one that the child citation overwrites
        if parent:
            merged_tokens = {}
            for k in template.tokens.keys():
                if self.raw_tokens.get(k):
                    merged_tokens.update(self.raw_tokens)
                    break
                else:
                    merged_tokens[k] = parent.raw_tokens.get(k)
            self.raw_tokens = merged_tokens
        
        # normalize raw_tokens to get consistent token values across
        # differently-formatted citations to the same source.
        # This will raise a SyntaxError if a mandatory edit fails
        for name, ttype in template.tokens.items():
            value = self.raw_tokens.get(name)
            self.tokens[name] = ttype.normalize(value)
        
        # Finally, compile the citation's idform and shortform regexes.
        # To avoid unneccessary work, first try to copy regexes from the
        # parent citation if applicable.
        
        if parent and parent.raw_tokens == self.raw_tokens:
        # then we can safely copy the parent's regexes to the child
            self.idform_regexes = parent.idform_regexes
            self.shortform_regexes = parent.shortform_regexes
            return
        
        # otherwise we'll need to compile new shortform regexes,
        # but we can still copy some of them from the parent
        
        kwargs = {'replacements': self.raw_tokens, 'token_prefix': 'same'}
        if parent:
        # we can copy regexes, but only if they do not reference a
        # specific value from the citation, e.g. {same volume}.
            self.shortform_regexes = [
                (
                    re.compile(_process_pattern(pattern, **kwargs))
                    if '{same ' in pattern else parent.shortform_regexes[i]
                )
                for i, pattern in enumerate(template._processed_shortforms)
            ]
            
            self.idform_regexes = [
                (
                    re.compile(_process_pattern(pattern, **kwargs))
                    if '{same ' in pattern else parent.idform_regexes[i]
                )
                for i, pattern in enumerate(template._processed_idforms)
            ]
            
        else: # compile all-new idforms and shortforms
            self.shortform_regexes = [
                re.compile(_process_pattern(pattern, **kwargs))
                for pattern in self.template._processed_shortforms
            ]
            self.idform_regexes = [
                re.compile(_process_pattern(pattern, **kwargs))
                for pattern in self.template._processed_idforms
            ]
        self.idform_regexes.append(BASIC_ID_REGEX)

    def from_str(cite_text: str, citator='DEFAULT'):
        """
        Convenience method to quickly define a citation using a
        citator's lookup() method. Uses the default citator if none is
        provided.
        """
        if citator == 'DEFAULT':
            citator = _get_default_citator()
        return citator.lookup(cite_text)
    
    def build_URL(self) -> str:
        "Build a URL to somewhere this citation can be found online"
        if not self.template.URL_builder:
            return None
        url =  self.template.URL_builder(self.tokens)
        if url:
            url = url.replace(' ', '%20')
        return url
    
    def build_name(self, fallback: bool=True) -> str:
        "Build a canonical name for this citation."
        if self.template.name_builder:
            return self.template.name_builder(self.tokens)
        elif fallback:
            return str(self)
        else:
            return None
    
    def get_shortform_cites(self) -> Iterable:
        keep_trying = True
        span_start = self.span[1]
        while keep_trying:
            try:
                match = next(_match_regexes(
                    regexes=self.shortform_regexes,
                    text=self.match.string,
                    span=(span_start,),
                ))
                span_start = match.span()[1]
                try:
                    yield Citation(
                        match=match,
                        template=self.template,
                        parent=self,
                    )
                except SyntaxError: # it's an invalid citation
                    pass
            except StopIteration:
                keep_trying = False
    
    def get_idform_cite(self, until_index: int=None):
        try:
            match = next(_match_regexes(
                regexes = self.idform_regexes,
                text = self.match.string,
                span = (self.span[1], until_index)
            ))
            return Citation(match=match, template=self.template, parent=self)
        except StopIteration:
            return None
        except SyntaxError:
            return None
    
    def get_next_child(self, span: tuple=None):
        try:
            match = next(_match_regexes(
                regexes = self.shortform_regexes + self.idform_regexes,
                text = self.match.string,
                span = span if span else (self.span[1], ),
            ))
            return Citation(match=match, template=self.template, parent=self)
        except StopIteration:
            return None
    
    def __str__(self):
        return str(self.match.group())
    
    def __repr__(self):
        return (
            f'Citation(match={self.match}, template={repr(self.template)}'
            + (f', parent={repr(self.parent)}' if self.parent else '')
        )
    
    def __contains__(self, other_citation):
        """
        Returns true if both citations are from templates with the same
        name, and the other citation references a subset of this one.
        """
        if (
            other_citation.template.name != self.template.name
            or other_citation.tokens == self.tokens
        ):
            return False
        for key, value in self.tokens.items():
            if value and other_citation.tokens.get(key) != value:
                if (
                    self.template.tokens[key].severable
                    and other_citation.tokens[key].startswith(value)
                ):
                    continue
                else:
                    return False
        else:
            return True
    
    def __eq__(self, other_citation):
        return (
            other_citation.template.name == self.template.name
            and other_citation.tokens == self.tokens
        )
    
    def __getattr__(self, name):
        if name in ['URL', 'url']:
            self.__dict__[name] = self.build_URL()
            return self.__dict__[name]
        elif name == 'name':
            self.name = self.build_name(fallback=False)
            return self.name
        else:
            raise AttributeError(
                f"'Citation' object has no attribute '{name}'"
            )
    
    def __len__(self):
        return len(str(self))



class Template:
    """
    A pattern to recognize a single kind of citation and extract
    information from it.
    """
    def __init__(
        self,
        name: str,
        tokens: dict[str, TokenType] = {},
        meta: dict[str, str] = {},
        patterns: list[str] = [],
        broad_patterns: list[str] = [],
        shortform_patterns: list[str] = [],
        idform_patterns: list[str] = [],
        name_builder: StringBuilder = None,
        URL_builder: StringBuilder = None,
        inherit_template = None,
    ):
        """
        Arguments:
            name: the name of this template
            
            tokens: The full dictionary of TokenTypes that citations from
                this template can contain. These must be listed in order
                from least-specific to most. For instance, the U.S.
                Constitution's template puts 'article' before 'section'
                before 'clause', because articles contain sections, and
                sections contain clauses.
            
            patterns: Patterns are essentially regexes to recognize
                recognize long-form citations to this template. However,
                wherever a token would appear in the regex, it should be
                replaced by the name of the token, enclosed in curly
                braces.
                
                Patterns are matched in the order that they are listed,
                so if there is a pattern that can only find a subset of
                tokens, it should be listed after the more-complete
                pattern so that the better match won't be precluded.
            
            broad_patterns: Same as `patterns`, except that they will
                only be used in contexts like search engines, where
                convenience is more important than avoiding false
                positive matches. When used, they will be used in
                addition to the normal patterns.
            
            shortform_patterns: Same as `patterns`, but these will only
                go into effect after a longform citation has been
                recognized. If a shortform pattern includes "same
                <token name>" in curly braces, e.g. "{same volume}", the
                bracketed portion will be replaced with the exact text
                of the corresponding `raw_token` from the long-form
                citation.
            
            idform_patterns: Same as `shortform_patterns`, except that
                they will only be used to scan text until the next
                different citation occurs.
            
            URL_builder: `StringBuilder` to construct URLs for found
                citations
            
            name_builder: `StringBuilder` to construct canonical names
                of found citations
            
            meta: Optional metadata relating to this template. Patterns
                and StringBuilders can access metadata fields as if they
                were tokens, though fields can be overridden by tokens
                with the same name.
            
            inherit_template: another `Template` whose values this one
                should copy unless expressly overwritten.
        """
        kwargs = locals()
        for attr, default in {
            'name':               None,
            'tokens':             {},
            'patterns':           [],
            'broad_patterns':     [],
            'shortform_patterns': [],
            'idform_patterns':    [],
            'URL_builder':        None,
            'name_builder':       None,
            'meta':               {},
        }.items():
            if inherit_template and kwargs[attr] == default:
                value = inherit_template.__dict__.get(attr)
            else:
                value = kwargs[attr]
            self.__dict__[attr] = value
        
        # update inherited StringBuilders with the correct metadata
        if inherit_template and self.meta:
            if self.URL_builder:
                self.URL_builder = copy(self.URL_builder)
                self.URL_builder.defaults = self.meta
            if self.name_builder:
                self.name_builder = copy(self.name_builder)
                self.name_builder.defaults = self.meta
        
        # use the template's metadata and tokens to make a dictionary
        # of replacements to insert into the regexes before compilation
        replacements = {k:str(v) for (k, v) in self.meta.items()}
        replacements.update({
            k:f'(?P<{k}>{v.regex})'
            for (k,v) in self.tokens.items()
        })
        
        # compile the template's regexes and broad_regexes
        self.regexes = []
        self.broad_regexes = []
        for kind in ['regexes', 'broad_regexes']:
            if kind == 'broad_regexes':
                pattern_list = self.patterns + self.broad_patterns
                flags = re.I
            else:
                pattern_list = self.patterns
                flags = 0
            
            for p in pattern_list:
                pattern = _process_pattern(
                    p,
                    replacements,
                    add_word_breaks=True)
                try:
                    regex = re.compile(pattern, flags)
                    self.__dict__[kind].append(regex)
                except re.error as e:
                    i = 'broad ' if kind == 'broad_regexes' else ''
                    raise re.error(
                        f'{self} template\'s {i}pattern "{pattern}" has '
                        f'an error: {e}'
                    )
        
        self._processed_shortforms = [
            _process_pattern(p, replacements, add_word_breaks=True)
            for p in self.shortform_patterns
        ]
        self._processed_idforms = [
            _process_pattern(p, replacements, add_word_breaks=True)
            for p in self.idform_patterns
        ]
    
    @classmethod
    def from_dict(cls, name: str, values: dict, inheritables: dict={}):
        """
        Return a template from a dictionary of values, like a dictionary
        created by parsing a template from YAML format.
        """
        values = {
            k.replace(' ', '_'):v
            for k,v in values.items()
        }
        
        # when pattern is listed in singular form,
        # replace it with a one-item list
        items = values.items()
        values = {}
        for key, value in items:
            if key.endswith('pattern'):
                values[key + 's'] = [value]
            else:
                values[key] = value
        
        # unrelated: when a single pattern is split
        # into a list (likely to take advantage of
        # YAML anchors), join it into one string
        for k,v in values.items():
            if not k.endswith('patterns'):
                continue
            for i, pattern in enumerate(v):
                if type(pattern) is list:
                    values[k][i] = ''.join(pattern)
        
        inherit = values.get('inherit')
        
        if inherit:
            values.pop('inherit')
            try:
                values['inherit_template'] = inheritables.get(inherit)
            except KeyError:
                raise KeyError(
                    f'Template "{name}" tried to inherit unknown '
                    + f'template "{inherit}"'
                )
        
        for key in ['name_builder', 'URL_builder']:
            data = values.get(key)
            if data:
                data['defaults'] = values.get('meta') or {}
                values[key] = StringBuilder.from_dict(data)
        values['tokens'] = {
            k: TokenType.from_dict(k, v)
            for k,v in values.get('tokens', {}).items()
        }
        return cls(name=name, **values)
    
    def to_dict(self) -> dict:
        "save this Template to a dictionary of values"
        output = {}
        if self.meta:
            output['meta'] = self.meta
        output['tokens'] = {
            k:v.to_dict() for k, v in self.tokens.items()
        }
        for key in ['patterns', 'shortform_patterns', 'idform_patterns']:
            value = self.__dict__.get(key)
            if not value:
                continue
            elif len(value) > 1:
                output[key] = value
            else: # de-pluralize lists that contain only one pattern
                output[key[:-1]] = value[0]
        for key in ['name_builder', 'URL_builder']:
            if self.__dict__.get(key):
                output[key] = self.__dict__[key].to_dict()
        
        spaced_output = {k.replace('_', ' '):v for k, v in output.items()}
        
        return spaced_output
    
    def to_yaml(self) -> str:
        "save this Template to a YAML string"
        return safe_dump(
            {self.name: self.to_dict()},
            sort_keys = False,
            allow_unicode = True,
        )
    
    def lookup(self, text, broad: bool=True, span: tuple=(0,)) -> Citation:
        """
        Return the first citation that matches this template. If 'broad'
        is True, case-insensitive matching and broad regex patterns will
        be used. If no matches are found, return None.
        """
        regexes = self.broad_regexes if broad else self.regexes
        matches = _match_regexes(text, regexes, span=span)
        for match in matches:
            try:
                return Citation(match, self)
            except SyntaxError: # invalid citation
                continue
        else:
            return None
    
    def list_longform_cites(self, text, broad: bool=False, span: tuple=(0,)):
        """
        Get a list of all long-form citations to this template found in
        the given text.
        """
        cites = []
        regexes = self.broad_regexes if broad else self.regexes
        for match in _match_regexes(text, regexes, span=span):
            try:
                cites.append(Citation(match, self))
            except SyntaxError:
                continue
        return cites
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return (
            f'Template(name="{self.name}"'
            + (f', tokens={self.tokens}' if self.tokens else '')
            + (f', meta={self.meta}' if self.meta else '')
            + (f', patterns={self.patterns}' if self.patterns else '')
            + (
                f', broad_patterns={self.broad_patterns}' 
                if self.broad_patterns else ''
            )
            + (
                f', shortform_patterns={self.shortform_patterns}'
                if self.shortform_patterns else ''
            )
            + (
                f', idform_patterns={self.idform_patterns}'
                if self.idform_patterns else ''
            )
            + (
                f', name_builder={self.name_builder}'
                if self.name_builder else ''
            )
            + (
                f', URL_builder={self.URL_builder}'
                if self.URL_builder else ''
            )
            + ')'
        )
    
    def __contains__(self, citation: Citation):
        return citation.template.name == self.name
    
    def __eq__(self, other_template):
        return repr(self) == repr(other_template)



class Citator:
    """
    A collection of citation templates, and the tools to match text
    against them en masse.
    
    Attributes:
        templates: a dictionary of citation templates that this citator
            will try to match against
    """
    
    def __init__(
        self,
        defaults = [
            'caselaw',
            'general federal law',
            'specific federal laws',
            'state law',
            'secondary sources',
        ],
        yaml_paths: list[str] = [],
        templates: dict[str, Template] = {},
    ):
        """
        Create a citator from any combination of CiteURL's default
        template sets (by default, all of them), plus any custom
        templates you want, either by pointing to custom YAML files or
        making Template objects at runtime.
        
        Arguments:
            defaults: names of files to load from the citeurl/templates
                folder. Each file contains one or more of CiteURL's
                built-in templates relevant to the given topic.
            yaml_paths: paths to custom YAML files to load templates
                from. These are loaded after the defaults, so they can
                inherit and/or overwrite them.
            templates: optional list of Template objects to load
                directly. These are loaded last, after the defaults and
                any yaml_paths.
        """
        self.templates = {}
        for d in defaults or []:
            self.load_yaml(TEMPLATE_YAMLS[d])
        for path in yaml_paths:
            self.load_yaml(Path(path).read_text())
        self.templates.update(templates)
    
    @classmethod
    def from_yaml(cls, yaml: str):
        """
        Create a citator from scratch (no default templates) by loading
        them from the specified YAML string.
        """
        citator = cls(defaults=None)
        citator.load_yaml(yaml)
        return citator
    
    def to_yaml(self):
        "Save this citator to a YAML string to load later"
        yamls = [t.to_yaml() for t in self.templates.values()]
        return '\n\n'.join(yamls)
    
    def load_yaml(self, yaml: str):
        """
        Load templates from the given YAML, overwriting any existing
        templates with the same name.
        """
        for name, data in safe_load(yaml).items():
            self.templates[name] = Template.from_dict(
                name, data, inheritables=self.templates
            )
    
    def lookup(self, potential_citation: str, broad: bool=True):
        for template in self.templates.values():
            cite = template.lookup(potential_citation, broad=broad)
            if cite:
                return cite
        else:
            return None
    
    def list_citations(self, text: str, id_break_regex: str=None):
        # first get a list of all long and shortform (not id.) citations
        longforms = []
        for template in self.templates.values():
            longforms += template.list_longform_cites(text)
        
        shortforms = []
        for longform in longforms:
            shortforms += longform.get_shortform_cites()
        citations = longforms + shortforms
        _sort_and_remove_overlaps(citations)
        
        # determine where to break strings of id. citations
        citation_starts = [c.span[0] for c in citations]
        if id_break_regex:
            other_breaks = [
                match.span()[0] for match in
                re.finditer(id_break_regex, text)
            ]
        else:
            other_breaks = []
        breakpoints = sorted(
            set(citation_starts + other_breaks),
        )
        # for each cite, look for idform citations until the next cite
        idforms = []
        for cite in citations:
            # find the next relevant breakpoint, and delete any
            # breakpoints that are already behind the current citation
            cite_end = cite.span[1]
            for i, breakpoint in enumerate(breakpoints):
                if breakpoint <= cite_end:
                    breakpoints = breakpoints[i+1:]
                    break
            try:
                breakpoint = breakpoints[0]
            except IndexError:
                breakpoint = None
            
            # get the citation's idform child, if any,
            # then that one's idform, and so on.
            idform = cite.get_idform_cite(until_index=breakpoint)
            while idform:
                idforms.append(idform)
                idform = idform.get_idform_cite(until_index=breakpoint)
        
        citations += idforms
        _sort_and_remove_overlaps(citations)
        
        return citations
    
    def __iter__(self):
        return self.templates.values().__iter__()
    
    def __getitem__(self, key):
        return self.templates[key]
    
    def __setitem__(self, key, value):
        self.templates[key] = value
    
    def __eq__(self, other_citator):
        return self.templates == other_citator.templates

########################################################################
# PUBLIC FUNCTIONS
########################################################################

def lookup(text: str, broad: bool = True):
    """
    Convenience function to find a single
    citation in text, using the default citator.
    """
    return _get_default_citator().lookup(text, broad=broad)

def list_citations(text):
    """
    Convenience function to list all citations
    in a text, using the default citator.
    """
    return _get_default_citator().list_citations(text)

########################################################################
# INTERNAL FUNCTIONS
########################################################################

def _process_pattern(
    pattern: str,
    replacements: dict,
    token_prefix: str=None,
    add_word_breaks: bool=False,
):
    for key, value in replacements.items():
        if not value:
            continue
        if token_prefix:
            marker = '{%s %s}' % (token_prefix, key)
        else:
            marker = '{%s}' % key
        if not (value.startswith('(') and value.endswith(')')):
            value = f'({value})'
        pattern = pattern.replace(marker, f'{value}')
    if add_word_breaks:
        pattern = fr'(?<!\w){pattern}(?!\w)'
    return pattern

def _sort_and_remove_overlaps(citations: list):
    """
    For a given list of citations found in the same text, sort them by
    their order of appearance. When two citations overlap, the shorter
    one will be deleted.
    """
    citations.sort(key=lambda x: x.match.span()[0])
    i = 1
    while i < len(citations):
        if citations[i].span[0] < citations[i-1].span[1]:
            if len(citations[i-1]) > len(citations[i]):
                citations.pop(i)
            else:
                citations.pop(i-1)
        else:
            i += 1

def _match_regexes(text: str, regexes: list, span: tuple=(0,)) -> Iterable:
    """
    For a given text and set of regex Pattern objects, generate each
    non-overlapping match found for any regex. Regexes earlier in
    the list take priority over later ones, such that a span of text
    that matches the first regex cannot also match the second.
    """
    start = span[0]
    if len(span) > 1:
        end = span[1]
    else:
        end = None
    
    keep_trying = True
    while keep_trying:
        span = (start, end) if end else (start,)
        matches = []
        for regex in regexes:
            match = regex.search(text, *span)
            if match:
                matches.append(match)
        if matches:
            matches.sort(key=lambda x: (x.span()[0], -len(x.group())))
            start = matches[0].span()[1]
            yield matches[0]
        else:
            keep_trying = False
        
def _get_default_citator():
    global _DEFAULT_CITATOR
    if not _DEFAULT_CITATOR:
        _DEFAULT_CITATOR = Citator()
    return _DEFAULT_CITATOR
