import os
import imp_items

class DirectorySetup:
    def __init__(self):
        """
        Initialize the DirectorySetup object.

        Args:
        - dir_paths (list): List of directory paths to be created.
        """
        self.dir_paths = imp_items.paths

    def create_directories(self):
        """
        Create directories if they do not exist.
        """
        for dir_path in self.dir_paths:
            os.makedirs(dir_path, exist_ok=True)
            print(f"Directory created: {dir_path}")

if __name__ == "__main__":

    # Create DirectorySetup object
    directory_setup = DirectorySetup()

    # Create directories
    directory_setup.create_directories()
