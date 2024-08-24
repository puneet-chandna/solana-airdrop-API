import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from solana-airdrop-api import app 

class TransferAPITestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('solana-airdrop-api.transfer_token')  # Mock the transfer_token function
    def test_transfer_success(self, mock_transfer_token):
        # Mock response from the transfer_token function
        mock_transfer_token.return_value = {
            'result': 'Transaction Successful',
            'transaction_id': 'some_txn_id'
        }

        # Mock input data
        mock_data = {
            "destination_wallet": "recipient_wallet_address",
            "amount": 1.23  # Represents 1.23 tokens
        }

        # Send POST request to the /transfer endpoint
        response = self.app.post('/transfer', json=mock_data)

        # Assert the status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json)
        self.assertIn('transaction_id', response.json)

    @patch('solana-airdrop-api.transfer_token')  # Mock the transfer_token function
    def test_transfer_invalid_wallet(self, mock_transfer_token):
        # Simulate an exception for an invalid wallet
        mock_transfer_token.side_effect = Exception("Invalid destination wallet")

        # Mock input data
        mock_data = {
            "destination_wallet": "invalid_wallet_address",
            "amount": 1.23  # Represents 1.23 tokens
        }

        # Send POST request to the /transfer endpoint
        response = self.app.post('/transfer', json=mock_data)

        # Assert the status code and error message
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Invalid destination wallet")

    @patch('solana-airdrop-api.transfer_token')  # Mock the transfer_token function
    def test_transfer_insufficient_funds(self, mock_transfer_token):
        # Simulate an exception for insufficient funds
        mock_transfer_token.side_effect = Exception("Insufficient funds")

        # Mock input data
        mock_data = {
            "destination_wallet": "recipient_wallet_address",
            "amount": 1000000  # Unrealistically large amount
        }

        # Send POST request to the /transfer endpoint
        response = self.app.post('/transfer', json=mock_data)

        # Assert the status code and error message
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Insufficient funds")

if __name__ == '__main__':
    unittest.main()

def test_transfer_missing_parameters(self):
    # Missing 'destination_wallet'
    mock_data = {"amount": 1.23}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)

    # Missing 'amount'
    mock_data = {"destination_wallet": "recipient_wallet_address"}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)

def test_transfer_invalid_amount_type(self):
    # 'amount' should be a number, not a string
    mock_data = {"destination_wallet": "recipient_wallet_address", "amount": "one hundred"}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)


def test_transfer_zero_or_negative_amount(self):
    # Test zero amount
    mock_data = {"destination_wallet": "recipient_wallet_address", "amount": 0}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)
    
    # Test negative amount
    mock_data = {"destination_wallet": "recipient_wallet_address", "amount": -10}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)


def test_transfer_large_amount(self):
    mock_data = {"destination_wallet": "recipient_wallet_address", "amount": 10**12}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 500)  # Assuming this triggers an exception
    self.assertIn('error', response.json)


def test_transfer_invalid_wallet_format(self):
    mock_data = {"destination_wallet": "invalid_wallet_format", "amount": 1.23}
    response = self.app.post('/transfer', json=mock_data)
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)
