from numpy import log as ln
from numpy import e

#C = b * ln(sum([e**q/b for q in [1, 4, 6]]))

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
        return b*ln(sum([e**(q/b) for q in quantities]))
        
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
        return b*ln(sum([e**(q/b) for q in quantities])) - self.cost  
    
    def buy(self, contract, q, user):
        """
        contract: dict
        q: float
        user: dict #this is the user object
        """
        c = [cont for cont in self.contracts if cont["title"]==contract].pop()
        c["q"]+=q #here, the contract should be updated in the database
        user["events"][self.title]["contracts"][contract] += q
        user["account"] -= self.query_cost(contract, q)
        #update user here
        return {"new_q": c["q"], contract : user["events"][self.title]["contracts"][contract]}
    
    
    def price(self, contract):
        b = self.b
        c = [cont for cont in self.contracts if cont["title"]==contract].pop()
        index = self.contracts.index(c)
        quantities = [float(contract["q"]) for contract in self.contracts]
        qi = quantities[index]
        return e**(qi/b)/sum([e**(q/b) for q in quantities])
    
def main():
    user = {"id": 12345, "events":{"Will I become a billionair in five years?":{"contracts":{"yes":20, "no":0}}}}

    user["account"]=500
    
    market =Market("Will I become a billionair in five years?",
                   [{"title":"yes", "q":300}, {"title":"no", "q":700}],
                   100)

    print "user shares: " + str(user)
    print "price of 10 shares of no: " + str(market.query_cost("no", 10))
    
    print "yes price: " + str(market.price("yes"))
    print "no price: " + str(market.price("no"))
    print "buying with user: " +str(market.buy("yes", 20, user))
    print "price of 20 shares of yes: " + str(market.query_cost("yes", 20))
    
    print "user account: " + str(user)
    
if __name__=="__main__":
    main()
