import re
import os

script_dir = os.path.dirname(__file__)

def cleanChatFunc():
	new_chat_line_pattern = '\[\d+\/\d+\/\d+'

	base_chat_path = os.path.join(script_dir, 'data/_chat.txt')
	base_chat = open(base_chat_path, 'r')

	cleaned_chat_path = os.path.join(script_dir, 'data/cleaned_chat.txt')
	cleaned_chat = open(cleaned_chat_path, 'w')

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
