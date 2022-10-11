import requests

login_url = "https://www.kopykitab.com/index.php?route=account/login"

client = requests.session()
client.get(login_url)

print(client)



