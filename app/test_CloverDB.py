import CloverDB
import os
import sqlite3

print("Running tests...")

#Create a test database
test_database = "test.db"
obj = CloverDB.sqlite3_DB(test_database)

#Remove the db if script ended in error previously
if os.path.isfile(test_database):
    os.remove(test_database)

#Expected results from File_Parser
expected_tablename = "testformat1"
expected_spec = ["name", "TEXT", "valid", "INTEGER", "count", "INTEGER"]
expected_data = [('Foonyor', '1', '1'), ('Barzane', '0', '-12'), ('Quuxitude', '1', '103')]
expected_widths = ['10', '1', '3']
obj.create_table(expected_tablename, expected_spec)
obj.fill_table(expected_tablename, expected_data)

#Use sqlite3 to access and test 
conn = sqlite3.connect(test_database)
c = conn.cursor()

#Check the master table for the expected tablename
#Note sqlite_master structure is as follows:
#CREATE TABLE sqlite_master (
#   type TEXT,
#   name TEXT,
#   tbl_name TEXT,
#   rootpage INTEGER,
#   sql TEXT
# );
c.execute("SELECT * FROM sqlite_master")
table_info = c.fetchall()

#Tests from this table:
#   - There is only one table added
#   - The name of this table will be expected_tablename
assert(len(table_info) == 1)
assert(table_info[0][2] == expected_tablename)

#Grab all the data from the expected_tablename and it should match the input
c.execute("SELECT * from {}".format(expected_tablename))
rows = c.fetchall()
for i in range(len(rows)):
    for j in range(len(rows[0])):
        assert(str(rows[i][j]) == str(expected_data[i][j]))
        
#Check that the column names are the same as input
descriptions = [desc[0] for desc in c.description]
for i in range(len(descriptions)):
    assert(descriptions[i] == expected_spec[i*2])


#Check to assure that the column names have the same datatype as input
c.execute("PRAGMA TABLE_INFO({})".format(expected_tablename))
table_info = c.fetchall()
for i in range(len(table_info)):
    assert(table_info[i][1] == expected_spec[i*2])
    assert(table_info[i][2] == expected_spec[i*2+1])

#Close sqlite3 access
conn.close()

#Remove the db after the test database
if os.path.isfile(test_database):
    os.remove(test_database)
    
print("...All tests passed")