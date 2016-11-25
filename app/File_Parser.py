import os

class Parser():
    """File parser for file formats specified by Clover challenge (See readme).
    
    Parser is a file parser that will take a specification, parse the 
    column values into a list and preserve the format for future use with
    data files.
    
    Attributes:
        filepath: the user-provided filepath for a csv or txt file
        format: the basename of the csv file or the basename of a txt file
                without the date
        file: file object used to read the file indicated by filepath
        format_map: a map of format to column widths
    """
    
    def __init__(self):
        """Parser constructor."""
        self.filepath = None
        self.format = None
        self.file = None
        self.format_map = {}
    
    def __open_file(self, filepath):
        """Opens the file indicated by filepath if it exists.
        
        Args:
            filepath: a string of the filepath for the file to be read 
                        e.g. 'specs/testformat1.csv'
                        
        Exceptions:
            This function will throw a NameError if the filepath is invalid.
        """
        #Sets filepath
        self.filepath = filepath 
        
        #Opens valid files and raises exception for invalid files
        if os.path.isfile(filepath):
            self.file = open(self.filepath)
        else:
            raise NameError("Invalid file")
            
        #Extract format
        self.__get_format()
    
    def __extension_is(self, extension):
        """Tests to see if the file extension is indicated format

        Args:
            extension: a string with the file extension to be checked 
                        e.g. 'csv' or '.csv'        
        """
        length = len(self.filepath)
        
        if self.filepath[length - len(extension) :] == extension:
            return True
        else:
            return False
    
    def __get_format(self):
        """Sets self.format based on the filename.
        
        If the file is a CSV file, the format will be the filename stripped of 
        the ".csv" extension. Otherwise, the format will be the filename with 
        the _YYYY-MM-DD.txt removed.
        """
        self.format = os.path.basename(self.filepath)
        length = len(self.format)
        
        if self.__extension_is("csv"):
            #The length of ".csv" is 4
            self.format = self.format[:length - 4]
        else:
            #The length of "_YYYY-MM-DD.txt" is 15
            self.format = self.format[:length - 15]
    
    def parse_spec(self, filepath):
        """Parse a format specification file.
        
        This function requires a list to be provided as result to be returned
        to the user and a filepath for the specifications file. The function
        will parse the entire file and place column names with datatype into the
        results list, while storing the widths in the format_map attribute for
        future use with data files.
        
        Note:
            BOOLEAN and INTEGER datatypes will be replaced by INT
        
        Args:
            filepath: the filepath for the file to be read 
                        e.g. specs/testformat1.csv
                        
        Returns:
            A list of strings containing column names and corresponding
            datatypes as interleaved elements.
        """
        
        #Open file
        self.__open_file(filepath)
        
        #Parse specifications only if it hasn't been parsed before
        if self.format_map.get(self.format) is not None:
            return
        
        #Save the sizes of the columns
        sizes = []
        result = []
        
        #Remove first line
        self.file.readline()
        
        #Read subsequent lines into lists
        for line in self.file:
            c, w, d = line.strip().split(',')
            result.append(c)
            sizes.append(w)
            if d == 'BOOLEAN' or d == 'INTEGER':
                d = "INT"
            result.append(d)

        #Add a mapping of the format to its sizes
        self.format_map[self.format] = sizes
        
        return result
        
    def parse_data(self, filepath):
        """Parse a data file.
        
        This function acquires the format from the filename by stripping the
        date and extension from the filename. Then it checks and assures that
        the specifications for the data file has previously been read. Then it
        will parse the data file into a list of lists, where each list is a 
        row in the data file.
        
        Args:
            filepath: the filepath for the file to be read 
                        e.g. 'data/testformat1_2015-06-28.txt'
                        
        Returns:
            A list that contains a list of strings with the column values for 
            every row.
            
        Exceptions:
            This function will throw a RuntimeError if the parse_spec function
            is not called with the appropriate format specifications before 
            calling parse_data on a data file of that specification.
        """        
        
        #Extract format
        self.__get_format()
        
        #Check if the specification has been parsed prior
        if self.format_map.get(self.format) is None:
            raise RuntimeError("Data format not specified")
        
        #Open file
        self.__open_file(filepath)
        
        #Build results
        column_sizes = self.format_map[self.format]
        result = []
        
        for line in self.file:
            tmp = []
            current = 0
            for sz in column_sizes:
                tmp.append(line[current : current + int(sz)].strip())
                current += int(sz)
            result.append(tmp)
        
        return result