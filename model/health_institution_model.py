class HealthInstitutionModel:
    def __init__(self, plan_code, plan_description):
        self.plan_code = plan_code
        self.plan_description = plan_description
        self.institutions = {}

    def add_institution(self, institution_name, city_name, district_name, health_institutions):
        if institution_name not in self.institutions:
            self.institutions[institution_name] = {}
        if city_name not in self.institutions[institution_name]:
            self.institutions[institution_name][city_name] = []
        self.institutions[institution_name][city_name].append({district_name: health_institutions})

    def to_dict(self):
        return {
            "kurumTipiKodu": self.plan_code,
            "kurumTipiIsmi": self.plan_description,
            "kurumlar": self.institutions
        }
