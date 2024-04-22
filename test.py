def jaccard_similarity(set1: set, set2: set) -> float:
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0


def coincidence_index(item1_params, item2_params):
    set1 = set(item1_params)
    set2 = set(item2_params)
    return jaccard_similarity(set1, set2)


# Example usage:
item1_params = []
item2_params = []
coincidence = coincidence_index(item1_params, item2_params)
print("Coincidence index:", coincidence)