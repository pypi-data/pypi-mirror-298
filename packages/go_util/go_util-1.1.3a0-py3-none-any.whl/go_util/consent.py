# src/go_util/consent.py
# (c) Aiden McCormack, 2024. All rights reserved.

import os
import json
from .bookmarks import BOOKMARKS_DIR

CONSENT_FILE = os.path.join(BOOKMARKS_DIR, "config.json")
LICENSE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "LICENSE")

def check_user_consent(consent_file=CONSENT_FILE):
    """Checks if the user has agreed to the license."""
    if not os.path.exists(consent_file):
        return False
    try:
        with open(consent_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('agreed_to_eula', False)
    except json.JSONDecodeError:
        return False

def prompt_user_consent(consent_file=CONSENT_FILE, license_file=LICENSE_FILE):
    """Displays the license agreement and prompts the user for consent."""
    # Read and display the license
    with open(license_file, 'r', encoding='utf-8') as f:
        license_text = f.read()
    print("Please read the following EULA:\n")
    print(license_text)
    print("\nDo you accept the terms of the EULA? (y/n): ", end='')
    response = input().strip().lower()
    if response == 'y':
        # Record consent
        config = {'agreed_to_eula': True}
        with open(consent_file, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        return True
    else:
        print("You must agree to the EULA to use this software.")
        return False
