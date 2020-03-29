import ssl
import threading
import wget


def run_check():
    threading.Timer(3600.0, run_check).start()
    ssl._create_default_https_context = ssl._create_unverified_context
    new_google_sheet_url = 'https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=xlsx'

    wget.download(new_google_sheet_url, './data/data.xlsx')
    print("new excel generated")


run_check()
