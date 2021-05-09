# %%
import os
import pandas as pd
import numpy as np
import csv
from auto_group import find_files
pd.options.display.max_rows = 200
# %%
current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'Math217')
course_roster_file = find_files('csv', data_path)
# %%
'''
Check zoom attendance
'''

# %%
all_weeks = ((0, 1, 2),
             (3, 4, 5),
             (6, 7, 8),
             (9, 10, 11),
             (12, 13, 14),
             (15, 16),
             (17, 18, 19),
             (20, 21, 22),
             (23, 24, 25),
             (26, 27, 28),
             (29, 30),
             (31, 32, 33),
             (34, 35, 36))

def replace_email(df):
    dict_email = {}
    for key in dict_email.keys():
        df.loc[df['Name (Original Name)']==key, 'User Email'] = dict_email[key]
    return df
# %%
df_ref = pd.read_csv(os.path.join(data_path, course_roster_file[0]))
df_ref = df_ref[['Name (Original Name)', 'User Email']]
# df_ref = replace_email(df_ref)


for n, week in enumerate(all_weeks):
    df_attn = []
    for i in week:
        df_lec = pd.read_csv(os.path.join(data_path, course_roster_file[i]))
        # df_lec = replace_email(df_lec)

        try:
            df_lec[['Total Duration (Minutes)']] = df_lec[['Total Duration (Minutes)']].fillna(0).copy()
        except:
            df_lec[['Duration (Minutes)']] = df_lec[['Duration (Minutes)']].fillna(0).copy()

        if 'Total Duration (Minutes)' not in df_lec.columns:
            df_lec['Total Duration (Minutes)'] = df_lec['Duration (Minutes)'].copy()

        df_lec['Total Duration (Minutes)'] = \
            np.where(df_lec['Total Duration (Minutes)'] == 'No',
                     0, df_lec['Total Duration (Minutes)']).astype(int)
        df_attn.append(df_lec)
        df_min = pd.concat(df_attn)\
            .groupby('User Email')['Total Duration (Minutes)']\
            .sum().reset_index()
    df_ref = pd.merge(df_ref, df_min, how='left', on='User Email', suffixes=(None, f' week {n+1}'))
    # if n>=2:
    #     break
# df_ref = df_ref.drop(columns=['Total Duration (Minutes)'])
df_ref = df_ref.sort_values(by=['Name (Original Name)'])
df_ref.fillna(0, inplace=True)
# %%
df_ref.to_csv('sec1_attn.csv', index=False)
# %%
