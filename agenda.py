import json
from datetime import datetime
from pathlib import Path


ARQUIVO_DADOS = Path(__file__).with_name("eventos.json")


def carregar_eventos():
	if not ARQUIVO_DADOS.exists():
		return []

	try:
		with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
			return json.load(arquivo)
	except (json.JSONDecodeError, OSError):
		print("Nao foi possivel ler os eventos salvos.")
		return []


def salvar_eventos(eventos):
	with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
		json.dump(eventos, arquivo, ensure_ascii=False, indent=2)


def cadastrar_evento(eventos):
	titulo = input("Nome do compromisso: ").strip()
	if not titulo:
		print("O nome do compromisso nao pode ficar vazio.")
		return

	try:
		data_hora = datetime.strptime(
			input("Data e hora (DD/MM/AAAA HH:MM): ").strip(),
			"%d/%m/%Y %H:%M",
		)
	except ValueError:
		print("Data ou hora invalida. Exemplo: 25/12/2026 14:30")
		return

	descricao = input("Descricao (opcional): ").strip()
	eventos.append(
		{
			"titulo": titulo,
			"data_hora": data_hora.isoformat(timespec="minutes"),
			"descricao": descricao,
		}
	)
	salvar_eventos(eventos)
	print("Compromisso cadastrado.")


def listar_eventos(eventos):
	if not eventos:
		print("Sua agenda esta vazia.")
		return

	eventos_ordenados = sorted(eventos, key=lambda evento: evento["data_hora"])
	print("\nCompromissos:")
	for numero, evento in enumerate(eventos_ordenados, start=1):
		data_hora = datetime.fromisoformat(evento["data_hora"])
		print(f"{numero}. {data_hora:%d/%m/%Y %H:%M} - {evento['titulo']}")
		if evento["descricao"]:
			print(f"   {evento['descricao']}")


def remover_evento(eventos):
	listar_eventos(eventos)
	if not eventos:
		return

	try:
		numero = int(input("Numero do compromisso para remover: "))
		eventos_ordenados = sorted(eventos, key=lambda evento: evento["data_hora"])
		evento = eventos_ordenados[numero - 1]
	except (ValueError, IndexError):
		print("Numero invalido.")
		return

	eventos.remove(evento)
	salvar_eventos(eventos)
	print("Compromisso removido.")


def main():
	eventos = carregar_eventos()

	while True:
		print("\n=== Minha Agenda ===")
		print("1. Cadastrar compromisso")
		print("2. Listar compromissos")
		print("3. Remover compromisso")
		print("4. Sair")
		opcao = input("Escolha uma opcao: ").strip()

		if opcao == "1":
			cadastrar_evento(eventos)
		elif opcao == "2":
			listar_eventos(eventos)
		elif opcao == "3":
			remover_evento(eventos)
		elif opcao == "4":
			print("Ate mais!")
			break
		else:
			print("Opcao invalida. Escolha de 1 a 4.")


if __name__ == "__main__":
	main()
