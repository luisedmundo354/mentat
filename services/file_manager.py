import os
import uuid
import json
from config import CONFIG

def create_and_write_report(content):
    """
    Creates a new file with a unique ID as the filename and writes JSON content to it.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = CONFIG['paths']['reports_dir']
    file_path = os.path.join(base_dir, reports_dir)

    # Ensure the reports directory exists
    os.makedirs(file_path, exist_ok=True)

    file_id = uuid.uuid4()
    filename = os.path.join(file_path, f"{file_id}.json")  # changed extension to .json

    try:
        with open(filename, "w") as file:  # "w" will overwrite safely (UUID ensures uniqueness)
            json.dump(content, file, indent=2)
        print(f"Report '{file_id}.json' created and written successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
