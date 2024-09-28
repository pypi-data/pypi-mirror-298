
# Gitignore Maker

A powerful command-line tool for managing `.gitignore` files with language-specific templates and size-based filtering. This tool allows you to create and update `.gitignore` files based on your project's programming languages, while also filtering out large files and folders exceeding a user-defined size limit.

## Introduction

Managing a clean and comprehensive `.gitignore` file is crucial for ensuring that unnecessary files are excluded from your Git repositories. This CLI tool simplifies that process by allowing you to:
- Automatically generate `.gitignore` content based on your project's programming languages.
- Filter files and folders by size, ensuring that large assets are ignored.
- Exclude specific files and folders from being added to `.gitignore`.

With just a few commands, you can maintain an optimized and language-specific `.gitignore` file tailored to your project's needs.

## Key Features

- **Language-Specific `.gitignore` Templates**: Generate `.gitignore` content based on the programming languages used in your project.
- **Size-Based File Exclusion**: Automatically add files and folders to `.gitignore` if they exceed a specified size limit.
- **Custom Folder and File Exclusion**: Specify folders and files to ignore during size-based filtering.
- **Seamless Integration**: The tool can be easily integrated into your project management workflow, automating the generation and update of `.gitignore`.

## Installation

Install the libray:

```bash
pip install gitignore-maker
```

## Usage

Run the CLI tool by specifying your desired options. 

```bash
gitignore_maker [OPTIONS]
```

### Options

| Option              | Description                                                                                   |
|---------------------|-----------------------------------------------------------------------------------------------|
| `--languages`       | Specify the programming languages to include in the `.gitignore`. Example: `--languages Python Node`. |
| `--size-limit`      | Set a size limit for files (in bytes). Files larger than this limit will be added to `.gitignore`. Default is 49 MB. |
| `--ignore-folders`  | Specify folders to exclude during file size checks. Example: `--ignore-folders venv node_modules`. |
| `--ignore-files`    | Specify files to exclude during file size checks. Example: `--ignore-files large_file.txt`.     |
| `--list-languages`  | List all supported programming languages and exit.                                             |

### Examples

1. **Generate a `.gitignore` for Python and Node.js**:
   ```bash
   gitignore_maker --languages Python Node
   ```

2. **Add files larger than 10 MB to `.gitignore`**:
   ```bash
   gitignore_maker --size-limit 10485760
   ```

3. **Ignore specific folders during size checks**:
   ```bash
   gitignore_maker --ignore-folders venv build
   ```

4. **List all supported programming languages**:
   ```bash
   gitignore_maker --list-languages
   ```

## Example Workflow

Here’s a typical workflow using this tool:

1. **Generate a language-specific `.gitignore` file**:
    ```bash
    gitignore_maker --languages Python Node
    ```
    This will create or update the `.gitignore` file with content for Python and Node.js.

2. **Filter large files**:
    After generating the `.gitignore`, you may want to exclude files larger than 50 MB:
    ```bash
    gitignore_maker --size-limit 52428800
    ```
    This will scan the project directory and add all files larger than 50 MB to the `.gitignore`.

3. **Customize exclusion**:
    To exclude certain folders like `venv` or `build` from being added to `.gitignore`, you can run:
    ```bash
    gitignore_maker --ignore-folders venv build
    ```

## Supported Languages

This tool supports `.gitignore` templates for various programming languages, including but not limited to:
- Python
- Node.js
- Java
- Ruby
- Go
- PHP
- C++
- ...and more.

To see the full list of supported languages, use the `--list-languages` option:
```bash
gitignore_maker --list-languages
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
