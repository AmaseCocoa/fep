import json
import hashlib
import os
from get_feps import get_feps

# --- Configuration ---
HASH_FILE = "hashes.json"
INPUT_DIR = "./fep/fep"

# --- Core Functions ---
def calculate_sha256(filepath):
    """Calculates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Error: Hash calculation failed. File not found at {filepath}")
        return None

def load_hashes():
    """Loads the hash cache file. Returns an empty dict if it doesn't exist."""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {HASH_FILE}. Starting with empty hashes.")
                return {}
    return {}

def save_hashes(hashes_dict):
    """Saves the given dictionary to the hash cache file."""
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes_dict, f, indent=2, ensure_ascii=False)

def main():
    """Main function to run the batch hashing process."""
    print(f"Starting batch hash generation for directory '{INPUT_DIR}'...")
    
    fep_files = get_feps()
    if not fep_files:
        print("No FEP files found. Exiting.")
        return

    print(f"Found {len(fep_files)} FEPs to process.")
    hashes = load_hashes()
    updated_count = 0

    for fep_filename in fep_files:
        input_path = os.path.join(os.path.join(INPUT_DIR, fep_filename), f"fep-{fep_filename}.md")
        if not os.path.isfile(input_path):
            print(f"Skipping non-file entry: {fep_filename}")
            continue

        fep_id = os.path.splitext(fep_filename)[0]
        current_hash = calculate_sha256(input_path)

        if not current_hash:
            continue # Skip if hash calculation failed

        if hashes.get(fep_id) != current_hash:
            print(f"Updating hash for {fep_id}...")
            hashes[fep_id] = current_hash
            updated_count += 1
        else:
            print(f"Hash for {fep_id} is already up to date.")

    save_hashes(hashes)
    print(f"\nFinished. Updated {updated_count} hash(es) in {HASH_FILE}.")

if __name__ == "__main__":
    main()