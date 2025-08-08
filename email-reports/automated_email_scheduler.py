# automated_email_scheduler.py
"""
Automated Email Report Scheduler for Foresight IQ
Runs in the background and sends weekly reports automatically
"""

import schedule
import time
import threading
import logging
from datetime import datetime
from weekly_email_report import WeeklyReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

class EmailScheduler:
    """Automated email report scheduler"""
    
    def __init__(self):
        self.generator = WeeklyReportGenerator()
        self.is_running = False
        
        # Default recipients - update these!
        self.recipients = [
            'manager@yourcafe.com',
            'owner@yourcafe.com',
            'analytics@elementalinsights.com'
        ]
    
    def send_weekly_report(self):
        """Function called by scheduler to send weekly report"""
        try:
            logging.info("🔄 Starting scheduled weekly report generation...")
            
            success = self.generator.generate_and_send_weekly_report(
                recipients=self.recipients,
                test_mode=False
            )
            
            if success:
                logging.info("✅ Weekly report sent successfully!")
                print(f"✅ Weekly report sent to {len(self.recipients)} recipients at {datetime.now().strftime('%I:%M %p')}")
            else:
                logging.error("❌ Failed to send weekly report")
                print("❌ Failed to send weekly report - check logs")
                
        except Exception as e:
            logging.error(f"❌ Error in scheduled report: {str(e)}")
            print(f"❌ Scheduler error: {str(e)}")
    
    def send_test_report(self):
        """Send a test report immediately"""
        try:
            print("🧪 Sending test report...")
            
            test_recipients = [
                input("Enter test email address: ").strip()
            ]
            
            success = self.generator.generate_and_send_weekly_report(
                recipients=test_recipients,
                test_mode=True
            )
            
            if success:
                print("✅ Test report sent successfully!")
            else:
                print("❌ Test report failed")
                
        except Exception as e:
            print(f"❌ Test error: {str(e)}")
    
    def setup_schedule(self):
        """Configure the email schedule"""
        
        print("📅 Email Schedule Configuration")
        print("=" * 40)
        print("Current options:")
        print("1. Weekly (Monday 9:00 AM)")
        print("2. Bi-weekly (Every other Monday 9:00 AM)")
        print("3. Custom schedule")
        print("4. Test mode (every 2 minutes)")
        
        choice = input("Choose schedule (1-4): ").strip()
        
        if choice == "1":
            # Weekly on Monday at 9 AM
            schedule.every().monday.at("09:00").do(self.send_weekly_report)
            print("✅ Scheduled: Weekly reports every Monday at 9:00 AM")
            
        elif choice == "2":
            # Bi-weekly (every other Monday)
            schedule.every(2).weeks.do(self.send_weekly_report)
            print("✅ Scheduled: Bi-weekly reports every other Monday")
            
        elif choice == "3":
            # Custom schedule
            print("\nCustom Schedule Options:")
            print("Examples:")
            print("- 'monday' at '09:00' (weekly)")
            print("- 'friday' at '17:00' (weekly)")
            print("- Every 7 days")
            
            day = input("Enter day (monday/tuesday/etc) or 'days': ").strip().lower()
            
            if day == "days":
                interval = int(input("Enter number of days: "))
                schedule.every(interval).days.at("09:00").do(self.send_weekly_report)
                print(f"✅ Scheduled: Every {interval} days at 9:00 AM")
            else:
                time_str = input("Enter time (HH:MM format, e.g., 09:00): ").strip()
                getattr(schedule.every(), day).at(time_str).do(self.send_weekly_report)
                print(f"✅ Scheduled: Every {day} at {time_str}")
                
        elif choice == "4":
            # Test mode - every 2 minutes
            schedule.every(2).minutes.do(self.send_weekly_report)
            print("🧪 Test mode: Sending reports every 2 minutes")
            print("⚠️  Remember to stop this after testing!")
        
        else:
            # Default to weekly
            schedule.every().monday.at("09:00").do(self.send_weekly_report)
            print("✅ Default: Weekly reports every Monday at 9:00 AM")
    
    def update_recipients(self):
        """Update email recipients"""
        
        print("\n📧 Update Email Recipients")
        print("Current recipients:")
        for i, email in enumerate(self.recipients, 1):
            print(f"{i}. {email}")
        
        print("\nOptions:")
        print("1. Add new recipient")
        print("2. Remove recipient")
        print("3. Replace all recipients")
        print("4. Keep current list")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == "1":
            new_email = input("Enter new email address: ").strip()
            if new_email and "@" in new_email:
                self.recipients.append(new_email)
                print(f"✅ Added {new_email}")
            else:
                print("❌ Invalid email address")
                
        elif choice == "2":
            try:
                index = int(input("Enter number to remove: ")) - 1
                removed = self.recipients.pop(index)
                print(f"✅ Removed {removed}")
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                
        elif choice == "3":
            emails_input = input("Enter all email addresses (comma-separated): ")
            new_recipients = [email.strip() for email in emails_input.split(',')]
            self.recipients = [email for email in new_recipients if email and "@" in email]
            print(f"✅ Updated to {len(self.recipients)} recipients")
        
        print(f"\nFinal recipient list: {', '.join(self.recipients)}")
    
    def run_scheduler(self):
        """Start the background scheduler"""
        
        self.is_running = True
        
        print("\n🚀 Email Report Scheduler Started!")
        print("=" * 40)
        print(f"📅 Next scheduled report: {schedule.next_run()}")
        print(f"📧 Recipients: {', '.join(self.recipients)}")
        print("💡 Keep this window open for automatic reports")
        print("🛑 Press Ctrl+C to stop the scheduler")
        print("-" * 40)
        
        # Log scheduler start
        logging.info("Email scheduler started successfully")
        logging.info(f"Recipients: {', '.join(self.recipients)}")
        logging.info(f"Next run: {schedule.next_run()}")
        
        # Run scheduler loop
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n🛑 Scheduler stopped by user")
            logging.info("Scheduler stopped by user")
            self.is_running = False
    
    def show_status(self):
        """Show current scheduler status"""
        
        print("\n📊 Scheduler Status")
        print("=" * 30)
        print(f"Running: {'Yes' if self.is_running else 'No'}")
        print(f"Recipients: {len(self.recipients)}")
        print(f"Next run: {schedule.next_run() if schedule.jobs else 'Not scheduled'}")
        
        if schedule.jobs:
            print("\nScheduled jobs:")
            for job in schedule.jobs:
                print(f"- {job}")
        
        print(f"\nRecipient list:")
        for email in self.recipients:
            print(f"- {email}")


def main():
    """Main function with interactive menu"""
    
    print("📧 Foresight IQ - Automated Email Report Scheduler")
    print("=" * 55)
    print("Automate weekly café performance reports via email")
    print()
    
    scheduler = EmailScheduler()
    
    while True:
        print("\n🔧 Main Menu")
        print("1. 📧 Send test report now")
        print("2. 📅 Configure schedule")
        print("3. 👥 Update recipients")
        print("4. 🚀 Start scheduler")
        print("5. 📊 Show status")
        print("6. 🔍 View logs")
        print("7. ❌ Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            scheduler.send_test_report()
            
        elif choice == "2":
            scheduler.setup_schedule()
            
        elif choice == "3":
            scheduler.update_recipients()
            
        elif choice == "4":
            if not schedule.jobs:
                print("⚠️  No schedule configured. Setting up default schedule...")
                scheduler.setup_schedule()
            
            # Ask for confirmation
            print(f"\n📅 About to start scheduler with:")
            print(f"Schedule: {schedule.next_run()}")
            print(f"Recipients: {', '.join(scheduler.recipients)}")
            
            confirm = input("\nStart scheduler? (y/n): ").lower() == 'y'
            
            if confirm:
                # Run in background thread
                scheduler_thread = threading.Thread(target=scheduler.run_scheduler, daemon=True)
                scheduler_thread.start()
                
                print("✅ Scheduler started in background")
                print("💡 You can continue using this menu while scheduler runs")
            else:
                print("❌ Scheduler not started")
                
        elif choice == "5":
            scheduler.show_status()
            
        elif choice == "6":
            try:
                print("\n📋 Recent Log Entries:")
                with open('scheduler.log', 'r') as f:
                    lines = f.readlines()
                    # Show last 10 lines
                    for line in lines[-10:]:
                        print(line.strip())
            except FileNotFoundError:
                print("No log file found yet")
                
        elif choice == "7":
            if scheduler.is_running:
                scheduler.is_running = False
                print("🛑 Stopping scheduler...")
                time.sleep(2)
            
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    # Install required package if not installed
    try:
        import schedule
    except ImportError:
        print("📦 Installing required package 'schedule'...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'schedule'])
        import schedule
        print("✅ Package installed successfully!")
    
    main()