import requests
from stringcolor import cs

class Translate:

 
    api_url = "http://api.funtranslations.com/translate/klingon?text="
    @staticmethod
    def Klingon(str):
        url = Translate.api_url + str 
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception("API request failed.")
        print(cs(f'API request OK:{response.status_code}','green'))
        
        
        return response.json()["contents"]["translated"]
    
