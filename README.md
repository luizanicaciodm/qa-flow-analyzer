🔍 QA Flow Analyzer

Uma ferramenta que criei para me ajudar no dia a dia como analista de QA.
Você fornece um print ou vídeo de qualquer tela de sistema, informa os critérios
de aceite, e a IA analisa tudo como se fosse um QA olhando para aquela tela.

---

🚀 Como surgiu esse projeto

Trabalho como QA Analyst e sinto que a tecnologia pode tornar algumas análises
mais ágeis e estruturadas. Decidi unir minha experiência em qualidade com
programação Python e criar algo que realmente uso no meu trabalho.

O resultado foi o QA Flow Analyzer, uma ferramenta que analisa interfaces
visualmente usando Inteligência Artificial e gera relatórios profissionais
de QA automaticamente, com pontos positivos, problemas, bugs, sugestões
e casos de teste sugeridos.

---

🎯 Objetivo

Simular o olhar de um QA na validação de sistemas, garantindo:

- Validação de critérios de aceite  
- Identificação de problemas e inconsistências  
- Detecção de riscos e possíveis bugs  
- Sugestões de melhoria de usabilidade (UX)  
- Apoio na criação de casos de teste  

---

⚙️ Funcionalidades

- 📸 Análise de imagens (prints de sistemas)
- 🎥 Análise de vídeos (fluxos completos)
- 🧠 Interpretação inteligente baseada em critérios de aceite
- 📊 Geração automática de relatórios contendo:
  - Status dos critérios (atendido/não atendido)
  - Problemas identificados com impacto
  - Bugs e riscos potenciais
  - Sugestões de melhoria
  - Casos de teste sugeridos
  - Score de qualidade
- 📄 Exportação de relatórios em `.txt` e `.pdf`
- 🌐 Interface web para uso simplificado (Streamlit)

---

🛠 Tecnologias utilizadas

- Python 3.10+
- Google Gemini API — IA com visão computacional
- Streamlit — interface web
- FPDF2 — geração de relatórios em PDF
- OpenCV — extração de frames de vídeo
- python-dotenv — variáveis de ambiente seguras

---

📁 Estrutura do projeto

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

▶️ Como executar

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

📄 Exemplo de relatório gerado

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
🎬 Demonstração do projeto

👉 [Veja o projeto em funcionamento](https://bit.ly/qa-flow-demo)

---

## 👩‍💻 Sobre mim

**Luiza Nicácio** – Analista de QA

🔗 [LinkedIn](https://linkedin.com/in/luizanicacio)