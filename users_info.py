from time import sleep
import requests
import json
import csv
from datetime import datetime

def get_json(url, data=None):
    response = requests.get(url, params = data)
    #print(response.url, '\n')
    return response.json()

def get_users(token, group_id, fields, offset=0, count=1000):
    users =[]
    while True:
        sleep(1)
        users_info = get_json("https://api.vk.com/method/groups.getMembers", {
                'group_id' : group_id, 
                'count' : count,
                'access_token' : token,
                'offset' : offset,
                'fields' : fields,
                'v' : '5.131'
                })
        
        count_users = users_info['response']['count']
        info = users_info['response']['items']

        print(len(info))
        users.extend(info)

        if len(info) == 0:
            break
        else:
            offset += 1000
    return users, count_users

def collect_info(users, group_id):
    filtered_data = []
    for user in users:
        try:
            id = user['id']
        except:
            id = 0
        try:
            bdate = datetime.strptime(user['bdate'], "%d.%m.%Y").date()
        except:
            bdate = ''
        try:
            city = user['city']['title']
        except:
            city = ''
        try:
            if user['sex'] == 1:
                sex = 'female'
            elif user['sex'] == 2:
                sex = 'male'
        except:
            sex = ''

        filtered_user = {
                'id': id,
                'bdate': bdate,
                'city': city,
                'sex': sex,
                'group': group_id
            }
    
        filtered_data.append(filtered_user)

    return filtered_data

def write_csv(data, encoding = 'utf-8'):
    group_id = data[0]['group']
    filename = f'{group_id}_users_info.csv'
    with open(filename, 'w', newline = '', encoding = encoding) as csvfile:
        fieldnames = ['id', 'sex', 'bdate', 'city', 'group']
        writer = csv.DictWriter(csvfile, delimiter = ';', fieldnames = fieldnames, extrasaction = 'ignore')
        writer.writeheader()
        writer.writerows(data)
         
        print ('Data written to csv', filename)
    csvfile.close