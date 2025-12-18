# Python Script to assert the data in Splunk supports detections 
# Written by Logan Flecke

import splunklib.client as client
import splunklib.results as results
import pandas as pd
import re
import json
import os
from dotenv import load_dotenv

def main():
    s = connect_to_splunk()
    detection_list = get_detections(s) # List of saved searches, specifically user-made detections
    fields_validated = validate_field_existence(get_detection_fields(detection_list), s, "main", "xmlwineventlog")
    print(fields_validated)

def connect_to_splunk():
    load_dotenv()
    required = ["SPLUNK_HOST", "SPLUNK_USERNAME", "SPLUNK_PASSWORD"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")
    return client.connect(
        host=os.getenv("SPLUNK_HOST"),
        port=int(os.getenv("SPLUNK_PORT", 8089)),
        username=os.getenv("SPLUNK_USERNAME"),
        password=os.getenv("SPLUNK_PASSWORD"),
    )

# Execute a Splunk search and return results as a list of dictionaries.
def splunk_query(service, search, *, earliest="-15m", latest="now", output_mode="json"):
    """
    Args:
        service (splunklib.client.Service): Authenticated Splunk service
        search (str): SPL search (minimal SPL recommended)
        earliest (str): Time range start
        latest (str): Time range end
        output_mode (str): Output format (default: json)
    """

    # Handle time span
    if not ("earliest=" in search or "latest=" in search):
        search = f"earliest={earliest} latest={latest} {search}"
    if not search.startswith("search"):
        search = f"search {search}"

    response = service.jobs.oneshot(
        search,
        output_mode=output_mode
    )

    reader = results.JSONResultsReader(response)

    return [item for item in reader if isinstance(item, dict)]

# Returns a list of Splunk Saved Searches
def get_detections(service):
    saved_searches = service.saved_searches
    detection_list = []

    for saved_search in saved_searches:
        # Convert all JSON-serializable attributes automatically
        saved_search_dict = {}

        # Include attributes from the SavedSearch object
        for key, value in saved_search.__dict__.items():
            try:
                json.dumps(value)  # test if value is JSON serializable
                saved_search_dict[key] = value
            except (TypeError, OverflowError):
                saved_search_dict[key] = str(value)  # fallback to string

        # Optionally include content dict (all the search metadata)
        if hasattr(saved_search, 'content'):
            for k, v in saved_search.content.items():
                try:
                    json.dumps(v)
                    saved_search_dict[k] = v
                except (TypeError, OverflowError):
                    saved_search_dict[k] = str(v)

        if saved_search.access.get('owner') != 'nobody':
            detection_list.append(saved_search_dict)
    return detection_list

# Returns a set of the fields extracted from a SPL search
def get_search_fields(search):
    # get all non-whitespace characters before “=“, “ IN “. Exclude “\=“ and any that are wrapped in “” or ''
    pattern = re.compile(r'''(?<!\\)(?<!["'])\b[^\s(=]+?(?=\s*(?:=|\sIN\s))''')
    fields = pattern.findall(search)
    return set(fields)

# Returns a set of fields present in a list of detection searches
def get_detection_fields(detection_list):
    detection_fields = set()
    for detection in detection_list:
        search = str(detection['_state']['content']['search'])
        search = search.strip()
        detection_fields = get_search_fields(search).union(detection_fields)
    return detection_fields

# Returns True if all fields provided exist in the given index and sourcetype, searching Splunk over a given service connection
def validate_field_existence(fields, service, index, sourcetype):
    fields_search_syntax = ", ".join(sorted(list(fields)))
    search_query = f'index={index} sourcetype={sourcetype} | fields {fields_search_syntax} | fieldsummary'
    events = splunk_query(service, search_query, earliest=0)
    field_existence_df = pd.DataFrame(events, columns=['field', 'count', 'distinct_count', 'values'])
    # missing_fields = field_existence_df.loc[(field_existence_df['count'].astype(int) == 0) | ~field_existence_df['field'].isin(fields).all()]
    present_fields = set(field_existence_df['field'])
    missing_fields = sorted(fields - present_fields)
    if not missing_fields:
        print("No missing fields")
        return True
    print("Missing fields:", ", ".join(missing_fields))
    return False

if __name__ == "__main__":
    main()
