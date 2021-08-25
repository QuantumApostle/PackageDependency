class PackageInfo(object):
    def __init__(self, name):
        self.name = name
        self.depends_on = []
        self.needed_by = []
        self.remove_mark = False
        self.installed = False
        self.needed = False
        self.implicitly_installed = False

