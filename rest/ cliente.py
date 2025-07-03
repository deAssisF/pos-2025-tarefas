import argparse
import json
from users_wrapper import UsersAPIWrapper

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de usuários via JSONPlaceholder")
    parser.add_argument("action", choices=["list", "create", "read", "update", "delete"], help="Operação desejada")
    parser.add_argument("--id", help="ID do usuário")
    parser.add_argument("--data", help="Dados do usuário em JSON para create/update")

    args = parser.parse_args()
    api = UsersAPIWrapper()

    try:
        if args.action == "list":
            resultado = api.list()

        elif args.action == "create":
            if not args.data:
                raise ValueError("Use --data para fornecer os dados do usuário.")
            dados = json.loads(args.data)
            resultado = api.create(dados)

        elif args.action == "read":
            if not args.id:
                raise ValueError("Informe o ID com --id para consultar um usuário.")
            resultado = api.read(args.id)

        elif args.action == "update":
            if not args.id or not args.data:
                raise ValueError("Use --id e --data para atualizar um usuário.")
            dados = json.loads(args.data)
            resultado = api.update(args.id, dados)

        elif args.action == "delete":
            if not args.id:
                raise ValueError("Informe o ID com --id para deletar um usuário.")
            resultado = api.delete(args.id)

        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Erro durante a operação: {e}")

if __name__ == "__main__":
    main()
