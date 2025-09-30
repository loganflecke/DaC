

from splunklib.client import connect
from pathlib import Path
import os

service = connect(
    host="172.18.1.20",
    port="8089",
    username="logan",
    password="krigsgaldr" # war sorcerer
)

for file_path in Path("converted_rules").rglob("*"):
    search_name = os.path.splitext(os.path.basename(file_path))[0]
    if search_name in service.saved_searches:
        saved_search = service.saved_searches[search_name]
        with open(file_path, "r") as f:
            search_query = f.read()
            saved_search.update(search_query) 
    else:
        with open(file_path, "r") as f:
            search_query = f.read()
            saved_search = service.saved_searches.create(search_name, search_query)

print(f"Created: {saved_search.name}")