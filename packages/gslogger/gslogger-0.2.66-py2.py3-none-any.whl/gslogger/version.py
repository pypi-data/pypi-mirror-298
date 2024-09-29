import pathlib

try:
    from extras import load_json, find_path
except:
    from .extras import load_json, find_path


# with open("glog.json", "r", encoding="utf-8") as fs:
#     config_data = load_json(fs.read())



config_data = load_json(find_path("glog.json"))

__version__ = "v" + ".".join(map(str, config_data["app"]["version_number"]))

__author__ = config_data["dev"]["developer"]

__author_email__ = config_data["dev"]["dev_email"]
