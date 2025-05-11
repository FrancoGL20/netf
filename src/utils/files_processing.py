"""
Functions to process entire files.
"""

import os

def drop_duplicates(input_filename: str, output_filename: str, output_dirname: str|None = None) -> tuple [int,int]:
    """
    Drop duplicates from a text file.
    
    Args:
        input_filename: str, path to the input file
        output_filename: str, name of the output file
            - If output_dirname is None, the input_filename directory will be used
            - If the output_dirname does not exist, it will be created
        output_dirname: str, path to the output directory
    
    Returns:
        tuple: (int, int), number of lines in the original file, number of lines in the new file
    """
    with open(input_filename, 'r', encoding='utf8') as f:
        lines = f.readlines()
        
        # verify if the last element (line) has a newline, if not, add it
        if lines[-1][-1] != '\n':
            lines[-1] += '\n'
        
        # print(lines)
        original_number_of_lines = len(lines)
        # print(f"Original number of lines: {original_number_of_lines}")
        temp = sorted(set(lines))
        lines = list(temp)
        new_number_of_lines = len(lines)
        # print(f"New number of lines: {new_number_of_lines}")
        # print(f"Total duplicates removed: {original_number_of_lines-new_number_of_lines}")

    if output_dirname is not None:
        # If output_dirname is provided, use it
        if not os.path.exists(output_dirname):
            os.makedirs(output_dirname)
    else:
        # If output_dirname is not provided, use the directory of the input file
        output_dirname = os.path.dirname(input_filename)

    with open(os.path.join(output_dirname, output_filename), 'w', encoding='utf8') as f:
        f.writelines(lines)
    
    return (original_number_of_lines,new_number_of_lines)


if __name__ == "__main__":
    input_filename = os.path.join(os.path.dirname(__file__), "../../tests/test_files/test_drop_duplicates_input01.txt")
    output_filename = "test_drop_duplicates_output1.txt"
    output_dirname = os.path.join(os.path.dirname(__file__), "../../tests/test_output")
    drop_duplicates(input_filename, output_filename, output_dirname)