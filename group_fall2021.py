#%%
import os
from os.path import join
import pandas as pd
import numpy as np
import csv
from auto_group import find_files
# %%
current_path = os.path.dirname(os.path.abspath(__file__))
files = find_files('csv', current_path)
group_file = files[1]
files = find_files('xls', current_path)
roster_file = files[1]
print(group_file, '\n', roster_file)
# %%
group_df = pd.read_csv(group_file)
roster_df = pd.read_excel(roster_file)
# %%
split_func = lambda x: x.split('@')[0]
roster_df['login_id'] = roster_df['EmailAddress'].apply(split_func)
# %%
# diff = set(roster_df['login_id']).difference(set(group_df['login_id']))
diff = set(roster_df['StdtId']).difference(set(group_df['user_id']))
print(len(diff))

sort_login_id = sorted(roster_df['login_id'])
sort_login_id_1 = sorted(group_df['login_id'])
print(sort_login_id[:20])
print(sort_login_id_1[:20])
# %%
group_df_new = pd.merge(group_df, roster_df[['StdtId', 'Sec']],
                                how='left', 
                                left_on=['user_id'], 
                                right_on = ['StdtId'], 
                                suffixes=('','_new'))
group_df_new['group_name'] = 'Section ' + group_df_new['Sec']
group_df = group_df_new.drop(columns=['StdtId', 'Sec'])
# %%
group_df.to_csv(os.path.join(current_path, f'math233_groups.csv'),index=False)  
# %%
