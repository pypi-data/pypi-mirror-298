
from .detect import run as run_detection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DHYOLODetector:
    """
    A class to encapsulate the YOLO model prediction for object detection.

    Attributes:
        model_path (str): Path to the trained YOLO model weights.

    Methods:
        predict(image_path):
            Runs object detection on the given image using YOLO model.
            Logs errors in case of failure and handles exceptions.
    """
    
    def __init__(self, model_path):
        """
        Initializes DHYOLODetector with the path to the YOLO model weights.
        
        Args:
            model_path (str): Path to the YOLO model.
        """
        self.model_path = model_path

    def predict(self, image_path):
        """
        Runs object detection on the provided image using the YOLO model.
        
        Args:
            image_path (str): Path to the image file (file path or a web url)
        
        Returns:
            result: The detection output from the YOLO model.
        
        Raises:
            FileNotFoundError: If the image file does not exist.
            Exception: For any general errors during prediction.
        """
        try:
            logger.info(f"Starting prediction for image: {image_path} with model: {self.model_path}")
            
            # Ensure image_path is valid
            if not isinstance(image_path, str) or not image_path:
                raise ValueError("Invalid image path provided.")
            
            # Run YOLO detection
            result = run_detection(
                weights=self.model_path,
                source=image_path
            )

            logger.info(f"Prediction completed successfully for image: {image_path}")
            return result
        
        except FileNotFoundError as e:
            logger.error(f"Image file not found: {image_path}. Exception: {e}")
            raise
        
        except Exception as e:
            logger.error(f"An error occurred during prediction. Exception: {e}")
            raise

