A Python package for recognizing and evaluating text in images.

## Installation

```
pip install image-text-recognition
```

## Usage

```python
from image_text_recognition import ImageTextRecognizer, evaluate_model, generate_test_images

# Recognize text in an image
recognizer = ImageTextRecognizer()
image_path = "path/to/your/image.jpg"
results = recognizer.recognize_text(image_path)

for bbox, text, probability in results:
    print(f"Text: {text}, Probability: {probability}")

# Generate test images
test_texts = ["Hello World", "Python Code", "OpenCV"]
generate_test_images("test_images", test_texts)

# Evaluate the model
ground_truth = {
    "test1.jpg": "Hello World",
    "test2.jpg": "Python Code",
    "test3.jpg": "OpenCV"
}
evaluation_results = evaluate_model("test_images", ground_truth)
print(evaluation_results)
```

## License

This project is licensed under the MIT License.
