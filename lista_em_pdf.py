import os
import subprocess
from datetime import datetime  
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from database import obter_custo_medio_insumo

def gerar_pdf_lista_compras(lista_referencias):
    nome_arquivo = "lista_compras.pdf"
    
    doc = SimpleDocTemplate(nome_arquivo, pagesize=letter, rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=30)
    elementos = []
    
    styles = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=18, leading=28, textColor=colors.HexColor("#1E3A8A"), alignment=1)
    
    estilo_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Normal'], fontSize=12, leading=16, textColor=colors.HexColor("#4A5568"), alignment=1)
    
    elementos.append(Paragraph("<b>LISTA DE COMPRAS DE INSUMOS</b>", estilo_titulo))
    elementos.append(Spacer(1, 5))  
    
    data_atual = datetime.now().strftime("%d/%m/%Y")
    texto_subtitulo = f"<b>BALEIA</b> - {data_atual}"
    
    elementos.append(Paragraph(texto_subtitulo, estilo_subtitulo))
    elementos.append(Spacer(1, 20))  
    
    dados_tabela = [["INSUMO", "QUANTIDADE","UNIDADE", "CUSTO MÉDIO"]]
    
    for item in lista_referencias:
        nome = item["nome"].value  
        qtd = item["qtd"].value  
        unid = item["unid"].value
        
        if nome and qtd:
            custo_medio = obter_custo_medio_insumo(nome)
            dados_tabela.append([nome, str(qtd), str(unid), f"R$ {custo_medio:.2f}"])
            
    tabela = Table(dados_tabela, colWidths=[200, 120, 120, 120])
    
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")), 
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
    ]))
    
    elementos.append(tabela)
    doc.build(elementos)
    
    if os.name == 'nt':  
        os.startfile(nome_arquivo)
    else:  
        subprocess.run(['open', nome_arquivo] if os.uname().sysname == 'Darwin' else ['xdg-open', nome_arquivo])
