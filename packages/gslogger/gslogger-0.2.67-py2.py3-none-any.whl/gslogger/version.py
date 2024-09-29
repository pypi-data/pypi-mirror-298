try:
    from extras import load_json, find_path
except:
    from .extras import load_json, find_path


# with open("glog.json", "r", encoding="utf-8") as fs:
#     config_data = load_json(fs.read())


try:
    config_data = load_json(find_path("glog.json"))

    __version__ = "v" + ".".join(map(str, config_data["app"]["version_number"]))
    __author__ = config_data["dev"]["developer"]
    __author_email__ = config_data["dev"]["dev_email"]

except Exception as e:
    __version__ = "v0.0.0"
    __author__ = "No Author"
    __author_email__ = "No Email"

    # raise Exception(f"VERSION: Error loading glog.json: {e}")
    # print(f"LOAD_JSON: Error loading glog.json: {e}")

