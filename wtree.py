from Xlib.display import Display

def printWindowHierrarchy(window, indent):
    children = window.query_tree().children
    print(indent+"p", window.get_wm_class(), window.get_wm_name())
    for w in children:
        print(indent, w.get_wm_class(), w.get_wm_name())
        printWindowHierrarchy(w, indent + '-----')

display = Display()
root = display.screen().root
printWindowHierrarchy(root, '-----')
