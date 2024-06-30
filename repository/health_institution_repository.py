import json
import requests
import os
from dotenv import load_dotenv


class HealthInstitutionRepository:
    def __init__(self):
        load_dotenv(dotenv_path='.env')
        self.base_url = os.getenv('BASE_URL')

    def fetch_options(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error occurred: {json_err}")
            print(f"Response content: {response.text}")
        return None

    def get_institutions(self, plan_code):
        url = f"{self.base_url}service/AnlasmaliSaglikKurumListesiniGetir/{plan_code}"
        return self.fetch_options(url)

    def get_cities(self, plan_code, institution_id):
        url = f"{self.base_url}service/SaglikIlGetir/{plan_code}/{institution_id}"
        return self.fetch_options(url)

    def get_districts(self, city_code, plan_code, institution_id):
        url = f"{self.base_url}service/SaglikIlceGetir/{city_code}/{plan_code}/{institution_id}"
        return self.fetch_options(url)

    def get_health_institutions(self, plan_code, institution_id, city_code, district_code):
        url = f"{self.base_url}service/AnlasmaliSaglikKuruluslariListesiniGetir/{plan_code}/{institution_id}/{city_code}/{district_code}"
        return self.fetch_options(url)
