from src.InputParser import ValidCommand
from src.InputParser import InputParser

from src.PackageInfo import PackageInfo


class PackageManager(object):
    def __init__(self):
        self._input_parser = InputParser()
        self._package_info = {}
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
            self._package_info.setdefault(package, PackageInfo())
        dependent = param[0]
        depends_on = param[1:]
        for package in depends_on:
            if dependent not in self._package_info[package].needed_by:
                self._package_info[package].needed_by.append(dependent)
                self._package_info[dependent].depends_on.append(package)
                if self._has_cycle():
                    self._package_info[package].needed_by.pop()
                    self._package_info[dependent].depends_on.pop()
                    print("{} depends on {}, ignoring command".format(
                        package, dependent
                    ))
                    break

    def _process_install(self, package, implicitly_install=False):

        if package in self._installed_packages:
            self._package_info[package].remove_mark = False
            if not implicitly_install:
                print("{} is already installed".format(package))
        else:
            if package not in self._package_info:
                self._package_info.setdefault(package, PackageInfo())
            else:
                for p in self._package_info[package].depends_on:
                    self._process_install(p, True)
                self._package_info[package].implicitly_installed = implicitly_install
            self._installed_packages.append(package)
            print("Installing {}".format(package))

    def _process_remove(self, package, implicitly_remove=False):
        if package not in self._installed_packages:
            print("{} is not installed".format(package))
        else:
            self._package_info[package].remove_mark = True
            is_still_needed = False
            for p in self._package_info[package].needed_by:
                if p in self._installed_packages:
                    is_still_needed = True
                    if not implicitly_remove:
                        print("{} is still needed".format(package))
                    break
            if not is_still_needed:
                idx = self._installed_packages.index(package)
                self._installed_packages.pop(idx)
                print("Removing {}".format(package))
                for p in self._package_info[package].depends_on:
                    if self._package_info[p].implicitly_installed:
                        self._process_remove(p, True)

    def _process_list(self):
        for package in self._installed_packages:
            print(package)

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
