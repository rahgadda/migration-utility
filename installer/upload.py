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

# -- List data in parent folder
print("Listing Existing Files --> ")
gdrive.list_all_files()
print()

# -- Delete all files
print("Deleting Existing Files --> ")
gdrive.delete_all_files()
print()

# -- Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# -- Replace with the path to your CSV file
print("Base Data Location --> ")
csv_file_path = current_directory+'/data/project.csv'
print("csv_file_path -- "+csv_file_path)
print()

# -- Check if the CSV file exists
if not os.path.exists(csv_file_path):
    print(f"CSV file '{csv_file_path}' does not exist.")
    exit

file_name = os.path.basename(csv_file_path)

# -- Create a new file on Google Drive with the CSV file
print("File Upload --> ")
gdrive.create_file(csv_file_path)
print(f"Created and uploaded '{file_name}' to Google Drive.")
print()

# -- Verification
print("Verification --> ")
file_id= gdrive.get_files_id_by_name("project.csv")
print(f"Google Drive have file'{file_name}' with id '{file_id['id']}'")
print()