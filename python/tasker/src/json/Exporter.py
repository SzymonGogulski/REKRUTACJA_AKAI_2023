import json
import os

class Exporter:

    def __init__(self):
        pass

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
    
    def save_tasks(self, tasks):
        """
        zapisz taski do pliku tutaj
        """
        path = self.get_path()

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
