from brownie import AdvancedCollectible,network,accounts,config
from metadata import sample_metadata
from scripts.helpful_scripts import get_planet
from pathlib import Path
import os
import requests,json

def main():
    dev=accounts.add(config["wallets"]["from_key"])
    advanced_collectible=AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_tokens=advanced_collectible.tokenCounter()
    print(number_of_tokens)
    write_metadata(number_of_tokens,advanced_collectible)


def write_metadata(number_of_tokens,nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata=sample_metadata.metadata_template
        planet=get_planet(nft_contract.tokenIdToPlanet(token_id))
        metadata_filename="./metadata/{}/".format(network.show_active())+str(token_id)+"-"+planet+".json"

        if Path(metadata_filename).exists():
            print("{} already found!!".format(metadata_filename))
        else:
            print("creating metadata file {}".format(metadata_filename))
            collectible_metadata["name"]="space settlement at {}".format(get_planet(nft_contract.tokenIdToPlanet(token_id)))
            collectible_metadata["description"] = "space settlement located at {} in the interspace!".format(get_planet(nft_contract.tokenIdToPlanet(token_id)))
            print(collectible_metadata)
            os.environ['UPLOAD_IPFS'] = 'true'
            image_to_upload=None
            if os.getenv('UPLOAD_IPFS')=="true":
                image_path="./images/{}.png".format(planet.lower())
                print(image_path)
                image_to_upload=upload_to_ipfs(image_path)
                collectible_metadata["image"]=image_to_upload

            with open(metadata_filename,"w") as file:
                json.dump(collectible_metadata,file)
            if(os.getenv("UPLOAD_IPFS")=="true"):
                upload_to_ipfs(metadata_filename)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary=fp.read()
        ipfs_url="http://127.0.0.1:5001"
        response=requests.post(ipfs_url+"/api/v0/add",files={"file":image_binary})
        print(response.json())
        ipfs_hash=response.json()["Hash"]
        filename=filepath.split("/")[-1:][0]
        uri="https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash,filename)
        print(uri)
        return uri

    return None

