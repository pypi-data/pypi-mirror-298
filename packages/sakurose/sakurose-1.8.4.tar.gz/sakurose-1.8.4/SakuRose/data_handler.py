import json
import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PACKAGE_DIR, 'data.json')

def data_save(password, key, value=None):
    if value is not None:
        data = {key: value}
    else:
        data = dict(item.split(':', 1) for item in key.split(','))

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r+') as f:
            current_data = json.load(f)
            if password not in current_data:
                current_data[password] = {}
            current_data[password].update(data)
            f.seek(0)
            json.dump(current_data, f, indent=4)
    else:
        with open(DATA_FILE, 'w') as f:
            json.dump({password: data}, f, indent=4)

def data_get(password, key=None):
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        if password not in data:
            return None
        if key:
            return data[password].get(key)
        return data[password]

def data_remove(password, key=None):
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        if password in data:
            if key:
                if key in data[password]:
                    del data[password][key]
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
            else:
                del data[password]
                f.seek(0)
                f.truncate()
                if data:
                    json.dump(data, f, indent=4)