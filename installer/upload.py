import lib.gdrive as gdrive
import os

################################
######### Variables ############
################################

################################
####### GenericFunctions #######
################################

################################
####### Display of data ########
################################

# -- List datat in parent folder
print("Listing Existing Files")
list_files = gdrive.list_files_in_folder()
print(gdrive.list_files_in_folder())

if len(list_files)>0:
    gdrive.delete_all_files_in_folder()

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# -- Replace with the path to your CSV file
print("current_directory -- "+current_directory)
csv_file_path = current_directory+'/data/project.csv'

# -- Check if the CSV file exists
if not os.path.exists(csv_file_path):
    print(f"CSV file '{csv_file_path}' does not exist.")
    exit

file_name = os.path.basename(csv_file_path)

# -- Create a new file on Google Drive with the CSV file
try:
    gdrive.create_file(file_name)
    print(f"Created and uploaded '{file_name}' to Google Drive.")
except Exception as e:
    print(f"Error creating/uploading file: {e}")