import LexicalAnalyser as LA
import SymbolTable as ST

import curses
from curses import wrapper
import os


def analyser_menu(stdscr, symbol_table) -> str:
    # File selection, shows a list of files in the directory ../
    files = [file for file in os.listdir("../owl_files/") if file.endswith((".txt", ".owl"))]
    file_name = files[0]

    while True:
        stdscr.clear()

        # Highlight the current row
        for i, file in enumerate(files):
            if i == files.index(file_name):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i, 0, file)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i, 0, file)
                stdscr.attroff(curses.color_pair(2))

        key = stdscr.getch()

        # Iteractive file selection menu
        if key == curses.KEY_UP and files.index(file_name) > 0:
            file_name = files[files.index(file_name) - 1]
        elif key == curses.KEY_DOWN and files.index(file_name) < len(files) - 1:
            file_name = files[files.index(file_name) + 1]
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break

    # Initialising Lexical Analyser
    try:
        lexical_analyser = LA.LexicalAnalyser(f"../owl_files/{file_name}")
    except FileNotFoundError:
        stdscr.addstr(0, 0, "File not found! Press any key to continue...", curses.A_BOLD)
        stdscr.refresh()

        stdscr.getch()
        return

    # Getting tokens from the file
    tokens = lexical_analyser.analyse_file()

    stdscr.clear()
    stdscr.refresh()

    # Adding tokens to the Symbol Table
    stdscr.addstr(0, 0, "Analysing Tokens...")
    log = []
    for i, token in enumerate(tokens):
        classified_token = lexical_analyser.classify_token(token)
        if classified_token == "NAMESPACE":
            source = token.split(":")[0]
            type = token.split(":")[1]
            symbol_table.add_symbol(source, "NAMESPACE_SOURCE")
            symbol_table.add_symbol(type, "NAMESPACE_TYPE")
        else:
            symbol_table.add_symbol(token, classified_token)
        log.append(f"{i+1} - {token} - {classified_token}")
    
    # Writing log
    with open(f"../reports/log_{file_name}.log", "w") as file:
        file.write("Token - Classification\n")
        for line in log:
            file.write(f"{line}\n")

    stdscr.addstr(1, 0, "Done! Press any key to continue...", curses.A_BOLD)
    stdscr.refresh()

    stdscr.getch()

    return file_name[:-4]


def report_menu(stdscr, symbol_table, file_name) -> None:
    stdscr.clear()
    stdscr.refresh()

    stdscr.addstr(0, 0, f"Exporting Report to reports/report_{file_name}.txt...")

    # Writing file
    with open(f"../reports/report_{file_name}.txt", "w") as file:
        file.write("Symbol - Token Type - Occurrences\n")
        for symbol, token in symbol_table.get_table().items():
            file.write(f"{symbol} - {token.get_token_type()} - {token.get_occurrences()}\n")
    
    stdscr.addstr(1, 0, "Done! Press any key to continue...", curses.A_BOLD)
    stdscr.refresh()

    stdscr.getch()
    

def main_menu(stdscr):
    # Menu options (Analyse File, Report, Exit)
    menu = ["Analyse File", "Export Report", "Exit"]

    # Current selected option
    current_row = 0

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Root Symbol Table
    symbol_table = ST.SymbolTable()

    # Loop where k is the last character pressed
    while True:
        stdscr.clear()

        # Highlight the current row
        for i, row in enumerate(menu):
            if i == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i, 0, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i, 0, row)
                stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()

        key = stdscr.getch()

        # Iteractive menu
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                file_name = analyser_menu(stdscr, symbol_table)
            elif current_row == 1:
                report_menu(stdscr, symbol_table, file_name)
            elif current_row == 2:
                break

        stdscr.clear()
        stdscr.refresh()


wrapper(main_menu)