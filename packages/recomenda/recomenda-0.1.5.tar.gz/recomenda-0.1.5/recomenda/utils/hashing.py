# ./recomenda/utils/hashing.py

from typing import Any, Dict, List, Union
import hashlib


def generate_hash(data: Union[Dict[str, Any], str]) -> str:
    """
    Generate a SHA-256 hash for a given input.

    The input can be a dictionary, string, or any other object that can be 
    converted to a string representation.
    """
    if isinstance(data, dict):
        data_string = str(sorted(data.items()))
    else:
        data_string = str(data)
    return hashlib.sha256(data_string.encode()).hexdigest()


def update_hashes(
    data_list: List[Dict[str, Any]], current_hashes: Dict[str, str]
) -> (List[Dict[str, Any]], Dict[str, str]):
    """
    Update the hashes for a list of input data and return the items that need 
    updating along with the new hashes.

    :param data_list: List of input data to be hashed.
    :param current_hashes: Existing hashes for the input data.
    :return: A tuple containing:
             - items_to_update: List of new or modified data that need re-hashing.
             - updated_hashes: Updated dictionary with new data hashes.
    """
    updated_hashes = {generate_hash(data): data for data in data_list}
    items_to_update = [
        data for hash_key, data in updated_hashes.items()
        if hash_key not in current_hashes or current_hashes[hash_key] != hash_key
    ]
    return items_to_update, updated_hashes
