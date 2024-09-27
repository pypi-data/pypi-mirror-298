from nimble_data.answerit import Answerit
from nimble_data.client import Client

client = Client(token="YWNjb3VudC1jcmF3bGl0LXBpcGVsaW5lLW5pbWJsZWRhdGE6UnYxNTJQM1k3VjlX")
json = Answerit(client).ask_domain_retreival(["https://www.nimbleway.com"],
                                        ["What does Nimble do?", "Who is their CEO?"])
print(json)