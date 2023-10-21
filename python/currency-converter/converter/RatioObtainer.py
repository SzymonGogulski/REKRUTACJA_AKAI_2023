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
                    return False # File exists but the entries array is empty

                for i in data:
                    if ((i['base_currency'] == self.base) and (i['target_currency'] == self.target) and (i['date_fetched'] == self.date_fetched)):
                        print("Found such entry today. ")
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

        
        I'm assuming that we want to keep old entries in json file.
        I don't really understand why this function has to "update exchange rates". Was_ratio_saved_today inside App.py
        if not obtainer.was_ratio_saved_today():
            obtainer.fetch_ratio()
        makes sure that we won't have to update anything if the ratio was already fetched today, so there is nothing to update.
        Basically, once we fetch the ratio, we will use it for the rest of the day; we won't update it for the rest of the day.
        The next day, we will simply create a new entry, so there's still no need to update any existing entries.
        This only makes sense if "create new exchange rate entry" and "update exchange rate" are synonymous.

        The task should specify if we want to retain historical entries in the file or update them to the current date.
        """
        new_entry = {
            "base_currency": self.base,
            "target_currency": self.target,
            "date_fetched": self.date_fetched,
            "ratio": ratio
        }
        path = self.get_ratio_file_path()

        #try to open file
        # if not os.path.exists(path): # File doesn't exist we have to create it.
        #     with open(path, 'w') as file:
        #         json.dump(new_entry, file, indent=2) 
        # save_ratio will be called allways after fetch_ratio() and was_ratio_saved_today()
        # was_ratio_saved_today() makes sure that ratios.json exists in given file path and has 
        # at least an empty array inside of it. This fact makes this code redundant. 
        # There's no need to check again if file exists. 
        #else: # File exists, we have to update it if responding entry exists
        
        #flag = True # theres no need to use it
        data = []
        with open(path, "r") as file: # Read ratios file to data variable
            data = json.load(file)

        # for i in data: # Update ratio if given pair already exists today
        #     if (i['base_currency'] == self.base and i['target_currency'] == self.target and i['date_fetched'] == self.date_fetched):
        #         i['ratio'] = ratio
        #         with open(path, "w") as file:
        #             json.dump(data, file, indent=2)
        #         flag = False # Found responding entry and updated it, no need to create a new one
        #         break
        # This code is also redundant. save_ratio will only run when was_ratio_saved_today returns False, 
        # meaning that no entry for given currency pair exists today, so there's no entry to update. We 
        # just need to create the new entry and append it to json file
 
        # if(flag): useless    
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

