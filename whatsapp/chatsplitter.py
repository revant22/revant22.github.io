import re
from collections import Counter
import os
import json

script_dir = os.path.dirname(__file__)

names = ['soha', 'rev']
meta_data_types = ['texts', 'images', 'links', 'gifs', 'videos', 'admissions of defeat', '`i love yous`', 'tongue out smileys', 'affectionate nicknames']

meta_data = {}

def incrementMetaData(key, name_prefix):
  if(not meta_data[name_prefix]):
    meta_data[name_prefix].update({key:None})
  if(meta_data[name_prefix][key] is None):
    meta_data[name_prefix][key] = 1
  else:
    meta_data[name_prefix][key] += 1

def writeMetaDataToCsv():

  with open(os.path.join(script_dir, '../webapp/data/meta_data.json'), 'w') as meta_data_file:
    json.dump(meta_data, meta_data_file)

def initializeMetaData():
  for name in names:
    baseObj = {}
    for meta_type in meta_data_types:
      baseObj.update({meta_type:None})
    meta_data.update({name:baseObj})

initializeMetaData()

revant_aliases = ["Revant Ohri:", "Revant:", "Rayvant:"]
soha_aliases = ["Soha Chhaya:", "Soha:"]

url_pattern = '(http[s]?|ftp):\/'

specialStrings = {
  'admissions of defeat': ["you're right", "you are right", "youre right"],
  '`i love yous`': ["iloveyou", "i love you"],
  'tongue out smileys': [":p"],
  'affectionate nicknames': ["bunny", "monkey", "babe", "baby"]
}

gif_str = "GIF omitted"
image_str = "image omitted"
video_str = "video omitted"

junk = open(os.path.join(script_dir, 'data/junk.txt'), 'w')

rev_count = open(os.path.join(script_dir, '../webapp/data/rev_count.csv'), 'w')

soha_count = open(os.path.join(script_dir, '../webapp/data/soha_count.csv'), 'w')

text_dump = open(os.path.join(script_dir, 'data/text_dump.txt'), 'w')

base_chat = open(os.path.join(script_dir, 'data/cleaned_chat.txt'), 'r')

line = base_chat.readline()

destination_count = junk
message_splitter = ':'

message_type = 'texts'

rev_counter = Counter()
soha_counter = Counter()

while line:
  if any(revant_alias in line for revant_alias in revant_aliases):
    destination_count = rev_count
    currCounter = rev_counter
    name_prefix = 'rev'

  elif any(soha_alias in line for soha_alias in soha_aliases):
    destination_count = soha_count
    currCounter = soha_counter
    name_prefix = 'soha'

  chunks = line.split(' ')

  date = chunks[0].lstrip('[').rstrip(',')
  time = chunks[1] + chunks[2].rstrip(']')

  # payload = ''.join(chunks[3::])
  match = re.compile("\]").search(line)
  first_split = line[match.start():]
  match = re.compile("\: ").search(first_split)
  message_payload = first_split[match.start():].lstrip(':').lstrip().rstrip()

  if(gif_str in message_payload):
    message_type = 'gifs'
  elif(image_str in message_payload):
    message_type = 'images'
  elif(video_str in message_payload):
    message_type = 'videos'
  elif(re.search(url_pattern, message_payload) is not None):
    message_type = 'links'
  else:
    message_type = 'texts'

    uncased_payload = message_payload.lower()
    for special_str in specialStrings:
      if any(concession_str in uncased_payload for concession_str in specialStrings[special_str]):
        incrementMetaData(special_str, name_prefix)      

  incrementMetaData(message_type, name_prefix)
  
  currCounter.update({date: 1})

  if(message_type is 'texts'):
    cleaned_message = re.sub(r"[^a-zA-Z ]", '', message_payload)
    cleaned_message = re.sub(r"\b[A-z]{1,2}\b", '', cleaned_message)
    text_dump.write(cleaned_message + ' ')

  line = base_chat.readline()

print(meta_data);
writeMetaDataToCsv()

rev_count.write('date,count\n')
for date in rev_counter:
  rev_count.write(date + ',' + str(rev_counter[date]) + '\n')


soha_count.write('date,count\n')
for date in soha_counter:
  soha_count.write(date + ',' + str(soha_counter[date]) + '\n')

