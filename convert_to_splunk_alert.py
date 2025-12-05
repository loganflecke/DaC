import subprocess
import git
from pathlib import Path
import json

mappings = {
        "rule_pipeline_mapping" : {
            "windows" : "splunk_windows"
        }
    }

def create_saved_search_base(rule, pipeline, output_filename):
    # Convert the Sigma rule to SPL format
    command = ['sigma', 'convert', '-t', 'splunk', '-p', pipeline, rule, '-o', output_filename]
    sigma_convert = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if sigma_convert.returncode != 0:
        raise RuntimeError(f"Error during conversion: {sigma_convert.stderr.decode()}")

    # Read the SPL string, creating the final search that because the detection
    with open(output_filename, 'r') as spl_file:
        splunk_search = "`sysmon` " + spl_file.read() if pipeline == "splunk_windows" else "index=main " + spl_file.read()

    # Create a dictionary of the base parameters required to make a detection
    return {
        'name': rule.stem,
        'search': splunk_search
    }

def main():
    rules_path = Path(get_git_root()) / "rules"
    rules = rules_path.iterdir()
    saved_searches = []

    for rule_type in rules:
        print(rule_type.name)
        pipeline = mappings["rule_pipeline_mapping"].get(rule_type.name)
        for rule in rule_type.iterdir():
            if rule.suffix == ".yml":
                output_filename = Path(get_git_root()) / "converted_rules" / (rule.stem + ".spl")
                saved_searches.append(create_saved_search_base(rule, pipeline, output_filename))
    # Save the saved searches to a JSON file for later use
    with open('savedsearches.json', 'w') as json_file:
        json.dump(saved_searches, json_file, indent=2)

def get_git_root() -> Path:
    repo = git.Repo(search_parent_directories=True)
    return Path(repo.working_tree_dir)

if __name__ == "__main__":
    main()
