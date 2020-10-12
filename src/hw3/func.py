"""
This script contains functions used in analysis.py
Some of these functions are later used for unit tests
"""





import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import collections
import argparse
import json
import os.path as osp



def pony_id(row):
  if row['pony'].lower() == 'twilight sparkle':
    return 'twilight'
  elif row['pony'].lower() == 'applejack':
    return 'applejack'
  elif row['pony'].lower() == 'rarity':
    return 'rarity'
  elif row['pony'].lower() == 'pinkie pie':
    return 'pinkie'
  elif row['pony'].lower() == 'rainbow dash':
    return 'rainbow'
  elif row['pony'].lower() == 'fluttershy':
    return 'fluttershy'
  else:
    return 'non-Pony'

def cap_and_split_names(name):
    name = name.title()
    if name == 'Twilight':
      name = ['Twilight','Sparkle']
    elif name == 'Pinkie':
      name = ['Pinkie', 'Pie']
    elif name == 'Rainbow':
      name = ['Rainbow', 'Dash']
    return name

def compile_name_regex(name):
  if type(name) == list:
    word1 = '[\W]+' + name[0] + '[\W]+'
    word2 = '[\W]+' + name[1] + '[\W]+'
    reg = [re.compile(word1), re.compile(word2)]
  else:
    word = f'[\W]+{name}[\W]+'
    reg = re.compile(word)
  return reg

def if_mentioend(name, reg, dialog):
  if (re.search(reg,dialog) != None) or (dialog.startswith(name)) or (dialog.endswith(name)):
    return 1
  else:
    return 0

#def normalize_dict(d, target=1.0):
#  raw = sum(d.values())
#  factor = target/raw
#  return {key:'%.2f'%(value*factor) for key,value in d.items()}

def normalize_dict(d, target=1.0):
    total = sum(d.values())
    total = total + 1e8 if total == 0 else total
    return {k: "%0.2f" % (v * target / total) for k, v in d.items()}

def mentions_subdicts(df_pony_mentioned1):
  p2 = {}
  for idx, row in df_pony_mentioned1.iterrows():
    # create sub-dictionary for each pony
    tmp = {}
    for colname in row.index.values:
      if row[['pony_id']].values[0] == colname or colname == 'pony_id':
        continue
      tmp[colname] = row[[colname]].values[0]

    # normalize elements in dict
    tmp1 = normalize_dict(tmp)
    p2[row[['pony_id']].values[0]] = tmp1
  return p2

def follow_on_comments_subdicts(df_count_follow):
  p3 = {}
  for idx, row in df_count_follow.iterrows():
    # create sub-dictionary for each pony, and other
    tmp = {}
    for colname in row.index.values:
      if idx == colname:
        continue
      tmp[colname] = row[[colname]].values[0]

    # normalize elements in dict
    tmp1 = normalize_dict(tmp)
    p3[idx] = tmp1
  return p3

def read_textfile(script_dir):
  text_address = osp.join(script_dir, '..', 'data', 'words_alpha.txt')
  text_file = open(text_address, "r")
  return text_file

def non_dictionary_words_subdicts(df4, words):
  p4 = {}
  for pony in df4['pony_id'].unique():
    p4[pony] = pony_nondict(pony,df4,words)
  return p4

def create_analysis(p1,p2,p3,p4):
  analysis = {'verbosity': p1}
  analysis['mentions'] = p2
  analysis['follow_on_comments'] = p3
  analysis['non_dictionary_words'] = p4
  return analysis


###############################################################
def pony_nondict(pony_name,df,words):
  print(f'Extracting non-dictionary words for pony {pony_name}')
  pony_df = df[df['pony_id']==pony_name]
  pony_df.index = range(0,len(pony_df))
  print(f"The number of dialogs for pony {pony_name} is:",len(pony_df))

  pony_nondict = []
  for idx, row in pony_df.iterrows():
    dialog_words = row.dialog
    if '<U+' in dialog_words:
      dialog_words = re.sub(r"<U\+\d+>", "", dialog_words)
    dialog_words = re.split("[^a-zA-Z0-9]",dialog_words)
    dialog_words = list(filter(lambda a: a != '', dialog_words))

    for dialog_word in dialog_words:
      if dialog_word.lower() not in words:
        pony_nondict.append(dialog_word)
  
  counter=collections.Counter(pony_nondict)
  common = [x[0] for x in counter.most_common(5)]
  print(f"The top five common non-dictionary words for pony {pony_name} is:",common)
  return common
