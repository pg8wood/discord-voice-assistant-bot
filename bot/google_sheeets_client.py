import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    """
    Gets data from Google Sheets. Specifically, the text channels that the bot is allowed to post in.
    """

    def __init__(self):
        print("Connecting to Google Sheets...")

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("./secret/google_sheets_secret.json", scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open("Discord Assistant Bot").sheet1
        self.records = self.sheet.get_all_records()

    def is_commands_channel(self, text_channel):

        for entry in self.records:
            if entry["command_channel_name"] == text_channel:
                return True
        else:
            return False
