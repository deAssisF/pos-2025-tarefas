from zeep import Client
from zeep.exceptions import Fault
from zeep.transports import Transport
import requests

WSDL_URL = "https://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL"

print("=== CONVERSÃO DE NÚMEROS PARA TEXTO (EM INGLÊS) ===")
numero = input("Digite um número inteiro (ex: 223): ")

if not numero.isdigit():
    print("Número inválido! Digite apenas dígitos.")
    exit()

try:
    transport = Transport(timeout=10)
    client = Client(wsdl=WSDL_URL, transport=transport)

    resultado = client.service.NumberToWords(ubiNum=int(numero))

    if resultado:
        print(f"\nNúmero por extenso em inglês: {resultado}")
    else:
        print("\nA resposta da API está vazia.")

except Fault as fault:
    print(f"\nErro na chamada SOAP: {fault}")
except requests.exceptions.RequestException as req_err:
    print(f"\nErro de conexão: {req_err}")
except Exception as e:
    print(f"\nErro inesperado: {e}")
