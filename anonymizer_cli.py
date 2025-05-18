#!/usr/bin/env python3
"""
Encrypto-Anonymizer CLI
Command-line interface for anonymizing and encrypting CSV data
"""

import argparse
import pandas as pd
import uuid
from cryptography.fernet import Fernet
import json
from pathlib import Path
import sys


def anonymize_data(csv_path, columns, output_dir, composite_key=True):
    """Anonymize specified columns in a CSV file."""
    
    # Load data
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path}")
    
    # Generate encryption key
    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)
    
    # Initialize mappings
    mapping = {}
    reverse_mapping = {}
    anon_df = df.copy()
    
    if composite_key and len(columns) > 1:
        print("Using composite key for multiple columns...")
        for index in range(len(df)):
            # Create composite key
            composite_parts = []
            for col in columns:
                val = str(df.iloc[index][col])
                composite_parts.append(val)
            
            composite_key = "|".join(composite_parts)
            
            # Check if already mapped
            if composite_key in reverse_mapping:
                anon_id = reverse_mapping[composite_key]
            else:
                anon_id = str(uuid.uuid4())
                encrypted_values = {}
                for i, col in enumerate(columns):
                    encrypted_val = fernet.encrypt(composite_parts[i].encode()).decode()
                    encrypted_values[col] = encrypted_val
                
                mapping[anon_id] = encrypted_values
                reverse_mapping[composite_key] = anon_id
            
            # Apply anonymous ID to all columns
            for col in columns:
                anon_df.loc[index, col] = anon_id
    else:
        print("Using separate mappings per value...")
        for col in columns:
            new_ids = []
            for val in df[col]:
                str_val = str(val)
                
                if str_val in reverse_mapping:
                    anon_id = reverse_mapping[str_val]
                else:
                    anon_id = str(uuid.uuid4())
                    encrypted_val = fernet.encrypt(str_val.encode()).decode()
                    mapping[anon_id] = encrypted_val
                    reverse_mapping[str_val] = anon_id
                
                new_ids.append(anon_id)
            anon_df[col] = new_ids
    
    # Save files
    output_dir.mkdir(exist_ok=True, parents=True)
    
    anon_path = output_dir / "anonymized.csv"
    anon_df.to_csv(anon_path, index=False)
    
    mapping_path = output_dir / "mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)
    
    key_path = output_dir / "key.key"
    with open(key_path, "wb") as f:
        f.write(fernet_key)
    
    print(f"✅ Anonymization complete. Files saved to {output_dir}")
    return anon_path, mapping_path, key_path


def deanonymize_data(anon_path, mapping_path, key_path, output_path=None):
    """Restore original values from anonymized data."""
    
    # Load files
    anon_df = pd.read_csv(anon_path)
    
    with open(mapping_path) as f:
        mapping = json.load(f)
    
    with open(key_path, "rb") as f:
        fernet = Fernet(f.read())
    
    restored_df = anon_df.copy()
    
    # Detect anonymized columns (containing UUIDs)
    import re
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    
    anonymized_columns = []
    for col in anon_df.columns:
        first_val = anon_df[col].dropna().iloc[0] if not anon_df[col].dropna().empty else None
        if first_val and isinstance(first_val, str) and uuid_pattern.match(first_val):
            anonymized_columns.append(col)
    
    print(f"Detected anonymized columns: {anonymized_columns}")
    
    # De-anonymize
    for col in anonymized_columns:
        original_values = []
        for anon_id in anon_df[col]:
            if pd.isna(anon_id):
                original_values.append(None)
            elif anon_id in mapping:
                if isinstance(mapping[anon_id], dict):
                    if col in mapping[anon_id]:
                        encrypted_val = mapping[anon_id][col]
                        decrypted_val = fernet.decrypt(encrypted_val.encode()).decode()
                    else:
                        decrypted_val = anon_id
                else:
                    decrypted_val = fernet.decrypt(mapping[anon_id].encode()).decode()
                original_values.append(decrypted_val)
            else:
                print(f"Warning: No mapping found for ID {anon_id}")
                original_values.append(anon_id)
        
        restored_df[col] = original_values
    
    # Save restored file
    if output_path is None:
        output_path = Path("restored.csv")
    
    restored_df.to_csv(output_path, index=False)
    print(f"✅ Restoration complete. File saved to: {output_path}")
    return restored_df


def main():
    parser = argparse.ArgumentParser(description="Anonymize and encrypt CSV data")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Anonymize command
    anon_parser = subparsers.add_parser('anonymize', help='Anonymize a CSV file')
    anon_parser.add_argument('csv_file', type=Path, help='Path to CSV file')
    anon_parser.add_argument('columns', nargs='+', help='Columns to anonymize')
    anon_parser.add_argument('-o', '--output', type=Path, default=Path('.'), 
                            help='Output directory (default: current directory)')
    anon_parser.add_argument('--separate-keys', action='store_true',
                            help='Use separate keys for each value (default: composite key)')
    
    # De-anonymize command
    deanon_parser = subparsers.add_parser('deanonymize', help='Restore original data')
    deanon_parser.add_argument('anonymized_file', type=Path, help='Path to anonymized CSV')
    deanon_parser.add_argument('mapping_file', type=Path, help='Path to mapping.json')
    deanon_parser.add_argument('key_file', type=Path, help='Path to key.key')
    deanon_parser.add_argument('-o', '--output', type=Path, help='Output file path')
    
    args = parser.parse_args()
    
    if args.command == 'anonymize':
        anonymize_data(
            args.csv_file, 
            args.columns, 
            args.output,
            composite_key=not args.separate_keys
        )
    elif args.command == 'deanonymize':
        deanonymize_data(
            args.anonymized_file,
            args.mapping_file,
            args.key_file,
            args.output
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()