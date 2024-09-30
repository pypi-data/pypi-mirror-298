#!/usr/bin/env python3

import garagedoor_service.tools.config as config
import bcrypt

MAX_CACHE_SIZE = 100

__secrets_cache: set[str] = set()


def verify_secret(secret: str, hashed: str) -> bool:
	"""
	Verify a password or key against a bcrypt hash.

    Parameters:
        secret (str): The password or key to verify.
        
    Returns:
        bool: True if the secret matches the hash, False otherwise.
	"""
	return bcrypt.checkpw(secret.encode('utf-8'), hashed.encode('utf-8'))


def verify(api_key: str) -> bool:
    """
    Verify an API key.

    Parameters:
        api_key (str): The API key to verify.
        
    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    if api_key in __secrets_cache:
        return True
    hashes = config.get_api_keys()
    for hash in hashes:
        if verify_secret(api_key, hash):
            if len(__secrets_cache) >= MAX_CACHE_SIZE:
                __secrets_cache.pop()
            __secrets_cache.add(api_key)
            return True
    return False


def clear_cache() -> None:
    """Clear the secrets cache."""
    __secrets_cache.clear()