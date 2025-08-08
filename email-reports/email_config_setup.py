# email_config_setup.py
"""
Easy setup script for Foresight IQ email reporting
"""

import json
import os
import getpass

def setup_email_config():
    """Interactive setup for email configuration"""
    
    print("🔧 Foresight IQ Email Report Setup")
    print("=" * 40)
    print("This will help you configure automated email reports.")
    print()
    
    print("📧 Zoho Mail Configuration")
    print("You'll need:")
    print("1. A Zoho Mail account")
    print("2. An 'App Password' (not your regular password)")
    print("3. SMTP access enabled")
    print()
    
    # Get email configuration
    email = input("Enter your Zoho email address: ").strip()
    
    print("\n🔐 App Password Setup:")
    print("1. Log into Zoho Mail")
    print("2. Go to Settings > Security")
    print("3. Enable 'App Passwords'")
    print("4. Generate a new app password for 'Email Client'")
    print("5. Copy the generated password")
    print()
    
    password = getpass.getpass("Enter your Zoho app password: ").strip()
    sender_name = input("Enter sender name (default: Foresight IQ Analytics): ").strip()
    
    if not sender_name:
        sender_name = "Foresight IQ Analytics"
    
    # Create configuration
    config = {
        "smtp_server": "smtp.zoho.com",
        "smtp_port": 587,
        "email": email,
        "password": password,
        "sender_name": sender_name
    }
    
    # Save configuration
    config_method = input("\nSave configuration as:\n1. JSON file (easier)\n2. Environment variables (more secure)\nChoose (1/2): ").strip()
    
    if config_method == "2":
        # Create .env file
        env_content = f"""# Zoho Email Configuration for Foresight IQ
ZOHO_EMAIL={email}
ZOHO_PASSWORD={password}
ZOHO_SMTP_SERVER=smtp.zoho.com
ZOHO_SMTP_PORT=587
SENDER_NAME={sender_name}
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Configuration saved to .env file")
        print("⚠️  Make sure to add '.env' to your .gitignore file!")
        
    else:
        # Create JSON file
        with open('email_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration saved to email_config.json")
        print("⚠️  Make sure to add 'email_config.json' to your .gitignore file!")
    
    # Update .gitignore
    gitignore_additions = """
# Email configuration files (sensitive)
email_config.json
.env
email_reports.log
weekly_report_*.html
weekly_report_*.txt
weekly_data_*.json
"""
    
    try:
        with open('../.gitignore', 'a') as f:
            f.write(gitignore_additions)
        print("✅ Updated .gitignore file")
    except:
        print("⚠️  Manually add these lines to your .gitignore:")
        print(gitignore_additions)
    
    print("\n🧪 Test Configuration")
    test = input("Would you like to send a test email? (y/n): ").lower() == 'y'
    
    if test:
        test_recipient = input("Enter test email address: ").strip()
        
        try:
            from weekly_email_report import WeeklyReportGenerator
            
            generator = WeeklyReportGenerator(config)
            success = generator.generate_and_send_weekly_report([test_recipient], test_mode=True)
            
            if success:
                print("🎉 Test email sent successfully!")
            else:
                print("❌ Test email failed. Check your configuration.")
                
        except Exception as e:
            print(f"❌ Error sending test email: {e}")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run 'python weekly_email_report.py' to send reports manually")
    print("2. Run 'python automated_email_scheduler.py' for automation")
    print("3. Add this to your GitHub repo (without the config files)")

if __name__ == "__main__":
    setup_email_config()