from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import io
import os
from dotenv import load_dotenv
import json
import tempfile

load_dotenv()

service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
credentials = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/drive.file"])

# Initialize Google Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

# Function to create a file on Google Drive
def create_google_drive_file(title, content):
    # Create an in-memory text stream and write the content into it
   # Create a temporary file to write the content into it
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Prepare the file metadata
    file_metadata = {
        "name": title,
        "mimeType": "text/markdown",
    }

    # Use MediaFileUpload class to upload the in-memory file to Google Drive
    media = MediaFileUpload(temp_file_path, mimetype="text/markdown", resumable=True)
    request = drive_service.files().create(
        body=file_metadata,
        media_body=media,
    )
    
    # Execute the file creation on Google Drive
    file = request.execute()
    return file["id"]

def share_with_me(file_id):
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'dan.kirsche@gmail.com'  # Replace with your email address
    }
    command = drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id'
    )
    command.execute()
# Function to generate GPT-4 response (hypothetical)
# def get_gpt4_response(prompt):
#    response = your_gpt4_client_library.generate_text(prompt)
#    return response

# Example usage
if __name__ == "__main__":
    file_title = "GPT-4_Response.md"
    
    # Hypothetical GPT-4 API usage
    # prompt = "Tell me about climate change."
    # gpt4_response = get_gpt4_response(prompt)

    # For demonstration, let's use a sample text as the GPT-4 response
    gpt4_response = """# Climate Change

    Climate change refers to significant changes in global temperatures and weather patterns over time.

    ## Causes
    - Human activities
    - Natural factors

    ## Effects
    - Rising sea levels
    - Extreme weather events
    """
    
    # Create Google Drive markdown file and upload the content
    file_id = create_google_drive_file(file_title, gpt4_response)
    print(f"File created with ID: {file_id}")
