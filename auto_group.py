#%%
import os
from os.path import join
import pandas as pd
import numpy as np
import csv
# %%
def find_files(name, path):
    result = []
    for root, _, files in os.walk(path):
        for _file in files:
            if name in _file:
                result.append(os.path.join(root, _file))
    return result


def argsort(seq):
    '''
    http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    '''
    return sorted(range(len(seq)), key=seq.__getitem__)

def split_string(string: str, string_lst):
    '''
    split a string with more than 1 types of delimiters
    '''
    index_string = []
    index_lst = []
    for idx, _str in enumerate(string_lst):
        if _str in string:
            index_string.append(string.index(_str))
            index_lst.append(idx)
        else:
            continue
    index_pointer = argsort(index_string)
    return [string_lst[index_lst[i]] for i in index_pointer]
# %%
if __name__ == "__main__": 
    current_path = os.path.dirname(os.path.abspath(__file__))

    section_roster_files = find_files('txt', current_path)
    course_roster_file = find_files('csv', current_path)

    section_numbers = [s.split('_')[-1].split('.')[0] for s in section_roster_files]
    section_roster_lst = []
    columns_names = ['Semester', 
                    'Number',  
                    'Section',
                    'Name, First or Preferred Name',
                    'Middle',
                    'Name, Last',
                    'Student ID',
                    'Email Address']

    
    course_df = pd.read_csv(course_roster_file[0])
    # course_df['Name, First or Preferred Name'] = [s.split(',')[-1][1:] for s in course_df['name']]
    # course_df['Name, Last'] = [s.split(',')[0] for s in course_df['name']]
    course_df[['group_name']] = None

    for _file in section_roster_files:
        print(f'Processing {_file}')
        with open(_file, newline='') as f:
            rows = csv.reader(f, delimiter='\t')
            _roster = []
            for i, row in enumerate(rows):
                if row:
                    if i == 0:
                        columns = split_string(row[0], columns_names)
                        if 'Middle' in columns:
                            index_middle = columns.index('Middle')
                            columns.remove('Middle')
                        _roster.append(columns)
                        len_columns = len(columns)
                    else:
                        row_student = row[0].split()
                        try:
                            if len(row_student) == len_columns + 1:
                                _ = row_student.pop(index_middle)
                        except:
                            pass
                        _roster.append(row_student)
        section_df = pd.DataFrame(_roster)
        section_df.columns = section_df.iloc[0]
        section_df = section_df[1:]
        section_df['name'] = section_df[['Name, Last', 'Name, First or Preferred Name']].agg(', '.join, axis=1)

        try:
            section_df['group_name'] = ['Section '+s for s in section_df.Section]
            course_df = pd.merge(course_df, section_df[['name', 'group_name']],
                                how='left', 
                                left_on=['name'], 
                                right_on = ['name'], 
                                suffixes=('','_new'))
            course_df['group_name'] = course_df['group_name'].fillna(course_df['group_name_new'])
            course_df = course_df.drop(columns=['group_name_new'])
            print(f'{_file} merged to course roster. \n')
        except:
            print('No section found.\n')
            pass
    
    course_name = course_df.sections.unique()[0].split(' - ')[0]
    course_df.to_csv(os.path.join(current_path, f'{course_name}_groups.csv'),index=False)   