import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    """
    Gets data from Google Sheets. Specifically, the text channels that the bot is allowed to post in.
    """

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("./secret/google_sheets_secret.json", scope)
        print("Connecting to Google Sheets...")
        client = gspread.authorize(credentials)
        self.sheet = client.open("Discord Assistant Bot").sheet1
        self.records = self.sheet.get_all_records()

    def can_post_in_text_channel(self, text_channel):
        print("text channel: " + str(text_channel))

        for entry in self.records:
            if text_channel == entry["allowed_channel_id"]:
                return True
        else:
            return False
