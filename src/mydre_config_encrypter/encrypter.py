#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Encryption functionality for myDRE configuration files.
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json

class ConfigEncrypter:
    """Handles encryption of myDRE configuration files."""

    def __init__(self):
        """Initialize the ConfigEncrypter."""
        self._salt = b'static_salt'  # In production, use a secure random salt
        self._min_pin_length = 6

    def derive_key(self, pin: str) -> bytes:
        """Derive an encryption key from a PIN."""
        if len(pin) < self._min_pin_length:
            raise ValueError(f"PIN must be at least {self._min_pin_length} characters long")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(pin.encode()))

    def encrypt_data(self, data: str, key: bytes) -> str:
        """Encrypt data using the provided key."""
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()

    def save_config(self, pin: str, ws_name: str, ws_description: str,
                   ws_key: str, tenant_key: str, user_name: str,
                   filename: str) -> None:
        """Create and save an encrypted configuration file."""
        if not all([pin, ws_name, ws_description, ws_key, tenant_key, user_name, filename]):
            raise ValueError("All fields must be filled")

        encryption_key = self.derive_key(pin)
        
        encrypted_data = {
            "WORKSPACE_NAME": ws_name,
            "WORKSPACE_DESCRIPTION": self.encrypt_data(ws_description, encryption_key),
            "WORKSPACE_KEY": self.encrypt_data(ws_key, encryption_key),
            "SUBSCRIPTION_KEY": self.encrypt_data(tenant_key, encryption_key),
            "USER_NAME": self.encrypt_data(user_name, encryption_key)
        }

        if not filename.lower().endswith('.json'):
            filename += '.json'

        try:
            with open(filename, "w") as f:
                json.dump(encrypted_data, f, indent=4)
        except Exception as e:
            raise IOError(f"Failed to save file: {str(e)}")