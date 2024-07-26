import csv
import re
from pymol import cmd

def extract_chains_from_csv(csv_file, pdb_file, delimiter=';'):
    # Load the PDB file
    cmd.load(pdb_file, "original_structure")
    cmd.show('surface', 'original_structure')

    # Read the CSV file
    with open(csv_file, 'r') as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        
        for row in csv_reader:
            chain_info = row['Chains']
            extract_name = row['extract_name']
            color = row['color']
            
            # Extract the chain identifier from within square brackets
            match = re.search(r'\[(.*?)\]', chain_info)
            if match:
                chain_id = match.group(1)
                
                # Create a selection for the chain
                selection = f"original_structure and chain {chain_id}"

                # Color the extract selection
                cmd.color(color,selection)
                
                # Extract the chain and create a new object with the associated name
                cmd.create(extract_name, selection)
                
                
                
                print(f"Extracted chain {chain_id} as {extract_name}")
    
    # Remove the original structure to leave only the extracted chains
    cmd.delete("original_structure")

cmd.extend('extract_chains_from_csv', extract_chains_from_csv)