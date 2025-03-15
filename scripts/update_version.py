#!/usr/bin/env python
import json
import sys
import os
from pathlib import Path

def update_version(score):
    """
    Updates model_scores.json with a new version entry
    
    Args:
        score (float): The current model score
        
    Returns:
        str: The new version number
    """
    scores_file = Path('model_scores.json')
    
    # Create file if it doesn't exist
    if not scores_file.exists():
        with open(scores_file, 'w') as f:
            json.dump([{"version": "1.0", "score": float(score)}], f, indent=4)
        return "1.0"
    
    # Read existing data
    with open(scores_file, 'r') as f:
        model_scores = json.load(f)

    # Get latest version and increment
    latest_version = model_scores[-1]['version'].split('.')
    new_version = f'{latest_version[0]}.{int(latest_version[1]) + 1}'

    # Add new entry
    model_scores.append({
        'version': new_version,
        'score': float(score)
    })

    # Write back
    with open(scores_file, 'w') as f:
        json.dump(model_scores, f, indent=4)
        
    return new_version

if __name__ == "__main__":
    if len(sys.argv) > 1:
        score = float(sys.argv[1])
        new_version = update_version(score)
        print(new_version)
    else:
        print("Please provide a score")
        sys.exit(1) 