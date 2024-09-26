import requests
import json
import base64
import os
from cryptography.fernet import Fernet
from typing import Optional, Tuple, Union, Dict, Any, List
from altcolor.altcolor import colored_text
from datetime import datetime
import socket

loaded_data: bool = False

def is_online(url='http://www.google.com', timeout=5) -> bool:
    try:
        response = requests.get(url, timeout=timeout)
        # If the response status code is 200, we have an internet connection
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False

def data_loaded() -> bool:
    return loaded_data

class GitBase:
    def __init__(self, token: str, repo_owner: str, repo_name: str, branch: str = 'main') -> None:
        self.token: str = token
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.branch: str = branch
        self.headers: Dict[str, str] = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _get_file_url(self, path: str) -> str:
        return f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{path}"

    def _get_file_content(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        url: str = self._get_file_url(path)
        response: requests.Response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            file_data: Dict[str, Union[str, bytes]] = response.json()
            sha: str = file_data['sha']
            content: str = base64.b64decode(file_data['content']).decode('utf-8')
            return content, sha
        return None, None

    def read_data(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        content, sha = self._get_file_content(path)
        return content, sha

    def write_data(self, path: str, data: str, message: str = "Updated data") -> int:
        try:
            url: str = self._get_file_url(path)
            content, sha = self._get_file_content(path)
            encoded_data: str = base64.b64encode(data.encode('utf-8')).decode('utf-8')

            payload: Dict[str, Union[str, None]] = {
                "message": message,
                "content": encoded_data,
                "branch": self.branch
            }

            if sha:
                payload["sha"] = sha

            response: requests.Response = requests.put(url, headers=self.headers, json=payload)
            return response.status_code
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            return 500

    def delete_data(self, path: str, message: str = "Deleted data") -> int:
        try:
            url: str = self._get_file_url(path)
            _, sha = self._get_file_content(path)

            if sha:
                payload: Dict[str, str] = {
                    "message": message,
                    "sha": sha,
                    "branch": self.branch
                }
                response: requests.Response = requests.delete(url, headers=self.headers, json=payload)
                return response.status_code
            else:
                return 404
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            return 500

    @staticmethod
    def generate_example() -> None:
        example_code: str = """import gitbase.gitbase as gitbase
from cryptography.fernet import Fernet
import sys

# Generate an example of how to use gitbase [NOT NEEDED IF YOU ARE READING THIS]
gitbase.GitBase.generate_example()

# Initialize GitHub database and encryption key
token = "your_github_token"
repo_owner = "your_github_username"
repo_name = "your_repo_name"
key = Fernet.generate_key()

db = gitbase.GitBase(token, repo_owner, repo_name)
player_data_system = gitbase.PlayerDataSystem(db, key)
data_system = gitbase.DataSystem(db, key)

# Player instance with some attributes
class Player:
    def __init__(self, username, score, password):
        self.username = username
        self.score = score
        self.password = password

player = Player("john_doe", 100, "123")

# Save specific attributes of the player instance
player_data_system.save_player_data("john_doe", player, attributes=["username", "score", "password"])

# Load player data
player_data_system.load_player_data("john_doe", player)

# Placeholder functions
def load_game():
    print("Cool game text")

def main_menu():
    sys.exit()

# Check if there is a valid account before prompting for password
if gitbase.data_loaded():
    if player.password == input("Enter your password: "):
        print("Correct!")
        load_game()
    else:
        print("Incorrect password!")
        main_menu()

# Save a piece of data using a key and value pair
data_system.save_data(key="key_name", value=69)

# Load the value of a specific key by its name
key_1 = data_system.load_data(key="key_name")

# Print the value
print(key_1)

# Delete data | data_system.delete_data(key="key_name")
# Delete account | player_data_system.delete_account(username="john_doe")
"""
        with open("example_code.py", "wb") as file:
            file.write(bytes(example_code, 'UTF-8'))

    def get_file_last_modified(self, path: str) -> Optional[float]:
        """Get the last modified timestamp of the file from the GitHub repository."""
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits?path={path}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                commits = response.json()
                if commits:
                    # Get the date of the most recent commit
                    last_modified = commits[0]['commit']['committer']['date']
                    return datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%SZ").timestamp()
        except Exception as e:
            print(colored_text("RED", f"Error getting last modified time for {path}: {e}"))
        return None

class PlayerDataSystem:
    def __init__(self, db: GitBase, encryption_key: bytes) -> None:
        self.db: GitBase = db
        self.encryption_key: bytes = encryption_key
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_player_data(self, username: str, player_instance: Any, attributes: Optional[List[str]] = None) -> None:
        try:
            if attributes:
                player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in attributes if hasattr(player_instance, var)}
            else:
                player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in player_instance.__dict__}

            encrypted_data: bytes = self.encrypt_data(json.dumps(player_data))
            path: str = f"players/{username}.json"

            if is_online():
                response_code = self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved data for {username}")
                if response_code == 201 or response_code == 200:
                    print(colored_text("GREEN", f"Successfully saved online data for {username}."))
                else:
                    print(colored_text("RED", f"Error saving online data for {username}. HTTP Status: {response_code}"))
            else:
                print(colored_text("YELLOW", "Network is offline, saving to offline backup version."))
                self.save_offline_data(username, player_instance, attributes)
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            print(colored_text("GREEN", "Attempting to save to offline backup version anyway."))
            self.save_offline_data(username, player_instance, attributes)

    def save_offline_data(self, username: str, player_instance: Any, attributes: Optional[List[str]] = None) -> None:
        if not os.path.exists("gitbase/data/players"):
            os.makedirs("gitbase/data/players")

        if attributes:
            player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in attributes if hasattr(player_instance, var)}
        else:
            player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in player_instance.__dict__}

        encrypted_data: bytes = self.encrypt_data(json.dumps(player_data))
        path: str = os.path.join("gitbase/data/players", f"{username}.gitbase")

        try:
            with open(path, "wb") as file:
                file.write(encrypted_data)
            print(colored_text("GREEN", f"Successfully saved offline backup for {username}."))
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))

    def load_player_data(self, username: str, player_instance: Any) -> None:
        global loaded_data
        try:
            path: str = f"players/{username}.json"
            if is_online():
                online_data, _ = self.db.read_data(path)
                offline_path: str = f"gitbase/data/players/{username}.gitbase"
                if os.path.exists(offline_path):
                    offline_data_exists = True
                else:
                    offline_data_exists = False

                if online_data:
                    online_timestamp = self.db.get_file_last_modified(path)
                    if offline_data_exists:
                        offline_timestamp = os.path.getmtime(offline_path)

                    if offline_data_exists and offline_timestamp < online_timestamp:
                        print(colored_text("GREEN", f"Loading offline backup for {username} (newer version found)."))
                        self.load_offline_data(username, player_instance)
                        self.db.write_data(path, json.dumps(player_instance.__dict__), "Syncing offline with online")
                        loaded_data = True
                    else:
                        print(colored_text("GREEN", f"Loading online data for {username} (newer version)."))
                        decrypted_data: str = self.decrypt_data(online_data.encode('utf-8'))
                        player_data: Dict[str, Union[str, int, float]] = json.loads(decrypted_data)
                        for var, value in player_data.items():
                            setattr(player_instance, var, value)
                        loaded_data = True
                        self.save_offline_data(username, player_instance)
                elif offline_data_exists:
                    print(colored_text("GREEN", f"Loading offline backup for {username} (no online data available)."))
                    self.load_offline_data(username, player_instance)
                else:
                    loaded_data = False
                    print(colored_text("RED", f"No data found for {username}."))
            else:
                print(colored_text("YELLOW", "Network is offline, loading from offline backup."))
                self.load_offline_data(username, player_instance)
        except Exception as e:
            loaded_data = False
            print(colored_text("RED", f"Error loading player data: {e}"))

    def load_offline_data(self, username: str, player_instance: Any) -> None:
        global loaded_data
        path: str = os.path.join("gitbase/data/players", f"{username}.gitbase")
        try:
            if os.path.exists(path):
                with open(path, "rb") as file:
                    encrypted_data = file.read()
                decrypted_data: str = self.decrypt_data(encrypted_data)
                player_data: Dict[str, Union[str, int, float]] = json.loads(decrypted_data)
                for var, value in player_data.items():
                    setattr(player_instance, var, value)
                print(colored_text("GREEN", f"Successfully loaded offline backup for {username}."))
                loaded_data = True
            else:
                print(colored_text("RED", f"No offline backup found for {username}."))
                loaded_data = False
        except Exception as e:
            print(colored_text("RED", f"Error loading offline backup: {e}"))
            loaded_data = False

class DataSystem:
    def __init__(self, db: GitBase, encryption_key: bytes) -> None:
        self.db: GitBase = db
        self.encryption_key: bytes = encryption_key
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_data(self, key: str, value: Any) -> None:
        try:
            encrypted_data: bytes = self.encrypt_data(json.dumps(value))
            path: str = f"{key}.json"

            if is_online():
                response_code = self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved {key}")
                if response_code == 201:
                    print(colored_text("GREEN", f"Successfully saved online data for {key}."))
                else:
                    print(colored_text("RED", f"Error saving online data for {key}. HTTP Status: {response_code}"))
            else:
                print(colored_text("YELLOW", "Network is offline, saving to offline backup version."))
                self.save_offline_data(key, value)
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            print(colored_text("GREEN", "Attempting to save to offline backup version anyway."))
            self.save_offline_data(key, value)

    def load_data(self, key: str) -> Optional[Any]:
        path: str = f"{key}.json"
        try:
            if is_online():
                online_data, _ = self.db.read_data(path)
                if online_data:
                    decrypted_data: str = self.decrypt_data(online_data.encode('utf-8'))
                    return json.loads(decrypted_data)
                print(colored_text("RED", f"No online data found for {key}."))
            else:
                print(colored_text("YELLOW", "Network is offline, loading from offline backup."))
                return self.load_offline_data(key)
        except Exception as e:
            print(colored_text("RED", f"Error loading data: {e}"))
            return None

    def save_offline_data(self, key: str, value: Any) -> None:
        os.makedirs("gitbase/data", exist_ok=True)

        encrypted_data: bytes = self.encrypt_data(json.dumps(value))
        path: str = os.path.join("gitbase/data", f"{key}.gitbase")

        try:
            with open(path, "wb") as file:
                file.write(encrypted_data)
            print(colored_text("GREEN", f"Successfully saved offline backup for {key}."))
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))

    def load_offline_data(self, key: str) -> Optional[Any]:
        path: str = os.path.join("gitbase/data", f"{key}.gitbase")
        try:
            with open(path, "rb") as file:
                encrypted_data = file.read()
            decrypted_data: str = self.decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            print(colored_text("RED", f"Error loading offline data for {key}: {e}"))
            return None
