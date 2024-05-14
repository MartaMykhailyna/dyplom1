import os
import requests
from django.http import JsonResponse

def convert_currency(request, currency):
    base_carrency = 'GBP'
    api_key = os.environ.get('66ea1e8ebc2c2ed41107f072')
    
    # url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_carrency}'
    url = f'https://api.exchangerate-api.com/v4/latest/{base_carrency}?apiKey={api_key}'
    
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['rates'].get(currency.upper(), 1)
        return JsonResponse({'rate': rate})
    else:
        return JsonResponse({'error': 'Unable to fetch conversion rate'}, status=500)
        