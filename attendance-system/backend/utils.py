import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match(input_embedding, stored_embeddings):
    
    input_embedding = np.array(input_embedding).reshape(1, -1)  # Make it 2D
    embeddings = np.array([embedding for _, embedding in stored_embeddings])
    
    similarities = cosine_similarity(input_embedding, embeddings)[0]  # Shape: (num_users,)
    
    best_idx = np.argmax(similarities)
    best_user_id = stored_embeddings[best_idx][0]
    best_score = similarities[best_idx]

    return best_user_id, best_score