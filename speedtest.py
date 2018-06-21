import subprocess
import sys
import time

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install('speedtest-cli')
install('pandas')

import speedtest
import pandas as pd

path = '/Users/Travis/Desktop'

for i in range(5):

    speed_test = speedtest.Speedtest()
    speed_test.get_best_server()


    speed_test.download()
    speed_test.upload()

    download = speed_test.results.download/1000000
    upload = speed_test.results.upload/1000000
    ping = speed_test.results.ping
    test_country = speed_test.results.server['country']
    host = speed_test.results.server['host']
    timestamp = speed_test.results.timestamp
    bytes_sent = speed_test.results.bytes_sent
    bytes_received = speed_test.results.bytes_received
    isp = speed_test.results.client['isp']
    isp_country = speed_test.results.client['country']


    d = {'download Mbit/s':[download], 'upload Mbit/s':[upload],'ping (ms)':[ping], 'test_country':[test_country],
     'host':[host], 'timestamp':[timestamp], 'bytes_sent':[bytes_sent], 'bytes_received':[bytes_received],
     'isp':[isp],'isp_country':[isp_country]}

    if 'df' not in locals():
        df = pd.DataFrame.from_dict(data=d, orient='columns')
    else:
        dftemp = pd.DataFrame.from_dict(data=d, orient='columns')

        df = df.append(dftemp,ignore_index=True)
        time.sleep(60*15)
