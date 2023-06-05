import os
import shutil


def deleteTempFolders(keep: str, year: int):
    """
    Deletes temporary folders and files based on the specified keep command and year.

    Parameters:
      keep (str): The keep command specifying which folders to keep. Valid values are 'A' (keep all), 'N' (keep none),
                    or 'I' (keep isolated events).
      year (int): The year for which the temporary folders should be deleted.

    Returns:
      None
    """

    command = keep.upper()
    # Determine the proper files to keep
    if command == "A":
        return
    elif command == "N":
        folders = ['Filtered_Data', 'Isolated_Events', 'Unfiltered_Data', 'Merged_Data']
    elif command == "I":
        folders = ['Filtered_Data', 'Unfiltered_Data', 'Merged_Data']

    for folder in folders:
        # Get the current working directory
        current_directory = os.getcwd()

        # Create the path to the folder
        folder_path = os.path.join(current_directory, folder)

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Iterate over the subdirectories in the folder
            for subdirectory in os.listdir(folder_path):
                # Create the subdirectory path
                subdirectory_path = os.path.join(folder_path, subdirectory)
                # Check if it is a directory before deleting
                if os.path.isdir(subdirectory_path) and subdirectory_path.endswith(str(year)):
                    # Delete the directory and its contents
                    shutil.rmtree(subdirectory_path)
                    print("Deleted folder:", subdirectory_path)
        else:
            print("Folder does not exist:", folder_path)
