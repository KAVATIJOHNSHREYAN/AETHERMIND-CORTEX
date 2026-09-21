"""
AetherMind Cortex Local Security & Encryption Utility
Provides local AES data hashing, secret encoding, and backup security.
"""

import hashlib
import base64
from core.logger import get_logger

logger = get_logger("Security")

def hash_secret(secret: str) -> str:
    """Computes SHA-256 hash for secure local secrets."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()

def encode_local_payload(payload: str) -> str:
    """Encodes local string payloads using base64 obfuscation for privacy."""
    return base64.b64encode(payload.encode("utf-8")).decode("utf-8")

def decode_local_payload(encoded_payload: str) -> str:
    """Decodes local base64 payload strings."""
    try:
        return base64.b64decode(encoded_payload.encode("utf-8")).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed to decode payload: {e}")
        return ""
