import os
from COPEX_high_rate_compression_quality_metrics.json_builder import create_summary_json_from_use_case_path
root_directory = os.path.join("data")
satellite_type = "S2_L1C"
test_case_number = 1
create_summary_json_from_use_case_path(root_directory=root_directory, satellite_type=satellite_type,
                                       test_case_number=test_case_number)