'''Inference of DNABarcoder and RDPClassifier'''

import json
import pandas as pd
from mycoai import utils
from mycoai.data import Data
from mycoai.evaluate import Evaluator

utils.WANDB_PROJECT = 'Comparison-alt'

data_folder = 'data/'
results_folder = 'results/'

testsets = ['test1.fasta',
            'test2.fasta',
            # 'trainset_valid.fasta'
            ]

# Evaluating DNABarcoder
for testset_name in testsets:

    name = testset_name[:-6] + " DNABarcoder"

    # Convert to csv and format properly
    classification = pd.read_csv(
        f'{results_folder}dnabarcoder/{testset_name[:-6]}' + 
        f'_prepped.trainset_identified_BLAST.classification', delimiter='\t'
    )
    classification = classification[utils.LEVELS]
    classification['species'] = classification['species'].str.replace(' ', '_')
    
    for lvl in utils.LEVELS:
        classification[lvl] = classification[lvl].replace('unidentified', 
                                                          utils.UNKNOWN_STR)

    # Evaluate
    reference = Data(data_folder + testset_name, allow_duplicates=True)
    evaluator = Evaluator(classification, reference, 
                          wandb_name=f'Results {name}')
    
    train_labels = json.load(open('models/MycoAI_known_labels.json', 'r'))
    for only_classified in [True]:
        for filter_labels in [train_labels]:
            _name = name
            results = evaluator.test(only_classified=only_classified, 
                                     filter_labels=filter_labels)
            if only_classified:
                _name += ' only_classified'
            if filter_labels is not None:
                _name += ' only_trained'
            results.to_csv(results_folder + 'results/' + _name + '.csv')
    evaluator.wandb_finish()

exit()

# Evaluating RDP classifier predictions
for testset_name in testsets:

    name = testset_name[:-6] + " RDP"

    # Convert to csv and format properly
    classification = pd.read_csv(f'{results_folder}rdp/{testset_name[:-6]}.txt',
                                 delimiter='\t', header=None)
    classification = classification[[8,11,14,17,20,23]]
    classification.columns = utils.LEVELS
    classification['species'] = classification['species'].str.split('|').str[0]

    # Evaluate
    reference = Data(data_folder + testset_name, allow_duplicates=True)
    evaluator = Evaluator(classification, reference, 
                          wandb_name=f'Results {name}')
    
    train_labels = json.load(open('models/MycoAI_known_labels.json', 'r'))
    for only_classified in [False, True]:
        for filter_labels in [None, train_labels]:
            _name = name
            results = evaluator.test(only_classified=only_classified, 
                                     filter_labels=filter_labels)
            if only_classified:
                _name += ' only_classified'
            if filter_labels is not None:
                _name += ' only_trained'
            results.to_csv(results_folder + 'results/' + _name + '.csv')

    evaluator.wandb_finish()