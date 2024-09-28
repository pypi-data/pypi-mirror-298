'''
functions for input and output of files for egger
    functions:
        read_tsv(filename: str) -> List[str]
'''
import csv
from typing import List

def read_tsv(filename: str) -> List[str]:
    '''
    read a tsv file
        arguments: 
            filename: path to .tsv file
        returns:
            lines: list of lines from the .tsv file
    '''
    with open(filename, 'r') as file: #os.path?
        reader = csv.reader(file, delimiter='\t')
        lines = []
        for row in reader:
            lines.append(row)
        return lines

def write_to_tsv(filename:str, contents: List) -> None:
    '''
    Writes a list of lines to a .tsv file with the path provided
        arguments:
            filename: path to write the .tsv
            contents: a list of lines to write
        returns:
            None
    '''
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(contents)
    