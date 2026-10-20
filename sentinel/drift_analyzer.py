import numpy as np

class DriftAnalyzer:
    def __init__(self, similarity_threshold: float = 0.75):
        self.threshold = similarity_threshold

    def calculate_cosine_similarity(self, vec_a: list, vec_b: list) -> float:
        a = np.array(vec_a)
        b = np.array(vec_b)
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    def detect_goal_drift(self, baseline_embedding: list, current_embedding: list) -> tuple[bool, float]:
        similarity = self.calculate_cosine_similarity(baseline_embedding, current_embedding)
        has_drifted = similarity < self.threshold
        return has_drifted, similarity
