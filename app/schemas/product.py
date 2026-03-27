from pydantic import BaseModel, Field
from typing import List

class ProductAttributes(BaseModel):
    """Schema para os atributos identificados do produto pela visao computacional."""
    nome: str = Field(..., description="Nome comercial curto e direto do produto")
    marca: str = Field(..., description="Marca do fabricante")
    modelo: str = Field(..., description="Modelo ou numero de serie do produto")
    categoria_sugerida: str = Field(..., description="Categoria sugerida para o Mercado Livre")
    cor_predominante: str = Field(default="nao identificada", description="Cor principal")
    condicao_aparente: str = Field(default="novo", description="Condicao aparente: novo ou usado")
    tags_projeto: List[str] = Field(default_factory=list, description="Lista de tags para facilitar a busca no radar")

class VisionResponse(BaseModel):
    """Resposta estruturada do servico de visao."""
    success: bool
    product: ProductAttributes = None
    confidence_score: float = Field(..., ge=0, le=1)
    raw_analysis: str = Field(..., description="Texto bruto da analise da IA")
    error_message: str = Field(default="", description="Mensagem de erro se houver")
