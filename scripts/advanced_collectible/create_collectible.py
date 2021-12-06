from brownie import AdvancedCollectible,network,accounts,config
from scripts.helpful_scripts import get_planet
import time


def main():
    dev=accounts.add(config['wallets']['from_key'])
    advanced_collectible=AdvancedCollectible[len(AdvancedCollectible)-1]
    transaction=advanced_collectible.createCollectible("None",{"from":dev})
    transaction.wait(1)
    requestId=transaction.events["requestedCollectible"]["requestId"]
    token_id=advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(60)
    planet=get_planet(advanced_collectible.tokenIdToPlanet(token_id))
    print("You just brought a settlement of token id {} in {} planet".format(token_id,planet))

