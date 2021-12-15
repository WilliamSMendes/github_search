import requests
import pymongo


# Connecting to the Mongo's database
client = pymongo.MongoClient("mongodb+srv://<user>:<password>@cluster0.sbi9l.mongodb.net/<database>?retryWrites=true&w=majority")
db = client['database']
collection = db['collection']


# Searching for repositories and storing them in the database
def search_repos(user):
    list_repos = []
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url)
    if response.status_code != 200:
        print('Error:', response.status_code)
    else:
        repos = response.json()
        print(f'\n{user} has {len(repos)} repos:\n')
        for repo in repos:
            list_repos.append(repo['name'])
            print("Repo: ", repo['name'])

        # Inserting the repos into the MongoDB
        for repo in list_repos:
            collection.insert_one({'username': user, 'repos': repo})
            
        
# Input
user = input('Enter a Github username: ')
search_repos(user)