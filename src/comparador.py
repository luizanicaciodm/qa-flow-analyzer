import anthropic
import base64
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def encode_imagem(caminho):
    with open(caminho, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')


def tipo_midia(caminho):
    ext = caminho.lower().split('.')[-1]
    return {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg'}.get(ext,'image/png')


def comparar_versoes(caminho_v1, caminho_v2, criterios=''):
    """
    Compara duas versões da mesma tela e identifica diferenças.
    caminho_v1 = versão antiga
    caminho_v2 = versão nova
    """
    key = os.environ.get('ANTHROPIC_API_KEY')
    client = anthropic.Anthropic(api_key=key)

    prompt = f"""Voce e um QA Analyst senior especializado em testes de regressao visual.

Voce recebeu DUAS imagens da mesma tela de um sistema:
- IMAGEM 1: Versao ANTERIOR (antes da mudanca)
- IMAGEM 2: Versao ATUAL (apos deploy/atualizacao)

{'Criterios de aceite: ' + criterios if criterios else ''}

Faca uma analise comparativa completa com:

## MUDANCAS VISUAIS IDENTIFICADAS
- Liste todas as diferencas visuais entre as duas versoes
- Seja especifico: qual elemento mudou, como era antes, como ficou

## REGRESSOES DETECTADAS
- O que existia na versao anterior e sumiu ou piorou na atual?
- Algum criterio de aceite que era atendido deixou de ser?

## MELHORIAS CONFIRMADAS
- O que melhorou visivelmente na versao nova?
- Novos elementos que agregam valor

## RISCOS E BUGS POTENCIAIS
- Mudancas suspeitas que podem gerar bugs em producao

## VEREDICTO FINAL
- Status: APROVADO PARA DEPLOY | REPROVADO | NECESSITA REVISAO
- Justificativa do veredicto
- Prioridade de correcao (se reprovado): Alta / Media / Baixa
- Nota comparativa: versao nova melhorou/piorou/manteve a qualidade?"""

    conteudo = [
        {'type':'text','text':'IMAGEM 1 (Versao Anterior):'},
        {'type':'image','source':{'type':'base64','media_type':tipo_midia(caminho_v1),'data':encode_imagem(caminho_v1)}},
        {'type':'text','text':'IMAGEM 2 (Versao Atual):'},
        {'type':'image','source':{'type':'base64','media_type':tipo_midia(caminho_v2),'data':encode_imagem(caminho_v2)}},
        {'type':'text','text':prompt}
    ]

    resp = client.messages.create(
        model='claude-opus-4-5', max_tokens=2048,
        messages=[{'role':'user','content':conteudo}]
    )
    return resp.content[0].text


def salvar_comparacao(v1, v2, relatorio):
    os.makedirs('relatorios', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome1 = os.path.splitext(os.path.basename(v1))[0]
    nome2 = os.path.splitext(os.path.basename(v2))[0]
    saida = f'relatorios/comparacao_{nome1}_vs_{nome2}_{ts}.txt'
    with open(saida, 'w', encoding='utf-8') as f:
        f.write('='*60 + '\n')
        f.write('RELATÓRIO DE COMPARAÇÃO — QA FLOW ANALYZER\n')
        f.write(f'Versao 1 (anterior): {v1}\n')
        f.write(f'Versao 2 (atual): {v2}\n')
        f.write(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
        f.write('='*60 + '\n\n')
        f.write(relatorio)
    print(f'\nRelatório salvo em: {saida}')
    return saida


def main():
    print('\n' + '='*60)
    print('QA FLOW ANALYZER — Comparador de Versoes')
    print('='*60)
    print('\nArquivo da versao ANTERIOR:')
    v1 = input('>>> ').strip().strip('"')
    print('Arquivo da versao ATUAL/NOVA:')
    v2 = input('>>> ').strip().strip('"')
    if not os.path.exists(v1) or not os.path.exists(v2):
        print('Um ou ambos os arquivos nao foram encontrados.'); sys.exit(1)
    print('Criterios de aceite (opcional — pressione Enter para pular):')
    criterios = input('>>> ').strip()
    print('\nComparando as versoes...')
    relatorio = comparar_versoes(v1, v2, criterios)
    print('\n' + relatorio)
    salvar_comparacao(v1, v2, relatorio)

if __name__ == '__main__':
    main()