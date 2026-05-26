import os
import json
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReceiptSystem:
    def __init__(self, record_file="receipt_records.json"):
        self.record_file = record_file
        self._ensure_record_file()

    def _ensure_record_file(self):
        if not os.path.exists(self.record_file):
            with open(self.record_file, 'w') as f:
                json.dump([], f)

    def generate_receipt(self, customer_name, items, discount_percent=0.0):
        # 1. Calculate subtotal, discount, and grand total
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        discount_amount = (subtotal * discount_percent) / 100
        grand_total = subtotal - discount_amount

        # 2. Generate unique ID and timestamp
        receipt_id = f"REC-{uuid.uuid4().hex[:8].upper()}"
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3. Create the transaction record
        transaction_data = {
            "receipt_id": receipt_id,
            "date": date_str,
            "customer_name": customer_name,
            "items": items,
            "subtotal": subtotal,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "grand_total": grand_total
        }

        # 4. Generate the PDF
        pdf_filename = f"{receipt_id}.pdf"
        self._create_pdf(pdf_filename, transaction_data)

        # 5. Save record to JSON
        self._save_record(transaction_data)

        print(f"\n✅ Success! Receipt generated: {pdf_filename}")
        print(f"Grand Total: ${grand_total:.2f}\n")
        return pdf_filename

    def _create_pdf(self, filename, data):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Header Information
        elements.append(Paragraph("<b>OFFICIAL PAYMENT RECEIPT</b>", styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"<b>Receipt ID:</b> {data['receipt_id']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Date:</b> {data['date']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Customer Name:</b> {data['customer_name']}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Table Header
        table_data = [["Item Description", "Quantity", "Unit Price", "Total"]]
        
        # Populate Table Rows
        for item in data['items']:
            item_total = item['quantity'] * item['price']
            table_data.append([
                item['name'],
                str(item['quantity']),
                f"${item['price']:.2f}",
                f"${item_total:.2f}"
            ])

        # Add Subtotal, Discount, and Grand Total Rows
        table_data.append(["", "", "Subtotal:", f"${data['subtotal']:.2f}"])
        if data['discount_percent'] > 0:
            table_data.append(["", "", f"Discount ({data['discount_percent']}%):", f"-${data['discount_amount']:.2f}"])
        table_data.append(["", "", "GRAND TOTAL:", f"${data['grand_total']:.2f}"])

        # Table Styling
        t = Table(table_data, colWidths=[200, 80, 100, 100])
        
        # Calculate where the summary rows start to style them correctly
        summary_start_row = len(data['items']) + 1 
        
        t.setStyle(TableStyle([
            # Header Row Style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data Rows Style
            ('BACKGROUND', (0, 1), (-1, summary_start_row - 1), colors.HexColor("#ECF0F1")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            
            # Summary Rows (Subtotal, Discount) Styling
            ('FONTNAME', (2, summary_start_row), (-1, -2), 'Helvetica-Oblique'),
            
            # Grand Total Row Style
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
            ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'), 
            ('TEXTCOLOR', (2, -1), (-1, -1), colors.HexColor("#27AE60")), # Green color for final total
        ]))

        elements.append(t)
        doc.build(elements)

    def _save_record(self, data):
        with open(self.record_file, 'r') as f:
            records = json.load(f)

        records.append(data)

        with open(self.record_file, 'w') as f:
            json.dump(records, f, indent=4)

def run_interactive_cli():
    print("===================================")
    print("    RECEIPT GENERATOR TERMINAL     ")
    print("===================================")
    
    customer_name = input("Enter Customer Name: ").strip()
    
    # Safely get discount
    while True:
        try:
            discount_input = input("Enter Discount Percentage (Enter 0 if none): ").strip()
            discount = float(discount_input) if discount_input else 0.0
            if discount < 0 or discount > 100:
                print("Discount must be between 0 and 100.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    items = []
    print("\n--- Add Items ---")
    print("(Type 'done' when you are finished adding items)\n")
    
    while True:
        item_name = input("Item Name (or 'done'): ").strip()
        if item_name.lower() == 'done':
            break
        if not item_name:
            print("Item name cannot be empty.")
            continue
            
        # Safely get quantity
        while True:
            try:
                quantity = int(input(f"Quantity of '{item_name}': ").strip())
                if quantity <= 0:
                    print("Quantity must be at least 1.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")
                
        # Safely get price
        while True:
            try:
                price = float(input(f"Unit Price of '{item_name}': $").strip())
                if price < 0:
                    print("Price cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid price.")

        items.append({"name": item_name, "quantity": quantity, "price": price})
        print(f"-> Added {quantity}x {item_name} @ ${price:.2f} each\n")

    if not items:
        print("\nNo items were added. Receipt generation cancelled.")
        return

    # Generate the actual receipt
    print("\nProcessing transaction...")
    system = ReceiptSystem()
    system.generate_receipt(customer_name, items, discount)

if __name__ == "__main__":
    run_interactive_cli()