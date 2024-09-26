import requests
from stringcolor import cs


class CurrencyConverter:
    api_url = 'https://api.exchangerate-api.com/v4/latest/'
    @staticmethod
    def convert(from_currency, to_currency, amount):
        url = CurrencyConverter.api_url + from_currency 
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception("API request failed.")
        print(cs(f'API request OK:{response.status_code}','green'))
        rates = response.json()['rates']
        if to_currency not in rates:
            raise Exception(f"Currency {to_currency} not available.")
        return amount*rates[to_currency]
    
    
