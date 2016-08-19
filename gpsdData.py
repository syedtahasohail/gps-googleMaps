import os
from gps import *
from time import *
import time
import threading
import httplib
import json
import sys
from subprocess import call

# GPS Settings
call (['sudo', 'gpsd', '-F', '/var/run/gpsd.sock', '/dev/ttyAMA0'])
#seting the global variable
gpsd = None
 
#clear the terminal (optional)
os.system('clear') 

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    #bring it in scope
    global gpsd 
    #starting the stream of info
    gpsd = gps(mode=WATCH_ENABLE) 
    self.current_value = None
    self.running = True 
    #setting the thread running to true
 
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
      sensorID = "NEO-6M"

      # current time and date
      currentTime = datetime.datetime.now().time().replace(second = 0, microsecond = 0)
      dateToday = datetime.datetime.now().date().strftime("%d-%m-%Y")
          
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

      currentTime = str (currentTime)
      dateToday = str (dateToday)

      #Creating connection with local server
      try:
        conn = httplib.HTTPConnection("192.168.0.199:8001")
        headers = {'Content-type': 'application/json'}
        foo = {'lat': gpsd.fix.latitude,
        'lng': gpsd.fix.longitude,'sensorID': sensorID,'time': currentTime,'date': dateToday,'flag': 1
        }

        json_foo = json.dumps(foo)
        if gpsd.fix.latitude != 0 and gpsd.fix.longitude != 0: 
          conn.request("POST", "/location", json_foo, headers)
          response = conn.getresponse()
          print response.status, response.reason
          data = response.read()
          print json.dumps(data, sort_keys = True, indent = 4, separators= (',', ': '))
          conn.close()

          # Update lat, lng after every minute
          time.sleep(60)
              
    except:
      print 'Server not ready.', sys.exc_info()
      sys.exit()
 
  except (KeyboardInterrupt, SystemExit):

        # Connection with Local server
        conn = httplib.HTTPConnection("192.168.0.199:8001")
        
        # POST flag for end of transmission from GPS.
        flag = {'flag': 0
        }

        json_flag = json.dumps(flag)
        conn.request("POST", "/location", json_flag, headers)
        response = conn.getresponse()
        print response.status, response.reason
        reply = response.read()
        conn.close()
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        
        
      # wait for the thread to finish what it's doing
        print "Done.\nExiting."
