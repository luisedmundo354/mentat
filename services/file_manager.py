import os
import uuid
import json
from datetime import datetime
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

def save_transcription(transcription_text: str, output_path: str = None) -> str:
    """
    Save the transcription text to a file.

    Args:
        transcription_text (str): The full transcription text to be saved.
        output_path (str, optional): The file path where the transcription should be saved.
                                     If not provided, a filename based on the current timestamp is used.

    Returns:
        str: The path where the transcription was saved.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    transcripts_dir = CONFIG['paths']['transcripts_dir']
    file_path = os.path.join(base_dir, transcripts_dir)

    # Ensure the reports directory exists
    os.makedirs(file_path, exist_ok=True)

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(file_path, f"transcription_{timestamp}.txt")

    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(transcription_text)
        print(f"Transcription successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save transcription: {e}")

    return output_path

