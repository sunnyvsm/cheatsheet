#!/usr/bin/env python3


import os
from argparse import ArgumentParser
from configparser import ConfigParser
from printer import PrinterFactory
from sys import exit


def main():
    # GENERAL SETTINGS!
    file_dir = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(file_dir, "sheets/")
    extention = ".ini"
    description = "Cool Command-line Cheatsheets"
    help_general = "The cheatsheet you want to see"
    help_inline = "One cheat per line, this is default"
    help_breakline = "Break lines"

    # COMMAND-LINE ARGUMENTS!
    argumentparser = ArgumentParser(description=description)
    printertype = argumentparser.add_mutually_exclusive_group()

    argumentparser.add_argument('cheatsheet', help=help_general)
    printertype.set_defaults(printer='InlinePrinter')
    printertype.add_argument('-l', help=help_inline, action='store_const', dest='printer', const='InlinePrinter')
    printertype.add_argument('-b', help=help_breakline, action='store_const', dest='printer', const='BreaklinePrinter')

    # WHERE THE RUBBER MEETS THE ROAD!
    cmd_arguments = argumentparser.parse_args()
    filename = directory + cmd_arguments.cheatsheet + extention
    CheatPrinterConstructor = PrinterFactory.create_printer(cmd_arguments.printer)
    configparser = ConfigParser()
    cheatprinter = CheatPrinterConstructor(configparser)

    try:
        configparser.read(filename)
        cheatprinter.printsheet()
        exitcode = 0
    except Exception as e:
        # I know lazy handling... Sorry.
        # TOOD better exception handling.
        print(filename + " not available or contains errors.")
        print(e)
        exitcode = 1
    finally:
        exit(exitcode)

if __name__ == "__main__":
    main()
