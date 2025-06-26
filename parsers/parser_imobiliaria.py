from xml.dom.minidom import parse

dom = parse("parsers/imobiliaria.xml")
imobiliaria = dom.documentElement
imoveis = imobiliaria.getElementsByTagName('imovel')

print("=== IMOBILIÁRIA ===")
print("ID   | Descrição")
print("-" * 40)
for imovel in imoveis:
    id_imovel = imovel.getAttribute('id')
    descricao = imovel.getElementsByTagName('descricao')[0].firstChild.nodeValue
    print(f"{id_imovel} | {descricao}")

escolha = input("\nDigite o ID do imóvel que deseja ver os detalhes: ")

encontrado = False
for imovel in imoveis:
    id_imovel = imovel.getAttribute('id')
    if id_imovel == escolha:
        descricao = imovel.getElementsByTagName('descricao')[0].firstChild.nodeValue
        proprietario = imovel.getElementsByTagName('proprietario')[0]
        nome = proprietario.getElementsByTagName('nome')[0].firstChild.nodeValue
        emails = [e.firstChild.nodeValue for e in proprietario.getElementsByTagName('email')]
        telefones = [t.firstChild.nodeValue for t in proprietario.getElementsByTagName('telefone')]
        endereco = imovel.getElementsByTagName('endereco')[0]
        rua = endereco.getElementsByTagName('rua')[0].firstChild.nodeValue
        numeros = endereco.getElementsByTagName('numero')
        if numeros and numeros[0].firstChild:
            numero = numeros[0].firstChild.nodeValue
        else:
            numero = "SN"
        bairro = endereco.getElementsByTagName('bairro')[0].firstChild.nodeValue
        cidade = endereco.getElementsByTagName('cidade')[0].firstChild.nodeValue
        estado = endereco.getElementsByTagName('estado')[0].firstChild.nodeValue
        caracteristicas = imovel.getElementsByTagName('caracteristicas')[0]
        tamanho = caracteristicas.getElementsByTagName('tamanho')[0].firstChild.nodeValue
        quartos = caracteristicas.getElementsByTagName('numQuartos')[0].firstChild.nodeValue
        banheiros = caracteristicas.getElementsByTagName('numBanheiros')[0].firstChild.nodeValue
    
        valor_node = imovel.getElementsByTagName('valor')[0]
        moeda = valor_node.getAttribute('moeda')
        valor = valor_node.firstChild.nodeValue
        
        print(f"\n=== DETALHES DO IMÓVEL {id_imovel} ===")
        print(f"Descrição: {descricao}")
        print(f"\nProprietário: {nome}")
        if emails: print("Emails:", ", ".join(emails))
        if telefones: print("Telefones:", ", ".join(telefones))
        print(f"\nEndereço: {rua}, {numero} - {bairro}")
        print(f"Cidade: {cidade}/{estado}")
        print(f"\nCaracterísticas:")
        print(f"  Tamanho: {tamanho}")
        print(f"  Quartos: {quartos}")
        print(f"  Banheiros: {banheiros}")
        print(f"\nValor: {moeda} {valor}")
        
        encontrado = True
        break

if not encontrado:
    print("\nID de imóvel não encontrado. Por favor, tente novamente.")