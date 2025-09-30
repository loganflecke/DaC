# Convert a Sigma rule to Elasticsearch_DSL

from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth
import requests
import warnings
import os
import json

RULES_DIR = "converted_rules"

for filename in os.listdir(RULES_DIR):
    print(filename)

# Suppress the generic 'SecurityWarning' from any package
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=Warning)  # fallback if it's not categorized

def main():
    current_rules_list = get_current_rules()
    print("get_current_rules() worked")
    print(current_rules_list)
    print("")
    print(json.dumps(current_rules_list, indent=2))


# list rules to see if the rule should be updated or created, follow https://www.elastic.co/docs/api/doc/kibana/operation/operation-findrules
# GET /api/detection_engine/rules/_find
def get_current_rules():
    # Using requests
    elastic_url = "http://172.18.1.10:80"
    headers = {"Content-Type": "application/json"}
    so_auth = HTTPBasicAuth('jupyter', 'Passw0rd') 
    all_rules = []
    page = 1

    while True:
        url = f"{elastic_url}/api/detection_engine/rules/_find?page={page}&per_page=1000"
        try:
            response = requests.get(url, auth=so_auth, headers=headers, verify=False)
            response.raise_for_status()
            data = response.json()
            rules = data.get('data', [])
            if not rules:
                break
            all_rules.extend(rules)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rules: {e}")
            break


    # Using Elasticsearch
    #current_rules = Elasticsearch(f"http://172.18.1.10:80", basic_auth=so_auth, verify_certs=False)
    #return current_rules.transport.perform_request("GET", "/api/detection_engine/rules/_find")
    return all_rules

# if updated, follow https://www.elastic.co/docs/api/doc/kibana/operation/operation-updaterule
# if created, follow https://www.elastic.co/docs/api/doc/kibana/operation/operation-createrule


main()
'''
es = Elasticsearch(['http://172.18.1.10:9200'])
searchContext = Search(using=es, index='logs-*', doc_type='doc')
s = searchContext.query('query_string', query='event_id:1')

response = s.execute()
if response.success():
    df = pd.DataFrame((d.to_dict() for d in s.scan()))
df
'''