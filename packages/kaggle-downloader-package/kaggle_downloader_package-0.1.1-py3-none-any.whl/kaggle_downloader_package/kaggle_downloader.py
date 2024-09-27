import os
import json
import subprocess
import zipfile
import argparse

class KaggleDownloader:
    """
    A class for authenticating, searching, downloading, and extracting datasets from Kaggle.
    This class requires the Kaggle API credentials to be present in a JSON file.
    """

    def __init__(self, api_token_path="./kaggle.json", alternative_token_path="~/.kaggle/kaggle.json", path_downloads="."):
        """
        Initializes the KaggleDownloader object with paths to the Kaggle API token and download directory.

        Parameters:
            api_token_path (str): Path to the primary Kaggle API token file.
            alternative_token_path (str): Path to an alternative location for the Kaggle API token file.
            path_downloads (str): Path where downloaded datasets will be stored. Defaults to the current directory.

        Returns:
            None
        """
        self._api_token_path = os.path.expanduser(api_token_path)
        self._alternative_token_path = os.path.expanduser(alternative_token_path)
        self._path_downloads = path_downloads

    def get_api_token_path(self):
        """
        Gets the primary Kaggle API token file path.

        Returns:
            str: The primary Kaggle API token file path.
        """
        return self._api_token_path
    
    def get_alternative_token_path(self):
        """
        Gets the alternative Kaggle API token file path.

        Returns:
            str: The alternative Kaggle API token file path.
        """
        return self._alternative_token_path
    
    def get_path_downloads(self):
        """
        Gets the path where datasets will be downloaded.

        Returns:
            str: The path to the download directory.
        """
        return self._path_downloads
    
    def set_api_token_path(self, new_path):
        """
        Sets a new path for the Kaggle API token.

        Parameters:
            new_path (str): The new path for the Kaggle API token file.

        Returns:
            None
        """
        self._api_token_path = new_path
    
    def set_alternative_token_path(self, new_path):
        """
        Sets a new path for the alternative Kaggle API token.

        Parameters:
            new_path (str): The new path for the alternative Kaggle API token file.

        Returns:
            None
        """
        self._alternative_token_path = new_path

    def set_path_downloads(self, new_path):
        """
        Sets a new path for the download directory.

        Parameters:
            new_path (str): The new path for saving downloaded datasets.

        Returns:
            None
        """
        self._path_downloads = new_path

    def authenticate_kaggle(self):
        """
        Authenticates the user with Kaggle by loading the Kaggle API token from a JSON file.

        Returns:
            None
        
        Raises:
            FileNotFoundError: If the Kaggle API token file is not found at either the primary or alternative path.
        """
        if not os.path.exists(self.get_api_token_path()) and not os.path.exists(self.get_alternative_token_path()):
            raise FileNotFoundError(f"Kaggle API token file not found at {self.get_api_token_path()} and {self.get_alternative_token_path()}.")
        elif os.path.exists(self.get_api_token_path()):
            token_path = self.get_api_token_path()
        else:
            token_path = self.get_alternative_token_path()
        
        with open(token_path, 'r') as f:
            token = json.load(f)
        
        os.environ['KAGGLE_USERNAME'] = token['username']
        os.environ['KAGGLE_KEY'] = token['key']
        print(f"Kaggle authentication successful with credentials in {token_path}")

    def search_datasets(self, dataset_theme):
        """
        Searches for datasets on Kaggle related to a specific theme or keyword.

        Parameters:
            dataset_theme (str): The keyword or theme to search for related datasets.

        Returns:
            None
        
        Raises:
            subprocess.CalledProcessError: If there is an issue running the Kaggle API command.
        """
        try:
            subprocess.run(["kaggle", "datasets", "list", "-s", dataset_theme], check=True)
            print(f"Datasets listed for theme: {dataset_theme}")
        except subprocess.CalledProcessError as e:
            print(f"Error listing datasets: {e}")

    def download_dataset(self, dataset_slug):
        """
        Downloads a dataset from Kaggle to the specified path.

        Parameters:
            dataset_slug (str): The identifier of the Kaggle dataset to download.

        Returns:
            None
        
        Raises:
            subprocess.CalledProcessError: If there is an issue running the Kaggle API command.
        """
        if not os.path.exists(self.get_path_downloads()):
            self.create_download_directory(self.get_path_downloads())
        
        try:
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset_slug, "-p", self.get_path_downloads(), "--unzip"], check=True)
            print(f"Dataset '{dataset_slug}' downloaded successfully to {self.get_path_downloads()}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading dataset: {e}")


    def extract_zip(self, zip_file):
        print("####### Debuggin en el método!!! ######")
        print(f"Attempting to extract: {zip_file}")  # Debugging
        
        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"{zip_file} not found.")
        
        if not zipfile.is_zipfile(zip_file):
            raise ValueError(f"{zip_file} is not a zip file.")
        
        # Obtén el directorio donde se extraerá el archivo
        extract_path = self.get_path_downloads()
        print(f"El extract_path es: {extract_path}")
        print(f"El zip file es: {zip_file}")
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            print("Entre al with de extract_zip")
            print(f"zip_ref: {zip_ref}")  # Para ver el objeto
            zip_ref.extractall(extract_path)  # Llama a extractall
            print("Extracall se ejecuto Ok Marian!!!")
        print(f"Dataset extracted successfully to {extract_path}")
        print("####### Fin del debugging en el método #########")
        print()


    def check_kaggle_json(self):
        """
        Verifies if the Kaggle API token file exists either at the primary path or the alternative path.

        Returns:
            str: The path where the Kaggle API token file is found.

        Raises:
            FileNotFoundError: If the Kaggle API token file is not found in both paths.
        """
        if os.path.exists(self.get_api_token_path()):
            print(f"Kaggle API token found at {self.get_api_token_path()}.")
            return self.get_api_token_path()
        elif os.path.exists(self.get_alternative_token_path()):
            print(f"Kaggle API token found at {self.get_alternative_token_path()}.")
            return self.get_alternative_token_path()
        else:
            raise FileNotFoundError(f"Kaggle API token file not found at {self.get_api_token_path()} or {self.get_alternative_token_path()}.")

    def create_download_directory(self, path):
        """
        Creates a directory for saving datasets if it does not already exist.

        Parameters:
            path (str): The directory path to create.

        Returns:
            None
        """
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Directory {path} created.")
            self.set_path_downloads(new_path=path)
            print(f"Directory config about downloader folder")
        else:
            print(f"Directory {path} already exists.")
            self.set_path_downloads(new_path=path)
            print(f"Directory config about downloader folder")

    @staticmethod
    def main():
        """
        Main function for running the KaggleDownloader from the command line.
        Parses command-line arguments to download a Kaggle dataset.

        Command-line Arguments:
            dataset_slug (str): The Kaggle dataset identifier.

        Returns:
            None
        """
        parser = argparse.ArgumentParser(description="Download datasets from Kaggle")
        parser.add_argument("dataset_slug", help="The Kaggle dataset identifier")
        args = parser.parse_args()

        downloader = KaggleDownloader()
        downloader.authenticate_kaggle()
        downloader.download_dataset(args.dataset_slug)

if __name__ == "__main__":
    KaggleDownloader.main()
