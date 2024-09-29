import os
import smtplib
import ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyfiglet

# Function to display header using pyfiglet
def display_header():
    header = pyfiglet.figlet_format("Bilkent Traffic", font="slant")
    print(header)

# Function to send the email
def send_email(sender_email, receiver_email, password, subject, message):
    smtp_server = "asmtp.bilkent.edu.tr"
    port = 465  # Use 465 for SSL/TLS

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to load the template from a text file
def load_template(template_file, data):
    try:
        # Get current directory
        current_directory = os.getcwd()
        template_path = os.path.join(current_directory, template_file)
        
        with open(template_path, 'r') as file:
            template = file.read()
            return template.format(**data)
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

# Function to extract name and surname from email
def extract_name_surname(email):
    try:
        local_part = email.split('@')[0]  # Extract the part before @
        name, surname = local_part.split('.')  # Split by dot to get name and surname
        return name.capitalize(), surname.capitalize()  # Capitalize for proper names
    except ValueError:
        # Fallback if email format is not as expected
        return "User", "Unknown"

def main():
    # Display pyfiglet header
    display_header()

    sender_email = input("Enter your Bilkent email address: ")
    password = getpass.getpass(prompt="Enter your email password: ")
    subject = input("Enter the email subject: ")

    # Extract the user's first name and surname from email
    name, surname = extract_name_surname(sender_email)

    # Language Selection
    language_choice = input("Choose language (EN/TR): ").strip().lower()
    if language_choice not in ["en", "tr"]:
        print("Invalid language choice. Please choose EN or TR.")
        return

    template_choice = input("Choose template (default/custom): ").strip().lower()

    if template_choice == "default":
        car_model = input("Enter car model: ")
        car_color = input("Enter car color: ")
        location = input("Enter location: ")
        reason = input("Enter the reason for the report: ")
        incident_time = input("Enter the time when the incident occurred (e.g., 14:30): ")

        data = {
            "car_model": car_model,
            "car_color": car_color,
            "location": location,
            "reason": reason,
            "incident_time": incident_time,
            "name": name,
            "surname": surname
        }

        # Load default template based on language selection
        if language_choice == "en":
            message = load_template("./assets/default_template_en.txt", data)
        elif language_choice == "tr":
            message = load_template("./assets/default_template_tr.txt", data)

    elif template_choice == "custom":
        template_file = input("Enter the path to your custom template file: ")
        print("Loading custom template...")
        message = load_template(template_file, {"name": name, "surname": surname})
    else:
        print("Invalid template choice.")
        return

    if message is None:
        print("Failed to load the template. Exiting.")
        return

    receiver_email = "onurcan.genc@ug.bilkent.edu.tr"
    send_email(sender_email, receiver_email, password, subject, message)

if __name__ == "__main__":
    main()
