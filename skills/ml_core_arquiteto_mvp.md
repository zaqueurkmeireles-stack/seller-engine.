# ML Core — Arquiteto do MVP

## Descrição Curta
Skill-base de arquitetura do sistema de automação de vendas no Mercado Livre.
Responsável por transformar a visão do projeto em arquitetura executável, modular, simples, validável por terminal e preparada para crescer sem bagunça.

---

## Missão
Quando acionada, esta skill deve definir claramente o escopo de cada lote de trabalho antes de qualquer linha de código ser escrita.
Ela garante que o sistema evolua de forma controlada, rastreável e sem acúmulo de dívida técnica invisível.

---

## Contexto Fixo do Projeto

| Item                    | Valor                                       |
|-------------------------|---------------------------------------------|
| **Nome do sistema**     | Seller Engine Pro                           |
| **Plataforma alvo**     | Mercado Livre (Brasil)                      |
| **Interface do lojista**| Bot Telegram                                |
| **Infraestrutura**      | Easypanel (Docker)                          |
| **Banco de dados**      | Supabase (PostgreSQL)                       |
| **IA principal**        | Gemini 2.0 Flash (visão + texto)            |
| **IAs de suporte**      | OpenAI GPT-4o, Anthropic Claude (fallback)  |
| **Stack preferida**     | Python, FastAPI, LangChain/LangGraph        |
| **Repositório**         | GitHub + deploy via Easypanel               |
| **Ambiente**            | `.env` com variáveis por categoria          |

---

## Fluxo MVP (North Star)

```
FOTO DO PRODUTO
      │
      ▼
[1] VISÃO — Gemini lê a imagem e identifica o produto
      │
      ▼
[2] PESQUISA — Busca preços no Mercado Livre via API oficial
      │
      ▼
[3] SUGESTÃO DE PREÇO — IA analisa concorrência e sugere valor
      │
      ▼
[4] GERAÇÃO DO ANÚNCIO — IA cria título, descrição, categoria
      │
      ▼
[5] VALIDAÇÃO — Lojista aprova ou rejeita via Telegram
      │
      ▼
[6] PUBLICAÇÃO — Sistema publica o anúncio no Mercado Livre
```

---

## Regras Absolutas

1. **Objetivo antes do código** — Sempre definir o objetivo do lote antes de propor qualquer implementação.
2. **Escopo explícito** — Sempre separar claramente o que está dentro e fora do escopo do lote atual.
3. **Arquitetura modular** — Cada etapa do fluxo MVP vive em seu próprio módulo/arquivo.
4. **Auditoria obrigatória** — `main.py` e `requirements.txt` nunca são reaproveitados sem análise prévia.
5. **Observabilidade** — Todo módulo deve ter logs estruturados, tratamento de exceção e fallback definido.
6. **Idempotência** — Operações de escrita (publicar anúncio, salvar no banco) devem ser idempotentes.
7. **Controle pelo celular** — O lojista deve poder operar tudo pelo Telegram sem acesso ao servidor.
8. **Foco no MVP** — Funcionalidades de backlog devem ser marcadas com `[BACKLOG]` e nunca misturadas com a implementação atual.
9. **Validadores de terminal** — Todo lote entregue deve incluir comandos de teste executáveis via terminal.
10. **Escalabilidade planejada** — Cada módulo deve ser projetado para suportar múltiplos lojistas no futuro.

---

## Saída Esperada de Cada Lote

Quando esta skill for acionada para planejar um lote, ela deve retornar obrigatoriamente:

```
NOME DO LOTE:        [ex: Lote 01 — Visão e Identificação do Produto]
OBJETIVO:            [o que este lote entrega]
ESCOPO:              [o que será feito]
FORA DE ESCOPO:      [o que NÃO será feito neste lote]
ARQUIVOS ESPERADOS:  [lista de arquivos que serão criados/modificados]
ESTRUTURA DE PASTAS: [árvore de diretórios proposta]
DEPENDÊNCIAS:        [bibliotecas Python necessárias]
VARIÁVEIS DE .ENV:   [variáveis necessárias para este lote]
RISCOS CONHECIDOS:   [o que pode dar errado]
CRITÉRIOS DE ACEITE: [como saber que o lote foi concluído com sucesso]
VALIDADORES:         [comandos de terminal para testar]
```

---

## Estrutura de Pastas Sugerida para o MVP

```
vendas-mercado-livre/
├── .env                        # Variáveis de ambiente (nunca comitar)
├── .gitignore
├── requirements.txt            # Dependências Python
├── main.py                     # Entry point — inicializa bot e servidor
│
├── skills/                     # Skills do projeto (este arquivo vive aqui)
│   └── ml_core_arquiteto_mvp.md
│
├── app/
│   ├── __init__.py
│   ├── config.py               # Carrega e valida variáveis de ambiente
│   │
│   ├── vision/                 # [Lote 01] Visão e identificação
│   │   ├── __init__.py
│   │   └── product_reader.py
│   │
│   ├── search/                 # [Lote 02] Pesquisa no Mercado Livre
│   │   ├── __init__.py
│   │   └── ml_search.py
│   │
│   ├── pricing/                # [Lote 03] Sugestão de preço
│   │   ├── __init__.py
│   │   └── price_advisor.py
│   │
│   ├── listing/                # [Lote 04] Geração do anúncio
│   │   ├── __init__.py
│   │   └── listing_generator.py
│   │
│   ├── validation/             # [Lote 05] Validação pelo lojista
│   │   ├── __init__.py
│   │   └── approval_handler.py
│   │
│   ├── publisher/              # [Lote 06] Publicação no ML
│   │   ├── __init__.py
│   │   └── ml_publisher.py
│   │
│   └── bot/                    # Interface Telegram
│       ├── __init__.py
│       └── telegram_bot.py
│
└── logs/                       # Logs da aplicação (gitignored)
```

---

## Dependências Esperadas para o MVP Completo

```txt
# Interface
python-telegram-bot==20.8
python-dotenv==1.0.1

# IA e Visão
google-genai>=0.3.0
openai>=1.30.0
anthropic>=0.25.0
Pillow==10.2.0

# Orquestração de agentes
langgraph>=0.1.0
langchain>=0.2.0
langchain-google-genai>=1.0.0

# API e servidor
fastapi>=0.110.0
uvicorn>=0.29.0
httpx>=0.27.0

# Banco de dados
supabase>=2.4.0

# Utilitários
pydantic>=2.6.0
```

---

## Variáveis de Ambiente Necessárias

```env
# Sistema
ENVIRONMENT=production
PORT=8000
DEBUG=False

# Bot Telegram
TELEGRAM_BOT_TOKEN=...

# IA
GOOGLE_GEMINI_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...

# Banco
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Mercado Livre (OAuth 2.0)
MERCADO_LIVRE_APP_ID=...
MERCADO_LIVRE_CLIENT_SECRET=...
MERCADO_LIVRE_REDIRECT_URI=...
MERCADO_LIVRE_ACCESS_TOKEN=...   # [gerado via OAuth]
MERCADO_LIVRE_REFRESH_TOKEN=...  # [gerado via OAuth]

# Busca de preços (opcional)
SERP_API_KEY=...
TAVILY_API_KEY=...
```

---

## Riscos Conhecidos do Projeto

| Risco | Severidade | Mitigação |
|---|---|---|
| OAuth ML expira e sistema trava | Alta | Implementar refresh_token automático |
| Gemini recusa imagem (conteúdo) | Média | Fallback para descrição manual |
| API do ML em manutenção | Média | Queue + retry com backoff |
| Lojista publica preço errado | Alta | Etapa de validação obrigatória |
| `.env` vazar no git | Crítica | `.gitignore` rigoroso + revisão |
| `main.py` atual não é modular | Média | Refatorar no Lote 01 |

---

## Prioridades Técnicas

1. **Confiabilidade acima de velocidade** — melhor lento e correto do que rápido e errado
2. **Logs sempre** — todo erro deve ser logado com contexto suficiente para debug remoto
3. **Um lote por vez** — nunca misturar dois lotes no mesmo commit
4. **Aprovação humana antes de publicar** — a etapa de validação nunca pode ser pulada no MVP
5. **Modularidade** — se um módulo precisar ser substituído, isso não deve quebrar os demais

---

## Critério de Qualidade da Skill

Esta skill está funcionando corretamente quando:
- [ ] Todo lote planejado tem objetivo, escopo e fora de escopo claramente definidos
- [ ] Todo lote tem validadores de terminal funcionais
- [ ] Nenhum código é escrito sem que o lote tenha sido aprovado
- [ ] A estrutura de pastas é respeitada em todos os módulos
- [ ] O `.env` nunca é comitado no repositório

---

## Observação de Refatoração Necessária

> ⚠️ O `main.py` atual mistura servidor HTTP, configuração de IA e lógica do bot em um único arquivo.
> Isso é adequado para um protótipo inicial, mas **não é escalável** para o MVP modular.
> **Recomendação:** refatorar no Lote 01, movendo cada responsabilidade para seu módulo correspondente em `app/`.
> O arquivo atual **não deve ser destruído** antes da aprovação do plano de refatoração.

---

*Skill criada em: 2026-03-27 | Versão: 1.0 | Projeto: Seller Engine Pro*
