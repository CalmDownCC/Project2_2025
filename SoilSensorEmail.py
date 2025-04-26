import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Email configuration
from_email_addr = "1169806185@qq.com"
from_email_pass = "scrmwkpywgleiigf"
to_email_addr = "3851752811@qq.com"

# GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# Time settings (using 24-hour format)
start_hour = 8 # First check at 8:00 AM
check_interval = 4 # Check every 4 hours
last_checked_hour = start_hour - check_interval # Initialize to ensure first check

def send_email(water_status):
    """Send email notification"""
    msg = EmailMessage()
    body = f"Plant status update at {datetime.now().strftime('%H:%M')}:\n{water_status}"
    msg.set_content(body)

    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = f'Plant Watering Alert: {water_status.split(" ")[0]}'

    try:
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()
        server.login(from_email_addr, from_email_pass)
        server.send_message(msg)
        print ('Email sent successfully')
        server.quit()
    except Exception as e:
        print (f"Failed to send email: {e}")

def check_soil_moisture():
    """Check soil moisture level"""
    moisture = GPIO.input(channel)
    return "Please water your plant" if moisture else "Water NOT needed"

print ("Plant monitoring system started...")
print (f"Initial check at {start_hour}:00, then every {check_interval} hours")

try:
    while True:
        # Get current time (adjusted for timezone if needed)
        current_time = time.localtime()
        current_hour = current_time.tm_hour # Use +8 here if you need timezone adjustment

        # Check if it's time for a new reading
        time_diff = current_hour - last_checked_hour
        if time_diff >= check_interval or (current_hour < last_checked_hour and (24 - last_checked_hour + current_hour) >= check_interval):
            status = check_soil_moisture()
            print (f"{current_hour:02d}:00 - {status}")
            send_email(status)
            last_checked_hour = current_hour
        else:
            # Optional: print waiting status
            if current_time.tm_min == 0: # Only print on the hour to reduce clutter
                print (f"{current_hour:02d}:00 - Next check in {check_interval - time_diff} hours")

        # Check every minute (adjust as needed)
        time.sleep(60)

except KeyboardInterrupt:
    print ("\nMonitoring stopped by user")
finally:
    GPIO.cleanup()
    print ("GPIO resources cleaned up")
