from xml.dom.minidom import parseString
import requests

URL_SERVICO = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"
HEADERS = {'Content-Type': 'text/xml; charset=utf-8'}

print("=== SERVIÇOS DISPONÍVEIS ===")
print("1. Moeda do país")
print("2. Código telefônico")
print("3. Capital do país")
print("-" * 40)

opcao = input("\nDigite o número do serviço desejado: ")
codigo_pais = input("Digite o código do país (ex: BR): ").upper()

if opcao == "1":
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <CountryCurrency xmlns="http://www.oorsprong.org/websamples.countryinfo">
          <sCountryISOCode>{codigo_pais}</sCountryISOCode>
        </CountryCurrency>
      </soap:Body>
    </soap:Envelope>"""
    tag_resposta = 'CountryCurrencyResult'
    
elif opcao == "2":
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <CountryIntPhoneCode xmlns="http://www.oorsprong.org/websamples.countryinfo">
          <sCountryISOCode>{codigo_pais}</sCountryISOCode>
        </CountryIntPhoneCode>
      </soap:Body>
    </soap:Envelope>"""
    tag_resposta = 'CountryIntPhoneCodeResult'
    
elif opcao == "3":
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <CapitalCity xmlns="http://www.oorsprong.org/websamples.countryinfo">
          <sCountryISOCode>{codigo_pais}</sCountryISOCode>
        </CapitalCity>
      </soap:Body>
    </soap:Envelope>"""
    tag_resposta = 'CapitalCityResult'
    
else:
    print("Opção inválida!")
    exit()

try:
    resposta = requests.post(URL_SERVICO, headers=HEADERS, data=payload)
    resposta.raise_for_status()
    
    dom = parseString(resposta.content)
    
    fault = dom.getElementsByTagName('soap:Fault')
    if fault:
        error_msg = fault[0].getElementsByTagName('faultstring')[0].firstChild.nodeValue
        print(f"\nERRO: {error_msg}")
        exit()

    resultado = dom.getElementsByTagName(tag_resposta)
    
    if not resultado:
        print("\nResposta inesperada da API. Elemento não encontrado.")
        print("Resposta completa:\n", resposta.text)
        exit()
        
    if opcao == "1":
        sISOCode = resultado[0].getElementsByTagName('sISOCode')
        sName = resultado[0].getElementsByTagName('sName')
        
        if sISOCode and sName and sISOCode[0].firstChild and sName[0].firstChild:
            print(f"\nMoeda: {sISOCode[0].firstChild.nodeValue} ({sName[0].firstChild.nodeValue})")
        else:
            print("\nDados incompletos na resposta da API")
            
    else:
        if resultado[0].firstChild:
            valor = resultado[0].firstChild.nodeValue
            if opcao == "2":
                print(f"\nCódigo telefônico: +{valor}")
            else:
                print(f"\nCapital: {valor}")
        else:
            print("\nResposta vazia da API")
            
except requests.exceptions.HTTPError as errh:
    print(f"\nErro HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"\nErro de conexão: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"\nTimeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"\nErro na requisição: {err}")
except Exception as e:
    print(f"\nErro inesperado: {e}")