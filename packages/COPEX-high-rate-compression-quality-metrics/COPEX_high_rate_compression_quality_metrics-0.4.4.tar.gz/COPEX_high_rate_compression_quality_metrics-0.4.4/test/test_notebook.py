import COPEX_high_rate_compression_quality_metrics.json_builder as COPEX_json_builder
from COPEX_high_rate_compression_quality_metrics import utils

root_directory = "data" # permet d'ajouter un chemin en plus si nécéssaire, ne rien mettre si les chemins sont respectés
dataset_name = "S2_L1C" # str
test_case_number = 1 #int qui sera remis sur 3 digit automatiquement, ou str sur 3 digit, définit le test case ou l'on souhaite faire le benshmark
nnvvppp_algoname = ["01-01-004_JJ2000_x200","01-01-005_JJ2000_x250"]  #algo ame au format nnvvpp_algoname

"utils.get_use_case_folder(root_directory,dataset_name,test_case_number,verbose=True)"
"""utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname[0], verbose=True)"""
for nnvvpp in nnvvppp_algoname:
    COPEX_json_builder.make_generic(root_directory=root_directory,
                          dataset_name=dataset_name,
                          test_case_number=test_case_number,
                          nnvvppp_algoname=nnvvpp,verbose=True,computing_block_size=2500)
"""COPEX_json_builder.make_generic(root_directory=root_directory,
                          dataset_name=dataset_name,
                          test_case_number=test_case_number,
                          nnvvppp_algoname=nnvvppp_algoname[0],verbose=True,computing_block_size=2500)"""