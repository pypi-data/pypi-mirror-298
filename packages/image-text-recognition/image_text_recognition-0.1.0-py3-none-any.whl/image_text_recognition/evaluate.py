from .image_text_recognition import ImageTextRecognizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from difflib import SequenceMatcher
import os

def calculate_edit_distance(predicted, actual):
    return SequenceMatcher(None, predicted, actual).ratio()

def evaluate_model(test_dir, ground_truth):
    recognizer = ImageTextRecognizer()
    predictions = []
    true_labels = []
    edit_distances = []

    for image_file, true_text in ground_truth.items():
        image_path = os.path.join(test_dir, image_file)
        result = recognizer.recognize_text(image_path)
        predicted_text = ' '.join([text for _, text, _ in result])
        
        predictions.append(predicted_text)
        true_labels.append(true_text)

        edit_distances.append(calculate_edit_distance(predicted_text, true_text))
    
    avg_edit_distance = sum(edit_distances) / len(edit_distances)
    
    all_true_chars = ''.join(true_labels)
    all_predicted_chars = ''.join(predictions)

    max_len = max(len(all_true_chars), len(all_predicted_chars))
    all_true_chars = all_true_chars.ljust(max_len)
    all_predicted_chars = all_predicted_chars.ljust(max_len)

    accuracy = accuracy_score(list(all_true_chars), list(all_predicted_chars))
    precision = precision_score(list(all_true_chars), list(all_predicted_chars), average='weighted', zero_division=0)
    recall = recall_score(list(all_true_chars), list(all_predicted_chars), average='weighted', zero_division=0)
    f1 = f1_score(list(all_true_chars), list(all_predicted_chars), average='weighted', zero_division=0)

    return {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "Average Edit Distance (similarity)": avg_edit_distance
    }
    