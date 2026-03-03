"""
PDF Report Generator for academic reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from datetime import datetime
import os

class PDFReportGenerator:
    """Generate comprehensive PDF reports for students"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
    
    @staticmethod
    def _draw_header(canvas, doc, student_name, roll_number):
        """Draw header on each page"""
        canvas.saveState()
        
        # Header rectangle
        canvas.setFillColor(colors.HexColor('#667eea'))
        canvas.rect(0, letter[1] - 60, letter[0], 60, fill=True, stroke=False)
        
        # Header text
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 18)
        canvas.drawString(inch, letter[1] - 30, "Academic Intelligence Platform")
        canvas.setFont('Helvetica', 10)
        canvas.drawRightString(letter[0] - inch, letter[1] - 30, f"{student_name} - {roll_number}")
        
        # Footer
        canvas.setFillColor(colors.grey)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(inch, 0.5 * inch, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
        canvas.drawRightString(letter[0] - inch, 0.5 * inch, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def generate_performance_report(self, student_data: dict, performance_data: list, 
                                   predictions: dict, output_path: str):
        """Generate comprehensive performance report"""
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=inch, leftMargin=inch,
                               topMargin=1.5*inch, bottomMargin=inch)
        
        story = []
        
        # Title
        title = Paragraph(f"Academic Performance Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Student Information
        story.append(Paragraph("Student Information", self.styles['SectionHeader']))
        
        student_info = [
            ['Name', f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}"],
            ['Roll Number', student_data.get('roll_number', 'N/A')],
            ['Department', student_data.get('department', 'N/A')],
            ['Semester', str(student_data.get('semester', 'N/A'))],
            ['Current CGPA', f"{student_data.get('current_cgpa', 0):.2f}"],
            ['Batch', student_data.get('batch', 'N/A')]
        ]
        
        student_table = Table(student_info, colWidths=[2.5*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(student_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Performance Summary
        story.append(Paragraph("Performance Summary", self.styles['SectionHeader']))
        
        if performance_data:
            perf_data = [['Subject', 'Internal', 'External', 'Total', 'Grade', 'Attendance']]
            for perf in performance_data[:10]:  # Show last 10 subjects
                perf_data.append([
                    perf.get('subject_name', 'N/A'),
                    str(perf.get('internal_marks', 0)),
                    str(perf.get('external_marks', 0)),
                    str(perf.get('total_marks', 0)),
                    perf.get('grade', 'N/A'),
                    f"{perf.get('attendance_percentage', 0)}%"
                ])
            
            performance_table = Table(perf_data, colWidths=[2*inch, inch, inch, inch, inch, inch])
            performance_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ]))
            story.append(performance_table)
        else:
            story.append(Paragraph("No performance data available", self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Predictions Section
        if predictions:
            story.append(Paragraph("AI Predictions & Analysis", self.styles['SectionHeader']))
            
            pred_data = []
            
            if 'gpa_prediction' in predictions:
                gpa_pred = predictions['gpa_prediction']
                pred_data.append(['Predicted Next Semester GPA', 
                                f"{gpa_pred.get('predicted_gpa', 0):.2f}"])
                pred_data.append(['Confidence', 
                                f"{gpa_pred.get('confidence', 0):.1f}%"])
            
            if 'risk_score' in predictions:
                risk = predictions['risk_score']
                pred_data.append(['Risk Score', 
                                f"{risk.get('risk_score', 0):.1f}/100"])
                pred_data.append(['Risk Level', 
                                risk.get('risk_level', 'N/A')])
            
            if 'scholarship' in predictions:
                scholar = predictions['scholarship']
                pred_data.append(['Scholarship Eligibility', 
                                'Eligible' if scholar.get('eligible', False) else 'Not Eligible'])
                pred_data.append(['Scholarship Probability', 
                                f"{scholar.get('probability', 0):.1f}%"])
            
            if pred_data:
                pred_table = Table(pred_data, colWidths=[3.5*inch, 3*inch])
                pred_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#11998e')),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                    ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#e8f8f5')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('PADDING', (0, 0), (-1, -1), 12),
                ]))
                story.append(pred_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        recommendations = predictions.get('gpa_prediction', {}).get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations[:5], 1):
                story.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("Keep up the good work! Continue your current study patterns.", 
                                  self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Strengths and Areas of Improvement
        story.append(Paragraph("Analysis", self.styles['SectionHeader']))
        
        analysis_text = f"""
        Based on your academic performance:
        <br/><br/>
        <b>Current Status:</b> Your CGPA of {student_data.get('current_cgpa', 0):.2f} places 
        you in the {'excellent' if student_data.get('current_cgpa', 0) >= 8.5 else 'good' if student_data.get('current_cgpa', 0) >= 7 else 'average'} 
        category. {'Keep maintaining this performance!' if student_data.get('current_cgpa', 0) >= 7 else 'Focus on improving your grades.'}
        <br/><br/>
        <b>Next Steps:</b> Review your weak subjects, attend extra classes if needed, and maintain 
        good attendance to improve your overall performance.
        """
        
        story.append(Paragraph(analysis_text, self.styles['Normal']))
        
        # Build PDF with header
        doc.build(story, onFirstPage=lambda c, d: self._draw_header(c, d, 
                                                                     f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}", 
                                                                     student_data.get('roll_number', '')),
                  onLaterPages=lambda c, d: self._draw_header(c, d, 
                                                               f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}", 
                                                               student_data.get('roll_number', '')))
        
        return output_path

pdf_generator = PDFReportGenerator()
