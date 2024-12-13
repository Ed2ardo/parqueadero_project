from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def generar_factura_pdf(factura):
    # Crear un buffer para el PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Factura de Parqueadero")

    # Detalles de la factura
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100,
                 f"Número de Factura: {factura.numero_factura}")
    c.drawString(50, height - 120,
                 f"Fecha de Emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 140,
                 f"Vehículo: {factura.registro_parqueo.vehiculo.placa}")
    c.drawString(50, height - 160,
                 f"Tipo de Vehículo: {factura.registro_parqueo.vehiculo.get_tipo_display()}")
    c.drawString(50, height - 180, f"Tiempo Estacionado: {
                 factura.registro_parqueo.tiempo_estacionado} minutos")
    c.drawString(50, height - 200,
                 f"Total a Pagar: ${factura.total_cobro:.2f}")

    # Detalles adicionales
    if factura.detalles:
        c.drawString(50, height - 220, "Detalles Adicionales:")
        c.drawString(70, height - 240, factura.detalles)

    # Pie de página
    c.drawString(50, 50, "Gracias por utilizar nuestro parqueadero.")

    # Finalizar el PDF
    c.save()

    buffer.seek(0)
    return buffer
