import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    """
    Gets data from Google Sheets. Specifically, the guild's command channels and the bot's custom responses.
    """

    def __init__(self):
        print("Connecting to Google Sheets...")

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("./secret/google_sheets_secret.json", scope)
        client = gspread.authorize(credentials)
        master_sheet = client.open("Discord Assistant Bot")

        self.command_channel_sheet = master_sheet.worksheet("Permissions")
        self.custom_response_sheet = master_sheet.worksheet("Custom Responses")
        self.command_channel_records = None
        self.custom_response_records = None

        self.refresh_records()

    def refresh_records(self):
        self.command_channel_records = self.command_channel_sheet.get_all_records()
        self.custom_response_records = self.custom_response_sheet.get_all_records()

    def get_command_channel_id(self, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id:
                return entry["command_channel_id"]

    def get_custom_response(self, text):
        for entry in self.custom_response_records:
            trigger_phrases = str(entry["trigger_phrases"]).split(',')

            for word in text.split(" "):
                if word in trigger_phrases:
                    return entry["response"]

    def is_command_channel(self, text_channel, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id and entry["command_channel_name"] == text_channel:
                return True

        return False
