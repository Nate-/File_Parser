import os

class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.fileObj = None
        self._open_file()
        
    def _open_file(self):
        if os.path.isfile(self.filename):
            self.fileObj = open(self.filename, "r")
        else:
            raise NameError("{} is not a valid file".format(self.filename))
    
    def parse_spec_line(self):
        line = self.fileObj.readline().strip()
        tokens = line.split(",")
        return tokens
        
    def parse_data_line(self):
        pass