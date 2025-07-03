import requests

class UsersAPIWrapper:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com/users"):
        self.base_url = base_url

    def list(self):
        resp = requests.get(self.base_url)
        resp.raise_for_status()
        return resp.json()

    def create(self, user_data):
        resp = requests.post(self.base_url, json=user_data)
        if resp.status_code == 201:
            return resp.json()
        resp.raise_for_status()

    def read(self, user_id):
        resp = requests.get(f"{self.base_url}/{user_id}")
        resp.raise_for_status()
        return resp.json()

    def update(self, user_id, new_data):
        resp = requests.put(f"{self.base_url}/{user_id}", json=new_data)
        resp.raise_for_status()
        return resp.json()

    def delete(self, user_id):
        resp = requests.delete(f"{self.base_url}/{user_id}")
        if resp.status_code == 200:
            return {"status": "success", "message": f"User {user_id} deleted."}
        resp.raise_for_status()
