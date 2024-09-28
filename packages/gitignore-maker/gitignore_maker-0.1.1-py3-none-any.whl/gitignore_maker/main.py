import argparse
import sys
import os
from gitignore_maker.constants import language_gitignore_map

# Set a default size limit (e.g., 49 MB)
DEFAULT_SIZE_LIMIT = 49 * 1024 * 1024  # 49 MB
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


def check_folder_size(folder_path, gitignore_entries, ignore_folder, size_limit):
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
            f for f in files_in_folder if os.path.getsize(f) > size_limit
        ]
        if len(oversized_files) == len(files_in_folder):
            # If all files in the folder exceed the limit, add the folder to .gitignore
            add_to_gitignore(folder_path)
            return True
    return False


def check_file_sizes(directory, gitignore_entries, ignore_folder, size_limit):
    for root, dirs, files in os.walk(directory):
        # Check each folder first
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if check_folder_size(
                folder_path, gitignore_entries, ignore_folder, size_limit
            ):
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
                if os.path.getsize(file_path) > size_limit:
                    add_to_gitignore(file_path)
            except Exception as e:
                print(f"Error checking {file_path}: {e}")


def get_gitignore_content(language_name: str, language_gitignore_map: dict) -> str:
    # Look up the language in the map
    if language_name in language_gitignore_map:
        file_path = language_gitignore_map[language_name]

        # Return the content of the gitignore file
        with open(file_path, "r") as file:
            content = file.read()
        return content
    else:
        return f"Error: No .gitignore file found for {language_name}."


def gitignore_maker(languages):
    create_gitignore_if_not_exists()
    gitignore_entries_raw = load_gitignore_entries()

    combined_language_entries = set()
    for lang in languages:
        language_gitignore_content = get_gitignore_content(lang, language_gitignore_map)
        combined_language_entries.update(language_gitignore_content.splitlines())

    unique_entries = set(gitignore_entries_raw + list(combined_language_entries))

    # Clear the current .gitignore
    with open(GITIGNORE_PATH, "w") as gitignore:
        gitignore.write("# .gitignore\n")
    with open(GITIGNORE_PATH, "a") as gitignore:
        for entry in unique_entries:
            gitignore.write(f"{entry}\n")

    print(f"Updated {GITIGNORE_PATH} with combined content.")


def list_languages():
    # Simply print out the list of available languages from the `language_gitignore_map`
    print("Supported languages:")
    for language in language_gitignore_map:
        print(f"- {language}")


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to manage .gitignore files with language templates and size-based filtering."
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        help="Specify the programming languages to include in the .gitignore (e.g., --languages Python Node).",
        required=False,
        default=[],
    )
    parser.add_argument(
        "--size-limit",
        type=int,
        help="Set the size limit for files in bytes. Files larger than this will be added to .gitignore.",
        default=DEFAULT_SIZE_LIMIT,
    )
    parser.add_argument(
        "--ignore-folders",
        nargs="+",
        help="Specify folders to ignore during file size checks (e.g., --ignore-folders venv node_modules).",
        default=[],
    )
    parser.add_argument(
        "--ignore-files",
        nargs="+",
        help="Specify files to ignore during file size checks (e.g., --ignore-files large_file.txt).",
        default=[],
    )
    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="List all supported languages and exit.",
    )

    args = parser.parse_args()

    # If the --list-languages flag is provided, list languages and exit immediately
    if args.list_languages:
        list_languages()
        sys.exit(0)  # Exit immediately after listing languages

    # Continue with other logic if --list-languages is not provided
    size_limit = args.size_limit

    gitignore_maker(args.languages)

    ignore_folder = args.ignore_folders + args.ignore_files

    gitignore_entries = structure_gitignore_entries(load_gitignore_entries())

    check_file_sizes(".", gitignore_entries, ignore_folder, size_limit)


if __name__ == "__main__":
    main()
