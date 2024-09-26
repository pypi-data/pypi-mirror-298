import unittest
from carjam import Client

class TestCarMethods(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_basic_details(self):
        expected_details = {
            'plate': 'FKK351', 
            'vin': '7AT0H63WX10005902', 
            'chassis': 'ACT10-0005902', 
            'current_vehicle_odometer_unit': 'K', 
            'reported_stolen': 'U', 
            'make': 'TOYOTA', 
            'year_of_manufacture': 2000, 
            'vehicle_type': 7, 
            'usage_level': 1.91, 
            'average_fleet_mileage': 10500
        }

        actual_details = self.client.basic_details('fkk351')
        
        self.assertDictEqual(actual_details, expected_details)
        
    def test_car_fuel_consumption_fkk351(self):
        expected_consumption = '7.50 litres/100km'
        
        actual_consumption = self.client.fuel_consumption('fkk351')
        
        self.assertEqual(expected_consumption, actual_consumption)
        
    def test_car_fuel_consumption_nyk908(self):
        expected_consumption = '3.60 litres/100km'
        
        actual_consumption = self.client.fuel_consumption('nyk908')
        
        self.assertEqual(expected_consumption, actual_consumption)
        
    def test_car_fuel_consumption_myw798(self):
        expected_consumption = '6.70 litres/100km'
        
        actual_consumption = self.client.fuel_consumption('myw798')
        
        self.assertEqual(expected_consumption, actual_consumption)
        
    def test_model_details(self):
        expected_details = {
            'car_id': 0, 
            'chassis_number': 
            'ACT10-0005902', 
            'make': 'TOYOTA', 
            'model': 'OPA', 
            'grade': 'I', 
            'manufacture_date': '2000-09', 
            'body': 'TA-ACT10', 
            'engine': '1AZFSE', 
            'drive': 'FF', 
            'transmission': 'CVT'
        }

        actual_details = self.client.model_details('fkk351')
        
        self.assertDictEqual(actual_details, expected_details)
        
    def test_car_image(self):
        expected_details = {
            'image': 'photos.carjam.co.nz/jph/_search_img_catalog_10102041_200404.jpg',
            'orig_image': 'photos.carjam.co.nz/jph/_search_img_catalog_10102041_200404.jpg'
        }
        
        actual_details = self.client.image('fkk351')
        
        self.assertDictEqual(actual_details, expected_details)
        
    def test_car_odometer_history(self):
        expected_details = [{
            'odometer_date': 1678618800,
            'odometer_reading': '296662',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 7,
            'seconds': 604800,
            'kms': 359,
            'daily_usage': 51.285714285714285
        }, {
            'odometer_date': 1678014000,
            'odometer_reading': '296303',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 368,
            'seconds': 31795200,
            'kms': 19113,
            'daily_usage': 51.9375
        }, {
            'odometer_date': 1646218800,
            'odometer_reading': '277190',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 7,
            'seconds': 604800,
            'kms': 55,
            'daily_usage': 7.857142857142857
        }, {
            'odometer_date': 1645614000,
            'odometer_reading': '277135',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 444,
            'seconds': 38361600,
            'kms': 9989,
            'daily_usage': 22.49774774774775
        }, {
            'odometer_date': 1607252400,
            'odometer_reading': '267146',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 380,
            'seconds': 32832000,
            'kms': 9213,
            'daily_usage': 24.24473684210526
        }, {
            'odometer_date': 1574420400,
            'odometer_reading': '257933',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 306,
            'seconds': 26438400,
            'kms': 14166,
            'daily_usage': 46.294117647058826
        }, {
            'odometer_date': 1547982000,
            'odometer_reading': '243767',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 33,
            'seconds': 2851200,
            'kms': 277,
            'daily_usage': 8.393939393939394
        }, {
            'odometer_date': 1545130800,
            'odometer_reading': '243490',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 364,
            'seconds': 31449600,
            'kms': 22796,
            'daily_usage': 62.62637362637363
        }, {
            'odometer_date': 1513681200,
            'odometer_reading': '220694',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 371,
            'seconds': 32054400,
            'kms': 28933,
            'daily_usage': 77.98652291105121
        }, {
            'odometer_date': 1481626800,
            'odometer_reading': '191761',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 378,
            'seconds': 32659200,
            'kms': 25217,
            'daily_usage': 66.71164021164022
        }, {
            'odometer_date': 1448967600,
            'odometer_reading': '166544',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 338,
            'seconds': 29203200,
            'kms': 23020,
            'daily_usage': 68.10650887573965
        }, {
            'odometer_date': 1419764400,
            'odometer_reading': '143524',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 191.95833333333334,
            'seconds': 16585200,
            'kms': 13481,
            'daily_usage': 70.22878228782288
        }, {
            'odometer_date': 1403179200,
            'odometer_reading': '130043',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 181.04166666666666,
            'seconds': 15642000,
            'kms': 12014,
            'daily_usage': 66.36041426927503
        }, {
            'odometer_date': 1387537200,
            'odometer_reading': '118029',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 212.95833333333334,
            'seconds': 18399600,
            'kms': 15093,
            'daily_usage': 70.87301897867344
        }, {
            'odometer_date': 1369137600,
            'odometer_reading': '102936',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 172.04166666666666,
            'seconds': 14864400,
            'kms': 9567,
            'daily_usage': 55.60862194235893
        }, {
            'odometer_date': 1354273200,
            'odometer_reading': '93369',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 162.95833333333334,
            'seconds': 14079600,
            'kms': 9559,
            'daily_usage': 58.65916645359243
        }, {
            'odometer_date': 1340193600,
            'odometer_reading': '83810',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 184.04166666666666,
            'seconds': 15901200,
            'kms': 10723,
            'daily_usage': 58.26398007697532
        }, {
            'odometer_date': 1324292400,
            'odometer_reading': '73087',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 186.95833333333334,
            'seconds': 16153200,
            'kms': 10954,
            'daily_usage': 58.59059505237352
        }, {
            'odometer_date': 1308139200,
            'odometer_reading': '62133',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 198.04166666666666,
            'seconds': 17110800,
            'kms': 12227,
            'daily_usage': 61.73953292657269
        }, {
            'odometer_date': 1291028400,
            'odometer_reading': '49906',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 181.95833333333334,
            'seconds': 15721200,
            'kms': 11703,
            'daily_usage': 64.31692237233798
        }, {
            'odometer_date': 1275307200,
            'odometer_reading': '38203',
            'odometer_unit': 'K',
            'odometer_source': 'IW',
            'days': 4,
            'seconds': 345600,
            'kms': 0,
            'daily_usage': 0
        }, {
            'odometer_date': 1274961600,
            'odometer_reading': '38203',
            'odometer_unit': 'K',
            'odometer_source': 'P',
            'days': 32,
            'seconds': 2764800,
            'kms': 3,
            'daily_usage': 0.09375
        }, {
            'odometer_date': 1272196800,
            'odometer_reading': '38200',
            'odometer_unit': '',
            'odometer_source': 'B',
            'days': 0,
            'seconds': 0,
            'kms': 0,
            'daily_usage': 0
        }]
        
        actual_details = self.client.odometer_history('fkk351')
        
        self.assertListEqual(actual_details, expected_details)
        
        
if __name__ == '__main__':
    unittest.main()