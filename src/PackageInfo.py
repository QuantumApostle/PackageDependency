class PackageInfo(object):
    def __init__(self):
        self.depends_on = []
        self.needed_by = []
        self.remove_mark = False
        self.implicitly_installed = False

