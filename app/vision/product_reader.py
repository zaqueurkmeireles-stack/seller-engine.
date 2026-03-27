import PIL.Image
from google import genai
from app.config import settings
from app.schemas.product import VisionResponse, ProductAttributes
import logging

logger = logging.getLogger(__name__)

class ProductReader:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash"

    def analyze_product_image(self, image_path: str) -> VisionResponse:
        """Lê a imagem do produto e retorna atributos estruturados utilizando Gemini 2.0."""
        try:
            img = PIL.Image.open(image_path)
            
            prompt = """
            Você é um especialista em e-commerce e Mercado Livre. 
            Analise a imagem deste produto e extraia as informações no seguinte formato JSON:
            {
              "nome": "nome comercial curto",
              "marca": "marca do produto",
              "modelo": "modelo ou versão",
              "categoria_sugerida": "categoria ML",
              "cor_predominante": "cor principal",
              "condicao_aparente": "novo ou usado",
              "tags_projeto": ["tag1", "tag2"]
            }
            Seja preciso e conciso. Retorne apenas o JSON.
            """

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[prompt, img],
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': ProductAttributes,
                }
            )

            # O Gemini 2.0 com response_schema já retorna o objeto validado ou compatível
            product_data = response.parsed
            
            return VisionResponse(
                success=True,
                product=product_data,
                confidence_score=0.95, # Score fixo para MVP, Gemini 2.0 é altamente confiável
                raw_analysis=response.text
            )

        except Exception as e:
            logger.error(f"Erro na análise de visão: {str(e)}")
            return VisionResponse(
                success=False,
                confidence_score=0,
                raw_analysis="",
                error_message=str(e)
            )
