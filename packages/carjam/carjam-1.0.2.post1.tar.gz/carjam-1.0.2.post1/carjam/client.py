import json
import time
import requests
from queue import Queue
from bs4 import BeautifulSoup

class Client:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 Firefox/71.0",
            "Accept": "*/*",
            "content-type": "application/json",
        }
        
    def isLoading(self, data):
        return data.startswith('<!DOCTYPE html>')
        
    def basic_details(self, plate):
        '''
        Returns a JSON object containing basic details about the car.
        Example of output shape:
        {
            "plate": "FKK351",
            "vin": "7AT0H63WX10005902",
            "chassis": "ACT10-0005902",
            "current_vehicle_odometer_unit": "K",
            "reported_stolen": "U",
            "make": "TOYOTA",
            "year_of_manufacture": 2000,
            "vehicle_type": 7,
            "usage_level": 1.91,
            "average_fleet_mileage": 10500
        }
        '''
        while True:
            resp = self.session.post(f'https://www.carjam.co.nz/car/?plate={plate}')
            raw_data = resp.text

            if not self.isLoading(raw_data):
                break 

            time.sleep(.3)  

        basic_details_start = raw_data.find("window.report.idh.vehicle") + 28
        basic_details_end = raw_data.find("}", basic_details_start) + 1
        
        try:
            json_data = json.loads(raw_data[basic_details_start:basic_details_end])
        except json.JSONDecodeError:
            return "Error decoding JSON data. No car exists under this plate, or this plate is not supported."

        return json_data
    
    def fuel_consumption(self, plate):
        '''
        Returns an a json object containing basic details about the car
        Example of output shape:
        "7.5 litres/100km"
        '''
        
        while True:
            resp = self.session.post(f'https://www.carjam.co.nz/car/?plate={plate}')
            raw_data = resp.text

            if not self.isLoading(raw_data):
                break 

            time.sleep(.3)  
        
        fuel_consumption_start = raw_data.find("Fuel\n<div>\n<small>")
        fuel_consumption_end = raw_data.find("</small>\n</div>\n</td>", fuel_consumption_start)
          
        fuel_consumption = (raw_data[fuel_consumption_start + 19:fuel_consumption_end-1])
        
        # Strip the tilde (~) which is sometimes present for some reason
        if (fuel_consumption.startswith('&#126;')):
            fuel_consumption = fuel_consumption[7:]
            

        return fuel_consumption
    
    def model_details(self, plate):
        '''
        Returns an a json object containing model details about the car
        Example of output shape:
        {"car_id":0,"chassis_number":"ACT10-0005902","make":"TOYOTA","model":"OPA","grade":"I","manufacture_date":"2000-09","body":"TA-ACT10",
            "engine":"1AZFSE","drive":"FF","transmission":"CVT"}
        '''
        
        while True:
            resp = self.session.post(f'https://www.carjam.co.nz/car/?plate={plate}')
            raw_data = resp.text

            if not self.isLoading(raw_data):
                break 

            time.sleep(.3)  
        
        model_details_start = raw_data.find("window.jph_search") + 50
        model_details_end = raw_data.find("\"image\"", model_details_start) - 1
        
        try:
            json_data = json.loads(raw_data[model_details_start:model_details_end] + "}")
        except json.JSONDecodeError:
            return "Error decoding JSON data. No car exists under this plate, or this plate is not supported."

        return json_data
    
    def image(self, plate):
        '''
        Returns an a json object containing image urls of the car
        Example of output shape:
        {'image': 'photos.carjam.co.nz/jph/_search_img_catalog_10102041_200404.jpg', 
            'orig_image': 'photos.carjam.co.nz/jph/_search_img_catalog_10102041_200404.jpg'}
        '''
        
        while True:
            resp = self.session.post(f'https://www.carjam.co.nz/car/?plate={plate}')
            raw_data = resp.text
            
            if not self.isLoading(raw_data):
                break 

            time.sleep(.3)  
        
        model_details_start = raw_data.find("window.jph_search") + 50
        image_url_start = raw_data.find("\"image\"", model_details_start) 
        image_url_end = raw_data.find("}", image_url_start) + 1 \
        
        try:
            json_data = json.loads("{" + raw_data[image_url_start:image_url_end])
        except json.JSONDecodeError:
            return "Error decoding JSON data. No car exists under this plate, or this plate is not supported."

        # Fix the URLs by removing the leading `//` and replacing backslashes with forward slashes
        json_data['image'] = json_data['image'].replace('\\/', '/').replace('//', '')
        json_data['orig_image'] = 'photos.carjam.co.nz' + json_data['orig_image'].replace('\\/', '/').replace('/search/img/catalog/', '/jph/_search_img_catalog_')

        return json_data

        
    def odometer_history(self, plate): 
        '''
        Returns an array containing the odometer details of the car
        Example of output shape:
        [{"odometer_date":1678618800,"odometer_reading":"296662","odometer_unit":"K","odometer_source":"IW","days":7,"seconds":604800,
            "kms":359,"daily_usage":51.285714285714285}]
        '''
        
        resp = self.session.post(f'https://www.carjam.co.nz/car/?plate={plate}')
        raw_data = resp.text
        
        odometer_details_start = raw_data.find("window.report.idh.odometer_history") + 37
        odometer_details_end = raw_data.find("]", odometer_details_start) + 1
        
        try:
            json_data = json.loads(raw_data[odometer_details_start:odometer_details_end])
        except json.JSONDecodeError:
            return "Error decoding JSON data. No car exists under this plate, or this plate is not supported."
        
        return json_data
    
    def fleet_details(self, page=1, query="", make="", fuel_type=""):
        '''
        https://www.carjam.co.nz/nz-fleet/?l=20&_ob=count+desc&make=ALFA+ROMEO&year=2022&motive_power=PETROL
        Returns information about car registration counts
        Example of output shape:
        [{'make': 'FORD', 'model': 'RANGER', 'year': '2021', 'count': '12463', 'rank': '1'}]
        '''
        
        page = (page - 1 ) * 20
        
        resp = self.session.post(f'https://www.carjam.co.nz/nz-fleet/?make={make}&l=20&of={page}&q={query}&motive_power={fuel_type}')
        raw_data = resp.text
        
        fleet_details_start = raw_data.find("<tr class=\"record\">")
        fleet_details_end = raw_data.find("</table>", fleet_details_start)
        
        fleet_table = raw_data[fleet_details_start:fleet_details_end]
        
        soup = BeautifulSoup(fleet_table, 'html.parser')
        
        records = []
        
        for row in soup.find_all('tr', class_='record'):
            cells = row.find_all('td')
            if len(cells) >= 5:
                record = {
                    "make": cells[0].get_text(strip=True),
                    "model": cells[1].get_text(strip=True),
                    "year": cells[2].get_text(strip=True),
                    "count": cells[3].get_text(strip=True).replace(',', ''),  # Remove commas for numeric value
                    "rank": cells[4].get_text(strip=True)
                }
                records.append(record)

        return records
    