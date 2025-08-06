import json

with open('user.json') as f:
    data = json.load(f)   # <- This will be a LIST

for user in data:
    print(user['name'], user['resume_score'], user['skills'])
