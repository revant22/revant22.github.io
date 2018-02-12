
def incrementMetaData(meta_data, key, name_prefix):
	if(not meta_data[name_prefix]):
		meta_data[name_prefix].update({key:None})
  if(meta_data[name_prefix][key] is None):
    meta_data[name_prefix][key] = 1
  else:
    meta_data[name_prefix][key] += 1
