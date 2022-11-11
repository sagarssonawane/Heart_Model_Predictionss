import config
import json
with open(config.JSON_FILE_PATH,"r") as file:
    json_data = json.load(file)
print(len(json_data["columns"]))
