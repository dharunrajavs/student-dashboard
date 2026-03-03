"""
Email notification service for alerts and reports
"""
from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
from typing import List

class EmailService:
    """Email notification service"""
    
    @staticmethod
    def send_email(recipients: List[str], subject: str, body: str, html: str = None):
        """Send email to recipients"""
        try:
            msg = Message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=recipients
            )
            msg.body = body
            if html:
                msg.html = html
            
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_alert_email(user_email: str, alert_title: str, alert_message: str):
        """Send alert notification email"""
        subject = f"Academic Alert: {alert_title}"
        
        body = f"""
Dear Student,

You have a new academic alert:

{alert_title}

{alert_message}

Please log in to your Academic AI platform to view more details.

Best regards,
Academic Intelligence Platform
        """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
        .alert-box {{ background: #fff; padding: 20px; margin: 20px 0; 
                      border-left: 4px solid #ff6b6b; border-radius: 4px; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        .button {{ display: inline-block; padding: 12px 24px; background: #667eea; 
                   color: white; text-decoration: none; border-radius: 6px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔔 Academic Alert</h1>
        </div>
        <div class="content">
            <p>Dear Student,</p>
            <p>You have received a new academic alert:</p>
            
            <div class="alert-box">
                <h2 style="margin-top: 0; color: #ff6b6b;">{alert_title}</h2>
                <p>{alert_message}</p>
            </div>
            
            <p>We recommend immediate action to address this concern.</p>
            
            <center>
                <a href="http://localhost:3000/dashboard" class="button">View Dashboard</a>
            </center>
            
            <div class="footer">
                <p>This is an automated message from Academic Intelligence Platform</p>
                <p>Please do not reply to this email</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService.send_email([user_email], subject, body, html)
    
    @staticmethod
    def send_scholarship_notification(user_email: str, student_name: str, eligibility: bool, criteria: dict):
        """Send scholarship eligibility notification"""
        subject = "Scholarship Eligibility Update"
        
        status = "ELIGIBLE" if eligibility else "NOT ELIGIBLE"
        
        body = f"""
Dear {student_name},

Your scholarship application has been evaluated.

Status: {status}

Please log in to view detailed eligibility criteria and recommendations.

Best regards,
Academic Intelligence Platform
        """
        
        criteria_html = ""
        for key, value in criteria.items():
            icon = "✅" if value else "❌"
            criteria_html += f"<li>{icon} {key.replace('_', ' ').title()}</li>"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
        .status-badge {{ display: inline-block; padding: 10px 20px; 
                        background: {'#38ef7d;' if eligibility else '#ff6b6b;'} 
                        color: white; border-radius: 6px; font-weight: bold; }}
        .criteria {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 8px 0; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Scholarship Evaluation</h1>
        </div>
        <div class="content">
            <p>Dear {student_name},</p>
            <p>Your scholarship application has been evaluated:</p>
            
            <center>
                <div class="status-badge">{status}</div>
            </center>
            
            <div class="criteria">
                <h3>Eligibility Criteria:</h3>
                <ul>
                    {criteria_html}
                </ul>
            </div>
            
            <p>For detailed information and next steps, please log in to your dashboard.</p>
            
            <div class="footer">
                <p>Academic Intelligence Platform - Scholarship Management</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService.send_email([user_email], subject, body, html)
    
    @staticmethod
    def send_performance_report(user_email: str, student_name: str, report_file_path: str):
        """Send performance report email with PDF attachment"""
        subject = "Your Academic Performance Report"
        
        body = f"""
Dear {student_name},

Your academic performance report for the current semester is ready.

Please find the detailed report attached.

Keep up the good work!

Best regards,
Academic Intelligence Platform
        """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
        .attachment {{ background: white; padding: 15px; margin: 20px 0; 
                      border-radius: 8px; border: 2px dashed #667eea; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Performance Report</h1>
        </div>
        <div class="content">
            <p>Dear {student_name},</p>
            <p>Your comprehensive academic performance report is ready!</p>
            
            <div class="attachment">
                <h3>📎 Report Attached</h3>
                <p>academic_report.pdf</p>
            </div>
            
            <p>This report includes:</p>
            <ul>
                <li>Overall academic performance</li>
                <li>Subject-wise analysis</li>
                <li>Attendance records</li>
                <li>Risk assessment</li>
                <li>Improvement recommendations</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """
        
        try:
            msg = Message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user_email]
            )
            msg.body = body
            msg.html = html
            
            with current_app.open_resource(report_file_path) as fp:
                msg.attach("academic_report.pdf", "application/pdf", fp.read())
            
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send report email: {str(e)}")
            return False

email_service = EmailService()
