import smtplib
import ssl
import getpass
import openpyxl

def read_recipients_from_excel(file_path):
    """
    Read recipient email addresses from an Excel file.
    """
    recipients = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        for row in sheet.iter_rows(values_only=True):
            for cell in row:
                if isinstance(cell, str) and '@' in cell:
                    recipients.append(cell)
        workbook.close()
    except Exception as e:
        print(f"Error reading recipients from Excel file: {e}")
    return recipients

def send_emails(sender_email, sender_password, subject, body, recipients):
    """
    Send emails to recipients.
    """
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            for recipient in recipients:
                message = f"Subject: {subject}\n\n{body}"
                server.sendmail(sender_email, recipient, message)
        print("Emails sent successfully!")
    except Exception as e:
        print(f"Error sending emails: {e}")

def main():
    # Input email credentials
    sender_email = input("Enter your email address: ")
    sender_password = getpass.getpass("Enter your email password: ")

    # Input email content
    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")

    # Input recipient list file
    file_path = input("Enter the path to the recipient list Excel file: ")

    # Read recipients from Excel file
    recipients = read_recipients_from_excel(file_path)

    # Send emails
    send_emails(sender_email, sender_password, subject, body, recipients)

if __name__== "__main__":
    main()