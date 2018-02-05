import re
from collections import Counter

revant = "Revant Ohri: "
soha = "Soha Chhaya: "
soha_alt = "Soha: "

url_pattern = '(http[s]?|ftp):\/'

specialStrings = {
  ':P': [':P'],
  'bunny': ['bunny', 'bunnny'],
  'you are right': ["you're right", "you are right", "youre right"]
}

gif_str = "GIF omitted"
image_str = "image omitted"
csv_cols = 'date,timestamp,message_type\n'

junk = open('junk.txt', 'w')

rev_meta = open('rev_dates.csv', 'w')
rev_count = open('rev_count.csv', 'w')

soha_meta = open('soha_dates.csv', 'w')
soha_count = open('soha_count.csv', 'w')

text_dump = open('text_dump.txt', 'w')

base_chat = open('whatsapp_cleaned.txt', 'r')

line = base_chat.readline()

rev_meta.write(csv_cols)
soha_meta.write(csv_cols)

destination = junk
destination_count = junk
message_splitter = ':'

message_type = 'text'

rev_counter = Counter()
soha_counter = Counter()

while line:
  if (revant in line):
    destination = rev_meta
    destination_count = rev_count
    message_splitter = revant
    currCounter = rev_counter

  elif (soha in line) or (soha_alt in line):
    destination = soha_meta
    destination_count = soha_count
    currCounter = soha_counter
    if (soha_alt in line):
      message_splitter = soha_alt
    else:
      message_splitter = soha


  for key, value in specialStrings.items():
    for variation in value:
      if (variation in line):
        if matchedSpecialStings[key] is None:
          matchedSpecialStings[key] = 1
        else:
          matchedSpecialStings[key] += 1

  chunks = line.split(' ')

  date = chunks[0].lstrip('[').rstrip(',')
  time = chunks[1] + chunks[2].rstrip(']')

  main_split = line.split(message_splitter)

  message_payload = main_split[1].lstrip().rstrip()

  if(gif_str in message_payload):
    message_type = 'gif'
  elif(image_str in message_payload):
    message_type = 'image'
  elif(re.search(url_pattern, message_payload) is not None):
    message_type = 'link'
  else:
    message_type = 'text'


  currCounter.update({date: 1})
  destination.write(date+ ',' + time + ',' + message_type + '\n')

  if(message_type is 'text'):
    cleaned_message = re.sub(r"[^a-zA-Z ']", '', message_payload)
    text_dump.write(cleaned_message + ' ')

  line = base_chat.readline()

print(matchedSpecialStings);

rev_count.write('date,count\n')
for date in rev_counter:
  rev_count.write(date + ',' + str(rev_counter[date]) + '\n')


soha_count.write('date,count\n')
for date in soha_counter:
  soha_count.write(date + ',' + str(soha_counter[date]) + '\n')
