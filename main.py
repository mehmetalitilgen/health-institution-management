from view.health_institution_view import HealthInstitutionView
from controller.health_institution_controller import HealthInstitutionController
from repository.health_institution_repository import HealthInstitutionRepository


def main():
    view = HealthInstitutionView()
    repository = HealthInstitutionRepository()
    controller = HealthInstitutionController(view, repository)

    view.display_message("It may take a while, please wait.")

    plan_values = controller.load_plan_values('plan_values.json')
    if plan_values:
        results = controller.process_plans(plan_values)
        controller.save_results(results)


if __name__ == "__main__":
    main()
