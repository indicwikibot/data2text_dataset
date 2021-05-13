# -*- coding:utf-8 -*-
"""
Created in May 2021

@author: Shivprasad Sagare (2020701015)
"""

"""
For a specific wikidata entity, this script fetches the outlinks present in the wikipedia page, and then fetches the wikidata IDs of those 
outlink entites. Script takes as input the entities present in entity-info.json file and produces the output in output.json file. 

It uses pywikibot API to fetch the titles of pages referred as outlinks. Then it fetches the wikidata ID from this title using the index 
which has to be created beforehand. The title-ID index file is created using wikimapper package. The steps to create such a index for a
specific language are as follows.

Steps to create language specific title-ID index file. ('en' is used here for English. Use appropriate language code.)

Step 1: Download SQL dump for the specified language
wikimapper download enwiki-latest --dir data

Step 2: Create index
wikimapper create enwiki-latest --dumpdir data --target data/index_enwiki-latest.db

Visit https://github.com/jcklie/wikimapper for information about wikimapper package and its use.
"""

import json
import requests
import logging

import pywikibot
from wikimapper import WikiMapper

logging.basicConfig(level=logging.INFO, filename='log.log') #for tracking the progress
mapper = WikiMapper("/scratch/shivprasad.sagare/index_hiwiki-latest.db")    #mention the path to your created index file

with open('entities-info.json', 'r', encoding='utf8') as read_file: 
    read_data = json.load(read_file, encoding='utf8')

write_data = {}
keys = list(read_data.keys())
for i, key in list(enumerate(keys)):
    logging.info(f"ID : {key}       entity number : {i}   total : {len(keys)}")
    write_data[key] = {}
    for lang, title in read_data[key].items():
        lang_code = lang.split('_')[0]  #extracting lang code from the string
        if(lang_code=='hi'):    #mention the specific language code of your interest.
            site = pywikibot.Site(lang_code, 'wikipedia')
            page = pywikibot.Page(site, title)
            out_links = page.linkedPages()
          
            write_data[key][lang_code] = {}
            write_data[key][lang_code]['title'] = title
            write_data[key][lang_code]['links']={}

            for i in out_links:
                try:
                    title = str(i).split(':')[1][:-2]   #heuristics to extract title from returned string output by pywikibot method
                    title = '_'.join(title.split())
                    Q_id = mapper.title_to_id(title)    #lookup for ID based on title
                    if(Q_id is not None):
                        write_data[key][lang_code]['links'][Q_id] = title
                except Exception as e:
                    print(e)
                    continue

with open('/scratch/shivprasad.sagare/output_hi.json', 'w', encoding='utf8') as write_file: #storing the output in json file
    json.dump(write_data, write_file)