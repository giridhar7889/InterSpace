from brownie import AdvancedCollectible,accounts,config,interface,network


def get_planet(planet_number):
    switch={0:'MARS',1:'MOON',2:'MERCURY',3:'VENUS',4:'JUPITER',5:'SATURN',6:'NEPTUNE',7:'URANUS'}
    return switch[planet_number]

def fund_advanced_collectible(nft_contract):
    dev=accounts.add(config['wallets']['from_key'])
    link_token=interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token']
    )
    link_token.transfer(nft_contract,100000000000000000,{"from":dev})