import os
from gps import *
from time import *
import time
import threading
import httplib
import json
from subprocess import call


call (['sudo', 'gpsd', '-F', '/var/run/gpsd.sock /dev/ttyAMA0'])
#seting the global variable
gpsd = None

 
#clear the terminal (optional)
os.system('clear') 


#clear the terminal (optional) 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() 

#this will continue to loop and grab EACH set of gpsd info to clear the buffer 
if __name__ == '__main__':
  gpsp = GpsPoller()
  
  # create the thread
  try:
    gpsp.start() 

    # start it up
    while True:
          
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
 
      print
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      print 'sats        ' , gpsd.satellites

      #POST request on Local Server
      conn = httplib.HTTPConnection("192.168.0.199:8001")
      headers = {'Content-type': 'application/json'}
      foo = {'lat': gpsd.fix.latitude,
      'lng': gpsd.fix.longitude
      }

      #JSON format
      json_foo = json.dumps(foo)
      conn.request("POST", "/location", json_foo, headers)
      response = conn.getresponse()
      print response.status, response.reason
      data = response.read()
      data
      conn.close()
      time.sleep(5)
      #set to whatever
 
  except (KeyboardInterrupt, SystemExit):
  #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join()
  # wait for the thread to finish what it's doing
  print "Done.\nExiting."
