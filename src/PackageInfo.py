class PackageInfo(object):
    def __init__(self):
        self.name = None
        self.depends_on = []
        self.needed_by = []
        self.remove_mark = False
        self.installed = False
        self.needed = False

