"""
This script comtains the main function for comp598 hw3, which does analysis on pony dialogs
"""




import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import collections
import argparse
import json
import os.path as osp
from hw3.func import *

script_dir = osp.dirname(__file__)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('src_file', help='the input csv file')
  parser.add_argument('-o','--output',help='the name of the output json file')
  args = parser.parse_args()

  src_file = args.src_file
  json_name = args.output
  df = pd.read_csv(src_file, delimiter=',')

  ### verbosity ###
  print('Analyzing verbosity...')
  new_col = df.apply(lambda row: pony_id(row), axis=1).values # add new col containing pony id
  df1 = df.assign(pony_id=new_col)

  df1_prev = df1.shift(1)
  df1_unique = df1[(df1['title'] != df1_prev['title']) | (df1['pony_id'] != df1_prev['pony_id'])]
  p1 = dict(df1_unique['pony_id'][df1_unique['pony_id']!='non-Pony'].value_counts(normalize=True))
  p1 = {key:'%.2f'%(value) for key,value in p1.items()}
  
  ### mentions ###
  print('Analyzing mentions...')
  df2 = df1[df1['pony_id']!='non-Pony'][['pony_id','dialog']] # get pony_id and dialog cols
  df2.index = range(0,len(df2))

  df2_copy = df2.copy()
  pony_mentioned = {}
  for name in df2['pony_id'].unique():
    name_copy = name
    new_col = []
    # capitalize and split name
    name = name.title()
    if name == 'Twilight':
      name = ['Twilight','Sparkle', 'Twilight Sparkle']
    elif name == 'Pinkie':
      name = ['Pinkie', 'Pie', 'Pinkie Pie']
    elif name == 'Rainbow':
      name = ['Rainbow', 'Dash', 'Rainbow Dash']

    # find pony names in dialogs
    for idx, row in df2[['dialog']].iterrows():
      if type(name) == list:
        num_first_name = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(name[0]), row.dialog))
        num_last_name = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(name[1]), row.dialog))
        num_whole_name = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(name[2]), row.dialog))
        num_names = num_first_name+num_last_name-num_whole_name
        new_col.append(num_names)
      else:
        num_names = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(name), row.dialog))
        new_col.append(num_names)


    pony_mentioned[name_copy] = np.array(new_col)

  df_pony_mentioned = pd.DataFrame.from_dict(pony_mentioned) # create df containing summary of mentions
  df_pony_mentioned['pony_id'] = df2[['pony_id']]
  dic = {'twilight': 'sum', 'applejack': 'sum', 'rainbow': 'sum', 'rarity': 'sum', 'fluttershy': 'sum', 'pinkie': 'sum'}
  df_pony_mentioned1 = df_pony_mentioned.groupby('pony_id', as_index=False).aggregate(dic).reindex(columns=df_pony_mentioned.columns)

  p2 = mentions_subdicts(df_pony_mentioned1) # create sub-dictionaries

  ### follow_on_comments ###
  print('Analyzing follow_on_comments...')
  df3 = df1.copy()
  df3['pony_id'][df3['pony_id']=='non-Pony']='other' # change value 'non-Pony' to 'other'

  # create summary df for follow_on_comments
  df_count_follow = pd.DataFrame(index=['twilight','applejack', 'rainbow', 'rarity','fluttershy', 'pinkie','other'],
                               columns=['twilight','applejack', 'rainbow', 'rarity','fluttershy', 'pinkie','other'])
  df_count_follow = df_count_follow.fillna(0)

  cnt = 0
  for idx, row in df3[['pony_id']].iterrows():
    current = row.pony_id
    next = df3.loc[idx+1,'pony_id']
    df_count_follow.loc[next,current]+=1

    if cnt == len(df3)-2:
      break
    cnt+=1


  cnt = 0
  for idx, row in df3[['title','pony_id']].iterrows():
    current_id = row.pony_id
    next_id = df3.loc[idx+1,'pony_id']
    current_title = row.title
    next_title = df3.loc[idx+1,'title']
    if current_title == next_title:
      df_count_follow.loc[next_id,current_id]+=1

    if cnt == len(df3)-2:
      break
    cnt+=1

  p3 = follow_on_comments_subdicts(df_count_follow) # create sub-dictionaries

  # non_dictionary_words
  print('Analyzing non_dictionary_words...')
  df4 = df1[df1['pony_id']!='non-Pony'][['pony_id','dialog']]

  text_file = read_textfile(script_dir) # read in txt
  words = text_file.read()
  words = words.split("\n")
  text_file.close()

  p4 = non_dictionary_words_subdicts(df4, words) # create sub-dictionaries

  analysis = create_analysis(p1,p2,p3,p4)

  # store or display as json
  if json_name == None:
    json_object = json.dumps(analysis, indent = 2)
    print(json_object)
  else:
    with open(json_name, "w") as outfile:
      json.dump(analysis, outfile)


if __name__ == '__main__':
  main()
