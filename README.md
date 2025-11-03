# ChatGPT Chatbot

Este projeto consiste em um chatbot baseado no ChatGPT que permite ao usuário interagir com modelos de IA, como GPT-3.5 Turbo e GPT-4 Turbo, através de uma interface web simples.

## 📌 Funcionalidades
- Seleção entre os modelos `GPT-3.5 Turbo` e `GPT-4 Turbo`
- Interface escura (dark mode) para melhor experiência do usuário
- Envio de mensagens do usuário e exibição de respostas do chatbot
- Integração com um endpoint `/chat` para comunicação com a API do ChatGPT

## 🛠️ Tecnologias Utilizadas
- **HTML5**: Estrutura da interface
- **CSS3**: Estilização da página
- **JavaScript (ES6)**: Lógica de envio e exibição de mensagens
- **Fetch API**: Comunicação com o backend

## 🚀 Como Executar o Projeto
### Pré-requisitos
Certifique-se de ter um ambiente com suporte a um servidor backend para processar as requisições.

### Passos
1. Clone este repositório:
   ```sh
   git clone (https://github.com/calebewerneckcouto/PythonGpt)
   ```
2. Entre no diretório do projeto:
   ```sh
   cd chatgpt-chatbot
   ```
3. Abra o arquivo `index.html` em um navegador ou sirva o projeto localmente com um servidor HTTP.

## 📡 Backend (Requisição para /chat)
Este frontend se comunica com um backend na rota `/chat`, que deve processar as mensagens e retornar uma resposta no formato JSON:
```json
{
    "response": "Aqui está a resposta do chatbot"
}
```
Certifique-se de configurar um servidor backend que processe corretamente as mensagens enviadas pelo frontend.

## 📌 Melhorias Futuras
- Adicionar suporte a WebSockets para respostas em tempo real
- Implementar autenticação de usuário
- Melhorar o design com bibliotecas como Bootstrap ou Tailwind CSS

## 📄 Licença
Este projeto está sob a licença MIT.

---
Feito com ❤️ por Calebe Werneck Couto

