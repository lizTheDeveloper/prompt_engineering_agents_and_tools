import os

def find_markdown_files(directory):
    """
    Finds all markdown files in the specified directory and its subdirectories.
    
    Parameters:
    directory (str): The directory to search through.

    Returns:
    None
    """
    # Iterate over all files and directories in the given directory
    for dirpath, dirnames, filenames in os.walk(directory):
        # Check each file to see if it's a markdown file
        for filename in filenames:
            if filename.endswith('.md'):
                # Print the full path to the markdown file
                print(os.path.join(dirpath, filename))

if __name__ == "__main__":
    # Example usage: change '/path/to/directory' to the directory you want to search
    find_markdown_files('/path/to/directory')
