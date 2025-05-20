import pandas as pd
import numpy as np
from typing import Union
import xml.etree.ElementTree as ET


def read_xml_template(xml_filename:str,has_details:bool=False) -> pd.DataFrame:
    """Function to read and convert an xml spreadsheet 2003 file to a pandas DataFrame

    Args:
        xml_filename (str): name of the xml spreadsheet 2003 file
        has_details (bool, optional): define if the template has a first row of details that should be ignored. Defaults to False.

    Returns:
        pandas.DataFrame: DataFrame with the information of the template converted correctly
    """
    
    tree=ET.parse(xml_filename)
    root = tree.getroot()
    namespace={
        "ss":"urn:schemas-microsoft-com:office:spreadsheet"
    }

    data=root.find("./ss:Worksheet[@ss:Name='Data']",namespace)
    table=data.find("./ss:Table",namespace)

    row_iteration_number=1
    file_headers=[]
    final_list=[]

    for row in table.iterfind("./ss:Row",namespace): # For every row
        index=1
        current_dict={}
        for cell in row.iterfind("./ss:Cell",namespace):
            # if there is a index value
                # need to modify the index to specified
            if cell.get(f"{{{namespace['ss']}}}Index") is not None:
                index_text_value=cell.get(f"{{{namespace['ss']}}}Index")
                index = int(index_text_value) if index_text_value else index
            
            # if there is a None value in the Data element
                # ignore it and go to the next row
            # if there is no Data element
                # ignore cell
            if (cell.find("./ss:Data",namespace) is not None) and (cell.find("./ss:Data",namespace).text is not None):
                if row_iteration_number==1:
                    file_headers.append(cell.find("./ss:Data",namespace).text)
                elif row_iteration_number==2 and has_details:
                    pass
                else:
                    current_dict[file_headers[index-1]]=cell.find("./ss:Data",namespace).text
            index+=1
            
            # print(current_dict)
        
        row_iteration_number+=1
        if len(current_dict):
            final_list.append(current_dict)
            # print(current_dict)
            # print()

    df = pd.DataFrame(final_list)

    return df


def expand_row_values(df: pd.DataFrame, column_to_expand:str,h_and_d_structure:bool=True, keep_old_col=False,print_result=False)->pd.DataFrame:
    """Function to expand the value of a column that contains lists to H and D structure

    Args:
        df (pd.DataFrame): dataframe with column to expand
        h_and_d_structure (bool): 
            True: indicates that if you want to have a structure of one row of H and the rest D (adds column Type)
            False: indicates that each row will be repeated with all the data of the columns, only varying the one of the column to expand
        column_to_expand (str): name of the column to expand of the dataframe (this must be a column that contains arrays)
        keep_old_col (bool, optional): define if the original column that was expanded is kept. Defaults to False.
        print result (bool, optional): define if print the result. Defaults to False.

    Raises:
        ValueError: if the column to expand does not exist in the DataFrame

    Returns:
        pd.DataFrame: Dataframe with the rows expanded according to the column sent
    """
    # Function to expand the value of a column that contains lists to H and D structure
    df_columns=df.columns.to_list()
    
    if column_to_expand not in df_columns:
        print(f"Column {column_to_expand} does not exist")
        raise ValueError(f"Column {column_to_expand} does not exist")
        return 1
    else:
        df_columns.remove(column_to_expand)
        
    rows = []
    
    for index_df, row_df in df.iterrows():
        
        if len(row_df[column_to_expand])==0:
            empty_row_to_insert:dict={}
            for column in df_columns:
                empty_row_to_insert[column]=row_df[column]
            if keep_old_col:
                empty_row_to_insert[f"{column_to_expand}_old"]=np.nan
            empty_row_to_insert[column_to_expand]=np.nan
            
            rows.append(empty_row_to_insert)
            continue
        
        for index,expanded_value in enumerate(row_df[column_to_expand]):
            row_to_insert:dict={}
            
            if h_and_d_structure:
                if index==0:
                    row_to_insert['Type']='H'
                    for column in df_columns:
                        row_to_insert[column]=row_df[column]
                    if keep_old_col:
                        row_to_insert[f"{column_to_expand}_old"]=row_df[column_to_expand]
                else:
                    row_to_insert['Type']='D'
                    for column in df_columns:
                        row_to_insert[column]=np.nan
                    if keep_old_col:
                        row_to_insert[f"{column_to_expand}_old"]=np.nan
            else:
                for column in df_columns:
                    row_to_insert[column]=row_df[column]
                if keep_old_col:
                    row_to_insert[f"{column_to_expand}_old"]=row_df[column_to_expand]
            
            row_to_insert[column_to_expand]=expanded_value
            rows.append(row_to_insert)
                
    
    expanded_df = pd.DataFrame(rows)
    
    if print_result:
        print(expanded_df)
    
    return expanded_df

def pf(df:Union[pd.DataFrame,pd.Series]):
    """
    Function to print DataFrames or Series with NaN representation as '-'
    """
    print(df.to_string(na_rep='-'))