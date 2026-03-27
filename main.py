import os
import threading
import PIL.Image
import google.generativeai as genai
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- SERVIDOR DE FACHADA (EASYPANEL) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Seller Engine Pro Online")

def run_fake_server():
    server = HTTPServer(('0.0.0.0', 80), SimpleHandler)
    server.serve_forever()

# --- CONFIGURAÇÕES ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! 🚀 Mande a foto de um produto e eu vou te dizer o que é e qual o preço médio de mercado.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Analisando a imagem... Aguarde um instante. 🧐")
    
    # Baixa a foto
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "produto_temp.jpg"
    await photo_file.download_to_drive(photo_path)
    
    # Carrega a imagem e manda para o Gemini
    img = PIL.Image.open(photo_path)
    prompt = "Identifique este produto e forneça uma estimativa de preço médio de venda no mercado brasileiro (novo e usado). Seja conciso."
    
    try:
        response = model.generate_content([prompt, img])
        await update.message.reply_text(f"📝 **Análise do Produto:**\n\n{response.text}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao analisar: {str(e)}")
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)

if __name__ == '__main__':
    threading.Thread(target=run_fake_server, daemon=True).start()
    
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo)) # Agora ele escuta FOTOS!
    
    print("Seller Engine Pro com Visão Ativa!")
    app.run_polling()