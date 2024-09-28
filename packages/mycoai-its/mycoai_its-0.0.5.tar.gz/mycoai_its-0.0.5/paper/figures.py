'''Produces figures for the paper'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mycoai import utils
import plotly.express as px

plotly_color_scale = px.colors.qualitative.Plotly
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plotly_color_scale)

results_folder = 'results/'

# # Baseline comparison
# testsets = { # 'Validation': 'trainset_valid',
#             'Test set 1': 'test1',
#             'Test set 2': 'test2'}

# methods = {'MycoAI-CNN': 'MycoAI-multi-CNN-Vu-HLS',
#            'MycoAI-BERT': 'MycoAI-multi-BERT-medium-HLS',
#            'DNABarcoder (all)': 'DNABarcoder',
#            'DNABarcoder (identified)': 'DNABarcoder only_classified',
#            'RDP classifier': 'RDP'} 

# metrics = ['Accuracy', 'Precision', 'Recall']


# for only_trained in ['', ' only_trained']:

#     if only_trained:
#         methods = {'MycoAI-CNN': 'MycoAI-multi-CNN-Vu-HLS',
#            'MycoAI-BERT': 'MycoAI-multi-BERT-medium-HLS',
#            'DNABarcoder': 'DNABarcoder',
#            'DNABarcoder (identified only)': 'DNABarcoder only_classified',} 

#     else:
#         methods = {'MycoAI-CNN': 'MycoAI-multi-CNN-Vu-HLS',
#            'MycoAI-BERT': 'MycoAI-multi-BERT-medium-HLS',
#            'DNABarcoder': 'DNABarcoder',
#            'DNABarcoder (identified only)': 'DNABarcoder only_classified',
#            'RDP classifier': 'RDP'} 


#     results = pd.DataFrame()
#     for testset_name in testsets:

#         test_file = testsets[testset_name]

#         for method_name in methods:

#             row = pd.read_csv(
#                 results_folder + 
#                 f'results/{test_file} {methods[method_name]}{only_trained}.csv'
#             )
#             row['testset_name'] = [testset_name]
#             row['method_name'] = [method_name]
#             results = pd.concat([results, row])
    
#     figure, axs = plt.subplots(len(metrics), len(testsets), figsize=(12,6))
#     width = 0.2

#     for i, metric in enumerate(metrics):
        
#         for j, testset_name in enumerate(testsets):

#             axs[0,j].set_title(testset_name)
#             axs[i,j].set_axisbelow(True)
#             axs[i,j].grid(axis='y', which='major')

#             multiplier = 0
#             for method in methods:
#                 data = results[(results['method_name'] == method) &
#                             (results['testset_name'] == testset_name)]
#                 columns = [f'{metric}|test|{lvl}' for lvl in utils.LEVELS]
#                 data = data[columns].iloc[0].values
#                 offset = width*multiplier

#                 if method == 'DNABarcoder (identified only)':
#                     offset -= width
#                     bar = axs[i,j].bar(
#                         x = np.arange(len(utils.LEVELS)) + offset,
#                         height = data,
#                         width = width,
#                         label = method,
#                         alpha = 0.4,
#                         color = bar[0].get_facecolor()
#                     )
#                 else:
#                     bar = axs[i,j].bar(
#                         x = np.arange(len(utils.LEVELS)) + offset,
#                         height = data,
#                         width = width,
#                         label = method
#                     )
#                     multiplier += 1
            
#             axs[i,0].set_ylabel(metric.capitalize())
#             if i < len(metrics)-1:
#                 axs[i,j].set_xticks([])
#             else:
#                 axs[i,j].set_xticks(np.arange(len(utils.LEVELS))+width,utils.LEVELS)
#             axs[i,j].set_ylim(0, 1.05)
#             axs[i,j].set_yticks(np.arange(1.05), minor=True)
    
#     handles, labels = axs[0,0].get_legend_handles_labels()
#     figure.legend(handles, labels, ncols=5, loc='upper left')
#     figure.tight_layout(rect=(0,0,1,0.95)) 
#     plt.savefig(f'baseline_comparison{only_trained}.png')
#     plt.savefig(f'baseline_comparison{only_trained}.pdf')

# Latent spaces
import torch
from mycoai.data import Data
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# utils.set_device('cuda:1')
model_folder = 'C:/Users/luukr/Downloads/'

figure, axs = plt.subplots(1, 1, figsize=(7,5))

setting = {
    # 'Single-head + LS': ('single', 'SLS'),
    'Multi-head + HLS': ('multi', 'HLS')
}

arch = {
    # 'MycoAI-BERT': 'BERT-medium',
    'MycoAI-CNN': 'CNN-Vu'
}

for i, x in enumerate(arch):

    for j, y in enumerate(setting):

        model_file = f'MycoAI-BERT.pt'
        model = torch.load(model_folder + model_file, utils.DEVICE)
        _, data = Data("C:/Users/luukr/Downloads/transfer_2851303_files_7f7e35a9/SH_tax.fasta").train_valid_split(0.1)
        _, unknown_data = Data("C:/Users/luukr/Downloads/transfer_2851303_files_7f7e35a9/SRR12386025_panicum.fasta", allow_duplicates=True,
                            tax_parser=None).train_valid_split(0.1)
        latent_repr1 = model.latent_space(data)
        latent_repr2 = model.latent_space(unknown_data)
        latent_repr = np.concatenate((latent_repr1, latent_repr2), axis=0)
        latent_repr = PCA(50).fit_transform(latent_repr)
        latent_repr = TSNE().fit_transform(latent_repr)
        data = data.data
        unknown_data = unknown_data.data
        data['Dim 1'] = latent_repr[:len(data),0]
        data['Dim 2'] = latent_repr[:len(data),1]
        unknown_data['Dim 1'] = latent_repr[len(data):,0]
        unknown_data['Dim 2'] = latent_repr[len(data):,1]
    
        phyla = (data.groupby('phylum', as_index=False)
                .count().sort_values('id', ascending=False)
                .head(9)['phylum'].values)
        data.loc[~data["phylum"].isin(phyla), 'phylum'] = "Other"

        for phylum in data['phylum'].unique():
            if phylum == "Other" or phylum == "?": 
                continue
            axs.scatter('Dim 1','Dim 2',data=data[data['phylum']==phylum], 
                            s=3, label=phylum, rasterized=True)
        axs.scatter('Dim 1','Dim 2', s=3, label='Other', rasterized=True,
            data=data[(data['phylum']=='Other')|(data['phylum']=='?')])
        axs.scatter('Dim 1','Dim 2',data=unknown_data, rasterized=True,
                         color='black', s=1, label='SRR12386025_panicum')
        axs.set_xticks([])
        axs.set_yticks([])

        # axs[0,j].set_title(y)
        # axs[i,0].set_ylabel(x, size='large')

handles, labels = axs.get_legend_handles_labels()
legend = figure.legend(handles, labels, loc='center right', markerscale=4.0,
                       title="Phylum")
legend.get_frame().set_linewidth(0.0)
legend._legend_box.align = "left"
figure.tight_layout(rect=(0,0,0.7,1))
plt.savefig(f'duong.png', dpi=300)
# plt.savefig(f'cnn_vs_bert_latent_spaces.pdf', dpi=300)
    
# # Hierarchical label smoothing comparison
# models = {'Multi-head + HLS':  'MycoAI-multi-BERT-medium-HLS',
#           'Multi-head':        'MycoAI-multi-BERT-medium-SLS',
#           'Single-head + HLS': 'MycoAI-single-BERT-medium-HLS', 
#           'Single-head':       'MycoAI-single-BERT-medium-SLS'}

# width = 1/5
# multiplier = 0
# figure, ax = plt.subplots(1, figsize=(8,2.5))
# subtract = 0
# ax.grid(axis='y', which='major')
# ax.set_axisbelow(True)

# for i, model in enumerate(models):

#     for parents_inferred in [False, True]:

#         if model.startswith('Single-head') and not parents_inferred:
#             continue
#         modelname = models[model]
#         if model.startswith('Multi-head') and parents_inferred:
#             modelname += ' parents inferred'

#         data = pd.read_csv(results_folder + 'results/trainset_valid ' + 
#                            modelname + '.csv')
#         data = data[[f'Accuracy|test|{lvl}' for lvl in utils.LEVELS]]
#         data = data.iloc[0].values

#         offset = width*multiplier
#         if not parents_inferred:
#             ax.bar(np.arange(6) + offset, data, width, 
#                    color=plotly_color_scale[i], alpha=0.4)
#         else:
#             ax.bar(np.arange(6) + offset, data, width, 
#                    color=plotly_color_scale[i], label=model)

#     multiplier += 1

# plt.ylabel('Accuracy')
# # figure.tight_layout() 
# plt.xticks(np.arange(len(utils.LEVELS))+width,utils.LEVELS)
# handles, labels = ax.get_legend_handles_labels()
# figure.legend(handles, labels, ncols=4, loc='lower center')
# plt.tight_layout(rect=(0,0.1,1,1))
# plt.savefig('parents_inferred_bert.png')
# plt.savefig('parents_inferred_bert.pdf')

# Hyperparameter plots
# def hyperparameter_plot(model_variants):

#     figure, axs = plt.subplots(1, figsize=(6,2.5))
#     axs.grid(axis='y', which='major')
#     axs.set_axisbelow(True)

#     xticks = []
#     progress = 0
    
#     for i, experiment in enumerate(model_variants):

#         data = []
#         for name in model_variants[experiment]:
#             model = model_variants[experiment][name]
#             accuracy = pd.read_csv(results_folder + 'results/trainset_valid '
#                               + model + '.csv').iloc[0]['Accuracy|test|species']
#             xticks.append(name)
#             data.append(accuracy)

#         axs.bar(progress + np.arange(len(data)), data, label=experiment, 
#                 color=plotly_color_scale[i])
#         progress += len(data)

#     axs.set_ylabel('Accuracy (species)')
#     axs.set_ylim(0,1)
#     axs.set_xticks(np.arange(len(xticks)), xticks, rotation=30)

#     handles, labels = axs.get_legend_handles_labels()
#     figure.legend(handles, labels, ncols=3, loc='lower center')

#     plt.tight_layout(rect=(0,0.1,1,1))
#     plt.savefig(f'hyperparameters.png')
#     plt.savefig(f'hyperparameters.pdf')

# hyperparameters = {
#     'Tokenizers (BERT)': {
#         'BPE': 'MycoAI-multi-BERT-medium-HLS',
#         '4-mer': 'MycoAI-multi-BERT-medium-4mer-HLS',
#         '5-mer': 'MycoAI-multi-BERT-medium-5mer-HLS',
#         '6-mer': 'MycoAI-multi-BERT-medium-6mer-HLS',
#     }, 
#     'Sizes (BERT)': {
#         'Small': 'MycoAI-multi-BERT-small-HLS',
#         'Medium': 'MycoAI-multi-BERT-medium-HLS',
#         'Large': 'MycoAI-multi-BERT-large-HLS',
#     },
#     'Architectures (CNN)': {
#         'Vu': 'MycoAI-multi-CNN-Vu-NoBN-HLS',
#         'Vu+BN': 'MycoAI-multi-CNN-Vu-HLS',
#         'ResNet9': 'MycoAI-multi-CNN-ResNet9-HLS',
#         'ResNet18': 'MycoAI-multi-CNN-ResNet18-HLS',
#     }
# }

# hyperparameter_plot(hyperparameters)

# # Big table
# metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'MCC']

# methods = {
#     'DNABarcoder': 'DNABarcoder',
#     'DNABarcoder (identified only)': 'DNABarcoder only_classified',
#     'RDP classifier': 'RDP',
#     'MycoAI-CNN (HLS)': 'MycoAI-multi-CNN-Vu-HLS',
#     'MycoAI-CNN (LS)': 'MycoAI-multi-CNN-Vu-SLS',
#     'MycoAI-BERT (HLS)': 'MycoAI-multi-BERT-medium-HLS',
#     'MycoAI-BERT (LS)': 'MycoAI-multi-BERT-medium-SLS',
# }

# testsets = {'Validation': 'trainset_valid',
#             'Test set 1': 'test1',
#             'Test set 2': 'test2'}

# table = []
# for metric in metrics:

#     for method in methods:

#         row = [metric, method]
#         methodfile = methods[method]

#         for testset in testsets:

#             testfile = testsets[testset]
#             data = pd.read_csv(results_folder + 'results/' + testfile + ' ' 
#                             + methodfile + '.csv')
#             data = data[[f'{metric}|test|{lvl}' for lvl in utils.LEVELS]]
#             row += list(data.values[0])

#         table.append(row)

# levels = ['P', 'C', 'O', 'F', 'G', 'S']
# table = pd.DataFrame(table, columns=['Metric', 'Method'] + levels*len(testsets))
# table.to_csv('table.csv', float_format="%.2f", index=False)