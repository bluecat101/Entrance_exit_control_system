from dotenv import load_dotenv
load_dotenv()
import os


NAMES = os.getenv('NAMES')
GOOGLE_APPLICATION_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_PATH')
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')

def get_name_list():
  return NAMES.split(',')
