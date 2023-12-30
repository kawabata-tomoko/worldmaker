import os
import glob
import json
import atexit
from collections import defaultdict


def get_module_installation_path(module_name: str) -> str:
    """
    Returns the installation path of the specified module.
    """
    # return os.environ.get ('TESLA_INSTALL_PATH',os.path.split(sys.modules[module_name].__file__)[0])
    return "/Users/zhengyulong/worldmaker/worldmaker"

class ConfigGroups:
    def __init__(self, path=None, **kwargs):
        self.root_path = get_module_installation_path('worldmaker')
        self.config_path = os.path.join(self.root_path, 'configs', 'configs') if path is None else path
        self.settings = defaultdict(dict)
        self.initial(**kwargs)
        atexit.register(self.export_json)

    def initial(self, **kwargs):
        for jsfile in glob.glob(os.path.join(self.config_path, '*.json')):
            with open(jsfile, "r") as file:
                key = os.path.splitext(os.path.basename(jsfile))[0].upper()
                self.settings[key] = json.load(file)

        default_paths = {
            "log_path": os.path.join(self.root_path, 'log'),
            "temp_path": os.path.join(self.root_path, 'temp'),
            "database": os.path.join(self.root_path, 'database')
        }

        for key, value in default_paths.items():
            self.settings["COMMON"].setdefault(key, kwargs.get(key, value))

    def common(self):
        return self.settings["COMMON"]

    def get(self, key, default):
        return self.settings.get(key, default)

    def export_json(self, path=None):
        path = path if not path is None else self.config_path
        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)
        for k, v in self.settings.items():
            with open(os.path.join(path, f"{k}.json"), "w") as file:
                json.dump(v, file)

    def __setitem__(self, name: str, value: any) -> None:
        self.settings[name] = value

    def __getitem__(self, name: str) -> any:
        return self.settings[name]

    def __iter__(self):
        return iter(self.settings.keys())

CONFIGS=ConfigGroups()
print(CONFIGS)
# __all__=["CONFIGS"]