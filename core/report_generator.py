import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

from ml.predictor import generate_prediction_data
from matplotlib.figure import Figure

def generate_report_pdf(output_path, report_name):
    """
    Generates a PDF report with a chart and data table.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = []

    # 1. Title
    title = Paragraph(f"Sales Performance Report: {report_name}", styles['h1'])
    story.append(title)
    story.append(Spacer(1, 0.25*inch))

    # 2. Introduction Paragraph
    intro_text = "This report summarizes the recent sales performance against the generated forecast. The following chart visualizes the comparison, and the table provides the underlying data points."
    intro = Paragraph(intro_text, styles['BodyText'])
    story.append(intro)
    story.append(Spacer(1, 0.25*inch))

    # 3. Generate Data and Chart
    data = generate_prediction_data()
    
    # Create Matplotlib chart in memory
    fig = Figure(figsize=(7, 3.5), dpi=300)
    ax = fig.add_subplot(111)
    ax.plot(data['historical_x'], data['historical_y'], marker='o', label='Actual Sales')
    ax.plot(data['predicted_x'], data['predicted_y'], marker='o', linestyle='--', label='Forecast')
    ax.set_title("Historical vs. Forecasted Sales")
    ax.set_xlabel("Time Period")
    ax.set_ylabel("Revenue (Units)")
    ax.legend()
    ax.grid(True)
    
    # Save the plot to a PNG in a memory buffer
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    
    # Add the image to the PDF story
    chart_image = Image(img_buffer, width=6*inch, height=3*inch)
    story.append(chart_image)
    story.append(Spacer(1, 0.25*inch))

    # 4. Create a Data Table
    table_title = Paragraph("Detailed Data", styles['h2'])
    story.append(table_title)
    
    table_data = [['Time Period', 'Actual Sales', 'Forecasted Sales']]
    
    # Combine historical and forecast data for the table
    all_periods = sorted(list(set(data['historical_x']) | set(data['predicted_x'])))
    hist_dict = dict(zip(data['historical_x'], data['historical_y']))
    pred_dict = dict(zip(data['predicted_x'], data['predicted_y']))

    for period in all_periods:
        actual_value = hist_dict.get(period, '-')
        forecast_value = pred_dict.get(period, '-')
        
        # Conditionally format only if the value is a number
        actual = f"{actual_value:.2f}" if isinstance(actual_value, (int, float)) else '-'
        forecast = f"{forecast_value:.2f}" if isinstance(forecast_value, (int, float)) else '-'
        
        table_data.append([period, actual, forecast])
        
    report_table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    report_table.setStyle(style)
    story.append(report_table)

    # 5. Build the PDF
    doc.build(story)
    print(f"Report successfully generated at: {output_path}")