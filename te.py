import sys

def get_filename_from_command_line():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return None

def load_text(filename):
    if not filename:
        return ""
    print('loading ' + filename)
    return "the text"

def edit_text(text):
    print('editing ' + text)

def save_text(text, filename):
    if not filename:
        print('ask for filename')
        print('save ' + text)
    else:
        print('saving ' + text + ' to ' + filename)

def main():
    filename = get_filename_from_command_line()
    text = load_text(filename)
    edit_text(text)
    save_text(text, filename)

main()
