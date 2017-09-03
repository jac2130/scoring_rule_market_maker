import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dateutil.parser import parse
import os, sys, datetime
sys.path.append("/root/collectiwise/collectiwise_backend/")
sys.path.append("/root/collectiwise/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collectiwise_backend.settings")
import django
django.setup()
sys.path.append("/root")

import cPickle as pickle
from trades import *

sample = "data/sample300_2017-09-03 16:23:04.920806.p"
events = pickle.load( open( sample, "rb" ) )
#loading and unpacking the data
for (event, event_vars), contracts in events:
    for contract, contract_vars in contracts:
        print contract.name
        for cont_var in contract_vars:
            print "price: " + str(cont_var.lastTradePrice)
