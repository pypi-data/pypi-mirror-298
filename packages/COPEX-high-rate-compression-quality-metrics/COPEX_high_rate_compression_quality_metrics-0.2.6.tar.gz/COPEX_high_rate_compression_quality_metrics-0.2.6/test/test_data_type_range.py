# Fonction de test pour différents types de données
import numpy as np

from COPEX_high_rate_compression_quality_metrics.metrics import get_data_type_range


def test_get_data_type_range():
    # Liste des types de données à tester
    data_types = [np.int8, np.int16, np.int32, np.int64, np.float16, np.float32]

    # Tester avec verbose=False
    print("Test avec verbose=False:")
    for dtype in data_types:
        try:
            range_val = get_data_type_range(dtype, verbose=False)
        except:
            continue
        print(f"Type {dtype.__name__}: Range = {range_val}")

    print("\nTest avec verbose=True:")
    # Tester avec verbose=True pour afficher les détails min/max
    for dtype in data_types:
        range_val = get_data_type_range(dtype, verbose=True)
        print(f"Type {dtype.__name__}: Range = {range_val}")

test_get_data_type_range()