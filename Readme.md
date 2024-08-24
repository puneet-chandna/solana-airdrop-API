
# Solana Token Transfer API Documentation

## Overview

This API provides an interface to transfer SPL tokens on the Solana blockchain. It allows users to specify a destination wallet and the amount of tokens to transfer. The API is built using Flask and communicates with the Solana blockchain via the `solana-py` and `spl-token` libraries.

## Base URL

```
http://localhost:5000/
```

## Environment Setup

Before running the API, ensure the following environment variables are set:

- **`SOLANA_PRIVATE_KEY`**: The private key of the sender in JSON format.
- **`TOKEN_MINT_ADDRESS`**: The address of the SPL token mint.
- **`SENDER_TOKEN_ACCOUNT`**: The sender's associated token account.
- **`DEVNET_URL`**: The Solana cluster endpoint (e.g., "https://api.devnet.solana.com").

## Endpoints

### 1. Transfer Tokens

- **Endpoint**: `/transfer`
- **Method**: `POST`
- **Description**: Transfers a specified amount of SPL tokens from the sender's account to the recipient's wallet.

#### Request Body

- **`destination_wallet`** (string, required): The Solana wallet address of the recipient.
- **`amount`** (float, required): The amount of tokens to transfer. This value should be in the token's base unit (e.g., for a token with 9 decimals, `1.23` represents `1.23 tokens`).

#### Example Request

```json
{
    "destination_wallet": "recipient_wallet_address",
    "amount": 1.23
}
```

#### Response

- **Success (200 OK)**:
  - Returns a JSON object containing the result and transaction ID if the transfer is successful.

  ```json
  {
      "result": "Transaction Successful",
      "transaction_id": "some_txn_id"
  }
  ```

- **Error (500 Internal Server Error)**:
  - Returns a JSON object with an error message if the transfer fails.

  ```json
  {
      "error": "Invalid destination wallet"
  }
  ```

#### Example Response

- **Successful Transfer**:
  ```json
  {
      "result": "Transaction Successful",
      "transaction_id": "3x2zPcsG4r6W1Fuy1tW2QsY4pCm9v1Edgcz6rKz4qv8Z"
  }
  ```

- **Failed Transfer**:
  ```json
  {
      "error": "Insufficient funds"
  }
  ```

#### Error Handling

- **400 Bad Request**: Missing or invalid parameters (e.g., missing `destination_wallet` or `amount`).
- **500 Internal Server Error**: General errors during the transfer process (e.g., invalid wallet, insufficient funds).

## Running the API

To start the API:

1. Set the required environment variables.
2. Run the Flask app:

   ```bash
   python solana-airdrop-api.py
   ```

3. The API will be available at `http://localhost:5000`.

## Dependencies

- `flask`: Web framework used to create the API.
- `solana-py`: Python client library for interacting with the Solana blockchain.
- `spl-token`: Python library for working with Solana SPL tokens.

## Example Use Cases

- **Automated Token Transfers**: Use this API to automate the distribution of tokens to multiple recipients, such as airdrops or reward distributions.
- **Payment Processing**: Integrate this API into a payment gateway that processes SPL token payments.

## Security Considerations

- **Private Key Management**: Ensure the `SOLANA_PRIVATE_KEY` is securely managed and not exposed in the source code or logs.
- **API Rate Limiting**: Consider implementing rate limiting to prevent abuse.
```

