# PRODUCCION
import requests
import json
import hashlib
import hmac
from datetime import datetime

x_login = "OOWCRMIi8c"
x_trans_key = "7xhdH4NDex"
secret_key = "oNVhBFRpZnZTvIS8b1rm2TEOUH7yozyUt"

url = "https://api.dlocal.com/payments"

# Cuerpo de la solicitud
body = { 
    "amount": 100, 
    "currency": "USD", 
    "country": "PA", 
    "payment_method_flow": "REDIRECT", 
    "payer": { 
        "name": "Joao Peres", 
        "email": "usertest@dlocal.com", 
        "address": { 
            "city": "Goa", 
            "street": "Maddo Vaddo", 
            "number": "1207" 
        } 
    }, 
    "order_id": "Zh3gb4jhbg34Vj10", 
    "notification_url": "http://merchant.com/notifications" 
}

# Convertir el cuerpo a JSON
body_json = json.dumps(body)

# Obtener la fecha actual en el formato requerido
x_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# Crear el string de firma
signature_string = f'{x_login}{x_date}{body_json}'

# Crear la firma HMAC-SHA256
signature = hmac.new(secret_key.encode(), signature_string.encode(), hashlib.sha256).hexdigest()

# Encabezados de la solicitud
headers = {
    'X-Date': x_date,
    'X-Login': x_login,
    'X-Trans-Key': x_trans_key,
    'Content-Type': 'application/json',
    'X-Version': '2.1',
    'User-Agent': 'Procesasdasdos',
    'Authorization': f'V2-HMAC-SHA256, Signature: {signature}'
}

print(headers)

try:
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=body_json)
    # Imprimir la respuesta
    print(response.text)
except Exception as e:
    print("Error:", e)
