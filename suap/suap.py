import requests
from getpass import getpass

SUAP_URL = "https://suap.ifrn.edu.br/api/"
HEADERS = {'Content-Type': 'application/json'}

def formatar_tabela(boletim):
    """Formata os dados do boletim em uma tabela textual"""
    cabecalho = (
        f"{'Disciplina':<40} | {'1º':<5} | {'2º':<5} | {'3º':<5} | {'4º':<5} | "
        f"{'Média':<6} | {'Situação':<15} | {'Faltas':<6}"
    )
    separador = "-" * len(cabecalho)
    
    linhas = [cabecalho, separador]
    
    for materia in boletim:
        disciplina = materia.get('disciplina', '')[:40]
        n1 = materia.get('nota_etapa_1', {}).get('nota', '—') or '—'
        n2 = materia.get('nota_etapa_2', {}).get('nota', '—') or '—'
        n3 = materia.get('nota_etapa_3', {}).get('nota', '—') or '—'
        n4 = materia.get('nota_etapa_4', {}).get('nota', '—') or '—'
        media = materia.get('media_final_disciplina', '—') or '—'
        situacao = materia.get('situacao', '—')
        faltas = materia.get('numero_faltas', '—')
        
        for nota in [n1, n2, n3, n4, media]:
            if isinstance(nota, (int, float)):
                nota = f"{nota:.1f}"
        
        linha = (
            f"{disciplina:<40} | {str(n1):<5} | {str(n2):<5} | {str(n3):<5} | {str(n4):<5} | "
            f"{str(media):<6} | {situacao:<15} | {str(faltas):<6}"
        )
        linhas.append(linha)
    
    return "\n".join(linhas)

print("\n" + "="*50)
print("Autenticação no SUAP".center(50))
print("="*50)
user = input("\nUsuário: ")
password = getpass("Senha: ")

payload = {"username": user, "password": password}
try:
    response = requests.post(
        SUAP_URL + "v2/autenticacao/token/", 
        json=payload, 
        headers=HEADERS
    )
    response.raise_for_status()
    token = response.json()["access"]
except requests.exceptions.RequestException as e:
    print(f"\nErro na autenticação: {e}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

print("\n" + "="*50)
print("Consulta de Boletim".center(50))
print("="*50)
ano = input("\nDigite o ano letivo (ex: 2024): ")
periodo = input("Digite o período (1 ou 2): ")

try:
    response = requests.get(
        f"{SUAP_URL}edu/meu-boletim/{ano}/{periodo}/", 
        headers=headers
    )
    response.raise_for_status()
    boletim = response.json()
except requests.exceptions.RequestException as e:
    print(f"\nErro ao buscar boletim: {e}")
    exit(1)

print("\n" + "="*80)
print(f"BOLETIM ESCOLAR - {ano}/{periodo}".center(80))
print("="*80)
print(formatar_tabela(boletim))
print("="*80)