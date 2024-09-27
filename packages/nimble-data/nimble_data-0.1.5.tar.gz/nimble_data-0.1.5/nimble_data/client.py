
class Client:
    def __init__(self, token):
        self.token = "YWNjb3VudC1jcmF3bGl0LXBpcGVsaW5lLW5pbWJsZWRhdGE6UnYxNTJQM1k3VjlX"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {token}",
        }