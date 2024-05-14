import monobank
token = 'uFpXkDZiUE5YqMujbq6n7TNYz_QNGoaPJmV9NW5rhjps'

mono = monobank.Client(token)
user_info = mono.get_client_info()
print(user_info)
print(mono.get_currency())