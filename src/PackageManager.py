from InputParser import ValidCommand

from InputParser import InputParser
from collections import defaultdict

from src.PackageInfo import PackageInfo


class PackageManager(object):
    def __init__(self):
        self._input_parser = InputParser()
        self._package_info = {}
        self._dependent_map = defaultdict(list)
        self._depends_on_map = defaultdict(list)
        self._INVALID = "INVALID"
        self._installed_packages = []

    def start(self):
        while True:
            cmdl_input = input()

            if cmdl_input == ValidCommand.END.name:
                break
            self._process_input(cmdl_input)

    def _process_input(self, cmdl_input):
        parsing_result = self._input_parser.parse(cmdl_input)
        if parsing_result is None:
            print("Invalid input")
        else:
            if ValidCommand.DEPEND.name in parsing_result:
                self._process_depend(parsing_result[ValidCommand.DEPEND.name])
            elif ValidCommand.INSTALL.name in parsing_result:
                self._process_install(parsing_result[ValidCommand.INSTALL.name])
            elif ValidCommand.REMOVE.name in parsing_result:
                self._process_remove(parsing_result[ValidCommand.REMOVE.name])
            elif ValidCommand.LIST.name in parsing_result:
                return self._process_list()

    def _process_depend(self, param):
        dependent = param[0]
        depends_on = param[1:]
        for package in depends_on:
            if dependent not in self._dependent_map[package]:
                self._dependent_map[package].append(dependent)
                self._depends_on_map[dependent].append(package)
                if self._has_cycle():
                    self._dependent_map[package].pop()
                    self._depends_on_map[dependent].pop()
                    print("{} depends on {}, ignoring command".format(
                        package, dependent
                    ))
                    break
                self._package_info.setdefault(package, PackageInfo(package))
                self._package_info.setdefault(dependent, PackageInfo(dependent))

    def _process_install(self, package):
        pass

    def _process_remove(self, package):
        pass

    def _process_list(self):
        for package in self._installed_packages:
            print(package, '\n')

    def _has_cycle(self):
        pass


print(ValidCommand.DEPEND.name)
