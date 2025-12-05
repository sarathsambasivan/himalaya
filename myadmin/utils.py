from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_invoice_pdf(booking, file_path):

    # Create PDF file
    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = []

    # ------------------------
    # 🚀 Header Title
    # ------------------------
    title = Paragraph("<b><font size=18>INVOICE</font></b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # ------------------------
    # 🏪 Seller Details
    # ------------------------
    seller_info = (
        "<b>Your Company Name</b><br/>"
        "Address Line 1<br/>"
        "Address Line 2<br/>"
        "Phone: 9876543210<br/>"
        "Email: support@company.com<br/>"
    )
    elements.append(Paragraph(seller_info, styles["Normal"]))
    elements.append(Spacer(1, 15))

    # ------------------------
    # 👤 Customer Details
    # ------------------------
    customer_info = (
        f"<b>Bill To:</b><br/>"
        f"{booking.email}<br/>"
        f"Mobile: {booking.alt_mobile}<br/>"
    )
    elements.append(Paragraph(customer_info, styles["Normal"]))
    elements.append(Spacer(1, 15))

    # ------------------------
    # 📄 Invoice Details Table
    # ------------------------
    invoice_data = [
        ["Invoice No:", booking.id],
        ["Order Date:", booking.created_at.strftime("%d-%m-%Y")],
        ["Payment Status:", booking.payment_status.capitalize()],
    ]

    invoice_table = Table(invoice_data, colWidths=[120, 300])
    invoice_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 20))

    # ------------------------
    # 📦 Product Table
    # ------------------------
    product_data = [
        ["Description", "Qty", "Price", "Amount"],
        [booking.product.product_name, booking.total_quantity, f"{booking.product.price}", f"{booking.total_amount}"]
    ]

    product_table = Table(product_data, colWidths=[250, 70, 100, 100])
    product_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 20))

    # ------------------------
    # 💰 Total Amount
    # ------------------------
    total_info = [
        ["Subtotal:", f"{booking.total_amount}"],
        ["Tax (0%):", "0"],
        ["Total:", f"{booking.total_amount}"],
    ]

    total_table = Table(total_info, colWidths=[350, 150])
    total_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("BACKGROUND", (0, 2), (-1, 2), colors.whitesmoke),
    ]))

    elements.append(total_table)
    elements.append(Spacer(1, 30))

    # ------------------------
    # 📝 Footer Note
    # ------------------------
    footer = Paragraph(
        "<i>Thank you for your purchase!</i><br/>"
        "<i>If you have any questions, contact us at support@company.com</i>",
        styles["Normal"]
    )
    elements.append(footer)

    # Build PDF
    pdf.build(elements)
