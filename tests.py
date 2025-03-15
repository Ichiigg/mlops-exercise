import os
import app
import json
from pathlib import Path

def test_model_file_created():
    app.main()  # Assuming the main function encapsulates the training logic
    assert os.path.exists('models/model.pkl')

def test_model_score():
    # Ensure model_scores.json exists
    scores_file = Path('model_scores.json')
    if not scores_file.exists():
        with open(scores_file, 'w') as f:
            json.dump([{"version": "1.0", "score": 0.0}], f)
    
    score = app.main()  # Get current model score
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

    # Load and compare with historical scores
    with open(scores_file, 'r') as f:
        model_scores = json.load(f)
    
    if model_scores:
        latest_score = model_scores[-1]['score']
        assert score >= latest_score, f"Model performance degraded: current={score}, previous={latest_score}"

def update_model_scores(score):
    """Update model scores file with new version and score"""
    scores_file = Path('model_scores.json')
    
    with open(scores_file, 'r') as f:
        model_scores = json.load(f)
    
    # Calculate new version
    latest_version = model_scores[-1]['version'].split('.')
    new_version = f"{latest_version[0]}.{int(latest_version[1]) + 1}"
    
    # Add new score
    model_scores.append({
        "version": new_version,
        "score": score
    })
    
    with open(scores_file, 'w') as f:
        json.dump(model_scores, f, indent=4)
    
    return new_version