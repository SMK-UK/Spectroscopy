'''
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023

Functions designed to load in and parse data form .csv or .txt
'''

import matplotlib.pyplot as mp
from natsort import natsorted
import numpy as np
import os, re
import pandas as pd

def check_str(string_one, string_two) -> bool:
    """
    Checks string for certain characters and flag if true
    
    Parameters
    ----------
    string_one : string to check
    string_two : string / characters to check against
    flip : choose to flip the strings 

    Returns
    -------
    Boolean
    
    """
    validation = set(string_one)
    char_allow = set(string_two)
   
    return validation.issubset(char_allow)

def check_digits(input_string: str) -> bool:
    """
    Checks if a string contains only digits and flag if True
    
    Parameters
    ----------
    input_string : string 

    Returns
    -------
    logical : Boolean

    """
    # check input string for digits and flag True
    if any(char.isdigit() for char in input_string) == True:

        logical = check_str((input_string), "0123456789\n\t\r eE-+,.;")
    else:
        logical = False

    return logical

def dir_interogate(path: str, 
                   extensions: list[str] = [], 
                   exceptions: list[str] = [], 
                   folders: list[str] = []) -> tuple[list[str], list[str]]:
    """
    Interogate directory and extract all folders and files. Optional: 'extensions', 
    'exceptions' and 'folders' enables selective read of files and folders.

    Only capable of extracting files that are nested once. Will not work for 
    subfolders or extract files from the main directory.

    Parameters
    ----------
    path : string - main folder / directory to interrogate
    extensions : tuple - file extensions to check for in directory
    exceptions : tuple - file extensions / strings to exclude
    folders : tuple - select folders to extract from

    Returns
    -------
    folder_list : list of folder names
    file_list : list of file names

    """       
    folder_list = []
    file_list = []
    for root, dirs, files in natsorted(os.walk(path)):

        if dirs:
            dirs = natsorted(dirs)
            if not folders:
                folder_list = dirs
            else:
                folder_list = [folder for folder in dirs 
                               if folder in folders]
            if exceptions:
                folder_list = [folder for folder in folder_list
                               if not any([x in folder for x in exceptions])]

        if not dirs:
            temp_files = []
            if not folders:
                temp_files = files
            elif any([x in os.path.split(root) for x in folders]):
                temp_files = files
            if exceptions:
                temp_files = [file for file in temp_files
                              if not any([x in file for x in exceptions])]
            else:
                temp_files = [file for file in temp_files]
            if extensions:
                    temp_files = [file for file in temp_files
                              if file.endswith(tuple(extensions))]
            if temp_files:
                file_list.append(natsorted(temp_files))

    if len(file_list) == 1:
        file_list = [file_name for sublist in file_list
                     for file_name in sublist]
    
    return folder_list, file_list

def find_numbers(string:str, pattern:str='-?\ *\d+\.?\d*(?:[Ee]\ *-?\ *\d+)?') -> list[str]:
    """
    Checks string for numbers and returns any hits
    
    Parameters
    ----------
    paths : path or list of paths

    Returns
    -------
    numbers : int or list of ints

    """
    match_number = re.compile(pattern)
    numbers = [x for x in re.findall(match_number, string)]

    if len(numbers) == 1:
        numbers = numbers[0]

    return numbers

def open_excel(path: str, seperators: str=",") -> list:
    """
    Open a given excel / csv file and convert each column 
    to np.array and place into a list
    
    Parameters
    ----------
    path : file path
    
    Returns
    -------
    excel_data : list of column data from pandas data frame

    """
    temp_df = pd.read_csv(path, sep=seperators, engine='python')
    excel_data = [temp_df[x].to_numpy() for x in temp_df]

    if len(excel_data) == 1:
        excel_data = [value for sublist in excel_data for value in sublist]

    return excel_data

def read_file(path: str) -> tuple:
    """
    Open a given file and read the first two columns to a list. Works with
    columns of different length

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    metadata_list : list of metadata read from path
    data_list : list of data read from path
    
    """
    data_list = []
    metadata_list = []
    with open(path, 'r', newline='') as raw_file:
    # cycle through each row in the file
        for row in raw_file:
            # check row for specific string / values
            if check_digits(row) == True:
                # generate list to populate with column data
                data_temp = [i for i in re.split(r"[\t|,|;]", row)
                             if i != '' and i != '\r\n']
                if not data_list:
                    data_list = [[] for _ in range(len(data_temp))]
                for index, data in enumerate(data_temp):
                    if len(data_list) < index + 1:
                        data_list.append([])
                    data_list[index].append((float(data)))
            else:
                # extract metadata
                metadata_temp = [i for i in re.split(r"[\t|,|;]", row)
                                 if i != '' and i != '\r\n']
                if not metadata_list:
                    # generate list to populate with column metadata
                    metadata_list = [[] for _ in range(len(metadata_temp))]
                for index, metadata in enumerate(metadata_temp):
                    if len(metadata_list) < index + 1:
                        metadata_list.append([])
                    metadata_list[index].append(metadata)
        raw_file.close()

    return metadata_list, data_list

def open_text(path: str):
    """
    Open a given file and read the first two columns to a list. Works with
    columns of different length

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    data_list : list of data read from path
    metadata_list : list of metadata read from path
    
    """
    data_list = []
    with open(path, 'r', newline='') as raw_file:
    # cycle through each row in the file
        for row in raw_file:
            # generate list to populate with column data
            data_temp = [i for i in re.split(r"[\t|,|;]", row)
                            if i != '' and i != '\r\n']
            if not data_list:
                data_list = [[] for _ in range(len(data_temp))]
            for index, data in enumerate(data_temp):
                if len(data_list) < index + 1:
                    data_list.append([])
                data_list[index].append(data)
        raw_file.close()

        if len(data_list) == 1:
            data_list = [data for sublist in data_list for data in sublist]

    return data_list

def search_paths(folders: list[str], files: list[str], include: list[str] = [], exclude: list[str] = []) -> list[str]:
    """
    search a list of paths for keys and join files to folders
        
    Parameters
    ----------
    folders : list of folder names
    files : list of file names
    keys : keywords to search folders and files for
    
    Returns
    -------
    paths : list of desired paths

    """
    paths = []
    for index, folder in enumerate(folders):
        desired = []
        for file in files[index]:
            path = os.path.join(folder, file)
            if include:
                if any([x in path for x in include]):
                    desired.append(path)
            else:
                desired.append(path)
            if exclude:
                desired = [x for x in desired
                               if not any([y in path for y in exclude])]
        if desired:
            paths.append(desired)

    if len(paths) == 1:
        paths = [data for sublist in paths for data in sublist]

    return paths

def seperate_lists(list_to_split):

    return [[x for x, y in sublist] for sublist in list_to_split], [[y for x, y in sublist] for sublist in list_to_split]

def spectrum_extract(paths: list[str], keys: list[str]=[], tail: int=1, 
                include: bool=True) -> tuple:
    """
    search a list of paths for strings and extract the data
    from selected files depending on the discriminator (keys)

    Parameters
    ----------
    paths : file paths
    keys : list of key values to search for in path if required
    tail : int value 1 or 0 to search head or tail of path
    include : True or False to include the data with key or exclude
    
    Returns
    -------
    extracted_metadata : list of metadata read from path
    extracted_data : list of data read from path
    
    """
    extracted_metadata = []
    extracted_data = []
    if not keys:
        for path in paths:
            extracted_metadata.append(read_file(path)[0])
            extracted_data.append(np.array(read_file(path)[1]))
    else:
        for key in keys:
            extracted_data_children = []
            extracted_metadata_children = []
            for path in paths:
                if include == True:
                    # extract data from path if it contains the key
                    if key in os.path.split(path)[tail]:
                        extracted_metadata_children.append(read_file(path)[0])
                        extracted_data_children.append(np.array(read_file(path)[1])) 
                    else:
                        continue
                else:
                    # extract data from path if it does not contain the key
                    if key in os.path.split(path)[tail]:
                        continue
                    else:                
                        # extract data from path if it doesn't contain the key
                        extracted_metadata_children.append(read_file(path)[0])
                        extracted_data_children.append(np.array(read_file(path)[1]))
            extracted_metadata.append(extracted_metadata_children)
            extracted_data.append(extracted_data_children)

    return extracted_metadata, extracted_data
