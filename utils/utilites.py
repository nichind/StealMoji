import json, discord
from config import *

def _getserverlanguage(user_id):
    with open(Folders.users, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    try: return str(data[str(user_id)])
    except: return 'EN'

def _GetText(line: str, user_id):
    lang = _getserverlanguage(user_id)
    with open(Folders.lang, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return str(data[str(line + '-' + lang)])

def CheckUser(user_id):
    with open(Folders.users, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    try:
        return str(data[str(user_id)]) in ['RU', 'EN']
    except: return False

def AddUser(user_id, lang):
    with open(Folders.users, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        data[f'{user_id}'] = lang
    with open(Folders.users, 'w', encoding='UTF-8') as f:
        json.dump(data, f)
        return lang

def UpdateStats(name, value=1, refresh=False):
    with open(Folders.stats, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        try:
            count = data[name]
            if refresh is True:
                data[f'{name}'] = str(value)
            else:
                data[f'{name}'] = str(int(count + value))
        except:
            data[f'{name}'] = value
    with open(Folders.stats, 'w', encoding='UTF-8') as f:
        json.dump(data, f)
        return value

def GetStats():
    with open(Folders.stats, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data