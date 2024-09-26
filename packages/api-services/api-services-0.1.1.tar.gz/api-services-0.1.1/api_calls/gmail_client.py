from api_services.utils import create_service
import json
import pandas as pd

class GoogleGmailClient:
    def __init__(self, client_secret_file,api_version='v1', scopes=None, prefix=''):
        if scopes is None:
            scopes=[]
        elif not isinstance(scopes,list):
            raise ValueError("Scopes must be a list.")
        self.service = create_service(client_secret_file, 'gmail', api_version, *scopes, prefix=prefix)
    
    def send_email(self, sender, to, subject, message_text):
        """Send an email using the Gmail API."""
        try:
            message = self.create_message(sender,to,subject,message_text)
            sent_message = self.service.users().messages().send(
                userId="me",
                body=message
            ).execute()
            return sent_message
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")
        
    def list_emails(self,user_id="me",max_results=10):
        """List recent emails from the users gmail inbox"""
        try:
            result = self.service.users().messages().list(
                userId=user_id,
                maxResults=max_results
            ).execute()
            return result.get("messages",[])
        except Exception as e:
            raise RuntimeError(f"Failed to list emails: {e}")
        
    def get_email(self,user_id="me",message_id=None):
        """Get details of a specific mail"""
        try:
            result = self.service.users().messages().get(
                userId=user_id,
                id=message_id
            ).execute()
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to get email: {e}")
        
    def search_emails(self, user_id="me", query="", max_results=10):
        """Search emails with specific criteria"""
        try:
            result = self.service.users().messages().list(
                userId=user_id,
                q=query,
                maxResults=max_results
            ).execute()
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to search emails: {e}")
        
    def create_message(self,sender,to,subject,message_text):
        """Create a message for an email"""
        from email.mime.text import MIMEText
        import base64
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw':raw}
    
    def send_message_with_attachment(self,to,sender,subject,message_text,file_path):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        import mimetypes
        import os
        import base64

        try:
            message = MIMEMultipart()
            message["To"] = to
            message["From"] = sender
            message["Subject"] = subject
            
            msg = MIMEText(message_text)

            message.attach(msg)

            content_type, encoding = mimetypes.guess_type(file_path)

            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"

            maintype, subtype = content_type.split("/",1)

            with open(file_path, "rb") as fp:
                attachment_data = MIMEApplication(fp.read(),_subtype=subtype)
                attachment_data.add_header(
                    'Content-Disposition',
                    "attachment",
                    filename=os.path.basename(file_path)
                )
                message.attach(attachment_data)

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message_body = {"raw":encoded_message}

            message_send = (
                self.service.users().messages().send(
                    userId="me",
                    body=create_message_body
                ).execute()
            )
            return message_send
        except Exception as e:
            raise RuntimeError(f"Failed to send message with attachment: {e}")




