import sys
import os

from COPEX_high_rate_compression_quality_metrics import utils

# Ajoute le dossier 'COPEX_high_rate_compression_quality_metrics' au chemin de recherche des modules, pour pouvoir acceder a tout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import COPEX_high_rate_compression_quality_metrics.json_builder as json_builder
import COPEX_high_rate_compression_quality_metrics.metrics as metrics
import COPEX_high_rate_compression_quality_metrics.thematic as tm

root_directory = "data"
dataset_name = "S1_GRD"
test_case_number = 1
nnvvppp_algoname = ["01-01-005_JJ2000FAKE_x250"]
# json_builder.initialize_json(root_directory=root_directory, dataset_name=dataset_name,test_case_number=test_case_number,nnvvppp_algoname=nnvvppp_algoname)


original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                    test_case_number=test_case_number)

#print("original_folder_path=", original_folder_path)

#print("satellite_type=", dataset_name)
for nn_vv_pp in nnvvppp_algoname:
    #print("root_directory = ", type(root_directory))
    #print("dataset_name = ", type(dataset_name))
    #print("test_case_number = ", type(test_case_number))
    #print("nn vv pp = ",type(nn_vv_pp))
    decompressed_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory,
                                                                     dataset_name=dataset_name,
                                                                     test_case_number=test_case_number,
                                                                     nnvvppp_algoname=nn_vv_pp)

    #print("decompressed_folder_path=", decompressed_folder_path)

    json_builder.make_thematic(root_directory,
                               dataset_name,
                               test_case_number,
                               nn_vv_pp,
                               tm.compute_kmeans_score_for_multiband,False,
                               str(original_folder_path),
                               decompressed_folder_path,
                               dataset_name, sample_interval = 10, n_clusters=20, random_state=42)
