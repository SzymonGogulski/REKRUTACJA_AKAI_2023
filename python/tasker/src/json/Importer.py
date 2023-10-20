import json
import os
os.system('cls')

class Importer:

    def __init__(self):
        self.data = None
    
    def get_path(self):
        """
        Method to get the taski.json file path 
        I'm assuming that the taski.json is going to be kept in tasker directory, 
        two directories above working directory
        """
        # Get the parent directory path
        parent_directory_path = os.path.dirname(os.path.abspath(__file__))
        parent_directory_path = os.path.dirname(parent_directory_path)
        parent_directory_path = os.path.dirname(parent_directory_path)
    
        #Define the relative path to the JSON file in the parent directory
        path = os.path.join(parent_directory_path, 'taski.json')
        return path
    
    def read_tasks(self):
        """
        odczytaj plik i zdekoduj treść tutaj
        """
        path = self.get_path()

        if not os.path.exists(path):
            with open(path, 'w') as file:
                data = []
                json.dump(data, file)
            self.data = data
        elif os.path.getsize(path) == 0:
            with open(path, 'w') as file:
                data = []
                json.dump(data, file)
                self.data = data
        else:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.data = data

    def get_tasks(self):
        """
        zwróć zdekodowane taski tutaj
        """
        return self.data
