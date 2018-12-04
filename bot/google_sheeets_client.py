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
        self.command_channel_sheet = client.open("Discord Assistant Bot").sheet1
        self.command_channel_records = self.command_channel_sheet.get_all_records()

    def get_command_channel_id(self, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id:
                return entry["command_channel_id"]

        return None

    def is_command_channel(self, text_channel, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id and entry["command_channel_name"] == text_channel:
                return True

        return False
