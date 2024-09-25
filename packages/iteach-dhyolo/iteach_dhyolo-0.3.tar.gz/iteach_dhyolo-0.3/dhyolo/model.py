from .detect import run as run_detection

class Predict:
    def __init__(self, image_path, model_path):
        self.image_path = image_path
        self.model_path = model_path

    def get_inference(self):
        run_detection(
            weights = self.model_path,
            source = self.image_path
        )
    


