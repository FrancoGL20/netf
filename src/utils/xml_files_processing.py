from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
import shutil

def map_ids(
        file_with_mapping: str,
        file_to_map: str,
        dir_output: str,
        columns_to_map: str|list[str] = ["TM Tariff ID", "Tariff ID", "TariffCode"],
        unmap: bool = False,
        has_details: bool = False,
    ) -> str|set[int,int,int]:
    """
    Maps IDs in an XML file based on a provided mapping xml excel spreadsheet 2003 file. The function
    creates a new mapped XML file in the specified output directory. It can also
    perform an unmapping process if specified.

    Args:
        file_with_mapping (str): Path to the xml excel spreadsheet 2003 file containing the ID mappings.
        file_to_map (str): Path to the XML file where IDs need to be mapped.
        dir_output (str): Directory where the mapped XML file will be saved.
        columns_to_map (str|list[str], optional): Column name or list of column names to be considered for mapping. Defaults to ["TM Tariff ID", "Tariff ID", "TariffCode"].
        unmap (bool, optional): Indicates if the process should reverse the mapping. Defaults to False.
        has_details (bool, optional): Indicates if the XML file contains detail rows that should be skipped. Defaults to False.

    Returns:
        str or set[int, int, int]: Error message if the mapping file cannot be read,
        or a tuple containing the total rows processed, number of IDs mapped, and number of errors.
    """
    
    file_mapped = Path(f"{dir_output}/{Path(file_to_map).stem} - Mapped{Path(file_to_map).suffix}")

    columns_file_mapping = {
        "tariff_id_to_map": "Tariff ID", # Original ID to map
        "tariff_number": "Tariff Number", # New ID
    }

    if unmap:
        columns_file_mapping = {
            "tariff_id_to_map": "Tariff Number", # New ID
            "tariff_number": "Tariff ID", # Original ID to map
        }

    # Verify if the output file exists and remove it
    if file_mapped.exists():
        file_mapped.unlink()

    # Copy the file to map to the output file (to modify it)
    shutil.copy(file_to_map, file_mapped)

    # Change the columns_file_mapping dict to value:key
    columns_file_mapping = {value: key for key, value in columns_file_mapping.items()}

    # Read mapping file
    try:
        df_mapping = pd.read_excel(file_with_mapping, dtype="string")
        try:
            df_mapping = df_mapping.loc[:, list(columns_file_mapping.keys())]
        except Exception as e:
            return f"The mapping file does not have the expected columns ['{list(columns_file_mapping.keys())[0]}', '{list(columns_file_mapping.keys())[1]}']"
        df_mapping = df_mapping.rename(columns=columns_file_mapping)
    except Exception as e:
        return str(e)

    # Convert mapping file to dictionary
    dict_mapping = df_mapping.set_index("tariff_id_to_map")["tariff_number"].to_dict()

    # * Modify the result file

    # Parse the file
    tree = ET.parse(file_mapped)
    root = tree.getroot()
    namespace = {
        "ss": "urn:schemas-microsoft-com:office:spreadsheet"
    }
    data = root.find("./ss:Worksheet[@ss:Name='Data']", namespace)
    table = data.find("./ss:Table", namespace)

    # Counters
    row_number = 1
    errors_number = 0
    mapped_counter = 0
    index_of_mapping_column = None
    counter_h = 0

    # Iterate over rows
    for row in table.iterfind("./ss:Row", namespace):
        column_number = 1
        for cell in row.iterfind("./ss:Cell", namespace):
            # If there is a index value
            #     # need to modify the index to specified
            if cell.get(f"{{{namespace['ss']}}}Index") is not None:
                index_text_value = cell.get(f"{{{namespace['ss']}}}Index")
                column_number = int(index_text_value) if index_text_value else column_number

            # If the row text is in the columns to map
            #     # Save the index of the column to map for the next rows
            if row_number == 1:
                if isinstance(columns_to_map, str):
                    if cell.find("./ss:Data", namespace).text == columns_to_map:
                        index_of_mapping_column = column_number
                        break # go to next row
                else:
                    if cell.find("./ss:Data", namespace).text in columns_to_map:
                        index_of_mapping_column = column_number
                        break # go to next row
                column_number += 1
                continue # go to next cell (column)
            
            # If there is no column to map in the file
            if row_number == 2 and index_of_mapping_column is None:
                file_mapped.unlink()
                if isinstance(columns_to_map, str):
                    return "No column to map was found in the file"
                else:
                    return "None of the columns to map were found in the file"
            
            # If the row is a detail ("D") row or the file has details
            #     # Skip it and not count it in the row total
            if (row_number == 2 and has_details) or (column_number == 1 and cell.find("./ss:Data", namespace).text == "D"):
                break # go to next row
            
            # If the column to map is found 
            # and the cell has the same column number as the index of the column to map
            if (index_of_mapping_column is not None) and (column_number == index_of_mapping_column):
                counter_h += 1
                original_id = cell.find("./ss:Data", namespace)
                # If the original id has a mapping value
                if dict_mapping.get(original_id.text) is not None:
                    new_id = dict_mapping[original_id.text]
                # If the original id has no mapping value
                else:
                    new_id = "XXXXX"
                    errors_number += 1
                
                original_id.text = new_id
                mapped_counter += 1
                break # go to next row (avoiding the rest of the cells in the row)
            
            column_number += 1

        row_number += 1

    # Write the file with the changes
    tree.write(file_mapped, encoding="UTF-8", xml_declaration=True, short_empty_elements=False)

    # Row total, mapped and errors
    return (counter_h, mapped_counter, errors_number)
