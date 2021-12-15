import requests
import pyodbc 


# Connecting to the database
server = 'db_name.database.windows.net' 
database = 'mydb' 
username = 'user' 
password = 'pass' 
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()


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

        # Inserting the repos into the database
        for repo in list_repos:
            sql = f"INSERT INTO mydb.dbo.Mousse (Username, Repos) VALUES ('{user}', '{repo}');"
            cursor.execute(sql)
            connection.commit()
        

# Input
user = input('Enter a Github username: ')
search_repos(user)


if __name__ == '__main__':
    search_repos(user)