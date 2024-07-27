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

# Load environment variables
PRIVATE_KEY = os.getenv('SOLANA_PRIVATE_KEY')
TOKEN_MINT_ADDRESS = "7fwzSLmfhW9RajxngqUCV3g3t87qoUgnkHRgrK57548B"  # Your custom token's mint address
DEVNET_URL = "https://api.devnet.solana.com"

# Function to load the sender's keypair
def load_keypair():
    return Keypair.from_secret_key(bytes.fromhex(PRIVATE_KEY))

# Function to transfer tokens
async def transfer_token(destination_wallet, amount):
    async with AsyncClient(DEVNET_URL) as client:
        # Load sender's keypair
        sender_keypair = load_keypair()
        
        # Get the sender's token account
        sender_token_account = await AsyncToken.get_associated_token_address(
            program_id=TOKEN_PROGRAM_ID, 
            mint=PublicKey(TOKEN_MINT_ADDRESS),
            owner=sender_keypair.public_key
        )

        # Get or create the recipient's token account
        recipient_token_account = await AsyncToken.get_associated_token_address(
            program_id=TOKEN_PROGRAM_ID, 
            mint=PublicKey(TOKEN_MINT_ADDRESS),
            owner=PublicKey(destination_wallet)
        )

        # Create the transaction
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

        # Send the transaction
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
