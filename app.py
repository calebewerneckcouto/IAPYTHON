from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração para openai 0.28
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({"error": "Mensagem não fornecida"}), 400
            
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Verificar se API key está configurada
        if not openai.api_key:
            return jsonify({"error": "API key não configurada"}), 500
        
        # Sintaxe para openai 0.28
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content.strip()
        return jsonify({"response": bot_response})
        
    except openai.error.AuthenticationError:
        return jsonify({"error": "API key inválida ou expirada"}), 401
    except openai.error.RateLimitError:
        return jsonify({"error": "Limite de requisições excedido"}), 429
    except openai.error.APIConnectionError:
        return jsonify({"error": "Erro de conexão com a API"}), 503
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": f"Requisição inválida: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)