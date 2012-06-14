import clang.cindex
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
    if parents == None:
	parents = []
    if node.displayname == glob and \
       node.kind != CursorKind.VAR_DECL and \
       node.kind == CursorKind.DECL_REF_EXPR:
	print " > ", str(node.location.file) + ":" + ("%5i" % node.location.line) + ",",# filecache[node.location.file.name][node.location.line],
	print "in %s:" % (",".join([p.displayname for p in parents if p.kind == CursorKind.FUNCTION_DECL])),
	print filecache[node.location.file.name][node.location.line].strip()
#	if parent:
#	  print " >> ", str(parent.kind).split(".")[1]

    for child in node.get_children():
	find_usage(child, glob, parents + [node])

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
        find_usage(tu.cursor, glob)
	print "-" * 40
	print ""

main("test.cpp")
