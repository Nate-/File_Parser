import sqlite3
import os

class sqlite3_DB():
    """sqlite3 database to be used with File_Parser.
    
    Parser is a file parser that will take a specification, parse the 
    column values into a list and preserve the format for future use with
    data files.
    
    Attributes:
        db: the user-defined filepath for their database, defaults to db/clover.db
        conn: database connection
        cursor: database connection cursor
    """
    
    def __init__(self, db=os.path.join('db', 'clover.db')):
        """Constructor.
        
        Args:
            db: the path to the database, defaults to db/clover.db
        """
        self.db = os.path.join(os.path.dirname(__file__), db)
        self.conn = None
        self.cursor = None
        
        #Create directory for database if it doesn't already exist
        if not os.path.exists(os.path.dirname(self.db)):
            os.makedirs(os.path.dirname(self.db))
        
    def __connect(self):
        """Establishes a connection to the database."""
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        
    def __disconnect(self):
        """Disconnects the connection to the database."""
        self.conn.close()
        
    def __commit(self):
        """Commit changes made to the database."""
        self.conn.commit()
    
    def create_table(self, table_name, column_data):
        """Creates an empty table in the database.
        
        Args:
            table_name: string with the name of the table to be created
            column_data: list of strings with column name interleaved with datatype
        """
        
        #Connect to database
        self.__connect()
        
        #Create table query
        length = len(column_data)
        query = "CREATE TABLE IF NOT EXISTS {}(".format(table_name)
        for i in range(0, length - 2, 2):
            #Add a comma behind all but last two elements of column data for
            #the last column name and datatype pair
            query += "{} {},".format(column_data[i], column_data[i+1])
        #Add the last column name and datatype pair
        if length > 1:
            query += "{} {})".format(column_data[length - 2], column_data[length - 1])
        
        #Execute query to create table
        self.cursor.execute(query)
        
        #Commit changes to database
        self.__commit()
        
        #Disconnect from database
        self.__disconnect()

    def fill_table(self, table_name, data):
        """Fill an empty table of table_name with data values
        
        Args:
            table_name: string with the name of the table to be filled
            data: list of tuples of values to be filled with each tuple
                    representing a row
        """        
    
        #Open and connect to database
        self.__connect()
        
        #Craft query
        num_values = len(data[0])
        query = "INSERT INTO {} VALUES(".format(table_name)
        query += "?," * (num_values - 1) + "?)"
        
        #Insert all data into table
        self.cursor.executemany(query, data)
        
        #Commit changes to database
        self.__commit()
        
        #Disconnect from database
        self.__disconnect()
    
    def __table_exists(self, table_name):
        """Checks if a table with table_name exists.
        
        Requires a connection to database to be pre-existing.
        """
        query = "SELECT 1 FROM sqlite_master WHERE type='table' and name = ?"
        result = self.cursor.execute(query, (table_name,)).fetchone() is not None
        return result
    
    def print_table(self, table_name, column_widths):
        """Prints the table in in a grid format.
        
        This function will print a table in the following format.
        Column_name | Column_name | Column_name
        ----------- | ----------- | -----------
        value       | value       | value
        value       | value       | value
            .           .             .
            .           .             .
            .           .             .
            
        Args:
            table_name: name of the table to print
            column_widths: the original widths of the columns
        """
        #Open and connect to database
        self.__connect()
        
        #Print table only if it exists
        if self.__table_exists(table_name):
            length = len(column_widths)
        
            #Query for all table elements
            query = "SELECT * FROM {}".format(table_name)
            self.cursor.execute(query)
            
            #Column names will always be 0th element of cursor description
            column_names = [desc[0] for desc in self.cursor.description]
            
            #Retreive all row data
            row_data = self.cursor.fetchall()
                
            #Create title row
            row = ""
            horizontal_line = ""
            seperator = " | "

            #Create a string that contains column data with seperator symbols
            for i in range(length - 1):
                width = max(int(column_widths[i]), len(column_names[i]))
                row += column_names[i].ljust(width) + seperator
                horizontal_line += ''.ljust(width, '-') + seperator
                
            #Repeat process with last column without  
            width = max(int(column_widths[length - 1]), len(column_names[length - 1]))
            row += column_names[length - 1].ljust(width)
            horizontal_line += ''.ljust(width, '-')
            
            #Print the column titles and horizontal line 
            print(row)
            print(horizontal_line)
            
            #Create the string with column data and separators
            for i in range(len(row_data)):
                #Reset row
                row = ""
                
                #Create a string with the column name with separators for 
                #all except the last column
                for j in range(length - 1):
                    width = max(int(column_widths[j]), len(column_names[j]))
                    data = row_data[i][j]
                    
                    #Check if the column holds a boolean value, if so,
                    #replace the 0 with false and 1 with true
                    if int(column_widths[j]) == 1:
                        data = "true" if data else "false"
                    row += str(data).ljust(width) + seperator
                
                #Repeat with the last column data without the separator
                width = max(int(column_widths[length - 1]), len(column_names[length - 1]))
                data = row_data[i][length - 1]
                if int(column_widths[length - 1]) == 1:
                    data = "true" if data else "false"
                row += str(data).rjust(width)
                print(row)
            
        else:
            print("Table <{}> does not exist.".format(table_name))
        
        #Disconnect from database
        self.__disconnect()