import os
import sys
import tempfile
from subprocess import Popen, PIPE, STDOUT
import fcntl
import time

import cherrypy
cherrypy.config.update({'server.socket_host': '10.0.0.54',
                        'server.socket_port': 80,
                       })
class cec_(object):
    cmd ={'Select':0,
          'Up':1,
          'Down':2,
          'Left':3,
          'Right':4,
          'Root Menu':9,
          'Exit':13,
          'Enter':43,
          'Clear':44}
    logfile = ''

    htmltxt = '''<html>
          <head></head>
          <body>
	    %%body%%
            <form method="get" action="sendKey">
	      <button name="key" value="On" type="submit">On</button>
	      <button name="key" value="Up" type="submit">Up</button> 
        <button name="key" value="Off" type="submit">Off</button></br>


        <button name="key" value="Left" type="submit">Left</button>
	      <button name="key" value="Select" type="submit">Select</button>
	      <button name="key" value="Right" type="submit">Right</button> </br>


        <button name="key" value="Enter" type="submit">Enter</button>
	      <button name="key" value="Down" type="submit">Down</button>
        <button name="key" value="Exit" type="submit">Exit</button>

            </form>
          </body>
        </html>'''


    @cherrypy.expose
    def index(self):
	if len(self.logfile) > 0:
		tem = self.logfile
		logfile = '' 
		return self.htmltxt.replace("%%body%%",tem)


    def check_for(self, string):
        while True:
                myoutputtext = ''
                try:
                        myoutputtext += self.client.stdout.read()
                        self.logfile +=  myoutputtext
                except IOError:
                        pass
                if string in myoutputtext:
                        break
                time.sleep(.1)    # short sleep before attempting another read

    def __init__(self):
        self.client = Popen(['cec-client', '-d', '8' 'RPI'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        fcntl.fcntl(self.client.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        self.check_for('waiting for input')

    @cherrypy.expose    
    def sendKey(self,key=''):
      if len(key) > 0 and key in self.cmd:
        key = "{0:0>2}".format(hex(self.cmd[key])[2:])
        self.client.stdin.write('tx 14:44:'+key+'\n')
        self.client.stdin.write('tx 14:45\n')
        self.check_for('45')
        return self.htmltxt.replace("%%body%%","Key Ok")
      elif key in "On":
        self.client.stdin.write('on 0\n')
        return self.htmltxt.replace("%%body%%","Key Ok")
      elif key in "Off":
        self.client.stdin.write('standby 0\n')
        return self.htmltxt.replace("%%body%%","Key Ok")

      return self.htmltxt.replace("%%body%%","Error")

    @cherrypy.expose
    def quit(self):
        self.client.stdin.write('q\n')

if __name__ == '__main__':
    cherrypy.quickstart(cec_())

#server_class = BaseHTTPSe
#cec.sendKey(cec.cmd['Left'])
#cec.sendKey(cec.cmd['Right'])
#cec.quit()

