"""
Functions to process entire files.
"""

from pathlib import Path

def drop_duplicates(input_filename: str, output_filename: str, output_dirname: str|None = None) -> tuple [int,int]:
    """
    Drop duplicates from a text file.
    
    Args:
        input_filename: str, path to the input file
        output_filename: str, name of the output file
            1. If output_dirname is None, the input_filename directory will be used
            2. If the output_dirname does not exist, it will be created
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
        if not Path(output_dirname).exists():
            Path(output_dirname).mkdir(parents=True, exist_ok=True)
    else:
        # If output_dirname is not provided, use the directory of the input file
        output_dirname = Path(input_filename).parent

    with open(Path(output_dirname, output_filename).as_posix(), 'w', encoding='utf8') as f:
        f.writelines(lines)
    
    return (original_number_of_lines,new_number_of_lines)
