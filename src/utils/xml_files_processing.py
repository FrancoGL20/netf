from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
import shutil
import os

# TODO: Finish the function

def map_ids(
        FILE_WITH_MAPPING:str,
        FILE_TO_MAP:str,
        DIR_OUTPUT:str,
        COLUMNS_TO_MAP:list,
        UNMAP:bool=False,
        HAS_DETAILS:bool=False,
    ) -> str|set[int,int,int]:
    
    FILE_MAPPED=Path(f"{DIR_OUTPUT}/{Path(FILE_TO_MAP).stem} - Mapped.{Path(FILE_TO_MAP).suffix}")

    columns_mapping={
        "tariff_id_to_map":"Tariff ID", # Original ID to map
        "tariff_number":"Tariff Number", # New ID
    }

    if UNMAP:
        columns_mapping={
            "tariff_id_to_map":"Tariff Number", # New ID
            "tariff_number":"Tariff ID", # Original ID to map
        }

    # Verify if the output file exists and remove it
    if FILE_MAPPED.exists():
        FILE_MAPPED.unlink()

    # Copy the file to map to the output file (to modify it)
    shutil.copy(FILE_TO_MAP,FILE_MAPPED)

    # Read mapping file
    columns_mapping={value:key for key,value in columns_mapping.items()}
    try:
        df_mapping=pd.read_excel(FILE_WITH_MAPPING,dtype="string").loc[:,list(columns_mapping.keys())].rename(columns=columns_mapping)
    except Exception as e:
        return str(e)

    # Convert mapping file to dictionary
    DICT_MAPPING=df_mapping.set_index("tariff_id_to_map")["tariff_number"].to_dict()

    # * Modify the result file

    # Parse the file
    tree=ET.parse(FILE_MAPPED)
    root=tree.getroot()
    namespace={
        "ss":"urn:schemas-microsoft-com:office:spreadsheet"
    }
    data=root.find("./ss:Worksheet[@ss:Name='Data']",namespace)
    table=data.find("./ss:Table",namespace)

    # Counters
    row_number=1
    errors_number=0
    mapped_counter=0
    index_of_mapping_column=None
    counter_h=0

    # Iterate over rows
    for row in table.iterfind("./ss:Row",namespace):
        column_number=1
        for cell in row.iterfind("./ss:Cell",namespace):
            # If there is a index value
            #     # need to modify the index to specified
            if cell.get(f"{{{namespace['ss']}}}Index") is not None:
                index_text_value=cell.get(f"{{{namespace['ss']}}}Index")
                column_number = int(index_text_value) if index_text_value else column_number

            # If the row text is in the columns to map
            #     # Save the index of the column to map for the next rows
            if row_number==1:
                if cell.find("./ss:Data",namespace).text in COLUMNS_TO_MAP:
                    index_of_mapping_column=column_number
                    break # go to next row
                column_number+=1
                continue # go to next cell (column)
            
            # If there is no column to map in the file
            if row_number==2 and index_of_mapping_column is None:
                FILE_MAPPED.unlink()
                return "No column to map was found"
            
            # If the row is a detail ("D") row or the file has details
            #     # Skip it and not count it in the row total
            if (row_number==2 and HAS_DETAILS) or (column_number==1 and cell.find("./ss:Data",namespace).text=="D"):
                break # go to next row
            
            # If the column to map is found 
            # and the cell has the same column number as the index of the column to map
            if (index_of_mapping_column is not None) and (column_number==index_of_mapping_column):
                counter_h+=1
                original_id=cell.find("./ss:Data",namespace)
                # If the original id has a mapping value
                if DICT_MAPPING.get(original_id.text) is not None:
                    new_id=DICT_MAPPING[original_id.text]
                # If the original id has no mapping value
                else:
                    new_id="XXXXX"
                    errors_number+=1
                
                original_id.text=new_id
                mapped_counter+=1
                break # go to next row (avoiding the rest of the cells in the row)
            
            column_number+=1

        row_number+=1

    # Write the file with the changes
    tree.write(FILE_MAPPED,encoding="UTF-8", xml_declaration=True,short_empty_elements=False)

    # Row total, mapped and errors
    return (counter_h,mapped_counter,errors_number)


FILE_WITH_MAPPING=Path(r"C:\Users\francisco.gutierrez\OneDrive - Netlogistik\Documentos\Python scripts (useful for any project)\Mapeo de IDs\Input\Mapping AP V3 con _.xlsx")
INPUT_DIRECTORY=Path(r"C:\Users\francisco.gutierrez\OneDrive - Netlogistik\Documentos\Python scripts (useful for any project)\Mapeo de IDs\Input")
TEMP_FILE_TO_MAP="AP Tariff 02 - Services"
OUPUT_DIRECTORY=Path(r"C:\Users\francisco.gutierrez\OneDrive - Netlogistik\Documentos\Python scripts (useful for any project)\Mapeo de IDs\Output")

COLUMNS_TO_MAP=["TM Tariff ID","Tariff ID","TariffCode"]
FILE_TO_MAP=Path(f"{INPUT_DIRECTORY}/{TEMP_FILE_TO_MAP}.xml")
# HAS_DETAILS=False
# UNMAP=False

result=map_ids(
        FILE_WITH_MAPPING,
        FILE_TO_MAP,
        OUPUT_DIRECTORY,
        COLUMNS_TO_MAP,
        # UNMAP,
        # HAS_DETAILS,
    )

print(result)
