import File_Parser

print("Running tests...")

#Basic test
obj = File_Parser.Parser()
assert(len(obj.format_map) == 0)

#Test with provided "testformat1.csv" file
#   - Assures that the results from parse_spec returns expected string
#   - Assures the input file is the expected input file
#   - Assures the format will be "testformat1"
#   - Assures that the format map has one item
#   - Assures that the format map item is {"testformat1" : ['10', '1', '3']}
expected_filepath = "specs/testformat1.csv"
expected_spec = ['name', 'TEXT', 'valid', 'INTEGER', 'count', 'INTEGER']
expected_format = "testformat1"
assert(obj.parse_spec(expected_filepath) == expected_spec)
assert(obj.filepath == expected_filepath)
assert(obj.format == expected_format)
assert(len(obj.format_map) == 1)
expected_width = ['10', '1', '3']
assert(obj.format_map["testformat1"] == expected_width)

#Test with provided "testformat1_2015-06-28.txt" file
#   - Assures that the results from parse_data returns expected string
#   - Assures that the filename is stored properly
#   - Assures that the format is stored properly
expected_filepath = "data/testformat1_2015-06-28.txt"
expected_data = [('Foonyor', '1', '1'), ('Barzane', '0', '-12'), ('Quuxitude', '1', '103')]
assert(obj.parse_data(expected_filepath) == expected_data)
assert(obj.filepath == expected_filepath)
assert(obj.format == expected_format)

print("...All tests passed")