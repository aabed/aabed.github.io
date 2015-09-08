import sys
import xmpp
import logging
import hpfeeds
class HpfeedsHandler(logging.Handler):
    def __init__(self,HOST,PORT,IDENT, SECRET, CHANNELS):
        logging.Handler.__init__(self)

        self.IDENT = IDENT
        self.CHANNELS=CHANNELS
        hpc = hpfeeds.new(HOST, PORT, IDENT, SECRET)
        hpc.subscribe(CHANNELS)

        self.hpc = hpc


    def emit(self, record):
        try:
            msg = self.format(record)
            self.hpc.publish(self.CHANNELS,msg)
        except:
            self.handleError(record)
