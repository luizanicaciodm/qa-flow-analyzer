import streamlit as st
import os
import sys
import tempfile
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from analisador import analisar, salvar_relatorio

load_dotenv()

st.set_page_config(
    page_title='QA Flow Analyzer',
    page_icon='🔍',
    layout='wide'
)

st.title('🔍 QA Flow Analyzer')
st.divider()

col_esq, col_dir = st.columns([1, 1])

with col_esq:
    st.subheader('📁 Upload do Arquivo')
    arquivo = st.file_uploader(
        'Selecione uma imagem ou vídeo do sistema:',
        type=['png', 'jpg', 'jpeg', 'webp', 'mp4', 'avi', 'mov', 'mkv'],
        help='Arraste e solte ou clique para selecionar'
    )
    if arquivo:
        if arquivo.type.startswith('image'):
            st.image(arquivo, caption=arquivo.name, width=400)
        else:
            st.video(arquivo)

with col_dir:
    st.subheader('📋 Critérios de Aceite')
    criterios = st.text_area(
        'Digite os critérios (um por linha):',
        height=250,
        placeholder='Campo de email deve ser obrigatorio\nBotao de login deve estar visivel\nMensagem de erro ao falhar...'
    )
    st.info('Dica: quanto mais detalhados os critérios, melhor a análise!')

st.divider()

if st.button('🧠 Analisar com IA', type='primary', use_container_width=True):
    if not arquivo:
        st.error('Por favor, faça upload de uma imagem ou vídeo.')
    else:
        if not criterios.strip():
            criterios = 'Analise geral de qualidade da interface.'

        sufixo = '.' + arquivo.name.split('.')[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
            tmp.write(arquivo.read())
            caminho_temp = tmp.name

        with st.spinner('🤖 Analisando com IA... aguarde...'):
            try:
                relatorio = analisar(caminho_temp, criterios)
                path_txt = salvar_relatorio(caminho_temp, relatorio, criterios)

                # Encontra o PDF gerado mais recente
                pasta = 'relatorios'
                arquivos_pdf = [
                    f for f in os.listdir(pasta) if f.endswith('.pdf')
                ]
                path_pdf = None
                if arquivos_pdf:
                    path_pdf = os.path.join(
                        pasta,
                        sorted(arquivos_pdf)[-1]
                    )

                st.success('✅ Análise concluída!')
                st.divider()
                st.subheader('📊 Relatório Gerado')
                st.markdown(relatorio)
                st.divider()

                c1, c2 = st.columns(2)
                with c1:
                    with open(path_txt, 'rb') as f:
                        st.download_button(
                            '📄 Baixar TXT',
                            f,
                            file_name=os.path.basename(path_txt)
                        )
                with c2:
                    if path_pdf:
                        with open(path_pdf, 'rb') as f:
                            st.download_button(
                                '📕 Baixar PDF',
                                f,
                                file_name=os.path.basename(path_pdf)
                            )

            except Exception as e:
                st.error(f'Erro na análise: {str(e)}')
            finally:
                try:
                    os.unlink(caminho_temp)
                except:
                    pass