import os
import sys

# Set your size limit in bytes (e.g., 10 MB)
SIZE_LIMIT = 10 * 1024 * 1024  # 10 MB
GITIGNORE_PATH = ".gitignore"


def create_gitignore_if_not_exists():
    # Create the .gitignore file if it does not exist
    if not os.path.exists(GITIGNORE_PATH):
        with open(GITIGNORE_PATH, "w") as gitignore:
            gitignore.write("# .gitignore\n")  # Optional: add a comment header
        print(f"Created {GITIGNORE_PATH}")


def load_gitignore_entries():
    # Load existing entries from .gitignore into a list
    if os.path.exists(GITIGNORE_PATH):
        with open(GITIGNORE_PATH, "r") as gitignore:
            return [line.strip() for line in gitignore.readlines()]
    return []


def normalize_path(entry):
    """Convert entry to a standardized relative path format."""
    entry = entry.replace("/", "\\")  # Convert to Windows-style backslashes
    if entry in {"venv", "./venv", ".\\venv"}:  # Specific correction for venv
        return ".\\venv"  # Standardize to .\venv
    if not entry.startswith(".\\"):
        entry = ".\\" + entry  # Add leading .\ if not present
    return entry


def structure_gitignore_entries(entries):
    structured_entries = {"files": set(), "folders": set()}

    for entry in entries:
        normalized_entry = normalize_path(entry)
        if os.path.isdir(normalized_entry):
            structured_entries["folders"].add(normalized_entry)
        else:
            structured_entries["files"].add(normalized_entry)

    return structured_entries


def add_to_gitignore(item):
    # Add item (file/folder) to .gitignore
    with open(GITIGNORE_PATH, "a") as gitignore:
        gitignore.write("\n" + item)
    print(f"Added {item} to .gitignore")


def is_parent_in_gitignore(folder_path, gitignore_entries):
    # Check if any parent folder is in .gitignore
    parent_path = os.path.dirname(folder_path)
    while parent_path:
        if parent_path in gitignore_entries["folders"]:
            print(
                f"Skipping {folder_path} because its parent {parent_path} is in .gitignore"
            )
            return True
        parent_path = os.path.dirname(parent_path)  # Move to the parent directory
    return False


def check_folder_size(folder_path, gitignore_entries, ignore_folder):
    # Skip folder if it's already in .gitignore
    if folder_path in gitignore_entries["folders"]:
        print(f"Skipping {folder_path}, already in .gitignore")
        return True

    # Skip if folder is in ignore_folder
    folder_name = os.path.basename(folder_path)
    if folder_name in ignore_folder:
        print(f"Skipping folder {folder_path}, it's in ignore_folder")
        return True

    # Check if any parent folder is in .gitignore
    if is_parent_in_gitignore(folder_path, gitignore_entries):
        return True

    files_in_folder = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if len(files_in_folder) > 1:
        oversized_files = [
            f for f in files_in_folder if os.path.getsize(f) > SIZE_LIMIT
        ]
        if len(oversized_files) == len(files_in_folder):
            # If all files in the folder exceed the limit, add the folder to .gitignore
            add_to_gitignore(folder_path)
            return True
    return False


def check_file_sizes(directory, gitignore_entries, ignore_folder):
    for root, dirs, files in os.walk(directory):
        # Check each folder first
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if check_folder_size(folder_path, gitignore_entries, ignore_folder):
                # Skip checking this folder if it's already in .gitignore
                dirs.remove(dir_name)
                continue

        # Check individual files in the current directory
        for file in files:
            file_path = os.path.join(root, file)

            # Skip if file is in ignore_folder
            if file in ignore_folder:
                print(f"Skipping file {file_path}, it's in ignore_folder")
                continue

            if file_path in gitignore_entries["files"]:
                print(f"Skipping {file_path}, already in .gitignore")
                continue

            try:
                if os.path.getsize(file_path) > SIZE_LIMIT:
                    add_to_gitignore(file_path)
            except Exception as e:
                print(f"Error checking {file_path}: {e}")


def gitignore_maker():
    ignore_folders = []  # Add folder names here
    ignore_files = ["file_to_ignore.txt"]  # Add file names here

    # Combine ignore_folders and ignore_files for checking
    ignore_folder = ignore_folders + ignore_files

    # Check if each ignore folder exists
    for folder in ignore_folders:
        if not os.path.exists(folder):
            print(f"{folder} does not exist. Exiting...")
            sys.exit(1)  # Exit the program with a non-zero exit code

    ignore_folders.append(".git")
    create_gitignore_if_not_exists()  # Create .gitignore if it doesn't exist

    gitignore_entries_raw = load_gitignore_entries()  # Load existing .gitignore entries
    gitignore_entries = structure_gitignore_entries(
        gitignore_entries_raw
    )  # Structure entries

    check_file_sizes(
        ".", gitignore_entries, ignore_folder
    )  # Run the check on the current directory


# if __name__ == "__main__":
#     gitignore_maker()
