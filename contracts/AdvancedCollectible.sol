pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";


contract AdvancedCollectible is ERC721,VRFConsumerBase{

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;
    enum Planet{MARS,MOON,MERCURY,VENUS,JUPITER,SATURN,NEPTUNE,URANUS}
    event requestedCollectible(bytes32 indexed requestId);
    mapping(bytes32 => address)public requestIdToSender;
    mapping(bytes32 => string)public  requestIdToTokenURI;
    mapping(uint256 => Planet)public tokenIdToPlanet;
    mapping(bytes32 => uint256)public requestIdToTokenId;


    constructor(address _VRFCoordinator,address _LinkToken,bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator,_LinkToken)
    ERC721("interspace","interspace")
    {
        keyHash=_keyhash;
        fee= 0.1 * 10 ** 18;
        tokenCounter=0;
    }
    function createCollectible(string memory tokenURI)
    public returns(bytes32)
    {
        bytes32 requestId=requestRandomness(keyHash,fee);
        requestIdToSender[requestId]=msg.sender;
        requestIdToTokenURI[requestId]=tokenURI;
        emit requestedCollectible(requestId);
    }
    function fulfillRandomness(bytes32 requestId,uint256 randomNumber)internal override{
        address settlementOwner=requestIdToSender[requestId];
        string memory tokenURI=requestIdToTokenURI[requestId];
        uint256 newItemId=tokenCounter;
        _safeMint(settlementOwner,newItemId);
        _setTokenURI(newItemId,tokenURI);
        Planet planet =Planet(randomNumber % 8);
        tokenIdToPlanet[newItemId]=planet;
        requestIdToTokenId[requestId]=newItemId;
        tokenCounter=tokenCounter+1;


    }
    function setTokenURI(uint256 tokenId,string memory _tokenURI) public{
        require(
            _isApprovedOrOwner(_msgSender(),tokenId),
            "ERC721 transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId,_tokenURI);
    }
}
