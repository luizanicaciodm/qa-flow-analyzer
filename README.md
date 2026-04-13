# 🔍 QA Flow Analyzer

Uma ferramenta que criei para me ajudar no dia a dia como analista de QA.
Você fornece um print ou vídeo de qualquer tela de sistema, informa os critérios
de aceite, e a IA analisa tudo como se fosse um QA olhando para aquela tela.

---

## Como surgiu esse projeto

Trabalho como Analista de QA e sinto que a tecnologia pode tornar algumas análises
mais ágeis e estruturadas. Decidi unir minha experiência em qualidade com
programação Python e criar algo que realmente uso no meu trabalho.

O resultado foi o QA Flow Analyzer — uma ferramenta que analisa interfaces
visualmente usando Inteligência Artificial e gera relatórios profissionais
de QA automaticamente, com pontos positivos, problemas, bugs, sugestões
e casos de teste sugeridos.

---

## O que ele faz

- Recebe uma imagem ou vídeo de um sistema
- Recebe os critérios de aceite que você definir
- Analisa a interface com visão de QA usando IA (Google Gemini)
- Gera um relatório completo com:
  - Status de cada critério (atendido ou não)
  - Problemas encontrados com severidade
  - Bugs e riscos técnicos
  - Sugestões de melhoria de UX
  - Casos de teste sugeridos
  - Nota de qualidade e status final
- Salva o relatório em `.txt` e `.pdf` automaticamente
- Interface web para usar pelo navegador (Streamlit)

---

## Tecnologias usadas

- Python 3.10+
- Google Gemini API — IA com visão computacional
- Streamlit — interface web
- FPDF2 — geração de relatórios em PDF
- Pillow — processamento de imagens
- OpenCV — extração de frames de vídeo
- python-dotenv — variáveis de ambiente seguras

---

## Estrutura do projeto
qa-flow-analyzer/
│
├── 📁 imagens/        ← prints para análise
├── 📁 videos/         ← vídeos de fluxo
├── 📁 relatorios/     ← relatórios gerados (.txt e .pdf)
├── 📁 src/
│   ├── analisador.py  ← lógica principal com IA
│   └── pdf_report.py  ← gerador de PDF
│
├── app_web.py         ← interface web (Streamlit)
├── .env               ← sua chave de API (não vai pro GitHub)
├── .gitignore
├── requirements.txt
└── README.md

---

## Como rodar

**1. Clone o repositório:**
```bash
git clone https://github.com/luizanicaciodm/qa-flow-analyzer.git
cd qa-flow-analyzer
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Configure sua chave da API:**

Crie um arquivo `.env` na raiz do projeto:
GEMINI_API_KEY=sua-chave-aqui

Obtenha sua chave gratuita em: [aistudio.google.com](https://aistudio.google.com)

**4. Rode pelo terminal:**
```bash
python src/analisador.py
```

**Ou rode a interface web:**
```bash
python -m streamlit run app_web.py
```

---

## Exemplo de relatório gerado

A ferramenta analisa a tela e retorna algo assim:
CRITÉRIOS ATENDIDOS

Campo de email obrigatório: NÃO ATENDIDO
Não há indicador visual de obrigatoriedade
Botão verde após preencher: ATENDIDO
Botão muda de cor conforme esperado

RESUMO

Nota: 3/10
Status: Reprovado
Critérios atendidos: 1 de 3
Prioridade: Alta

---

## 🎬 Demonstração do Projeto

Este projeto está em funcionamento e pode ser visualizado no vídeo abaixo, demonstrando:

- Análise de fluxo com IA  
- Validação baseada em critérios de aceite  
- Geração automatizada de relatório QA (em PDF)  

👉 [Ver demonstração do projeto](https://bit.ly/qa-flow-demo)

---

## Sobre mim

**Luiza Nicácio** — Analista de QA  

[linkedin.com/in/luizanicacio](https://linkedin.com/in/luizanicacio) •
