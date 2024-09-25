from field_manager_api.auth.auth import set_bearer_token_header
from field_manager_api.config.request_handler import get_request_handler
from field_manager_api.locations.get_locations import get_locations_request
from field_manager_api.projects.get_projects import get_projects_request
from field_manager_api.methods.get_methods import get_methods
from field_manager_api.utils.ground_models import Plotter
from field_manager_api.utils.folium_plotter import MapHandler
from field_manager_api.utils.automatic_datarapport import WordDocReport


class FieldManagerAPI:
    """Field Manager API class"""

    headers: dict
    locations: list[dict]
    projects: list[dict]
    project_id: str

    def __init__(self):
        print("Field Manager API init")

    def set_token(self, token):
        self.headers = set_bearer_token_header(token)
        print("Token set successfully")

    def get_projects(self):
        self.validate_header()
        self.projects = get_projects_request(self.headers, get_request_handler)
        print("Projects retrieved successfully")
        print([project["name"] for project in self.projects])

    def set_project(self, project_id: str = None, project_name: str = None):
        if project_id is None and project_name is None:
            raise ValueError("Project ID or Project Name must be set")
        if project_id is None and project_name is not None:
            for project in self.projects:
                if project["name"] == project_name:
                    project_id = project["project_id"]
        self.project_id = project_id
        print(f"Project set to successfully to {project_id}")

    def validate_header(self):
        if self.headers is None:
            raise ValueError("Token not set")

    def get_locations(self, project_id: str = None):
        self.validate_header()
        if project_id is None and self.project_id is not None:
            project_id = self.project_id
        self.locations = get_locations_request(
            self.headers, project_id, get_request_handler
        )

    def get_methods(self, method_types: list[int] = None):
        self.methods = get_methods(self.locations, method_types)

    def plot_locations(self):
        self.m = MapHandler(self.methods)
        self.m.plot_locations()
        return self.m.get_map()

    def plot_heatmap(self):
        self.m.add_heatmap()
        self.m.add_prediction_ring_around_locations()
        return self.m.get_map()

    def create_ground_model(self):
        if self.methods is None:
            raise ValueError("Methods not set")
        plotter = Plotter(self.methods)
        plotter.plot()

    def create_bedrock_model(self):
        if self.methods is None:
            raise ValueError("Methods not set")
        plotter = Plotter(self.methods)
        plotter.plot_3d_surface_with_layers()

    def create_datarapport(self):
        if self.methods is None:
            raise ValueError("Methods not set")
        # Example of how to use this class

        # Assuming 'get_methods()' gives a list of Method objects

        print("Connecting to ChatGPTAPI..")
        # Create the report class
        report = WordDocReport(self.methods)

        # Generate the map and capture a screenshot
        report.add_existing_map(self.m.map)
        print("Creating datarapport..")
        report.capture_map_screenshot()

        # Create the Word document report
        report.create_report(
            description="This report contains geotechnical data and visualizations of sounding locations."
        )
        print("Datarapport created successfully")
