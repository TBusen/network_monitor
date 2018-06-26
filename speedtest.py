import subprocess
import sys
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from my_secrets import Secrets

pg = Secrets('postgres')

uid = pg.login()[0]+':'
pw = pg.login()[1]
server = '@pgmeta.travbus.xyz:5432/'
db = 'app_acct'
dialect = 'postgresql+psycopg2://'

engine = create_engine(dialect+uid+pw+server+db)

Session = sessionmaker()

Session.configure(bind=engine)

session = Session()

# take care of dependencies for virgin runs
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install('speedtest-cli')
# install('pandas')

# define table object

Base = declarative_base()

class Network_Stats(Base):
    __tablename__ = 'network_stats'

    id = Column(Integer, primary_key=True)
    download = Column(Float)
    upload = Column(Float)
    ping = Column(Float)
    test_country = Column(String(50))
    host = Column(String(150))
    timestamp = Column(DateTime)
    bytes_sent = Column(Integer)
    bytes_received = Column(Integer)
    isp = Column(String(150))
    isp_country = Column(String(50))

    def __repr__(self):
        return '''<Network_Stats(id=' %s',download=' %s',upload=' %s', 
               ping=' %s', test_country=' %s',host=' %s',timestamp=' %s',
               bytes_sent=' %s',bytes_received=' %s',isp=' %s',
               isp_country=' %s' '''%(self.id, self.download, self.upload,
                                      self.ping, self.test_country, self.host,
                                      self.timestamp, self.bytes_sent,
                                      self.bytes_received, self.isp,
                                      self.isp_country)


import speedtest

# run 5 times per hour
# 7 min. between runs
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

    d = {'download': download, 'upload': upload,
         'ping': ping, 'test_country':test_country,
         'host': host, 'timestamp': timestamp, 'bytes_sent': bytes_sent,
         'bytes_received': bytes_received,
         'isp': isp, 'isp_country': isp_country}

    # insert into temp object
    temp_obj = Network_Stats(download = d['download'],
                         upload = d['upload'],
                         ping = d['ping'],
                         test_country = d['test_country'],
                         host = d['host'],
                         timestamp = d['timestamp'],
                         bytes_sent = d['bytes_sent'],
                         bytes_received = d['bytes_received'],
                        isp = d['isp'],
                        isp_country = d['isp_country']
                         )
    session.add(temp_obj) # add to session
    session.commit() # commit
    time.sleep(420) # sleep for 7 minutes

