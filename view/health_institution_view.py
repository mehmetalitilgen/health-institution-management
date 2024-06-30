import json


class HealthInstitutionView:

    def display_message(self, message):
        print(message)

    def write_to_file(self, data, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            self.display_message(f"Error writing to file {file_name}: {e}")
