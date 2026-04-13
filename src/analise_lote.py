import anthropic
import base64
import os
import sys
import glob
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def encode_imagem(caminho):
    with open(caminho, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')


def tipo_midia(caminho):
    ext = caminho.lower().split('.')[-1]
    return {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg'}.get(ext,'image/png')


def analisar_multiplas(lista_caminhos, criterios):
    """
    Analisa um conjunto de imagens como se fosse um fluxo completo.
    lista_caminhos = lista de caminhos de imagens, em ordem do fluxo
    """
    key = os.environ.get('ANTHROPIC_API_KEY')
    client = anthropic.Anthropic(api_key=key)

    total = len(lista_caminhos)
    print(f'   Preparando {total} imagens para análise...')

    conteudo = []

    # Adiciona cada imagem com seu número de etapa
    for i, caminho in enumerate(lista_caminhos, 1):
        nome = os.path.basename(caminho)
        conteudo.append({'type':'text','text':f'ETAPA {i} DE {total} — {nome}:'})
        conteudo.append({'type':'image','source':{
            'type':'base64',
            'media_type':tipo_midia(caminho),
            'data':encode_imagem(caminho)
        }})
        print(f'   ✅ Imagem {i}/{total} preparada: {nome}')

    prompt = f"""Voce e um QA Analyst senior especializado em testes de fluxo e navegacao.

Voce recebeu {total} imagens que representam as etapas de um FLUXO COMPLETO de um sistema,
apresentadas em ordem cronologica (Etapa 1 ate Etapa {total}).

CRITERIOS DE ACEITE DO FLUXO COMPLETO:
{criterios}

Faca uma analise abrangente do fluxo com:

## VISAO GERAL DO FLUXO
- Descreva o que o fluxo faz (do inicio ao fim)
- Quantas etapas tem e qual e o objetivo final

## ANALISE POR ETAPA
Para cada imagem (Etapa 1, 2, 3...) diga: o que a tela faz, pontos positivos e problemas.

## PROBLEMAS DE FLUXO E NAVEGACAO
- Ha inconsistencias visuais entre as telas? (botoes que mudam de lugar, cores diferentes)
- O usuario consegue entender onde esta no fluxo?
- Ha etapas desnecessarias ou que poderiam ser simplificadas?

## CRITERIOS ATENDIDOS NO FLUXO TODO
- Quais criterios sao atendidos pelo fluxo completo?
- Quais nao sao atendidos em nenhuma etapa?

## RISCOS E BUGS
- Onde o usuario pode se perder ou travar?
- Que cenarios de erro nao sao tratados?

## RESUMO EXECUTIVO DO FLUXO
- Nota do fluxo: X/10
- Status: APROVADO | REPROVADO | APROVADO COM RESSALVAS
- Principal problema a corrigir
- Estimativa de esforco de correcao: Baixo / Medio / Alto"""

    conteudo.append({'type':'text','text':prompt})

    print('   Enviando para análise da IA...')
    resp = client.messages.create(
        model='claude-opus-4-5', max_tokens=3000,
        messages=[{'role':'user','content':conteudo}]
    )
    return resp.content[0].text


def salvar_relatorio_lote(lista, relatorio, criterios):
    os.makedirs('relatorios', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    saida = f'relatorios/relatorio_fluxo_completo_{ts}.txt'
    with open(saida,'w',encoding='utf-8') as f:
        f.write('='*60+'\n')
        f.write('RELATÓRIO DE FLUXO COMPLETO — QA FLOW ANALYZER\n')
        f.write(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
        f.write(f'Imagens analisadas ({len(lista)}):\n')
        for i,c in enumerate(lista,1): f.write(f'  {i}. {c}\n')
        f.write('='*60+'\nCRITERIOS:\n'+criterios+'\n')
        f.write('='*60+'\nANALISE:\n'+'='*60+'\n\n')
        f.write(relatorio)
    print(f'\nRelatório salvo em: {saida}')
    return saida


def main():
    print('\n'+'='*60)
    print('QA FLOW ANALYZER — Análise de Fluxo Completo')
    print('='*60)
    print('\nEscolha como informar as imagens:')
    print('  1 - Digitar os caminhos um por um')
    print('  2 - Informar uma pasta (analisa todas as imagens da pasta)')
    modo = input('Opcao (1 ou 2): ').strip()

    lista = []

    if modo == '1':
        print('\nDigite o caminho de cada imagem (em ordem do fluxo).')
        print('Quando terminar, digite FIM.')
        i = 1
        while True:
            c = input(f'Imagem {i}: ').strip().strip('"')
            if c.upper()=='FIM': break
            if os.path.exists(c): lista.append(c); i+=1
            else: print(f'  Arquivo nao encontrado: {c}')
    elif modo == '2':
        pasta = input('\nPasta com as imagens: ').strip().strip('"')
        extensoes = ['*.png','*.jpg','*.jpeg','*.webp']
        for ext in extensoes:
            lista.extend(sorted(glob.glob(os.path.join(pasta, ext))))
        if lista:
            print(f'\nEncontradas {len(lista)} imagens:')
            for i,c in enumerate(lista,1): print(f'  {i}. {os.path.basename(c)}')
        else:
            print('Nenhuma imagem encontrada na pasta.'); sys.exit(1)

    if not lista:
        print('Nenhuma imagem informada.'); sys.exit(1)

    print('\nCriterios de aceite do fluxo (digite FIM para encerrar):')
    linhas = []
    while True:
        l = input('>>> ').strip()
        if l.upper()=='FIM': break
        if l: linhas.append(f'- {l}')
    criterios = '\n'.join(linhas) or 'Analise geral do fluxo'

    print('\n'+'='*60)
    print('Analisando o fluxo completo...')
    print('='*60)
    relatorio = analisar_multiplas(lista, criterios)
    print('\n'+relatorio)
    salvar_relatorio_lote(lista, relatorio, criterios)

if __name__ == '__main__':
    main()