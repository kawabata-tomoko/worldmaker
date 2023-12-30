import os
import json
import glob
from typing import Any


def get_module_installation_path(module_name: str) -> str:
    """
    Returns the installation path of the specified module.
    """
    # return os.environ.get ('TESLA_INSTALL_PATH',os.path.split(sys.modules[module_name].__file__)[0])
    return "/Users/zhengyulong/worldmaker/worldmaker"
class ConfigGroups:
    def __init__(self, path=None,**kwargs):
        self.root_path = get_module_installation_path('worldmaker')
        self.config_path = os.path.join(self.root_path, 'configs/configs') if path is None else path
        self.settings={}
        self.initial(**kwargs)
    def initial(self,**kwargs):
        answer={}
        for jsfile in glob.glob(os.path.join(self.config_path, '*.json')):
            with open(jsfile,"r") as file:
                answer[os.path.splitext(os.path.basename(jsfile))[0]]=json.load(file)
                self.settings.update(answer)
        default_paths = {
            "log_path": os.path.join(self.root_path, 'log'),
            "temp_path": os.path.join(self.root_path, 'temp'),
            "database": os.path.join(self.root_path, 'database')
        }

        for key, value in default_paths.items():
            self.settings["default_settings"]["COMMON"][key]=kwargs.get(key, value)
    def export_json(self,path=None):
        path = path if path is not None else self.config_path
        for k,v in self.settings.items():
            with open(os.path.join(self.config_path,f"{k}.json"),"w") as file:
                json.dump(v,file)
    def __setitem__(self,__name: str, __value: Any) -> None:
        self.settings[__name]=__value
    def __getitem__(self, __name: str) -> Any:
        return self.settings[__name]
    def __iter__(self):
        return iter(self.settings.keys())
CONFIGS=ConfigGroups()
CONFIGS.export_json()
print(CONFIGS)
# __all__=["CONFIGS"]