import urllib , json
from urllib.request import urlopen

url = "http://181.115.203.250:4040/api/Usuarios"
response = urlopen(url)
data =response.read()

print(data)

def usuarioServicio(self):
    try:
        # url = ruta
        url = "http://181.115.203.250:4040/api/Usuarios"
        headers = {'Content-Type': 'application/json'}
        string = dict()
        cadena = json.dumps(string)
        body = cadena
        resp = requests.get(url, data=body, headers=headers, verify=False)
        response = json.loads(resp.text)
        print(response)
        # self.db.close()
    except Exception as e:
        print("Error: " + str(e))