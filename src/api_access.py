import json
import requests

class ApiAccess:
    def get(self, url, headers):
        response = requests.get(url, headers)
        return json.loads(response.text)

class FakeApiAccess:
    def get(self, url, headers):
        if url.startswith("https://api.api-ninjas.com/v1/historicalevents"):
            return [{"year": 1440, "event": "Emperor Gratian elevates Flavius Theodosius at Sirmium to Augustus, and gives him authority over all the eastern provinces of the Roman Empire."}]
        else:
            return {}