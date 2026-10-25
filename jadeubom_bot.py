import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
import tools

# Configuração do cliente local (LM Studio na porta 1234)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Histórico de conversas por ID de usuário do Telegram
historico_usuarios = {}

# Definição das 5 ferramentas avançadas para a IA
FERRAMENTAS = [
    {
        "type": "function",
        "function": {
            "name": "web_scrape",
            "description": "Lê e extrai o conteúdo de texto de um site na web a partir de uma URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL completa do site, ex: https://exemplo.com"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_code",
            "description": "Cria ou edita o conteúdo de um arquivo de código ou texto no computador local.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Caminho do arquivo, ex: D:\\jadeubom_ia\\script.py"},
                    "content": {"type": "string", "description": "O conteúdo de texto ou código completo que será gravado no arquivo."}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_code",
            "description": "Lê o conteúdo de um arquivo existente no computador.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Caminho completo do arquivo a ser lido."}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_code",
            "description": "Executa um arquivo de script Python no computador e retorna o resultado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Caminho completo do arquivo .py a ser executado."}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal",
            "description": "Executa um comando no Prompt de Comando (CMD) do Windows (ex: instalar pacotes via pip, listar diretórios, etc).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Comando exato do CMD a ser executado."}
                },
                "required": ["command"]
            }
        }
    }
]

async def responder_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    texto_usuario = update.message.text
    print(f"\n[+] Mensagem de {user_name}: {texto_usuario}")

    # Inicializa o histórico se o usuário falar pela primeira vez
    if user_id not in historico_usuarios:
        historico_usuarios[user_id] = [
            {"role": "system", "content": "Você é um assistente virtual autônomo avançado rodando localmente. Você possui ferramentas para navegar na web, criar/editar códigos, ler arquivos, rodar scripts Python e executar comandos no terminal do Windows. Lembre-se do contexto da conversa anterior para ajudar o usuário."}
        ]

    historico_usuarios[user_id].append({"role": "user", "content": texto_usuario})

    try:
        response = client.chat.completions.create(
            model="qwen2.5-7b-instruct",
            messages=historico_usuarios[user_id],
            tools=FERRAMENTAS,
            tool_choice="auto",
            temperature=0.7,
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            historico_usuarios[user_id].append(response_message)

            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"[🛠️] IA executando ferramenta: {func_name} com argumentos {arguments}")

                if func_name == "web_scrape":
                    resultado = tools.web_scrape(arguments.get("url"))
                elif func_name == "edit_code":
                    resultado = tools.edit_code(arguments.get("filepath"), arguments.get("content"))
                elif func_name == "read_code":
                    resultado = tools.read_code(arguments.get("filepath"))
                elif func_name == "run_code":
                    resultado = tools.run_code(arguments.get("filepath"))
                elif func_name == "run_terminal":
                    resultado = tools.run_terminal(arguments.get("command"))
                else:
                    resultado = "Ferramenta não encontrada."

                historico_usuarios[user_id].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(resultado)
                })

            segunda_resposta = client.chat.completions.create(
                model="qwen2.5-7b-instruct",
                messages=historico_usuarios[user_id],
                temperature=0.7
            )
            resposta_final = segunda_resposta.choices[0].message.content
            historico_usuarios[user_id].append({"role": "assistant", "content": resposta_final})
        else:
            resposta_final = response_message.content
            historico_usuarios[user_id].append({"role": "assistant", "content": resposta_final})

    except Exception as e:
        resposta_final = f"Ocorreu um erro no processamento: {str(e)}"
        print(f"[!] Erro: {e}")

    await update.message.reply_text(resposta_final)

if __name__ == '__main__':
    TOKEN = "8983997905:AAHiVJClbgp8lPT-R-TeWh0U3IawWGb5g9o"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_ia))
    
    print("🤖 Bot autônomo com memória e 5 ferramentas ativas rodando na RX 590...")
    app.run_polling()