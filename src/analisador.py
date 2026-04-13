import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

sys.path.insert(0, os.path.dirname(__file__))
from pdf_report import gerar_pdf

load_dotenv()


def analise_fallback(motivo):
    return f"""MODO FALLBACK ATIVADO

Motivo: {motivo}

Analise alternativa de QA:
- Verificar obrigatoriedade dos campos
- Validar mensagens de erro
- Avaliar clareza da interface
- Conferir consistencia visual
"""


def analisar(caminho_imagem, criterios):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return analise_fallback("API Key nao encontrada no .env")

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return analise_fallback(f"Falha ao criar cliente: {e}")

    try:
        with open(caminho_imagem, "rb") as f:
            imagem_bytes = f.read()
    except Exception as e:
        return analise_fallback(f"Erro ao ler imagem: {e}")

    ext = caminho_imagem.lower().split(".")[-1]
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")

    prompt = f"""
Voce e um QA Analyst senior com 10 anos de experiencia em sistemas corporativos reais.
Sua analise deve ser tecnica, detalhada e diretamente utilizavel em um relatorio de QA profissional.

CRITERIOS DE ACEITE FORNECIDOS:
{criterios}

Gere o relatorio no seguinte formato EXATO:

## VISAO GERAL
- Tipo de tela identificado
- Objetivo da tela
- Publico-alvo provavel

## CRITERIOS ATENDIDOS
Para cada criterio diga ATENDIDO ou NAO ATENDIDO com justificativa visual.

## PROBLEMAS ENCONTRADOS
Para cada problema:
- Severidade: Critico | Alto | Medio | Baixo
- Descricao do problema
- Impacto para o usuario
- Criterio violado

## BUGS E RISCOS TECNICOS
- Descricao do risco
- Probabilidade: Alta | Media | Baixa
- Sugestao de teste

## SUGESTOES DE MELHORIA
- O que melhorar
- Por que melhorar
- Como implementar

## RESUMO
- Nota de Qualidade: X/10
- Status: Aprovado / Reprovado / Aprovado com Ressalvas
- Criterios Atendidos: X de Y
- Prioridade de Correcao: Alta / Media / Baixa

## CASOS DE TESTE SUGERIDOS
- CT-01: Descricao | Resultado Esperado
- CT-02: Descricao | Resultado Esperado
- CT-03: Descricao | Resultado Esperado
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(data=imagem_bytes, mime_type=mime),
                types.Part(text=prompt)
            ]
        )
    ]

    for tentativa in range(5):
        try:
            print(f"Tentativa {tentativa + 1}...")
            time.sleep(3)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )
            if response and response.text:
                return response.text
            return analise_fallback("Resposta vazia da API.")
        except Exception as e:
            erro = str(e)
            if "429" in erro:
                print(f"Rate limit. Aguardando 65s...")
                time.sleep(65)
            else:
                return analise_fallback(f"Erro: {erro}")

    return analise_fallback("Limite de tentativas atingido.")


def salvar_relatorio(caminho, texto, criterios):
    os.makedirs("relatorios", exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path_txt = f"relatorios/relatorio_{nome}_{ts}.txt"
    with open(path_txt, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("RELATORIO QA - QA FLOW ANALYZER\n")
        f.write(f"Arquivo: {caminho}\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("CRITERIOS:\n" + criterios + "\n\n")
        f.write("=" * 60 + "\nANALISE:\n" + "=" * 60 + "\n\n")
        f.write(texto)
    gerar_pdf(caminho, texto, criterios)
    print(f"\nRelatorio salvo em: {path_txt}")
    return path_txt


def main():
    print("\n" + "=" * 60)
    print("QA FLOW ANALYZER - Analisador de Fluxo com IA")
    print("=" * 60)
    print("\nArquivo (imagem ou video):")
    caminho = input(">>> ").strip().strip('"')
    if not os.path.exists(caminho):
        print(f"Arquivo nao encontrado: {caminho}")
        sys.exit(1)
    print("\nCriterios de aceite (digite FIM para encerrar):")
    linhas = []
    while True:
        l = input(">>> ").strip()
        if l.upper() == "FIM":
            break
        if l:
            linhas.append(f"- {l}")
    criterios = "\n".join(linhas) or "Analise geral de qualidade"
    print("\nAnalisando...")
    relatorio = analisar(caminho, criterios)
    print("\n" + relatorio)
    salvar_relatorio(caminho, relatorio, criterios)


if __name__ == "__main__":
    main()