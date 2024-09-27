import requests
from pathlib import Path
from datetime import datetime
from msal import PublicClientApplication
from string import Template
from enum import Enum


class Status(Enum):
    """The status of the process

    failure = 0
    attention = 1
    success = 2

    """


    failure = 0
    attention = 1
    success = 2


class Robot_mailer:
    """
    params:

    sender: str The sender in the "from:" field of the email
    secrets: {"clientid","tenantid","username","password"}
    """

    def __init__(
        self,
        secrets: dict,
        sender: str = None,
    ) -> None:
        self.sender: str = sender
        self.secrets = secrets
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.email_recipients: list[str] = None
        self.process_name: str = None
        self.process_status: Status = None

        self.files_handled: list[str] = None
        self.message: str = None


    def _form_email(self):
        """form the email"""
        match self.process_status:
            case Status.failure:
                email_subject = f"Robotin {self.process_name} ajo epäonnistui!"
            case Status.attention:
                email_subject = f"Robotin {self.process_name} ajossa huomioita!"
            case Status.success:
                email_subject = (
                    f"Robotin {self.process_name} ajo suoritettu onnistuneesti!"
                )

        email_data = {
            "message": {
                "subject": email_subject,
                "body": {
                    "contentType": "HTML",
                    "content": self._create_email_body(),

                },
                "toRecipients": [
                    {"emailAddress": {"address": email}}
                    for email in self.email_recipients
                ],
            }
        }
        return email_data

    def _create_email_body(self):

        """Create the body element for the email"""
        date = self.date
        current_file = Path(__file__)
        resource_path = current_file.parent / "resources" / "email_template.html"

        match self.process_status:
            case Status.failure:
                status_message = f"""<p>
                                {self.process_name} ajo {date}
                                <span style="color: red; font-weight: bolder">epäonnistui!</span>
                                </p>"""
            case Status.attention:
                status_message = f"""<p>
                                {self.process_name} ajossa {date}
                                <span style="color: blue; font-weight: bolder">oli huomioita</span>
                                </p>"""
            case Status.success:
                status_message = f"""<p>
                                {self.process_name} ajo {date} suoritettu
                                <span style="color: green; font-weight: bolder">onnistuneesti!</span>
                                </p>"""

        with resource_path.open("r", encoding="utf-8") as html_file:
            html_content = html_file.read()



        template = Template(html_content)
        values = {
            "statusmessage": status_message,
            "process": self.process_name,
            "date": self.date,
            "message": self.message if self.message else "",
            "listitems": self.files_handled if self.files_handled else "",

        }
        email = template.substitute(values)
        return email

    def _create_file_list(self, files_handled):
        """create a list of files as links to be embedded into the email"""

        style = """style='
        margin: 5px; 
        padding: 6px; 
        border-color: rgb(211, 197, 133);
        border-width: 5px;
        border-style: solid;'
        """
        file_list = f"<div {style}><h3> Suorituksen tiedostot:</h3> <ul>"
        for file in files_handled:
            file_list += f" <li>{file}</li>\n"

        file_list += "</ul> </div>"
        return file_list

    def _acquire_ms_authentication_token(self):
        """get the token used in ms graph"""
        CLIENT_ID = self.secrets["clientid"]
        TENANT_ID = self.secrets["tenantid"]
        USERNAME = self.secrets["username"]
        PASSWORD = self.secrets["password"]
        SCOPES = ["https://graph.microsoft.com/.default"]

        app = PublicClientApplication(
            CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}"
        )
        result = app.acquire_token_by_username_password(
            USERNAME, PASSWORD, scopes=SCOPES
        )

        return result["access_token"]

    def send_report_email(
        self,
        recipients: list[str],
        process_name,
        status: int | Status,
        *,
        files_handled: list[str] = None,
        optional_message: str = None,

    ) -> None:
        """
        Sends a notification email using the Microsoft Graph API.

        Args:
            recipients (list of str): A list of email addresses to send the notification to.
            process_name (str): The name of the process being reported.
            status (int | Status): The status of the process run.
                          - 0 for failure,
                          - 1 for attention required,
                          - 2 for success.
            files_handled (list of str): A list of file paths for the files that were handled during the process run.
            message (str): an optional message to be sent in the email.


        Raises:
            `HTTPError`: If the email fails to send or if there are issues with the API request.
        """
        self.email_recipients = recipients
        self.process_name = process_name
        self.process_status = Status(status)
        self.files_handled = files_handled
        self.message = optional_message


        access_token = self._acquire_ms_authentication_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        email = self._form_email()
        if self.sender:
            url = f"https://graph.microsoft.com/v1.0/users/{self.sender}/sendMail"
        else:
            url = "https://graph.microsoft.com/v1.0/me/sendMail"

        response = requests.post(url=url, headers=headers, json=email)
        if response.status_code != 202:
            raise response.raise_for_status()
