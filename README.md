## Problem definition

Drops of data files and specification files need to be loaded these files into 
a database.

## Problem specifications

Data files will be dropped in the folder "data/" relative to your application
and specification files will be dropped in the folder "specs/" relative to
your application.

Specification files will have filenames equal to the file type they specify and
extension of ".csv". So "fileformat1.csv" would be the specification for files
of type "fileformat1".

Data files will have filenames equal to their file format type, followed by
an underscore, followed by the drop date and an extension of ".txt". 
For example, "fileformat1_2007-10-01.txt" would be a
data file to be parsed using "specs/fileformat1.csv", which arrived on 10/01/2007.

Format files will be csv formated with columns "column name", "width", and
"datatype". 

* "column name" will be the name of that column in the database table  
* "width" is the number of characters taken up by the column in the data file  
* "datatype" is the SQL data type that should be used to store the value
in the database table.

Data files will be flat text files with rows matching single records for the
database. Rows are formatted as specified by the associated format file.

## Examples

This is an example file pair; other files may vary in structure while still
fitting the structure of the problem details (above):

specs/testformat1.csv

```text
"column name",width,datatype
name,10,TEXT
valid,1,BOOLEAN
count,3,INTEGER
```

data/testformat1_2015-06-28.txt

```text
Foonyor   1  1
Barzane   0-12
Quuxitude 1103
```

Sample table output: 
```text
name      | valid | count 
--------- | ----- | -----
Foonyor   | True  |     1 
Barzane   | False |   -12 
Quuxitude | True  |   103 
```

## Usage Guide

1. Create a Parser_Manager object
2. Load the specification file into the Parser_Manager
3. Run the Parser_Manager with any files with that specification

For example:
```python
pm = Parser_Manager()
pm.load_spec_file("specs/testformat1.csv")
pm.run("data/testformat1_2015-06-28.txt")
```