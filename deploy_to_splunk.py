import json
from splunklib.client import Service

def deploy_saved_search(saved_search):
    service = Service(
        host='172.18.1.20',
        port=8089,
        username='user',
        password='password'
    )
    service.login()

    if saved_search["name"] in service.saved_searches:
        service.saved_searches.delete(saved_search["name"])
    search = service.saved_searches.create(**saved_search)
    search.update(**create_saved_search_actions(saved_search["name"]))
    search.refresh()
    print(f"Successfully created alert: {saved_search['name']}")

def create_saved_search_actions(search_name):
    return {
        'alert_type': 'number of events',
        'alert_comparator': 'greater than',
        'alert_threshold': '0',
        'alert.severity': '3',
        'is_scheduled': '1',
        'cron_schedule': '*/5 * * * *',   # runs every 5 minutes
        "dispatch.earliest_time": "-5m",
        "dispatch.latest_time": "now",
        'actions': 'logevent',
        'action.logevent': '1',
        'action.logevent.param.event': f"{search_name} created on $result.host$ by $result.user$",
        'action.logevent.param.index': 'alert',
        'action.logevent.param.sourcetype': 'generic_single_line'
    }

def main():
    # Load saved searches from the JSON file
    with open('savedsearches.json', 'r') as json_file:
        deployable_searched = json.load(json_file)

    for search in deployable_searched:
        deploy_saved_search(search)

if __name__ == "__main__":
    main()
