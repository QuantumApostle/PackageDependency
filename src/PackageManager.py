from InputParser import ValidCommand
from InputParser import InputParser
from collections import defaultdict

from PackageInfo import PackageInfo


class PackageManager(object):
    def __init__(self):
        self._input_parser = InputParser()
        self._package_info = {}
        self._needed_by_map = defaultdict(list)
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
        for package in param:
            self._package_info.setdefault((package, PackageInfo(package)))
        dependent = param[0]
        depends_on = param[1:]
        for package in depends_on:
            if dependent not in self._needed_by_map[package]:
                self._package_info[package].needed_by.append(dependent)
                self._package_info[dependent].depends_on.append(package)
                if self._has_cycle():
                    self._package_info[package].needed_by.pop()
                    self._package_info[dependent].depends_on.pop()
                    print("{} depends on {}, ignoring command".format(
                        package, dependent
                    ))
                    break

    def _process_install(self, package, implictly_install=False):

        if package not in self._package_info:
            self._package_info.setdefault(package, PackageInfo(package))
            self._package_info[package].implicitly_installed = implictly_install
            self._installed_packages.append(package)
            print("Installing {}".format(package))
        elif package not in self._installed_packages:
            for depends_on_package in self._package_info[package].depends_on:
                self._process_install(depends_on_package, True)
            self._package_info[package].implicitly_installed = implictly_install
            self._installed_packages.append(package)
            print("Installing {}".format(package))

    def _process_remove(self, package):
        pass

    def _process_list(self):
        for package in self._installed_packages:
            print(package, '\n')

    def _has_cycle(self):
        status = {}

        def check_cycle(p):
            if p in status:
                if status[p] == "visited":
                    return False
                if status[p] == "visiting":
                    return True
            status[p] = "visiting"
            for depends_on_package in self._package_info[p].depends_on:
                if check_cycle(depends_on_package):
                    return True
            status[p] = "visited"
            return False

        for package in self._package_info:
            if package not in status:
                if check_cycle(package):
                    return True

        return False
