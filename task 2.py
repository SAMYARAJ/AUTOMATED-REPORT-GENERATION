import pandas as pd
from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        # Logo and Title
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Monthly Sales Analysis Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_report(data_file, output_file):
    # 1. Data Analysis Phase
    try:
        df = pd.read_csv(data_file)
        
        # Calculations
        total_revenue = df['Price'].sum()
        total_units = df['Quantity'].sum()
        avg_order = df['Price'].mean()
        top_product = df.groupby('Product')['Quantity'].sum().idxmax()
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. PDF Generation Phase
    pdf = PDFReport()
    pdf.add_page()
    
    # Executive Summary Section
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, '1. Executive Summary', 0, 1, 'L', fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.ln(5)
    
    summary_metrics = [
        f"Total Revenue: ${total_revenue:,.2f}",
        f"Total Units Sold: {total_units}",
        f"Average Order Value: ${avg_order:,.2f}",
        f"Best Selling Product: {top_product}"
    ]
    
    for metric in summary_metrics:
        pdf.cell(0, 7, f"- {metric}", 0, 1)
    
    pdf.ln(10)

    # Data Table Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Detailed Transaction Logs', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_font('Arial', 'B', 10)
    cols = ['Date', 'Product', 'Qty', 'Price']
    col_widths = [40, 70, 30, 50]
    
    for i in range(len(cols)):
        pdf.cell(col_widths[i], 10, cols[i], 1, 0, 'C')
    pdf.ln()

    # Table Rows
    pdf.set_font('Arial', '', 10)
    for index, row in df.iterrows():
        pdf.cell(col_widths[0], 8, str(row['Date']), 1)
        pdf.cell(col_widths[1], 8, str(row['Product']), 1)
        pdf.cell(col_widths[2], 8, str(row['Quantity']), 1, 0, 'C')
        pdf.cell(col_widths[3], 8, f"${row['Price']:.2f}", 1, 0, 'R')
        pdf.ln()

    # Save output
    pdf.output(output_file)
    print(f"Success: Report saved as {output_file}")

# Sample Execution
if __name__ == "__main__":
    # Create a dummy CSV for the demonstration
    data = {
        'Date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04'],
        'Product': ['Cloud Server A', 'Database Instance', 'SSL Certificate', 'Cloud Server B'],
        'Quantity': [2, 1, 5, 1],
        'Price': [1200.00, 450.00, 250.00, 800.00]
    }
    pd.DataFrame(data).to_csv('sales_data.csv', index=False)
    
    # Generate the report
    generate_report('sales_data.csv', 'Final_Analytics_Report.pdf')
