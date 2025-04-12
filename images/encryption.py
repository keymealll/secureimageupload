import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from django.conf import settings


class ImageEncryption:
    """Handle image encryption and decryption"""

    @staticmethod
    def generate_key():
        """Generate a secure encryption key"""
        # In production, use a proper key management system
        # This is just a simple example
        return os.urandom(32)  # 256-bit key for AES-256

    @staticmethod
    def encrypt_image(image_data, key=None):
        """
        Encrypt image data using AES-256-CBC

        Args:
            image_data (bytes): The raw image data
            key (bytes, optional): Encryption key. If None, a new key is generated.

        Returns:
            tuple: (encrypted_data, key, iv)
        """
        if key is None:
            key = ImageEncryption.generate_key()

        # Generate a random IV
        iv = os.urandom(16)

        # Create AES cipher with CBC mode
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )

        # Pad the data to be a multiple of block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(image_data) + padder.finalize()

        # Encrypt the data
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Combine IV and encrypted data
        # IV needs to be stored with the encrypted data for decryption
        return encrypted_data, key, iv

    @staticmethod
    def decrypt_image(encrypted_data, key, iv):
        """
        Decrypt encrypted image data

        Args:
            encrypted_data (bytes): The encrypted image data
            key (bytes): The encryption key
            iv (bytes): The initialization vector used for encryption

        Returns:
            bytes: The decrypted image data
        """
        # Create AES cipher with CBC mode
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )

        # Decrypt the data
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data
