import json
def edit_datajson(json_file_name,id,value):
  with open(f'cogs//{json_file_name}.json', 'r+') as f:
      data = json.load(f)
      data[id] = list(value) if type(value) is tuple else value 
      #doing this because list is unhashable type so have to send tags using tuple
      f.seek(0)# <--- should reset file position to the beginning.
      json.dump(data, f, indent=4)
      f.truncate()
    
def get_datajson(json_file_name):
    with open(f'cogs//{json_file_name}.json', 'r+') as f:
        data = f.read()
        jsonObj = json.loads(data)
    return(jsonObj)