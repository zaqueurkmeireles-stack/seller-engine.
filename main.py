import os
import threading
import PIL.Image
from google import genai
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- SERVIDOR DE FACHADA PARA O EASYPANEL ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Seller Engine Pro 2.0 Online")

def run_fake_server():
    server = HTTPServer(('0.0.0.0', 80), SimpleHandler)
    server.serve_forever()

# --- CONFIGURAÇÕES ---
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! 🚀 Versão 2.0 Ativa. Mande a foto de um produto para análise imediata!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Analisando com Gemini 2.0... 🧐")
    
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "temp_prod.jpg"
    await photo_file.download_to_drive(photo_path)
    
    try:
        img = PIL.Image.open(photo_path)
        # Usando a nova SDK unificada
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=["Identifique este produto e estime o preço médio no Brasil (novo e usado).", img]
        )
        await msg.edit_text(f"📝 **Análise Pro:**\n\n{response.text}")
    except Exception as e:
        await msg.edit_text(f"Erro na análise: {str(e)}")
    finally:
        if os.path.exists(photo_path): os.remove(photo_path)

if __name__ == '__main__':
    threading.Thread(target=run_fake_server, daemon=True).start()
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🚀 Seller Engine Pro 2.0: ON")
    app.run_polling()