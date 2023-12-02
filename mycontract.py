from thirdweb import ThirdwebSDK
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3
import os
from thirdweb.types.settings.metadata import NFTCollectionContractMetadata

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

RPC_URL = "https://rpc-mumbai.matcvigil.com"

provider = Web3(Web3.HTTPProvider(RPC_URL))

signer = Account.from_key(PRIVATE_KEY)

sdk = ThirdwebSDK(provider, signer)

sdk.deployer.delpoy_nft_collection(NFTCollectionContractMetadata(name="Smart Contract"))
