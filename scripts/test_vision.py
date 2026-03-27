import argparse
import sys
import os

# Adiciona o diretorio atual ao PYTHONPATH para importar o modulo app
sys.path.append(os.getcwd())

from app.vision.product_reader import ProductReader
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Validador de Terminal - Visao Seller Engine Pro")
    parser.add_argument("--image", required=True, help="Caminho para a imagem do produto")
    args = parser.parse_args()

    print(f"\nAnalisando imagem: {args.image}...")
    
    reader = ProductReader()
    result = reader.analyze_product_image(args.image)

    if result.success:
        print("\n[OK] Produto Identificado com Sucesso!")
        print(f"Produto:   {result.product.nome}")
        print(f"Marca:     {result.product.marca}")
        print(f"Modelo:    {result.product.modelo}")
        print(f"Categoria: {result.product.categoria_sugerida}")
        print(f"Cor:       {result.product.cor_predominante}")
        print(f"Condicao:  {result.product.condicao_aparente}")
        print(f"Tags:      {', '.join(result.product.tags_projeto)}")
        print(f"\nConfianca: {result.confidence_score * 100}%")
    else:
        print(f"\n[ERRO] Erro na analise: {result.error_message}")

if __name__ == "__main__":
    main()
