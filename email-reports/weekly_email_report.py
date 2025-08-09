# weekly_email_report.py
"""
Foresight IQ Weekly Café Performance Report Generator
Generates and sends professional email reports via Zoho Mail
Part of Elemental Insights Analytics Suite
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from datetime import datetime, timedelta
import logging
import os

# Configure logging
logging.basicConfig(
    filename='email_reports.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WeeklyReportGenerator:
    """Generate and send weekly café performance reports"""
    
    def __init__(self, email_config=None):
        """Initialize with email configuration"""
        self.email_config = email_config or self.load_email_config()
        
    def load_email_config(self):  # ← This line must be indented exactly like __init__
        """Load email configuration from environment variables or config file"""
        
        # Option 1: Use environment variables (recommended for security)
        config = {
            'smtp_server': os.getenv('ZOHO_SMTP_SERVER', 'smtp.zoho.eu'),
            'smtp_port': int(os.getenv('ZOHO_SMTP_PORT', '587')),
            'email': os.getenv('ZOHO_EMAIL'),
            'password': os.getenv('ZOHO_PASSWORD'),
            'sender_name': os.getenv('SENDER_NAME', 'Foresight IQ Analytics')
        }
        
        # Option 2: Load from config file (less secure, but easier for testing)
        if not config['email']:
            try:
                with open('email_config.json', 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except FileNotFoundError:
                logging.warning("No email config found. Create email_config.json or set environment variables.")
        
        return config
    
    def get_weekly_data(self, week_start=None):
        """Generate or fetch weekly performance data"""
        
        if week_start is None:
            week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            # Get Monday of current week
            days_since_monday = week_start.weekday()
            week_start = week_start - timedelta(days=days_since_monday)
        
        week_end = week_start + timedelta(days=6)
        
        # In real implementation, this would fetch from your data source
        # For demo, we'll generate realistic sample data
        import random
        
        base_daily_revenue = 1000
        weekly_data = {
            'week_start': week_start.strftime('%d %b'),
            'week_end': week_end.strftime('%d %b %Y'),
            'expected_weekly_revenue': 7350.00,
            'last_week_revenue': 7120.40,
            'forecast_accuracy': 96.9,
            'weather_summary': 'Mild week ahead with light showers midweek',
            'peak_hour': '13:00–14:00',
            'product_mix': {
                'hot_drinks': 48.2,
                'cold_drinks': 28.3,
                'food': 23.5
            },
            'top_items': ['Flat White', 'Iced Latte', 'Ham & Cheese Toastie'],
            'avg_items_per_transaction': 2.1,
            'daily_forecasts': []
        }
        
        # Generate daily forecasts
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weather_conditions = ['Sunny', 'Cloudy', 'Light Showers', 'Rain', 'Sunny', 'Partly Cloudy', 'Overcast']
        peak_hours = ['12:00–13:00', '13:00–14:00', '12:00–13:00', '13:00–14:00', '12:00–13:00', '13:00–14:00', '12:00–13:00']
        
        for i, day in enumerate(days):
            date = week_start + timedelta(days=i)
            daily_revenue = base_daily_revenue + (i * 30) + random.randint(-50, 50)
            
            weekly_data['daily_forecasts'].append({
                'day': day,
                'date': date.strftime('%d %b'),
                'revenue': daily_revenue,
                'weather': weather_conditions[i],
                'peak_hour': peak_hours[i]
            })
        
        return weekly_data
    
    def generate_text_table(self, daily_forecasts):
        """Generate ASCII table for daily forecasts"""
        
        # Table header
        table = "+-------------------+-------------------------+--------------------+----------------+\n"
        table += "| Date              | Forecasted Revenue (£)  | Expected Weather   | Peak Hour      |\n"
        table += "+-------------------+-------------------------+--------------------+----------------+\n"
        
        # Table rows
        for forecast in daily_forecasts:
            date_str = f"{forecast['day']}, {forecast['date']}"
            revenue_str = f"{forecast['revenue']:,}"
            weather_str = forecast['weather']
            peak_str = forecast['peak_hour']
            
            table += f"| {date_str:<17} | {revenue_str:<23} | {weather_str:<18} | {peak_str:<14} |\n"
        
        table += "+-------------------+-------------------------+--------------------+----------------+"
        
        return table
    
    def generate_html_email(self, data):
        """Generate HTML version of the email"""
        
        # Generate daily forecast table (HTML version)
        forecast_rows = ""
        for forecast in data['daily_forecasts']:
            forecast_rows += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{forecast['day']}, {forecast['date']}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">£{forecast['revenue']:,}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{forecast['weather']}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{forecast['peak_hour']}</td>
            </tr>"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 5px; min-width: 120px; text-align: center; }}
                .metric-value {{ font-size: 1.5em; font-weight: bold; color: #2c3e50; }}
                .metric-label {{ font-size: 0.9em; color: #7f8c8d; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background: #3498db; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 8px; border: 1px solid #ddd; }}
                tr:nth-child(even) {{ background: #f2f2f2; }}
                .recommendations {{ background: #e8f5e8; border-left: 4px solid #27ae60; padding: 15px; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #34495e; color: white; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                
                <!-- Header -->
                <div class="header">
                    <h1>📬 Weekly Café Performance Report</h1>
                    <p><strong>Foresight IQ Analytics</strong></p>
                    <p>Week: {data['week_start']} – {data['week_end']}</p>
                </div>
                
                <!-- Forecast Summary -->
                <div class="section">
                    <h2>🔮 Forecast Summary</h2>
                    <div class="metric">
                        <div class="metric-value">£{data['expected_weekly_revenue']:,.2f}</div>
                        <div class="metric-label">Expected Weekly Revenue</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data['forecast_accuracy']:.1f}%</div>
                        <div class="metric-label">Historic Forecast Accuracy</div>
                    </div>
                    <p><strong>Predicted Weather:</strong> {data['weather_summary']}</p>
                </div>
                
                <!-- Actual Performance -->
                <div class="section">
                    <h2>📈 Actual Performance</h2>
                    <div class="metric">
                        <div class="metric-value">£{data['last_week_revenue']:,.2f}</div>
                        <div class="metric-label">Last Week's Revenue</div>
                    </div>
                    <p><strong>Peak Sales Hour:</strong> {data['peak_hour']}</p>
                </div>
                
                <!-- Product Mix -->
                <div class="section">
                    <h2>🍽️ Product Mix</h2>
                    <div class="metric">
                        <div class="metric-value">{data['product_mix']['hot_drinks']:.1f}%</div>
                        <div class="metric-label">Hot Drinks</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data['product_mix']['cold_drinks']:.1f}%</div>
                        <div class="metric-label">Cold Drinks</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data['product_mix']['food']:.1f}%</div>
                        <div class="metric-label">Food</div>
                    </div>
                    
                    <h3>🔥 Top-Selling Items:</h3>
                    <ul>
                        {' '.join([f'<li>{item}</li>' for item in data['top_items']])}
                    </ul>
                </div>
                
                <!-- Daily Forecast Table -->
                <div class="section">
                    <h2>📅 Daily Forecast</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Forecasted Revenue (£)</th>
                                <th>Expected Weather</th>
                                <th>Peak Hour</th>
                            </tr>
                        </thead>
                        <tbody>
                            {forecast_rows}
                        </tbody>
                    </table>
                </div>
                
                <!-- Recommendations -->
                <div class="recommendations">
                    <h2>💡 Recommendations</h2>
                    <ul>
                        <li>☕ <strong>Stock up on high-demand hot drinks</strong> — Flat Whites and Cappuccinos are popular.</li>
                        <li>🥗 <strong>Offer lunchtime meal deals</strong> targeting the 12–2 PM window.</li>
                        <li>🌧️ <strong>Wednesday and Thursday may see lower footfall</strong> — consider indoor promotions.</li>
                        <li>📊 <strong>Encourage multiple-item purchases</strong> — average per transaction is {data['avg_items_per_transaction']} items.</li>
                    </ul>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <p><strong>Powered by Elemental Insights Analytics</strong></p>
                    <p>Automated report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>For questions, contact: <a href="mailto:analytics@elementalinsights.com" style="color: #3498db;">analytics@elementalinsights.com</a></p>
                </div>
                
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_text_email(self, data):
        """Generate plain text version of the email"""
        
        forecast_table = self.generate_text_table(data['daily_forecasts'])
        top_items_text = '\n'.join([f"- {item}" for item in data['top_items']])
        
        text_content = f"""
📬 Weekly Café Performance Report
Week: {data['week_start']} – {data['week_end']}

🔮 Forecast Summary
- Expected Weekly Revenue: £{data['expected_weekly_revenue']:,.2f}
- Historic Forecast Accuracy: {data['forecast_accuracy']:.1f}%
- Predicted Weather: {data['weather_summary']}

📈 Actual Performance
- Last Week's Revenue: £{data['last_week_revenue']:,.2f}
- Peak Sales Hour: {data['peak_hour']}

🍽️ Product Mix
- Hot Drinks: {data['product_mix']['hot_drinks']:.1f}%
- Cold Drinks: {data['product_mix']['cold_drinks']:.1f}%
- Food: {data['product_mix']['food']:.1f}%

🔥 Top-Selling Items:
{top_items_text}

{forecast_table}

💡 Recommendations:
- ☕ Stock up on high-demand hot drinks — Flat Whites and Cappuccinos are popular.
- 🥗 Offer lunchtime meal deals targeting the 12–2 PM window.
- 🌧️ Wednesday and Thursday may see lower footfall — consider indoor promotions.
- 📊 Encourage multiple-item purchases — average per transaction is {data['avg_items_per_transaction']} items.

---
Powered by Elemental Insights Analytics
Automated report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
For questions, contact: analytics@elementalinsights.com
        """
        
        return text_content.strip()
    
    def send_email(self, recipients, subject, data, include_html=True):
        """Send the weekly report email via Zoho"""
        
        if not self.email_config['email'] or not self.email_config['password']:
            logging.error("Email configuration missing. Cannot send email.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['email']}>"
            msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
            msg['Subject'] = subject
            
            # Generate email content
            text_content = self.generate_text_email(data)
            html_content = self.generate_html_email(data) if include_html else None
            
            # Attach plain text version
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
            
            # Attach HTML version
            if html_content:
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
            
            # Connect to Zoho SMTP server
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.email_config['email'], self.email_config['password'])
                
                # Send email
                server.send_message(msg)
                
            logging.info(f"Email sent successfully to {recipients}")
            print(f"✅ Weekly report sent successfully to {recipients}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def generate_and_send_weekly_report(self, recipients, test_mode=False):
        """Main function to generate and send weekly report"""
        
        print("🔄 Generating weekly café performance report...")
        
        # Get weekly data
        data = self.get_weekly_data()
        
        # Generate subject line
        subject = f"📊 Foresight IQ Weekly Report - Week {data['week_start']} to {data['week_end']}"
        
        if test_mode:
            subject = f"[TEST] {subject}"
            print("🧪 Running in test mode")
        
        # Send email
        success = self.send_email(recipients, subject, data)
        
        if success:
            # Save report locally for records
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save as HTML
            html_content = self.generate_html_email(data)
            with open(f'weekly_report_{timestamp}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Save as text
            text_content = self.generate_text_email(data)
            with open(f'weekly_report_{timestamp}.txt', 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            # Save data as JSON
            with open(f'weekly_data_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"📁 Report files saved locally with timestamp {timestamp}")
        
        return success


def main():
    """Main function for running the weekly report generator"""
    
    print("📊 Foresight IQ Weekly Report Generator")
    print("=" * 50)
    
    # Initialize report generator
    generator = WeeklyReportGenerator()
    
    # Example recipients (update these)
    test_recipients = [
        'manager@cafename.com',
        'owner@cafename.com'
    ]
    
    # Ask user for input
    print("Email recipients (comma-separated):")
    recipients_input = input(f"Press Enter for default ({', '.join(test_recipients)}): ").strip()
    
    if recipients_input:
        recipients = [email.strip() for email in recipients_input.split(',')]
    else:
        recipients = test_recipients
    
    # Ask if this is a test
    test_mode = input("Send as test email? (y/n): ").lower() == 'y'
    
    # Generate and send report
    success = generator.generate_and_send_weekly_report(recipients, test_mode)
    
    if success:
        print("\n🎉 Weekly report process completed successfully!")
    else:
        print("\n❌ Weekly report process failed. Check email_reports.log for details.")


if __name__ == "__main__":
    main()
