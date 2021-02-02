import os
import json
import requests
from datetime import datetime, date
class Common:
    def __init__(self):
        pass

    def make_json_request(self,uri:str,body:dict = None):
        if body is None:
            response = requests.get(uri)
            return response.json()
        else:
            response = requests.post(url=uri,data = body)
            return response.json
    
    def get_secret_info(self,key:str):
        try:
            jsonpath = os.path.abspath('./parameters/secrets.json')
            with open(jsonpath,'r') as json_file:
                data = json.load(json_file)
            return data[key]
        except:
            raise Exception(f'Failure on Config load')
        pass
    
    def get_day_of_year(self):
        return datetime.now().timetuple().tm_yday
    
    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def post_discord_webhook(self,message,username=None) -> None:
        webhook = {"content": message}
        if username is not None:
            webhook['username'] = username
        webhook_url = self.get_secret_info("discord")['webhook']
        requests.post(url=webhook_url,data=webhook)

        