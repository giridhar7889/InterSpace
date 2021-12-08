#!/usr/bin/python3
from brownie import AdvancedCollectible, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_planet
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"



def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        planet=get_planet(advanced_collectible.tokenIdToPlanet(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("setting tokenURI of {}".format(token_id))
            ipfs_address = "https://ipfs.io/ipfs/QmcfzBL6dk9zGRusJGAL3mDchjv32f2LxYzvuADUCtqRxU?filename=0-MARS.json"
            set_tokenURI(token_id,advanced_collectible,ipfs_address)
        else:
            print("skipping this")    


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
