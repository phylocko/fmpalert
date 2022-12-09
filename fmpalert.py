from fmpclient import Client
from notifier import Notifier
from settings import API_URL, EXEC_COMMAND, CHECK_INTERVAL

if __name__ == '__main__':

    fmp_client = Client(API_URL)
    notifier = Notifier(fmp_client, EXEC_COMMAND, check_interval=CHECK_INTERVAL)
    try:
        notifier.monitor()
    except KeyboardInterrupt:
        quit(0)
