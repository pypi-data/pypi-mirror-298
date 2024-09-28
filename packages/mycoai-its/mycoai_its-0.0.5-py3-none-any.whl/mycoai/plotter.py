'''Classes for creating plots and visualizations.'''

import torch
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import sklearn.metrics as skmetric
from mycoai import utils
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def counts_barchart(dataprep, level='phylum', id=''):
    '''Plots the number of sequences per class'''

    data = dataprep.data[dataprep.data[level] != utils.UNKNOWN_STR]
    counts = data.groupby(level, as_index=False)['id'].count().sort_values('id', 
                                                                ascending=False)
    ax = counts.plot.bar(ylabel='# sequences', xlabel=level, width=1, 
                         color='#636EFA', figsize=(6,3), legend=False)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yscale('log')
    id = '_' + id if len(id) > 0 else ''
    plt.tight_layout()
    plt.savefig(utils.OUTPUT_DIR + level + '_counts' + id + '.pdf')
    plt.close()

def counts_boxplot(dataprep, id=''):
    '''Plots the number of sequences per class as boxplot (all taxon levels)'''

    fig, axs = plt.subplots(nrows=1,ncols=6,figsize=(9,3))
    id = '_' + id if len(id) > 0 else ''

    for i in range(len(utils.LEVELS)):
        lvl = utils.LEVELS[i]
        counts = dataprep.data.groupby(lvl, as_index=False)[lvl].count()
        counts = counts.sort_values(lvl, ascending=False)
        counts.boxplot(ax=axs[i])

    axs[0].set_ylabel("# sequences")
    fig.suptitle('Taxon class counts')
    fig.tight_layout()
    plt.savefig(utils.OUTPUT_DIR + 'boxplot' + id + '.png')
    plt.close()

def counts_sunburstplot(dataprep, id=''):
    '''Plots the taxonomic class distribution as a sunburst plot'''

    print("Creating sunburst plot...")
    counts = dataprep.data.groupby(utils.LEVELS, as_index=False).count()
    fig = px.sunburst(counts, path=utils.LEVELS, values='sequence', width=750, height=595)
    id = '_' + id if len(id) > 0 else ''

    for level, color in zip(dataprep.data['phylum'].value_counts().head(8).index.to_list(), px.colors.qualitative.Plotly[:8]):
        fig.add_trace(go.Scatter(
            x=[None], y=[None], 
            mode='markers',
            marker=dict(size=10, color=color), 
            name=level,
        ))


    fig.update_layout(legend_title_text='Phylum',
                      legend={'y':0.5}, margin = dict(t=0, l=0, r=0, b=0),
                              xaxis=dict(visible=False),  # Hide the x-axis
                             yaxis=dict(visible=False),
                             paper_bgcolor='white',  # Set background color to transparent
        plot_bgcolor='white')
    pio.write_image(fig, utils.OUTPUT_DIR + "sunburst" + id + ".pdf", scale=1)

def counts_multisunburstplot(data, ids):
    '''Plots the taxonomic class distribution as a sunburst plot'''

    print("Creating sunburst plots...")

    fig = make_subplots(rows=1, cols=len(data), subplot_titles=ids, specs=[[{"type": "sunburst"}]*len(data)], horizontal_spacing=0.03)

    for i, (dataprep, id) in enumerate(zip(data, ids)):

        counts = dataprep.data.groupby(utils.LEVELS, as_index=False).count()
        sunburst_fig = px.sunburst(counts, path=utils.LEVELS, values='sequence')
        id = '_' + id if len(id) > 0 else ''

        for trace in sunburst_fig.data:
            fig.add_trace(trace, row=1, col=i+1)

    
    for level, color in zip(data[0].data['phylum'].value_counts().head(8).index.to_list(), px.colors.qualitative.Plotly[:8]):
        fig.add_trace(go.Scatter(
            x=[None], y=[None], 
            mode='markers',
            marker=dict(size=10, color=color), 
            name=level,
        ))

    fig.update_layout(legend_title_text='Phylum',
                      height=400, width=400 * len(data),
                      legend={'y':0.5}, margin = dict(t=30, l=0, r=0, b=0),
                              xaxis=dict(visible=False),  # Hide the x-axis
                             yaxis=dict(visible=False),
                             paper_bgcolor='white',  # Set background color to transparent
        plot_bgcolor='white')
    pio.write_image(fig, "combined_sunburst.pdf", scale=1)

def classification_learning_curve(history, metric_name, levels, 
                                  show_valid=True, show_train=False):
    '''Plots the learning curves for a single metric on all specified levels'''
    
    for lvl in levels:
        valid_plot = False
        if show_valid:
            valid_plot = plt.plot(
                history[f'{metric_name}|valid|{utils.LEVELS[lvl]}'],
                label=utils.LEVELS[lvl] + " (valid)"
            )
        if show_train:
            if valid_plot is not False:
                plt.plot(history[f'{metric_name}|train|{utils.LEVELS[lvl]}'], 
                         alpha=0.5, color=valid_plot[0].get_color(), 
                         label=utils.LEVELS[lvl] + " (train)")
            else:
                plt.plot(history[f'{metric_name}|train|{utils.LEVELS[lvl]}'], 
                         alpha=0.5, label=utils.LEVELS[lvl] + " (train)")
    
    plt.xlabel('Epochs')
    plt.ylabel(metric_name)
    plt.legend()
    plt.savefig(utils.OUTPUT_DIR + '/' + metric_name.lower() + '.png')
    plt.close()
    
    return

def confusion_matrices(model, data):
    '''Plots a confusion matrix for each predicted taxonomy level'''
    model.eval()
    with torch.no_grad():
        y_pred, y = model._predict(data, return_labels=True) 
        for i in range(len(y_pred)):
            argmax_y_pred = torch.argmax(y_pred[i].cpu(), dim=1)
            matrix = skmetric.confusion_matrix(y[:,i].cpu(), argmax_y_pred)
            plt.imshow(matrix)
            plt.savefig(utils.OUTPUT_DIR + '/' + 
                        utils.LEVELS[i] + '.png')
            plt.close()