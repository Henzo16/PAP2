from reportlab.pdfgen import canvas
from models.log import Log

def generate_pdf(logs: list[Log], filename="relatorio.pdf"):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)

    y = 800

    for log in logs:
        c.drawString(50, y, f"[{log.timestamp}] ACTION: {log.action}")
        y -= 20
        c.drawString(50, y, "Commands:")
        y -= 20

        for cmd in log.commands.split("\n"):
            c.drawString(70, y, cmd)
            y -= 15

        y -= 20

        if y < 100:
            c.showPage()
            y = 800

    c.save()
    return filename
