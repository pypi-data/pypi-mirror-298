# GitBase

GitBase is a Python package for custom databases powered by GitHub, with encryption using `cryptography`. It allows you, as a python developer to have a quick and easy to use database without learning a whole new programming language. Furthermore, we offer offline backups for users of your application, this means their data can be saved, loaded, and deleted even if they have no internet. Moreover, the online version will be updated based on which file, the offline or online, is the latest.

## Installation

Install via pip:

```bash
pip install gitbase
```

Example code: 

```py
from gitbase.gitbase import GitHubDatabase, PlayerDataSystem, DataSystem
from cryptography.fernet import Fernet

# Generate an example of how to use gitbase [NOT NEEDED IF YOU ARE READING THIS]
GitHubDatabase.generate_example()

# Initialize GitHub database and encryption key
token = "your_github_token"
repo_owner = "your_repo_owner"
repo_name = "your_repo_name"
key = Fernet.generate_key()

db = GitHubDatabase(token, repo_owner, repo_name)
player_data_system = PlayerDataSystem(db, key)
data_system = DataSystem(db, key)

# Player instance with some attributes
class Player:
    def __init__(self, username, score):
        self.username = username
        self.score = score

player = Player("john_doe", 100)

# Save specific attributes of the player instance
player_data_system.save_player_data("john_doe", player, attributes=["username", "score"])

# Load player data
player_data_system.load_player_data("john_doe", player)

# Save a piece of data using a key and value pair
data_system.save_data(key="key_name", value=69)

# Load the value of a specific key by its name
key_1 = data_system.load_data(key="key_name")

# Print the value
print(key_1)

# Delete data | data_system.delete_data(key="key_name")
# Delete account | player_data_system.delete_account(username="john_doe")
```

# Consider using GitBase Web: https://github.com/TaireruLLC/gitbase-web

## Gitbase Web: 

### Gitbase Web is an extension of the PyPi module by Taireru LLC called GitBase. This extension allows the developer to veiw all of their saved data via the web.
### Please note that to view said data you **MUST** use a private repo and use a website hosting service such as vercel.

## Links: 
### GitBase: https://pypi.org/project/gitbase/
### Website: https://tairerullc.vercel.app/


#### Contact 'tairerullc@gmail.com' for any inquires and we will get back at our latest expense. Thank you for using our product and happy coding!