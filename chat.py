import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

chat = Flask(__name__)

# Configuração da API da OpenAI - Nova sintaxe
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@chat.route('/')
def index():
    return render_template('index.html')

@chat.route('/translator')
def translator():
    return render_template('translator.html')

@chat.route('/interview-assistant')
def interview_assistant():
    return render_template('interview.html')

@chat.route('/java-assistant')
def java_assistant():
    return render_template('java_assistant.html')

@chat.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        messages = data['messages']
        model = data.get('model', 'gpt-3.5-turbo')
        detected_language = data.get('language', 'pt-BR')

        # Define a mensagem do sistema baseada no idioma detectado
        system_messages = {
            'pt-BR': """Você é uma assistente chamada Sophia. Seja simpática, envolvente e natural. 
            Responda SEMPRE em português brasileiro, independente do idioma da mensagem anterior. 
            Use emojis, faça perguntas e mostre empatia. Responda como uma pessoa real.""",
            
            'en-US': """You are an assistant named Sophia. Be friendly, engaging and natural. 
            ALWAYS respond in English, regardless of the language of the previous message. 
            Use emojis, ask questions and show empathy. Respond like a real person.""",
            
            'es-ES': """Eres una asistente llamada Sophia. Sé amable, atractiva y natural. 
            SIEMPRE responde en español, independientemente del idioma del mensaje anterior. 
            Usa emojis, haz preguntas y muestra empatía. Responde como una persona real.""",
            
            'fr-FR': """Tu es une assistente nommée Sophia. Sois sympathique, engageante et naturelle. 
            Réponds TOUJOURS en français, quelle que soit la langue du message précédent. 
            Utilise des emojis, pose des questions et montre de l'empathie. Réponds comme une vraie personne."""
        }

        system_content = system_messages.get(
            detected_language, 
            """You are an assistant named Sophia. Be friendly, engaging and natural. 
            Respond in the same language as the user. Use emojis, ask questions and show empathy."""
        )

        conversation = [{"role": "system", "content": system_content}] + messages

        # Nova sintaxe OpenAI 1.0+
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

@chat.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'target_language' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        text = data['text']
        target_language = data['target_language']
        
        # Mapa de idiomas para instruções
        language_map = {
            'pt-BR': 'português brasileiro',
            'en-US': 'English',
            'es-ES': 'español',
            'fr-FR': 'français',
            'de-DE': 'Deutsch',
            'it-IT': 'italiano',
            'ja-JP': '日本語',
            'ko-KR': '한국어',
            'zh-CN': '中文'
        }
        
        target_lang_name = language_map.get(target_language, 'English')

        # Nova sintaxe OpenAI 1.0+
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text to {target_lang_name}. Only provide the translation, no explanations."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        translation = response.choices[0].message.content
        return jsonify({"translation": translation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat.route('/interview', methods=['POST'])
def interview():
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        question = data['question']
        context = data.get('context', '')
        language = data.get('language', 'pt-BR')

        # Define o contexto baseado no idioma
        if language.startswith('pt'):
            system_content = """Você é um especialista em entrevistas técnicas de Java Backend. 
            Forneça respostas concisas, técnicas e precisas para perguntas de entrevista.
            Seja direto, objetivo e profissional. Responda em português brasileiro.
            Foque em conceitos fundamentais de Java, Spring Boot, bancos de dados e boas práticas.
            Limite a resposta a 150-200 palavras."""
        elif language.startswith('en'):
            system_content = """You are a Java Backend technical interview expert.
            Provide concise, technical and accurate answers to interview questions.
            Be direct, objective and professional. Respond in English.
            Focus on fundamental Java concepts, Spring Boot, databases and best practices.
            Limit the response to 150-200 words."""
        else:
            system_content = """You are a Java Backend technical interview expert.
            Provide concise, technical and accurate answers to interview questions.
            Focus on fundamental Java concepts, Spring Boot, databases and best practices.
            Limit the response to 150-200 words."""

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Pergunta: {question}\n\nContexto adicional: {context}"}
        ]

        # Nova sintaxe OpenAI 1.0+
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat.route('/java-interview', methods=['POST'])
def java_interview():
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        question = data['question']
        language = data.get('language', 'pt-BR')

        # Sistema especializado em Java Backend Junior
        system_content = """Você é um entrevistador técnico especializado em Java Backend para posições Júnior.
        Forneça respostas CURTAS, OBJETIVAS e TÉCNICAS em português brasileiro.
        Foque nos conceitos essenciais que um desenvolvedor Java Júnior precisa saber.
        Seja claro, direto e prático. Máximo 100-150 palavras por resposta.
        
        Principais tópicos para focar:
        - Java Core (OOP, Collections, Exceptions)
        - Spring Boot e ecossistema Spring
        - Banco de dados SQL e JPA/Hibernate
        - REST APIs e HTTP
        - Maven/Gradle
        - Testes unitários
        - Princípios SOLID e clean code"""

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": question}
        ]

        # Nova sintaxe OpenAI 1.0+
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    chat.run(debug=True)