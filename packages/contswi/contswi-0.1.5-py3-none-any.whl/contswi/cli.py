# ------------------------------------------------------------
# Filename: cli.py
# Description: Command-line tool to switch Kubernetes contexts
# Author: Gabor Puskas
# Email: pg@0r.hu
# Date: 2024-09-24
# Version: 0.1
# Dependencies: kubectl, subprocess, termios
# ------------------------------------------------------------
import subprocess
import sys
import termios
import tty

def get_contexts():
    result = subprocess.run(["kubectl", "config", "get-contexts"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Failed to retrieve contexts from kubectl.")
        sys.exit(1)

    contexts = []
    current_context = None

    lines = result.stdout.splitlines()

    header_fields = lines[0].split()
    if len(header_fields) != 5:
        print("Error: Unexpected header format. Expected 5 fields in the header.")
        sys.exit(1)

    for line in lines[1:]:
        fields = line.split()
        if fields:
            if '*' in fields[0]:
                context_name = fields[1]
                current_context = context_name
            else:
                context_name = fields[0]
            contexts.append(context_name)
    
    return contexts, current_context

def print_menu(contexts, current_selection):
    sys.stdout.write("\033[1A" * len(contexts))
    
    for idx, context in enumerate(contexts):
        if idx == current_selection:
            sys.stdout.write(f"> {context} <\n")
        else:
            sys.stdout.write(f"  {context}  \n")
    sys.stdout.flush()

def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def menu(contexts, current_context):
    current_selection = contexts.index(current_context) if current_context else 0
    sys.stdout.write("\nPlease select a new Kubernetes context::\n\n")
    sys.stdout.write("\n" * len(contexts))
    sys.stdout.flush()
    print_menu(contexts, current_selection)
    while True:
        key = read_key()

        if key == '\x1b[A' and current_selection > 0:  # Up
            current_selection -= 1
        elif key == '\x1b[B' and current_selection < len(contexts) - 1:  # Down
            current_selection += 1
        elif key == '\r':  # Enter
            return contexts[current_selection]
        elif key == '\x03':  # Ctrl+C
            raise KeyboardInterrupt

        print_menu(contexts, current_selection)

def set_context(selected_context):
    print("\n")
    subprocess.run(["kubectl", "config", "use-context", selected_context])
    print("\n")

def main():
    contexts, current_context = get_contexts()
    try:
        selected_context = menu(contexts, current_context)
        set_context(selected_context)
    except KeyboardInterrupt:
        print("\nProgram interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
