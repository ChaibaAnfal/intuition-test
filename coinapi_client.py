import requests

class CoinAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://rest.coinapi.io/v1"

    def get_price(self, asset_id):
        url = f"{self.base_url}/exchangerate/{asset_id}/USD"
        headers = {"X-CoinAPI-Key": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["rate"]
        else:
            raise Exception(f"Erreur API : {response.status_code} - {response.text}")