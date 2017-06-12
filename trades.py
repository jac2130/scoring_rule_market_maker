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
        user: str #this is the user id
        """
        pass

    
def main():
    market =Market("Will I become a billionair in five years?",
                   [{"title":"yes", "q":300}, {"title":"no", "q":700}],
                   100)
    
    print market.query_cost("no", 1)

if __name__=="__main__":
    main()
