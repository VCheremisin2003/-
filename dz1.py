import requests
import json
'''user_name = str(input())
url = 'https://api.github.com/users/' + user_name + '/repos'
response = requests.get(url)
j_data = response.json()
user_repos = []
print('репозитории пользователя ' + str(user_name) + ':')
for r in j_data:
    user_repos.append(r['name'])
    print (r['name'])'''
print('введите группу')
group_id = str(input())
print('введите токен')
token = str(input())
url = 'https://api.vk.com/method/groups.getMembers?group_id=' + group_id + '&access_token=' + token + '&v=5.130'
Group_Users = requests.get(url).json()
print(Group_Users)





