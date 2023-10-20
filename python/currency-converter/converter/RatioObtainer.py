import json, datetime, urllib.request
from datetime import datetime
import os, requests

class RatioObtainer:
    base = None
    target = None
    date_fetched = None

    def __init__(self, base, target):
        self.base = str(base)
        self.target = str(target)
        self.date_fetched = datetime.now().strftime("%Y-%m-%d") # Get date of fetching

    def get_ratio_file_path(self):
        """
        Method to get the ratio.json file path 
        I'm assuming that the ratios.json is going to be kept in parent directory to this file
        """
        # Get the parent directory path
        parent_directory_path = os.path.dirname(os.path.abspath(__file__))
        parent_directory_path = os.path.dirname(parent_directory_path)

        # Define the relative path to the JSON file in the parent directory
        json_file_path = os.path.join(parent_directory_path, 'ratios.json')
        return json_file_path

    def was_ratio_saved_today(self):
        """
        This function checks if given ratio was saved today and if the file with ratios is created at all
        should return false when file doesn't exist or if there's no today's exchange rate for given values at all
        should return true otherwise
        """
        path = self.get_ratio_file_path()

        #try to open file
        if not os.path.exists(path): # File doesn't exist at all
            with open(path, 'w') as file:
                file.write('[]')
            return False
        elif os.path.getsize(path) == 0: # File exists but is empty
            with open(path, 'w') as file:
                file.write('[]')
            return False
        else:
            with open(path, "r") as file:
                data = json.load(file)
            
            if len(data) == 0:
                return False # File exists and is empty

            for i in data:
                if ((i['base_currency'] == self.base) and (i['target_currency'] == self.target) and (i['date_fetched'] == self.date_fetched)):
                    file.close()
                    return True # There is already such an entry today in ratios.json
                
        return False # there's no today's entry for given values at all

    def fetch_ratio(self):
        """
        This function calls API for today's exchange ratio
        Should ask API for today's exchange ratio with given base and target currency
        and call save_ratio method to save it    
        """
        # URL tags
        BASE_URL = "http://api.exchangerate.host/"
        ENDPOINT = "convert"
        ACCESS_KEY = "c38675298fe9b259b8723aa75add29c6"
        AMOUNT = 10 # hard coded amount, we don't really need it, I just haven't found anything better in documentation

        # Fetch exchange rates
        exchange = requests.get(f'{BASE_URL}{ENDPOINT}?access_key=' + 
                        f'{ACCESS_KEY}&from={self.base}' + 
                        f'&to={self.target}&amount={AMOUNT}')

        ratio = exchange.json()['info']['quote'] # Get the exchange ratio

        self.save_ratio(ratio)

    def save_ratio(self, ratio):
        """
        Should save or update exchange rate for given pair in json file
        takes ratio as argument
        example file structure is shipped in project's directory, yours can differ (as long as it works)
        """
        new_entry = {
            "base_currency": self.base,
            "target_currency": self.target,
            "date_fetched": self.date_fetched,
            "ratio": ratio
        }
        path = self.get_ratio_file_path()

        #try to open file
        if not os.path.exists(path): # File doesn't exist we have to create it.
            with open(path, 'w') as file:
                json.dump(new_entry, file, indent=2)
        
        else: # File exists, we have to update it if responding entry exists
            with open(path, "r") as file:
                data = json.load(file)

            flag = True
            for i in data: # Update ratio if given pair already exists today
                if (i['base_currency'] == self.base and i['target_currency'] == self.target and i['date_fetched'] == self.date_fetched):
                    i['ratio'] = ratio
                    flag = False # Found responding entry and updated it, no need to create a new one
                    break

            if(flag):    
                data.append(new_entry)
                with open(path, "w") as file:
                    json.dump(data, file, indent=2)
        
    def get_matched_ratio_value(self):
        """
        Should read file and receive exchange rate for given base and target currency from that file
        """
        path = self.get_ratio_file_path()
        with open(path, "r") as file:
            data = json.load(file)
            
        for i in data: # Update ratio if given pair already exists today
            if (i['base_currency'] == self.base and i['target_currency'] == self.target and i['date_fetched'] == self.date_fetched):
                return float(i['ratio'])
        return 1.0
