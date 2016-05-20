import requests
import json

headers = {'Content-type': 'application/json'}

def post_info(url, data={}):  
    data = json.dumps(data)
    response = -1
    res = ''
    try:
        response = requests.post(url, data=data, headers=headers)
    except:
        pass

    if response == -1:
        res = 'Unable to connect: ' + url 
    elif response.ok:
          res = 'Done'
    else:
        res = response.content
    return res

def put_info(url, data={}):  
    data = json.dumps(data)
    response = -1

    try:
        response = requests.put(url, data=data, headers=headers)
    except:
        pass

    rest_data_dict = {}
    res = ''
    if response == -1:
        res = 'Unable to connect: ' + url 
    elif response.ok:
        rest_data_dict = json.loads(response.content)
        res = 'Done'
    elif int(response.status_code) == 500:
        res = 'Error! Please look into server logs for details.'
    else:
        res = response.content
    return rest_data_dict, res

def delete_info(url, data={}):  
    data = json.dumps(data)
    response = -1
    try:
        response = requests.delete(url, data=data, headers=headers)
    except:
        pass

    res = ''
    if response == -1:
        res = 'Unable to connect: ' + url 
    elif response.ok:
        res = 'Done'
    elif int(response.status_code) == 500:
        res = 'Error! Please look into server logs for details.'
    else:
        res = response.content
    return res

def get_info(url, data={}):  
    data = json.dumps(data)
    response = -1
    try:
        response = requests.get(url, data=data, headers=headers)
    except:
        pass

    rest_data_dict = {}
    res = ''
    if response == -1:
        res = 'Unable to connect: ' + url 
    elif response.ok:
        rest_data_dict = json.loads(response.content)
    elif int(response.status_code) == 500:
        res = 'Error! Please look into server logs for details.'
    else:
        res = response.content
    return rest_data_dict, res
