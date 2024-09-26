from pathlib import Path
from google.oauth2.credentials import Credentials
import sys
import os
from datetime import datetime
import pytz
import time
import traceback

class SheetLogger:
    """
    A logger that appends log messages to specific Google Sheets tabs with batching, timestamping, and API rate limit checks.
    
    Features:
        - Timestamps: Automatically prepends log messages with a timestamp ("YYYY-MM-DD HH:MM:SS").
        - Batching: Accumulates log entries and writes them in batches to reduce API calls (batch size is configurable).
        - API Rate Limit: Monitors and enforces Google's 60 API requests per minute limit, pausing if necessary.
        - Server Mode: Disables all local print outputs by redirecting stdout and stderr.
    
    Attributes:
        spreadsheet_id (str): Google Spreadsheet ID.
        service (obj): Google Sheets API service object.
        logs (dict): Stores log messages by tab.
        batch_size (int): Number of log entries to accumulate before flushing to the sheet.
        batch_data (list): Stores batched data separately for each tab before sending to the sheet.
        api_write_counter (int): Tracks API write calls.
        api_write_reset_time (datetime): Tracks time for resetting API rate limit counter.
    
    Methods:
        write_prints_to_sheet(tab_name, message): Adds a log entry with a timestamp to the specified tab and flushes if batch size is reached.
        write_errors_to_sheet(tab_name, exception): Logs verbose error output, including the error type, message, and full traceback, to the specified tab.
        flush(tab_name): Writes accumulated batch data to the specified tab.
        check_api_limit(): Ensures API write calls do not exceed 60 requests per minute.
        release_remaining_logs(): Releases all remaining logs for all tabs, even if batch size is not reached.
        run_in_server_mode(): Disables all local prints by redirecting stdout and stderr to `None`.

    Example Usage:
    Log call: sheet_logger.write_prints_to_sheet(tab_name, message)
    Log error: sheet_logger.write_errors_to_sheet(tab_name, exception)
    Log output format: "YYYY-MM-DD HH:MM:SS - message"
    """

    def __init__(self, spreadsheet_id, scopes, batch_size=5, token_full_path=None, timezone='Europe/Madrid'):
        """
        Initializes the SheetLogger by obtaining Google Sheets API credentials, setting up logs, and batch settings.
        Args:
            spreadsheet_id (str): The ID of the Google Spreadsheet.
            scopes (list): The API access scopes for Google Sheets.
            batch_size (int): Number of log entries to batch before writing to the sheet (default is 5).
            token_full_path (str): Folder path where the token file is located.
            timezone (str): Timezone to use for timestamping log entries (default is 'Europe/Madrid').
        """
        self.spreadsheet_id = spreadsheet_id
        self.token_full_path = token_full_path
        self.service = self.get_service(scopes)
        self.logs = {}  # Dynamic log storage for tabs
        self.batch_size = batch_size
        self.batch_data = {}  # Stores batched data separately for each tab
        self.api_write_counter = 0
        self.api_write_reset_time = datetime.now()
        self.timezone = timezone

    def get_service(self, scopes):
        """
        Sets up the Google Sheets API service using the provided scopes and returns
        Google Sheets service object or None if credentials couldn't be obtained.
        """
        creds = self.get_token_creds(scopes)
        if creds:
            from googleapiclient.discovery import build
            return build('sheets', 'v4', credentials=creds)
        else:
            print("Error: Could not obtain credentials.")
            return None

    def get_token_creds(self, scopes):
        """
        Obtains or refreshes token credentials for the specified API scopes and
        returns the credentials object or None if credentials couldn't be loaded.
        """
        creds = None
        try:
            # Check if the token file path is provided; otherwise, use the default location
            if self.token_full_path:
                token_file = Path(self.token_full_path)

            # Check if the token file exists
            if not token_file.exists():
                raise FileNotFoundError(f"Error: token.json not found at {token_file}. "
                                        "Make sure the file is located in the correct folder.")

            # Load the token credentials from the 'token.json' file
            creds = Credentials.from_authorized_user_file(token_file, scopes)

        except Exception as e:
            print(f"An error occurred: {e}")

        return creds

    def check_api_limit(self):
        """
        Checks if the API call limit has been reached and waits for reset if necessary.
        Google Sheets has a rate limit of 60 requests per user per minute.
        """
        elapsed_time = (datetime.now() - self.api_write_reset_time).total_seconds()
        if elapsed_time < 60:
            if self.api_write_counter >= 59:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - API limit reached. Pausing for 60 seconds.")
                time.sleep(60)
                self.api_write_counter = 0
                self.api_write_reset_time = datetime.now()
        else:
            self.api_write_counter = 0
            self.api_write_reset_time = datetime.now()

    def write(self, message, tab_name):
        """
        Adds a log message to the specified sheet tab and batches it.
        NOTE: Appends each line of the message to the logs for the specified tab,
        with a timestamp in the format "YYYY-MM-DD HH:MM:SS -", using CET/CEST (Madrid time).
        """
        if tab_name not in self.logs:
            self.logs[tab_name] = []  # Dynamically add tab names if they don't already exist

        # Ensure batch data exists for this tab
        if tab_name not in self.batch_data:
            self.batch_data[tab_name] = []

        # Get current time in defined timezone - considering daylight saving time (if applicable)
        timezone_ = pytz.timezone(self.timezone)
        timestamp = datetime.now(timezone_).strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message}"

        lines = formatted_message.split('\n')
        for line in lines:
            if line:  # Only append non-empty lines
                self.logs[tab_name].append([line])
                self.batch_data[tab_name].append([line])

        # Flush the data if batch size limit is reached
        if len(self.batch_data[tab_name]) >= self.batch_size:
            self.flush(tab_name)

    def flush(self, tab_name):
        """
        Flushes all logs stored for the specified tab to the Google Sheet in batches, inserting new rows at the top.
        """
        if tab_name in self.batch_data and self.batch_data[tab_name]:
            self.check_api_limit()  # Ensure API limit is respected before writing
            try:
                ## Prepare the batch data to write
                batch_to_write = self.batch_data[tab_name]

                ## Fetch existing data from the sheet
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{tab_name}!A:B'  # Adjust range as needed
                ).execute()

                existing_values = result.get('values', [])

                ## Combine new data at the top of the existing data
                updated_values = batch_to_write + existing_values

                ## Write the combined data back to the sheet, starting at A1
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{tab_name}!A1',
                    valueInputOption='RAW',
                    body={'values': updated_values}
                ).execute()

                # Clear the batch after flushing
                self.batch_data[tab_name] = []
                self.api_write_counter += 1  ## Increment API write call counter
            except Exception as e:
                print(f"Failed to append logs: {e}", file=sys.__stdout__)

    def release_remaining_logs(self):
        """
        Flushes all remaining logs for all tabs, ensuring all logs are written even if the batch size is not reached.
        """
        for tab_name in self.logs:
            if self.logs[tab_name]:  # Check if there are logs remaining in the tab
                # print(f"Flushing logs for tab: {tab_name}")  # Debugging output
                self.flush(tab_name)

    def write_prints_to_sheet(self, tab_name, message, flush=False):
        """
        Writes a log message (such as print statements) to a specified tab and flushes if batch size is reached.

        Args:
            tab_name (str): The name of the tab in the Google Sheet to write the log message.
            message (str): The log message to write to the specified tab.
            flush (bool): If True, flushes the logs immediately after writing the message (default is False).

        NOTE:
            - Dynamically adds new tab names to the logs dictionary if they don't already exist.
            - Flushes automatically when the batch size is reached or when explicitly requested.
        """
        self.write(message, tab_name)

        if flush:
            self.flush(tab_name)

    def write_errors_to_sheet(self, tab_name, exception, flush=False):
        """
        Writes a verbose error message, including the exception type, message, and full traceback, to the specified tab.
        This method is intended for use in exception handling blocks.
        
        Args:
            tab_name (str): The name of the tab in the Google Sheet to write the error logs.
            exception (Exception): The exception object to log details about.
            flush (bool): If True, flushes the logs immediately after writing the error message (default is False).
        """
        error_type = type(exception).__name__
        error_message = str(exception)
        error_traceback = traceback.format_exc()

        verbose_message = (
            f"Error type: {error_type}\n"
            f"Error message: {error_message}\n"
            f"Traceback:\n{error_traceback}"
        )

        self.write(verbose_message, tab_name)

        if flush:
            self.flush(tab_name)

    def run_in_server_mode(self, enable: bool):
        """
        Enables or disables all local prints by redirecting stdout and stderr to None if enable is True.
        If enable is False, it restores the normal behavior of stdout and stderr.
        
        Args:
            enable (bool): If True, disables prints by redirecting to os.devnull. If False, restores stdout/stderr.
        """
        if enable:
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
        else:
            sys.stdout = sys.__stdout__  ## Restore normal stdout
            sys.stderr = sys.__stderr__  ## Restore normal stderr