from flask import Blueprint

spiders = Blueprint('spiders', __name__)

from bet10 import Bet10
from bet365 import Bet365
from betfred import BetFred
from coral import Coral
from eight88 import Eight88
from ladbrokes import LadBrokes
from netbet import Netbet
from paddy import Paddy
from real import RealDealBet
from stan import StanJames
from titanbet import TitanBet
from victor import Victor
from william import William

class Spider(object):
    """
    Spider class to handle all of spider instances
    """
    def __init__(self):
        pass

    def run(self):
        bet10 = Bet10()
        bet10.run()

        bet365 = Bet365()
        bet365.run()

        bet365Other = Bet365()
        bet365Other.run('Bet365Other', 'bigfreebet1281', 'Porsche911')

        betFred = BetFred()
        betFred.run()

        coral = Coral()
        coral.run()

        eight88 = Eight88()
        eight88.run()

        ladbrokes = LadBrokes()
        ladbrokes.run()

        netbet = Netbet()
        netbet.run()

        paddy = Paddy()
        paddy.run()

        real = RealDealBet()
        real.run()

        stan = StanJames()
        stan.run()

        titanbet = TitanBet()
        titanbet.run()

        victor = Victor()
        victor.run()

        william = William()
        william.run()

if __name__ == "__main__":
    spider = Spider()
    spider.run()