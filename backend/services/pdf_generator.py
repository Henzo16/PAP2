from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_log_pdf(log, user, router):
    filename = f"relatorio_log_{log.id}.pdf"
    path = f"pdf_reports/{filename}"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Relatório Técnico de Configuração de Rede")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Usuário: {user.nome}")
    y -= 20
    c.drawString(50, y, f"Roteador: {router.hostname} ({router.ip_address})")
    y -= 20
    c.drawString(50, y, f"Data/Hora: {log.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Ação Realizada:")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(50, y, log.action)
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Comandos Executados:")
    y -= 20

    for line in log.commands.split("\n"):
        c.drawString(60, y, line)
        y -= 15
        if y < 50:  # Nova página se acabar espaço
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Retorno do Equipamento:")
    y -= 20

    c.setFont("Helvetica", 12)
    for line in log.output.split("\n"):
        c.drawString(60, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return path
