import os

from termcolor import colored
import chromadb

from constants import ROOT_DIR
from src.traversal import traverse_dir


class Embeddings():
    
    EXCLUDE_PATTERNS = ["*.png","*.jpg","*.jpeg","*.gif","*.bmp","*.svg","*.ico","*.tif","*.tiff"]
    
    def __init__(self, debug=False):
        self.debug = debug
        self.GENERATED_FILES_COLLECTION_NAME = "generated_files"

        DB_DIR = os.path.join(ROOT_DIR, ".chroma_db")
        # Create the embedding database directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        self.client = chromadb.Client(
          chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=DB_DIR,
          )
        )

        self.ensure_generated_files_collection_exists()

    def ensure_generated_files_collection_exists(self):
        # Create the generated files collection if it doesn't exist
        self.generated_files_collection = self.client.get_or_create_collection(self.GENERATED_FILES_COLLECTION_NAME)


    def persist_generated_file_contents(self, reset=False):
        if reset:
            self.generated_files_collection.reset()
        self.ensure_generated_files_collection_exists()

        # Iterate over all files in the generated directory
        file_paths_list = []
        file_contents_list = []
        metadatas_list = []
        for file_path in traverse_dir("generated", exclude_patterns=self.EXCLUDE_PATTERNS):
            file_paths_list.append(file_path)
            if self.debug:
                print("embedding: " + colored(file_path, 'green'))
            # Read the file
            with open(file_path, "r") as file:
                file_contents_list.append(file.read())
                # Get the filename
                filename = os.path.basename(file_path)
                # Get the extension
                extension = filename.split(".")[-1]
                metadatas_list.append({
                    "filename": filename,
                    "extension": extension,
                })

        # Upsert the file into the database
        self.generated_files_collection.upsert(
            documents=file_contents_list,
            metadatas=metadatas_list,
            ids=file_paths_list,
        )
        if self.debug:
            print(colored("persisted embeddings for %s files." % len(file_paths_list), 'yellow'))
        
        