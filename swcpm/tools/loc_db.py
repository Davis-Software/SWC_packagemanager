import os
import json
from pathlib import Path


class LocationDatabase:
    database_dir = os.path.join(str(Path.home()), "SWC", "database")
    database_path = os.path.join(database_dir, "locations.json")

    def __init__(self):
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_dir, exist_ok=True)
            with open(self.database_path, "w") as f:
                f.write("{}")

        with open(self.database_path, "r") as f:
            self.locations = json.loads(f.read())

    def __update(self):
        with open(self.database_path, "w") as f:
            f.write(json.dumps(self.locations))

    def get_location(self, package):
        try:
            return self.locations[package]
        except KeyError:
            return None

    def set_location(self, package, location):
        self.locations[package] = location
        self.__update()

    def remove_location(self, package):
        del self.locations[package]
        self.__update()
