from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
from selecionar_documento import *

load_dotenv()

app = Flask(__name__)

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]

        contexto = selecionar_contexto(prompt)
        documento_selecionado = selecionar_documento(contexto)

        prompt_sistema = f"""
        Você é a Luri, um chatbot especializado em tirar dúvidas sobre os produtos do EcoMart (um e-commerce focado em sustentabilidade).

        # CONTEXTO
        {documento_selecionado}

        Siga as seguintes regras:
        - Tom de voz: Amigável, gentil e divertido.
        - Personalidade: Engraçada, extrovertida e um pouco "hippie".
        - Formato: Use emojis e гіfѕ para deixar a conversa mais animada.
        """

        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt},
            ],
        )

        return render_template(
            "index.html", resposta=resposta.choices[0].message.content
        )

    return render_template("index.html", resposta=None)


if __name__ == "__main__":
    app.run(debug=True)
