import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- TRUQUE PARA O EASYPANEL (FACHADA) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Seller Engine Online")

def run_fake_server():
    # Cria um mini site na porta 80 para o Easypanel ficar feliz
    server = HTTPServer(('0.0.0.0', 80), SimpleHandler)
    server.serve_forever()
# ----------------------------------------

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! 🚀 Eu sou o seu Seller Engine Pro.\n\n"
        "Agora estou rodando 100% nas nuvens e pronto para trabalhar!\n"
        "Me mande a foto de um produto para começarmos."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Recebi sua mensagem! Em breve poderei analisar preços e fotos.")

if __name__ == '__main__':
    # Liga o site de fachada em segundo plano
    threading.Thread(target=run_fake_server, daemon=True).start()
    
    print("Iniciando o Seller Engine Pro...")
    
    # Liga o Robô do Telegram
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot e Site ativos. Pronto para o deploy!")
    app.run_polling()