import clang.cindex
import re
from clang.cindex import CursorKind

import collections
class FileCache(collections.defaultdict):
    def __missing__(self, key):
        f = open(key)
	self[key] = [''] + [" " + l.rstrip("\r\n") for l in f.read().splitlines()]
	return self[key]

filecache = FileCache()

def recursor(node, indent=0):
    print "|" * indent + "-", str(node.kind).split(".")[1], node.displayname, node.location, 
    if node.location.file:
      print filecache[node.location.file.name][node.location.line], "-->", filecache[node.location.file.name][node.location.line][node.extent.start.column:node.extent.end.column], "<--"
    else:
      print "(no file)"
    for child in node.get_children():
        recursor(child, indent+1)

def find_usage(node, glob, parents=None):
    matcher = re.compile(glob + r"\s*=[^=]")
    if parents == None:
	parents = []
    if node.displayname == glob and \
       node.kind != CursorKind.VAR_DECL and \
       node.kind == CursorKind.DECL_REF_EXPR:
        line = filecache[node.location.file.name][node.location.line].strip()
        yield {'fileline': line,
                'write': bool(re.findall(glob + r"\s*=[^=]", line)),
                'file': str(node.location.file),
                'line#': node.location.line,
                'infunction': ",".join([p.displayname for p in parents if p.kind == CursorKind.FUNCTION_DECL])}

    for child in node.get_children():
        for entry in find_usage(child, glob, parents + [node]):
            yield entry

def get_globals(parent, file):
    globals = {}
    for node in parent.get_children():
	if node.kind == CursorKind.VAR_DECL and \
           node.location.file.name == file:
            globals[node.displayname] = node
    return globals

def main(file):
    index = clang.cindex.Index.create()
    tu = index.parse(file)
    globals = get_globals(tu.cursor, file)

    globkeys = sorted(globals.keys(), key=lambda x: x.lower())
    for glob in globkeys:
	print glob, "at", globals[glob].location
        results = [res for res in find_usage(tu.cursor, glob)]
        results.sort(key=lambda x: (not x["write"], x["file"], x["line#"]))

        fmt = "in %(file)s, on line %(line#) 6i, in %(infunction)s: %(fileline)s"

        print "\n".join(
            "> " + (fmt % res) for res in results if res["write"])
        print ""
        print "\n".join (
            "  " + (fmt % res) for res in results if not res["write"])
	print "-" * 40
	print ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main("test.cpp")
