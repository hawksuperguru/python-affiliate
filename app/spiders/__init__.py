from flask import Blueprint

spiders = Blueprint('spiders', __name__)

from bet10 import Bet10
from bet365 import Bet365
from betfred import BetFred
from coral import Coral

class Spider(object):
    """
    Spider class to handle all of spider instances
    """
    def __init__(self):
        pass

    def run(self):
        # bet10 = Bet10()
        # bet10.run()

        # bet365 = Bet365()
        # bet365.run()

        # bet365Other = Bet365()
        # bet365Other.run('Bet365Other', 'bigfreebet1281', 'Porsche911')

        # betFred = BetFred()
        # betFred.run()

        coral = Coral()
        coral.run()


if __name__ == "__main__":
    spider = Spider()
    spider.run()