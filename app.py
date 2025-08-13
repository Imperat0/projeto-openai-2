import os
from dotenv import load_dotenv
from openai import OpenAI
from assistente_ecomart import pegar_json

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistente = pegar_json()
thread_id = assistente["thread_id"]
assistente_id = assistente["assistant_id"]
file_ids = assistente["file_ids"]


def enviar_mensagem(thread_id, role, content):
    cliente.beta.threads.messages.create(
        thread_id=thread_id, role=role, content=content
    )


def executar_thread(thread_id, assistant_id):
    run = cliente.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run


def esperar_thread(thread_id, run_id):
    while True:
        run = cliente.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            mensagens = cliente.beta.threads.messages.list(thread_id=thread_id)
            for mensagem in mensagens.data:
                if mensagem.role == "assistant":
                    return mensagem.content[0].text.value
        else:
            print("Aguardando...")


while True:
    mensagem_usuario = input("Digite sua mensagem: ")
    enviar_mensagem(thread_id, "user", mensagem_usuario)
    run = executar_thread(thread_id, assistente_id)
    resposta = esperar_thread(thread_id, run.id)
    print(resposta)
