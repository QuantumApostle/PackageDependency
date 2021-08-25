from enum import Enum


class InputParser(object):
    def __init__(self):
        self._VALID_CMDS = {name for name in ValidCommand.__members__.keys()}

    def parse(self, cmdl_input):
        if len(cmdl_input) >= 3:
            cmd = cmdl_input.split()[0]
            if cmd in self._VALID_CMDS:
                args = cmdl_input.split()[1:]
                if cmd == ValidCommand.LIST.name and not args:
                    return {cmd: []}
                if cmd in [ValidCommand.INSTALL.name, ValidCommand.REMOVE.name]:
                    if len(args) == 1:
                        return {cmd: args[0]}
                if cmd == ValidCommand.DEPEND.name:
                    if len(args) >= 2:
                        dependent = args[1]
                        depends_on = args[2:]
                        if dependent not in depends_on:
                            return {cmd: args[1:]}
        return None


class ValidCommand(Enum):
    DEPEND = 1
    INSTALL = 2
    REMOVE = 3
    LIST = 4
    END = 5


print(set())
