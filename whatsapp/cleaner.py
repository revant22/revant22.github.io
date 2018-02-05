import re
new_chat_line_pattern = '\[\d+\/\d+\/\d+'

base_chat = open('whatsapp.txt', 'r')
cleaned_chat = open('whatsapp_cleaned.txt', 'w')

line = base_chat.readline().decode('utf-8-sig').encode('utf-8')
is_first_line = True
while line:
  if line.rstrip():
    if(re.search(new_chat_line_pattern, line) is None):
      cleaned_chat.write(' '+line.rstrip())
    elif (is_first_line):
      cleaned_chat.write(line.rstrip())
      is_first_line = False
    else:
      cleaned_chat.write('\n'+line.rstrip())

  line = base_chat.readline().decode('utf-8-sig').encode('utf-8')
