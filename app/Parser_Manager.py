import CloverDB
import File_Parser

class Parser_Manager():
    """Wrapper for CloverDB and File_Parser modules.
    
    This 
    
    Attributes:
        parser: Parser object from File_Parser module
        db: sqlite3_DB object from CloverDB module
        buffer: buffer for transitioning data between parser and database
    """
    
    def __init__(self):
        """Constructor.

        This constructor creates the Parser and sqlite3_DB objects.
        """
        self.parser = File_Parser.Parser()
        self.db = CloverDB.sqlite3_DB()
        self.buffer = None
        
    def load_spec_file(self, filepath):
        """Manually load specification file.
        
        Args:
            filepath: string containing spec file with file path
        """
        self.spec_filepath = filepath
        
        self.buffer = self.parser.parse_spec(self.spec_filepath)
        self.db.create_table(self.parser.format, self.buffer)
        
    def run(self, data_file):
        """Adds data with specifications to database and prints database.
        
        This function requires there has been specification file and a data file
        loaded into the Parser Manager. The specification file only has to be 
        loaded for each unique specification. Afterwards, user can use
        load_data_file() to load different data files of the same specification
        or specifications that have been previously loaded.
        """
        self.buffer = self.parser.parse_data(data_file)
        
        if self.parser.format_map.get(self.parser.format) is None:
            raise RuntimeError("Specification not loaded for this data file")
        
        self.db.fill_table(self.parser.format, self.buffer)
        
        self.db.print_table(self.parser.format, self.parser.format_map[self.parser.format])

if __name__ == "__main__":        
    pm = Parser_Manager()
    pm.load_spec_file("specs/testformat1.csv")
    pm.run("data/testformat1_2015-06-28.txt")