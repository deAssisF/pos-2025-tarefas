from xml.dom.minidom import parse

dom = parse("cardapio.xml")
cardapio = dom.documentElement
pratos = cardapio.getElementsByTagName('prato')

print("=== MENU DE PRATOS ===")
for prato in pratos:
    id_prato = prato.getAttribute('id')
    nome = prato.getElementsByTagName('nome')[0].firstChild.nodeValue
    print(f"ID: {id_prato} - Nome: {nome}")

escolha = input("\nDigite o ID do prato que deseja ver os detalhes: ")

encontrado = False
for prato in pratos:
    id_prato = prato.getAttribute('id')
    if id_prato == escolha:
        nome = prato.getElementsByTagName('nome')[0].firstChild.nodeValue
        descricao = prato.getElementsByTagName('descricao')[0].firstChild.nodeValue
        preco = prato.getElementsByTagName('preco')[0].firstChild.nodeValue
        calorias = prato.getElementsByTagName('calorias')[0].firstChild.nodeValue
        tempo = prato.getElementsByTagName('tempoPreparo')[0].firstChild.nodeValue
        ingredientes = prato.getElementsByTagName('ingrediente')
        lista_ingredientes = [ing.firstChild.nodeValue for ing in ingredientes]

        print(f"\n=== Detalhes do Prato ID {id_prato} ===")
        print(f"Nome: {nome}")
        print(f"Descrição: {descricao}")
        print("Ingredientes:", ", ".join(lista_ingredientes))
        print(f"Preço: R${preco}")
        print(f"Calorias: {calorias} kcal")
        print(f"Tempo de Preparo: {tempo}")
        encontrado = True
        break

if not encontrado:
    print("\nID de prato não encontrado. Por favor, tente novamente.")
