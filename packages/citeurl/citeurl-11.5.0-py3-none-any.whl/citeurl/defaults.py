from pathlib import Path
from re import compile

# make dictionary of the built-in citation template files, so
# users can choose which ones they want to load
_yaml_path = Path(__file__).parent.absolute() / 'templates'
TEMPLATE_YAMLS = {}
for path in _yaml_path.iterdir():
    TEMPLATE_YAMLS[path.stem] = path.read_text()

BASIC_ID_REGEX = compile('[Ii](bi)?d\.')

# this does nothing so far
TOKEN_PREFIXES = {
    'title':     '[Tt]it(le|\.)',
    'volume':    '[Vv]ol(ume|\.)',
    'page':      '[Pp](age|\.?)',
    'footnote':  '([Ff]?n\.|([Ff]oot)?note)',
    'article':   '[Aa]rt(icle|\.)',
    'amendment': '[Aa]m(end(ment|\.)|dt?\.?)',
    'chapter':   '[Cc]h(apter |\.)',
    'section':   '[Ss]ec(tion|\.)',
    'paragraph': '[Pp]ar(agraph|a?\.)',
    'clause':    '[Cc]l(ause|\.)',
    'rule':      '[Rr]ule( (number|#|no\.))?',
    'code':      '[Cc]ode of',
}
TOKEN_SUFFIXES = {
    'code': '[Cc]ode',
}
TOKEN_ORDER = [
    'reporter',
    'title',
    'volume',
    'article',
    'amendment',
    'chapter',
    'rule',
    'section',
    'subsection',
    'page',
    'pincite',
    'footnote',
    'clause',
]
