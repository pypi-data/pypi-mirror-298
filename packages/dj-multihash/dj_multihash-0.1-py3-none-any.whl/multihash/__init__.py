import os
import string
import base64
import random
import json

def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Generate a dictionary for all printable characters
def create_char_dict():
    all_characters = string.printable  # Includes letters, digits, punctuation, whitespace, etc.
    char_dict_list = [{char: generate_random_string(10)} for char in all_characters]
    return char_dict_list

# Chemin du fichier JSON
json_file_path = os.path.expanduser("~/multihash.json")

# Vérifier si le fichier existe et s'il est vide
if not os.path.exists(json_file_path) or os.path.getsize(json_file_path) == 0:
    json_prepared = create_char_dict()
    
    # Ajouter la chaîne salt_string encodée
    json_prepared.append({"salt_string": base64.b64encode(os.urandom(16)).decode('utf-8')})

    # Écriture dans le fichier JSON en utilisant un bloc `with`
    with open(json_file_path, "w") as file:
        json.dump(json_prepared, file, indent=2)

from .dj_multihash import hashstring256
