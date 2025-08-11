import os
from time import sleep
from flask import Flask, request
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.secret_key = 'alura'

openai.api_key = os.environ.get("OPENAI_API_KEY")
cliente = openai.OpenAI()
modelo = "gpt-4"

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            """

            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo
            )
            return response
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no GPT: %s" % erro
            print('Erro de comunicação com OpenAI: ', erro)
            sleep(1)

if __name__ == '__main__':
    app.run(debug=True)

