#!/usr/bin/python

import sys
from Xlib import X, display, Xutil, Xatom

from argparse import ArgumentParser

def     cmdline():

    parser = ArgumentParser()

    #parser.add_argument('fnames', metavar='fname',  nargs='+',
    #                help='The two file names to compare. [REF / SRC1 .. SRCN]')

    parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose",
                  help="print extended status messages to stdout")
    parser.add_argument("-d", "--doc",
                  action="store_true", dest="doc",
                  help="print docstr")
    parser.add_argument("-q", "--quiet",
                  action="store_true", dest="quiet",
                  help="don't print status messages to stdout")
    parser.add_argument("-e", "--echo",
                  action="store_true", dest="echo",
                  help="echo newer status to stdout")
    parser.add_argument("-l", "--lib", dest="libx",
                  action="store", default="X",
                  help="Which lib to search (X, display, Xutil)")
    return parser


def main():

    global clargs
    parser = cmdline(); clargs = parser.parse_args()

    if clargs.verbose:
        print("args:", clargs)

    try:
        mm = eval(clargs.libx)
    except:
        print("look for", clargs.libx)
        exec("import " + clargs.libx)
        mm = eval(clargs.libx)
    print("mm:", mm)
    if clargs.doc:
        print(getattr(mm, "__doc__"))
        sys.exit(0)
    #print(mm)
    dd = dir(mm)
    for aa in dd:
        if aa[:2] == "__":
            continue
        print (aa, getattr(mm, aa))
    sys.exit(0)

if __name__ == '__main__':
    main()
