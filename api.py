import os
import asyncio
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from solana.keypair import Keypair
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from flask import Flask, request, jsonify

app = Flask(__name__)

PRIVATE_KEY = os.getenv('SOLANA_PRIVATE_KEY')
TOKEN_MINT_ADDRESS = os.getenv('TOKEN_MINT_ADDRESS')  
DEVNET_URL = "https://api.devnet.solana.com"

def load_keypair():
    return Keypair.from_secret_key(bytes.fromhex(PRIVATE_KEY))

async def transfer_token(destination_wallet, amount):
    async with AsyncClient(DEVNET_URL) as client:
        
        sender_keypair = load_keypair()
       
        sender_token_account = await AsyncToken.get_associated_token_address(
            program_id=TOKEN_PROGRAM_ID, 
            mint=PublicKey(TOKEN_MINT_ADDRESS),
            owner=sender_keypair.public_key
        )

        recipient_token_account = await AsyncToken.get_associated_token_address(
            program_id=TOKEN_PROGRAM_ID, 
            mint=PublicKey(TOKEN_MINT_ADDRESS),
            owner=PublicKey(destination_wallet)
        )

        tx = Transaction()
        token = AsyncToken(
            conn=client, 
            pubkey=PublicKey(TOKEN_MINT_ADDRESS),
            program_id=TOKEN_PROGRAM_ID,
            payer=sender_keypair
        )

        tx.add(
            token.transfer(
                source=sender_token_account,
                dest=recipient_token_account,
                owner=sender_keypair.public_key,
                amount=amount,
            )
        )

        
        response = await client.send_transaction(
            tx, 
            sender_keypair, 
            opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed)
        )
        return response

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    destination_wallet = data['destination_wallet']
    amount = data['amount']
    
    try:
        response = asyncio.run(transfer_token(destination_wallet, amount))
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
