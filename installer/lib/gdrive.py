import os
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import json

# Get environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_EMAIL = os.getenv('CLIENT_EMAIL')
PRIVATE_KEY_ID = os.getenv('PRIVATE_KEY_ID')
PRIVATE_KEY = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
PROJECT_ID = os.getenv("PROJECT_ID")
CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")

# Define your OAuth2 credentials directly
JSON_DATA = {
                "type": "service_account",
                "project_id": PROJECT_ID,
                "private_key_id": PRIVATE_KEY_ID,
                "private_key": PRIVATE_KEY,
                "client_email": CLIENT_EMAIL,
                "client_id": CLIENT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": CLIENT_X509_CERT_URL,
                "universe_domain": "googleapis.com"
            }

# Authentication
def get_drive_service():
    """
    Authenticate and return the Google Drive API service.
    """
    
    # Build and return the Drive service
    credentials = service_account.Credentials.from_service_account_info(
                                                                            JSON_DATA, 
                                                                            scopes=['https://www.googleapis.com/auth/drive']
                                                                       )
    service = build('drive', 'v3', credentials=credentials)
    return service

# List all files 
def list_all_files():
    """
    List all file IDs and names in Google Drive.
    """

    # Build the Drive service
    drive_service = get_drive_service()

    try:
        results = drive_service.files().list(fields="nextPageToken, files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            print("No files found in Google Drive.")
        else:
            for file in files:
                print(f"File ID: {file['id']}, Name: {file['name']}")
    except Exception as e:
        print(f"Error listing files: {e}")
        raise e

# Get File ID from File Name
def get_files_id_by_name(file_names):
    """
    List file IDs for specific file names in Google Drive.
    """

    # Build the Drive service
    drive_service = get_drive_service()

    # Set the query parameters
    fields = 'files(id, name)'
    pageSize = 1000  # Set an appropriate page size to retrieve all files

    # List the files matching the query
    results = drive_service.files().list(
                                            fields=fields, 
                                            pageSize=pageSize
                                        ).execute()
    files = results.get('files', [])

    return files[0]


# Create a new file
def create_file(file_path):
    """
    Create a new file on Google Drive.
    """

    # Build the Drive service
    print(file_path)
    drive_service = get_drive_service()

    try:
        file_name = os.path.basename(file_path)
        media = MediaFileUpload(file_path, mimetype='application/octet-stream')
        file_metadata = {'name': file_name}
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"Uploaded '{file_name}' with ID: {file['id']}")
        
        return file
    except Exception as e:
        print(f"Upload error: {e}")
        raise e

# Update existing file
def update_file(new_file):
    """
    Update an existing file on Google Drive.
    """

    # Build the Drive service
    drive_service = get_drive_service()

    # get file id
    file_id = get_files_id_by_name(file_metadata={'name': new_file})

    # Update the file
    file = drive_service.files().update(fileId=file_id, body=file_metadata).execute()
    return file

# Delete a file by its ID
def delete_file(file_id):
    """
    Delete a file in Google Drive by its ID.
    """

    # Build the Drive service
    drive_service = get_drive_service()

    # Deleting specific file
    try:
        drive_service.files().delete(fileId=file_id).execute()
        print(f"Deleted file with ID: {file_id}")
    except Exception as e:
        print(f"Error deleting file with ID {file_id}: {e}")
        raise e

# List and delete all files 
def delete_all_files():
    """
    List and delete all files in Google Drive.
    """

    # Build the Drive service
    drive_service = get_drive_service()

    # Set the query parameters to list all files
    fields = 'files(id, name)'
    pageSize = 1000  # Set an appropriate page size to retrieve all files

    try:
        # List all files
        results = drive_service.files().list(
                                                fields=fields, 
                                                pageSize=pageSize                  
                                            ).execute()
        files = results.get('files', [])

        # Delete each file in the list
        for file in files:
            delete_file(file['id'])
    except Exception as e:
        print(f"Error deleting files: {e}")
        raise e
