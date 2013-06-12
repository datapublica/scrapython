from __future__ import print_function
import sys
from io import StringIO
from code import compile_command
import traceback


# Inspired from doctest module

# Override some StringIO methods.
class OutputCapture(StringIO):
    def getvalue(self):
        result = StringIO.getvalue(self)
        # If anything at all was written, make sure there's a trailing
        # newline.  There's no way for the expected output to indicate
        # that a trailing newline is missing.
        if result and not result.endswith("\n"):
            result += "\n"
        return result

    def truncate(self, size=None):
        self.seek(size)
        StringIO.truncate(self)
        self.buf = ''

    def write(self, content):
        if sys.version_info < (3, 0):
            content = unicode(content)
            StringIO.write(self, content)
        else:
            StringIO.write(self, content)


def get_result(code, scope, filename, multi):
    try:
        oldout = sys.stdout
        sys.stdout = OutputCapture()
        try:
            if not code.strip()[0] == '#':
                # Exec the code
                mode = "single" if not multi else "exec"
                if sys.version_info >= (3, 0):
                    exec(compile(code + "\n", filename, mode, 0, 1), scope)
                else:
                    ncode = code + "\n"
                    exec(compile(ncode, filename, mode, 0, 1), scope)
            # Get the output
            ret = sys.stdout.getvalue()
            if ret == "":
                ret = None
            if ret is not None:
                # Eval for output
                try:
                    ret = eval(ret)
                except:
                    ret = ret

            return (code, ret)
        except:
            return (code, traceback.format_exc())

    finally:
        sys.stdout = oldout


def count_start_spaces(string):
    spaces = 0

    for char in string:
        if char.isspace():
            spaces += 1
        else:
            break

    return spaces


def snippet_needs_more(snippet, filename):
    try:
        code = compile_command(snippet, filename, "single")
        if code is None:
            return True
        return False

    except:
        return False


def snippet_result(snippet, filename, scope, multi):
    try:
        if len(snippet.strip()) == 0:
            return ("", None)

        code = compile_command(snippet, filename,
                               "exec" if multi else "single")

        if code is not None:
            return get_result(snippet, scope, filename, multi)

        return (snippet, None)

    except:
        return (snippet.strip(), traceback.format_exc())


def eval_code(code, filename="stdin"):
    snippets = []

    scope = {}
    snippet = ""
    multi = False

    for line in code.strip().splitlines():
        # Count spaces
        # If zero, must evaluate (no continuation possible)
        #  (to avoid comments being eat with valid instructions)
        # Else, should concatenate until zero again
        #  and evaluate as "exec", not "single"
        cur_spaces = count_start_spaces(line)

        if ((cur_spaces > 0 or
             (len(snippet) == 0 and snippet_needs_more(line, filename)) or
             snippet_needs_more(snippet, filename))):
            snippet = snippet + line + "\n"
            multi = True
            continue

        if multi:
            res = snippet_result(snippet, filename, scope, True)
            snippet = ""
        else:
            res = snippet_result(line, filename, scope, False)

        snippets.append(res)
        multi = False

    if multi:
        res = snippet_result(snippet, filename, scope, multi)
        snippets.append(res)
    return snippets


if __name__ == "__main__":
    for snippet, res in eval_code(open(sys.argv[1]).read(), sys.argv[1]):
        for idx, line in enumerate(snippet.splitlines()):
            if idx == 0:
                print(">>>", line)
            else:
                print("...", line)
        if res is not None:
            print(res)
