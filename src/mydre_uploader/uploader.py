#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload functionality for myDRE workspace.

This module handles the secure file upload process to myDRE workspaces.
"""

import requests
from datetime import datetime
from azure.storage.blob import ContainerClient
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(pin):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'static_salt',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(pin.encode()))
    return key

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

class Upload:
    """Handles secure file uploads to myDRE workspace."""
    def __init__(self, ws_name, ws_description, ws_key, tenant_key, user_name):
        self.workspace_name = ws_name
        self.workspace_description = ws_description
        self.workspace_key = ws_key
        self.tenant_key = tenant_key
        self.uploader = user_name 
        self.BASE_URL = 'https://andreanl-api-management.azure-api.net/v1'
        self.container_location = ''
        
        # Get the path to the favicon
        self.icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'favicon.ico')

    def getHeaders(self):
        return {
            'Api-Key': self.workspace_key,
            'Ocp-Apim-Subscription-Key': self.tenant_key
        }

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(str(method).upper(), url, headers=self.getHeaders(), json=data) 
        response.raise_for_status()
        return response

    def create_workspace_container(self):
        timestamp = f'{datetime.now():%Y%m%d %H%M%S}'
        title = f'{timestamp} {self.workspace_name}'
        endpoint = f"/api/workspace/{self.workspace_name}/files/containers"
        url = f"{self.BASE_URL}{endpoint}"
    
        params = {'title': title}
        response = requests.post(url, headers=self.getHeaders(), params=params)
        response.raise_for_status()  
        self.container_location = response.headers['Location']
        
    def commit_workspace_container(self):
        container_identifier = self.container_location.rsplit('/', 1)[-1]
        endpoint = f"/api/workspace/{self.workspace_name}/files/containers/{container_identifier}"
        url = f"{self.BASE_URL}{endpoint}"
    
        response = requests.patch(url, headers=self.getHeaders())
        response.raise_for_status()
        return response

    def file2(self, local_file_path):
        container_client = ContainerClient.from_container_url(self.container_location)
        file_name = os.path.basename(local_file_path)
        with open(local_file_path, "rb") as file_to_upload:
            container_client.upload_blob(file_name, file_to_upload, overwrite=True) 