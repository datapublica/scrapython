"""Presentation generator

Usage:
    main.py serve
    main.py build
    main.py (-h | --help)
    main.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""


from __future__ import print_function
from docopt import docopt
from bottle import run, get, static_file, post, request
import re
from run import eval_code
import sys


# Compatibility
def to_uni(s):
    if sys.version_info >= (3, 0):
        return str(s)
    else:
        return unicode(s)


def open_file_uni(fname, mode):
    if sys.version_info < (3, 0):
        import codecs
        return codecs.open(fname, mode, encoding="utf8")
    else:
        return open(fname, mode)
# /Compatibility


def wrap_result(snippets, with_fragment=True):

    def tpl(snippet, result):
        if sys.version_info < (3, 0):
            snippet = snippet.decode("utf8")

        res = snippet.replace("<", "&lt;").replace(">", "&gt;") + "\n"

        frag = "fragment" if with_fragment else ""
        if result is not None:
            result = to_uni(result)
            result = result.replace("<", "&lt;").replace(">", "&gt;")
            res += u"<code class='%s result'>%s</code>" % (frag, result)

        return res

    snippets = [tpl(*s) for s in snippets]

    return snippets


def hide_nodisplay(snippets):
    snippets = re.sub(" *## nodisplay.*\n((?:.|\n)*?) *## /nodisplay\n",
                      "<span style='display:None;'>\\1</span>",
                      snippets,
                      flags=re.M)
    return snippets


class ExampleCache:
    def __init__(self):
        self.cache = {}

    def get(self, expr):
        group = expr.group(1).split(":")
        filename = None
        options = ""

        if len(group) == 1:
            (filename,) = group
        elif len(group) == 2:
            (filename, options) = group

        options = set([e.strip() for e in options.split(",")])

        if filename not in self.cache:
            content = open("examples/%s" % filename).read()
            # Remove headers
            content = re.sub("# -\\*-.*-\\*-", "", content)

            exec_ = "exec" in options

            if exec_:
                snippets = eval_code(content, filename)
            else:
                snippets = [(content, None)]

            ext = filename.rsplit(".", 1)[1]
            lang = {"py": "python", "sh": "bash",
                    "json": "json", "html": "html"}[ext]

            snippets = wrap_result(snippets, False)
            snippets = ''.join(snippets)
            snippets = ("<pre><code"
                        " class='snippet %s %s'"
                        " data-trim"
                        " %s"
                        " data-noescape>"
                        "%s"
                        "</code></pre>"
                        "<div class='source'>"
                        "  <a class='source' href='examples/%s'>"
                        "  source"
                        "  </a>"
                        "</div>"
                        ) % ("exec" if exec_ else "",
                             lang,
                             "contenteditable" if exec_ else "",
                             snippets,
                             filename)
            snippets = hide_nodisplay(snippets)
            self.cache[filename] = snippets

        snippets = self.cache[filename]

        return snippets


@get('/')
def index():
    cache = ExampleCache()
    x = re.compile(u"{{([-\\w/\\.:]*)}}", re.U)
    content = open_file_uni("template.html", "r").read()
    return x.sub(cache.get, content)


@post('/eval')
def evalpy():
    content = request.json["code"]
    print(content)

    snippets = eval_code(content)
    snippets = wrap_result(snippets, False)

    return {"eval": ''.join(snippets)}


@get('/<path:path>')
def static(path):
    return static_file(path, ".")


if __name__ == "__main__":
    arguments = docopt(__doc__, version='1.0')
    if arguments["serve"]:
        run(host="0.0.0.0", port=8000, debug=True, reloader=True, quiet=False)
    else:
        open_file_uni("index.html", "w").write(index())
