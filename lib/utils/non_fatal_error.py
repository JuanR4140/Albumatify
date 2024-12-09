def throw_non_fatal_error(message, console, getch):
    console.print("\n\n" + message + "\nPress 'k' to continue.\n\n")
    while True:
        if getch() == "k":
            break
