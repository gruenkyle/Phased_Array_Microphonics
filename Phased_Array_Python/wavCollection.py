import os

# Function to get the current number from the file and update it
def get_and_update_number(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            current_number = int(file.read().strip())
            updated_number = current_number + 1
            file.seek(0)
            file.write(str(updated_number).zfill(4))  # Write the updated number with leading zeros
    else:
        with open(file_path, 'w') as file:
            updated_number = 1
            file.write(str(updated_number).zfill(4))  # Write the initial number with leading zeros
    return str(updated_number).zfill(4)  # Return the updated number with leading zeros

# Creates a folder called MICRECORD
def micRecord():
    # Navigate into the folder "MICRECORD"
    micrecord_folder = "MICRECORD"
    if not os.path.exists(micrecord_folder):
        print(f"Folder '{micrecord_folder}' does not exist.")
        return

    os.chdir(micrecord_folder)

    # Get and update the current number
    number_file_path = "current_number.txt"
    current_number = get_and_update_number(number_file_path)

    # Generate the folder name using the updated number
    folder_name = current_number

    # Create the folder
    os.mkdir(folder_name)
    print(f"Folder '{folder_name}' created successfully in '{micrecord_folder}'.")

    # Navigate into the newly created folder
    os.chdir(folder_name)

    # Create a folder called "INDIV" inside the new folder
    indiv_folder = "INDIV"
    os.mkdir(indiv_folder)
    print(f"Folder '{indiv_folder}' created successfully in '{folder_name}'.")

    # Create folder called "SUM" inside new folder
    os.mkdir("SUM")

