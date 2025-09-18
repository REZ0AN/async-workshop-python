import hashlib
import os

def are_csv_files_identical(file_paths):
    """
    Checks if all given CSV files have identical contents by comparing their SHA-256 hashes.
    
    Args:
    file_paths (list of str): List of paths to the CSV files.
    
    Returns:
    bool: True if all files are identical, False otherwise.
    """
    if not file_paths:
        return True  # No files to compare, trivially true
    
    # Compute hash for the first file as reference
    reference_hash = compute_file_hash(file_paths[0])
    
    # Compare hashes of remaining files
    for path in file_paths[1:]:
        if compute_file_hash(path) != reference_hash:
            return False
    return True

def compute_file_hash(file_path, chunk_size=8192):
    """
    Computes SHA-256 hash of a file in chunks for efficiency.
    
    Args:
    file_path (str): Path to the file.
    chunk_size (int): Size of chunks to read (default 8KB).
    
    Returns:
    str: Hex digest of the hash.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()

# Example usage
files_to_compare = ['listing_languages_1.csv', 'listing_languages_2.csv', 'listing_languages_3.csv']
if are_csv_files_identical(files_to_compare):
    print("All CSV files are identical.")
else:
    print("CSV files differ.")