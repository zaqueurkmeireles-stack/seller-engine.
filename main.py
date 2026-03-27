from app.config import settings
import logging

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("SellerEnginePro")

def main():
    logger.info(f"🚀 Seller Engine Pro 2.0 inicializado em modo: {settings.ENVIRONMENT}")
    logger.info("Módulos de infraestrutura e visão carregados. Use scripts/test_vision.py para testes individuais.")

if __name__ == "__main__":
    main()