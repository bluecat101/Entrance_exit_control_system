from dotenv import load_dotenv
load_dotenv()
import os


NAMES = os.getenv('NAMES')


def get_name_list():
  return NAMES.split(',')
