import easyocr
import os
import logging
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageTextRecognizer:
    def __init__(self, lang='en'):
        self.reader = easyocr.Reader([lang], gpu=False)
        logging.info(f"Initialized EasyOCR with language: {lang}")

    def preprocess_image(self, image_path, resize=None, enhance_contrast=1.5, sharpen=True):
        logging.info(f"Preprocessing image: {image_path}")
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if resize:
                    img = img.resize(resize)
                
                if enhance_contrast != 1.0:
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(enhance_contrast)

                if sharpen:
                    img = img.filter(ImageFilter.SHARPEN)

                return np.array(img)
        except Exception as e:
            logging.error(f"Error preprocessing image: {str(e)}")
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Unable to open image: {image_path}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img

    def detect_text(self, image):
        logging.info("Detecting text in the image")
        result = self.reader.readtext(image)
        return result

    def extract_alphanumeric(self, detections):
        logging.info("Extracting alphanumeric and special characters text")
        alphanumeric_results = []
        for detection in detections:
            bbox, text, prob = detection
            alphanumeric_text = re.sub(r'[^\w\s.,!?@#$%^&*()_+-=]', '', text)
            if alphanumeric_text:
                alphanumeric_results.append((bbox, alphanumeric_text, prob))
        return alphanumeric_results

    def post_process(self, detections, min_confidence=0.5, min_length=2):
        logging.info("Post-processing detected text")
        processed_results = []
        for detection in detections:
            bbox, text, prob = detection
            if prob >= min_confidence and len(text) >= min_length:
                processed_results.append((bbox, text, prob))
        return processed_results

    def recognize_text(self, image_path):
        if not os.path.exists(image_path):
            logging.error(f"Image file not found: {image_path}")
            return []

        try:
            preprocessed_image = self.preprocess_image(image_path)
            detections = self.detect_text(preprocessed_image)
            alphanumeric_results = self.extract_alphanumeric(detections)
            final_results = self.post_process(alphanumeric_results)
            
            logging.info(f"Recognized text: {final_results}")
            return final_results
        except Exception as e:
            logging.error(f"Error recognizing text: {str(e)}")
            return []