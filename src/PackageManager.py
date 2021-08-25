from enum import Enum

from InputParser import ValidCommand

from InputParser import InputParser


class PackageManager(object):
    def __init__(self):
        self._input_parser = InputParser()
        self._package_info = {}

    def start(self):
        while True:
            cmdl_input = input()

            if cmdl_input == ValidCommand.END.name:
                break

    def _parse_input(self, cmdl_input):
        return None


print(ValidCommand.DEPEND.name)
