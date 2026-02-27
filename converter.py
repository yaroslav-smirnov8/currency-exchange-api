import requests
import json
from os.path import join, dirname
from dotenv import load_dotenv
from dotenv import dotenv_values

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = dotenv_values(".env")


class Converter:
    @staticmethod
    def get_price(base, amount, sym):
        base_key = str(base).strip().upper()
        sym_key = str(sym).strip().upper()
        api_key = config.get("EXCHANGERATE_API_KEY") or config.get("API_KEY")
        if not api_key:
            raise ValueError("EXCHANGERATE_API_KEY is not configured.")
        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_key}"
        )
        resp = json.loads(r.content)
        new_price = resp['conversion_rates'][sym_key] * float(amount)
        return new_price
