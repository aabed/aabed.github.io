import handler
import logging
new=handler.HpfeedsHandler("127.0.0.1",10000,"menna","12345",["aabed.events"])
loger=logging.getLogger('handler')
loger.addHandler(new)
loger.critical("a7eeeeeeh")
