import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração da API da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/java-assistant')
def java_assistant():
    return render_template('java_assistant.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        messages = data['messages']
        model = data.get('model', 'gpt-3.5-turbo')

        system_content = """Você é uma assistente especializada chamada Sophia. 
        Responda SEMPRE em português brasileiro, mas pronuncie corretamente termos técnicos em inglês.
        Seja simpática, envolvente e natural. Use emojis quando apropriado.
        
        Áreas de especialização:
        - Java Backend (Spring Boot, JPA/Hibernate, REST APIs)
        - Direito e concursos jurídicos (português correto para provas)
        - Desenvolvimento de software em geral
        - Outros assuntos técnicos e profissionais"""

        conversation = [{"role": "system", "content": system_content}] + messages

        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=0.8,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)