from fpdf import FPDF
from datetime import datetime
import os
import re


def limpar(texto):
    texto = str(texto)
    texto = re.sub(r'\*+', '', texto)
    texto = re.sub(r'#+', '', texto)
    texto = texto.replace('📋','').replace('✅','').replace('⚠️','')
    texto = texto.replace('🐛','').replace('💡','').replace('📊','')
    texto = texto.replace('📝','').replace('❌','').replace('✔','')
    texto = texto.replace('•', '-')
    texto = texto.strip()
    return texto.encode("latin-1", "ignore").decode("latin-1")


class RelatorioPDF(FPDF):
    def header(self):
        self.set_fill_color(26, 58, 92)
        self.rect(0, 0, 210, 22, 'F')
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(190, 8, 'QA FLOW ANALYZER')
        self.set_font('Helvetica', '', 9)
        self.set_xy(10, 13)
        self.cell(190, 7, 'Relatorio de Analise de Qualidade')
        self.set_y(28)

    def footer(self):
        self.set_y(-13)
        self.set_fill_color(26, 58, 92)
        self.rect(0, self.get_y(), 210, 15, 'F')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(200, 200, 200)
        self.cell(0, 10, f'Pagina {self.page_no()}  |  QA Flow Analyzer', align='C')

    def bloco_titulo(self, texto, r, g, b):
        self.ln(4)
        self.set_fill_color(r, g, b)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_x(10)
        self.cell(190, 10, f'  {limpar(texto)}', fill=True, ln=True)
        self.set_text_color(40, 40, 40)
        self.ln(2)

    def linha_normal(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.set_x(10)
        self.multi_cell(190, 6, limpar(texto))

    def linha_item(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.set_x(14)
        self.multi_cell(186, 6, limpar('- ' + texto))


CORES_SECAO = {
    'VISAO GERAL':           (46, 125, 50),
    'CRITERIOS ATENDIDOS':   (21, 101, 192),
    'PROBLEMAS ENCONTRADOS': (183, 28, 28),
    'BUGS E RISCOS':         (230, 81, 0),
    'SUGESTOES DE MELHORIA': (0, 121, 107),
    'RESUMO':                (55, 71, 79),
    'CASOS DE TESTE':        (74, 20, 140),
}


def eh_titulo(linha):
    l = linha.strip()
    return l.startswith('##') or (l.startswith('**') and l.endswith('**') and len(l) < 80)


def get_cor(titulo):
    t = titulo.upper()
    for chave, cor in CORES_SECAO.items():
        if chave in t:
            return cor
    return (46, 109, 164)


def gerar_pdf(caminho_arquivo, relatorio_texto, criterios, pasta_saida='relatorios'):
    try:
        os.makedirs(pasta_saida, exist_ok=True)
        ts = datetime.now().strftime('%d%m%Y_%H%M')
        saida = f'{pasta_saida}/relatorio_qa_{ts}.pdf'

        pdf = RelatorioPDF()
        pdf.set_margins(left=10, top=10, right=10)
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.add_page()

        # Info
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(26, 58, 92)
        pdf.set_x(10)
        pdf.multi_cell(190, 7, limpar(f'Data: {datetime.now().strftime("%d/%m/%Y as %H:%M")}'))
        pdf.ln(5)

        # Criterios
        pdf.bloco_titulo('CRITERIOS DE ACEITE', 94, 53, 177)
        for linha in criterios.split('\n'):
            if linha.strip():
                pdf.linha_item(linha.strip().lstrip('-').strip())
        pdf.ln(4)

        # Relatorio
        for linha in relatorio_texto.replace("\r", "").split('\n'):

            if not linha.strip():
                pdf.ln(2)
                continue

            if eh_titulo(linha):
                titulo = limpar(linha)
                pdf.bloco_titulo(titulo, *get_cor(titulo))
                continue

            texto = linha.strip()
            if not texto:
                continue

            if texto.startswith('-') or texto.startswith('*'):
                pdf.linha_item(texto.lstrip('-* ').strip())
            else:
                pdf.linha_normal(texto)

        pdf.output(saida)
        print(f'PDF gerado: {saida}')
        return saida

    except Exception as e:
        print(f'Erro ao gerar PDF: {e}')
        return None