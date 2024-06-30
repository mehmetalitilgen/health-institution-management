import json
from model.health_institution_model import HealthInstitutionModel


class HealthInstitutionController:
    def __init__(self, view, repository):
        self.view = view
        self.repository = repository

    def load_plan_values(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.view.display_message(f"File {file_path} not found.")
            return None
        except json.JSONDecodeError:
            self.view.display_message(f"Error decoding JSON from file {file_path}.")
            return None

    def remove_prefix(self, data, prefix):
        if isinstance(data, dict):
            return {key[len(prefix):] if key.startswith(prefix) else key: self.remove_prefix(value, prefix) for
                    key, value in data.items()}
        elif isinstance(data, list):
            return [self.remove_prefix(item, prefix) for item in data]
        else:
            return data

    def format_district_data(self, districts):
        formatted = []
        if districts:
            for district in districts:
                district = self.remove_prefix(district, 'b:')
                district_id = district.get('Id')[0] if isinstance(district.get('Id'), list) else district.get('Id')
                district_name = district.get('Name')[0] if isinstance(district.get('Name'), list) else district.get(
                    'Name')
                formatted.append({
                    "ilceKodu": district_id,
                    "ilceIsmi": district_name
                })
        return formatted

    def format_health_institutions(self, health_institutions):
        formatted = []
        if health_institutions:
            for institution in health_institutions:
                institution = self.remove_prefix(institution, 'b:')
                institution_id = institution.get('Id')[0] if isinstance(institution.get('Id'),
                                                                        list) else institution.get('Id')
                institution_name = institution.get('Name')[0] if isinstance(institution.get('Name'),
                                                                            list) else institution.get('Name')
                institution_address = institution.get('Address')[0] if isinstance(institution.get('Address'),
                                                                                  list) else institution.get('Address')
                institution_phone = institution.get('Phone')[0] if isinstance(institution.get('Phone'),
                                                                              list) else institution.get('Phone')
                formatted.append({
                    "kurumKodu": institution_id,
                    "kurumIsmi": institution_name,
                    "kurumAdress": institution_address,
                    "phone": institution_phone
                })
        return formatted

    def process_plans(self, plan_values):
        if not plan_values:
            self.view.display_message("No plan values to process.")
            return []
        results = []
        for plan_code, plan_description in plan_values.items():
            model_instance = HealthInstitutionModel(plan_code, plan_description)
            institutions_data = self.repository.get_institutions(plan_code)
            print(institutions_data)
            if institutions_data:
                for institution in institutions_data:
                    print(institution)
                    institution = self.remove_prefix(institution, 'b:')
                    print(institution, "2")
                    institution_id = institution.get('Id')[0] if isinstance(institution.get('Id'),
                                                                            list) else institution.get(
                        'Id')  # hata fırlatmak yerine none döner
                    institution_name = institution.get('Name')[0] if isinstance(institution.get('Name'),
                                                                                list) else institution.get('Name')
                    if institution_id:
                        cities_data = self.repository.get_cities(plan_code, institution_id)
                        print(cities_data, "cities_data")
                        if cities_data:
                            for city in cities_data:
                                city = self.remove_prefix(city, 'b:')
                                city_code = city.get('Id')[0] if isinstance(city.get('Id'), list) else city.get('Id')
                                city_name = city.get('Name')[0] if isinstance(city.get('Name'), list) else city.get(
                                    'Name')
                                if city_code:
                                    districts_data = self.repository.get_districts(city_code, plan_code, institution_id)
                                    if districts_data:
                                        formatted_districts = self.format_district_data(districts_data)
                                        for district in formatted_districts:
                                            district_code = district['ilceKodu']
                                            district_name = district['ilceIsmi']
                                            health_institutions = self.repository.get_health_institutions(plan_code,
                                                                                                          institution_id,
                                                                                                          city_code,
                                                                                                          district_code)
                                            if health_institutions:
                                                formatted_health_institutions = self.format_health_institutions(
                                                    health_institutions)
                                                model_instance.add_institution(institution_name, city_name,
                                                                               district_name,
                                                                               formatted_health_institutions)
            results.append(model_instance)
        return results

    def save_results(self, results):
        formatted_results = [model.to_dict() for model in results]
        if formatted_results:
            self.view.write_to_file(formatted_results, 'result.json')
            self.view.display_message("The data was written to the file.--> result.json")
        else:
            self.view.display_message("Data not found.")
