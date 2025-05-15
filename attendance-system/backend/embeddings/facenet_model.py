from keras_facenet import FaceNet
import numpy as np

class FaceEmbedder:
    def __init__(self):
        self.model = FaceNet()
    
    def get_embedding(self, image):
        embedding = self.model.embeddings([image])
        return np.array(embedding[0])