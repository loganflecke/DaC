

from splunklib.client import connect
from pathlib import Path
import os

service = connect(
    host="192.168.1.1", # Splunk IP
    port="8089", # Splunk management port
    username="username", # user name with admin privileges to create/modify rules
    password="password"
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
