import os
import glob
import json
from config import CONFIG
from services.file_manager import create_and_write_report
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

os.environ["AZURE_INFERENCE_CREDENTIAL"] = CONFIG['services']['AZURE_INFERENCE_CREDENTIAL']
api_key = os.getenv("AZURE_INFERENCE_CREDENTIAL")
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# Create the client
client = ChatCompletionsClient(
    endpoint='https://Phi-3-5-MoE-instruct-gaqxj.eastus2.models.ai.azure.com',
    credential=AzureKeyCredential(api_key)
)

# Get model info
model_info = client.get_model_info()
print("Model name:", model_info.model_name)
print("Model type:", model_info.model_type)
print("Model provider name:", model_info.model_provider_name)

def generate_report():
    # Get the latest transcript file from the specified directory
    directory = CONFIG['paths']['transcripts_dir']
    list_of_files = glob.glob(os.path.join(directory, "*.txt"))
    if not list_of_files:
        print("No transcript files found.")
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    
    try:
        with open(latest_file, 'r') as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Process the file content to get a title, summary, and a rewritten report
    title, summary, report = organize_text(client, file_content)

    report_data = {
        'title': title,
        'summary': summary,
        'report': report
    }
    # Save the report using the file manager
    create_and_write_report(report_data)

    return report_data

def organize_text(client, input_text):
    # First, rewrite the conversation report
    messages = [
        {
            "role": "system",
            "content": "You need to clean this text conversation between a patient and a doctor. Rewrite this report correcting any mistakes and deleting text with no meaning."
        },
        {
            "role": "user",
            "content": f"This is the text you need to rewrite: {input_text}"
        }
    ]
    payload = {
        "messages": messages,
        "max_tokens": 3000,
        "temperature": 0.2,
        "top_p": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }
    response = client.complete(payload)
    report = response.choices[0].message.content

    # Next, generate a summary and title
    messages = [
        {
            "role": "system",
            "content": (
                "Generate a 2 sentence summary of this conversation between a patient and a doctor "
                "and give it a title. Output the result as a JSON string with the keys 'summary' and 'title'."
            )
        },
        {
            "role": "user",
            "content": input_text
        }
    ]
    payload = {
        "messages": messages,
        "max_tokens": 3000,
        "temperature": 0.2,
        "top_p": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }
    response = client.complete(payload)
    summary_title_str = response.choices[0].message.content

    try:
        summary_title = json.loads(summary_title_str)
        summary = summary_title.get("summary", "")
        title = summary_title.get("title", "")
    except json.JSONDecodeError as e:
        print(f"Error parsing summary and title: {e}")
        summary = ""
        title = ""

    return title, summary, report
