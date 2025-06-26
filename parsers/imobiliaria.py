import xml.etree.ElementTree as ET
import json

tree = ET.parse('parsers/imobiliaria.xml')
root = tree.getroot()

json_data = {
    "imobiliaria": {
        "imovel": []
    }
}

for imovel in root.findall('imovel'):
    imovel_data = {
        "id": imovel.get('id').replace("Imovel_", ""),
        "descricao": imovel.find('descricao').text
    }
    
    proprietario = imovel.find('proprietario')
    proprietario_data = {"nome": proprietario.find('nome').text}
    
    emails = [e.text for e in proprietario.findall('email')]
    if emails:
        proprietario_data["email"] = emails[0] if len(emails) == 1 else emails
    
    telefones = [t.text for t in proprietario.findall('telefone')]
    if telefones:
        proprietario_data["telefone"] = telefones[0] if len(telefones) == 1 else telefones
    
    imovel_data["proprietario"] = proprietario_data
    
    endereco = imovel.find('endereco')
    endereco_data = {
        "rua": endereco.find('rua').text,
        "bairro": endereco.find('bairro').text,
        "cidade": endereco.find('cidade').text,
        "estado": endereco.find('estado').text
    }
    
    numero = endereco.find('numero')
    if numero is not None and numero.text:
        endereco_data["numero"] = numero.text
    
    imovel_data["endereco"] = endereco_data
    
    # Características
    caracteristicas = imovel.find('caracteristicas')
    imovel_data["caracteristicas"] = {
        "tamanho": f"{float(caracteristicas.find('tamanho').text.split()[0]):.2f}",
        "numQuartos": caracteristicas.find('numQuartos').text,
        "numBanheiros": caracteristicas.find('numBanheiros').text
    }
    
    valor = imovel.find('valor')
    imovel_data["valor"] = f"{float(valor.text):.2f}"
    
    json_data["imobiliaria"]["imovel"].append(imovel_data)

with open('imobiliaria.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print("Conversão concluída. Arquivo 'imobiliaria.json' criado.")