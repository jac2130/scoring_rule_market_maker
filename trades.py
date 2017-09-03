from numpy import log as ln
from numpy import e
from math import ceil, floor
import numpy as np
import os, sys, datetime
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')
from dateutil.parser import parse

sys.path.append("/root/collectiwise/collectiwise_backend/")
sys.path.append("/root/collectiwise/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collectiwise_backend.settings")
sys.path.append("/root/collectiwise/collectiwise_backend/collectiwise_core/")
import django
django.setup()
sys.path.append("/root")

from collectiwise_core.models import Event, EventVar, Contract, ContractVar, User, UserBalance, UserContract, Purchase

bigBrother = User("Big Brother")
bigBroBalance = UserBalance(bigBrother, 10000)

def round_up(cont_money):
    cents =cont_money*100
    return int(ceil(cents))

def round_down(cont_money):
    cents = cont_money*100
    return int(floor(cents))

class Market(object):
    """
    In the future, this class should instantiate by
    querying an event and add all of its contracts automatically
    to the contract list and fill in the title of the event
    for now, I instantiate the class by explicitly feeding
    it with a list of contracts.
    """
    def __init__(self, title, contracts, b):
        """
        title: str
        contracts: list
        b: float #b is chosen by the market maker so as to govern the
        volatility of the price to quantities
        """
        self.title= title
        self.contracts = contracts

        self.b = float(b)


    @property
    def cost(self):
        b = self.b
        quantities = [float(contract["q"]) for contract in self.contracts]
        return b*ln(sum([e**(qi/b) for qi in quantities]))


    def query_cost(self, contract, q):
        """
        contract: dict
        q : float
        """
        b = self.b
        c = [cont for cont in self.contracts if cont["title"]==contract].pop()
        index = self.contracts.index(c)
        quantities = [float(contract["q"]) for contract in self.contracts]
        quantities[index]+=float(q)
        if q>0:
            return round_up(b*ln(sum([e**(qi/b) for qi in quantities])) - self.cost)
        else:
            return -round_down(-b*ln(sum([e**(qi/b) for qi in quantities])) + self.cost)

    def buy(self, contract, q, user):
        """
        contract: dict
        q: float
        user: dict #this is the user object
        """
        c = [cont for cont in self.contracts if cont["title"]==contract].pop()
        c["q"]+=q

        #here, the contract should be updated in the database
        user["events"][self.title]["contracts"][contract] += q
        user["account"] -= self.query_cost(contract, q)/100.00 #in dollars
        #update user here
        return {"new_q": c["q"], contract : user["events"][self.title]["contracts"][contract]}

    def sell(self, contract, q, user):
        return self.buy(contract, -q, user)


    def price(self, contract):
        b = self.b
        c = [cont for cont in self.contracts if cont["title"]==contract].pop()
        index = self.contracts.index(c)
        quantities = [float(contract["q"]) for contract in self.contracts]
        q = quantities[index]
        return e**(q/b)/sum([e**(qi/b) for qi in quantities])

    def quantities(self):
         #set one of the quantities (here the first one) to b (a good base number)
        price_vector = [contract.lastTradePrice for contract in self.contracts]
        q1= [contract.volume for contract in self.contracts][0]
        if q1<=0:
            q1 = self.b

        p1 = price_vector[0]
        return [q1] + [b*ln(e**(q1/b)*(pk/p1)) for pk in price_vector[1:]]

    @property
    def quants(self):
        prices =[self.price(contract["title"]) for contract in self.contracts]
        return self.quantities(prices)

    def equilibriate_quantities(self, price_vector, param=2):
        bigBrother["events"] = {self.title:{"contracts":{contract["title"]:0 for contract in self.contracts}}}

        while np.abs(sum(np.array(self.quants) - np.array(self.quantities(price_vector)))) > param:
            diff = np.array(self.quantities(price_vector)) - np.array(self.quants) #the difference of what I should have minus the ones I do have
            index = list(diff).index(max(diff))
            if int(max(diff)/2.0) > 0:
                self.buy(self.contracts[index]["title"], int(max(diff)/2.0), bigBrother)
            else:
                break
        return

def main():
    user = {"id": 12345, "events":{"Will I become a billionair in five years?":{"contracts":{"yes":20, "no":0}}}}

    user["account"]=500

    market =Market("Will I become a billionair in five years?",
                   [{"title":"yes", "q":300}, {"title":"no", "q":700}],
                   100)

    print "user shares: " + str(user)
    print "price of 10 shares of no: " + str(market.query_cost("no", 10)/100.0)

    print "yes price: " + str(market.price("yes"))
    print "no price: " + str(market.price("no"))
    print "buying with user: " +str(market.buy("yes", 20, user))
    print "price of 20 shares of yes: " + str(market.query_cost("yes", 20)/100.0)

    print "user account: " + str(user)
    print "yes price: " + str(market.price("yes"))
    print "no price: " + str(market.price("no"))
    print "price of selling 20 shares of no: " + str(-market.query_cost("no", -20)/100.0)
    print "selling no with user: " +str(market.sell("no", 20, user))
    print "user account: " + str(user)
    print "yes price: " + str(market.price("yes"))
    print "no price: " + str(market.price("no"))
    market2 = Market("how many tweets will I sent before next week?", [{"title": 0}, {"title":10}, {"title":25}, {"title":30}], 10)

    print "quantities from prices (p1=0.1, p2=0.2, p3=0.2, p4=0.5): " + str(market2.quantities([0.1, 0.2, 0.2, 0.5]))

    #query from predictit has prices:
    predictit_query = {"yes": 1, "no":99}
    market.equilibriate_quantities([1, 99])
    print bigBrother
    print "yes price: " + str(market.price("yes"))
    print "no price: " + str(market.price("no"))
if __name__=="__main__":
    main()
