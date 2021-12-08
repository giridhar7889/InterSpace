from brownie import AdvancedCollectible,network,accounts,config
from scripts.helpful_scripts import fund_advanced_collectible


def main():
    dev=accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    publish_source=False
    advanced_collectible=AdvancedCollectible.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        {"from":dev},
        publish_source=publish_source


    )
    fund_advanced_collectible(advanced_collectible)
    return advanced_collectible


#0x44658e5365aEc7004E91Ce6B841E623736259AdD
#0x422bdAA2DB12Af0dF3E49748b867CD1993d82880
