'''
Specific functions for handling spectroscopy data and analysing
'''

import os
import matplotlib.pyplot as mp

def check_str(input_string):
    """
    Checks string for certain characters
    
    Parameters
    ----------

    input_string : string 

    Returns
    -------

    logical : Boolean
        True or False  
    """
    if any(char.isdigit() for char in input_string) == True:
        # search input_string for any of the following characters
        char_allow = set("0123456789\n\t\r eE-+,.;")
        validation = set((input_string))
        logical = validation.issubset(char_allow)
    else:
        logical = False

    return logical

def check_len(lists):
    """
    Checks nested list for each list lengths
    
    Parameters
    ----------

    lists : list of lists

    Returns
    -------

    boolean : True or False value depending on if the lists are all the same length
    lengths : list or single value of lengths for each list in lists
        True or False  
    """
    check = [len(data) for group in lists for data in group]
    lengths = [x for x in set(check)]
    # if only one length all lengths are the same so boolean is True
    if len(lengths) == 1:
        boolean = True
        indexes = None
    else:
        boolean = False
        indexes = [[index_1, index_2] for index_1, value_1 in enumerate(lists) for index_2, value_2 in enumerate(value_1) if len(value_2) > min(lengths)]
    
    return boolean, indexes

def plotter(x_data, y_data, axis_lbls=None, file_name=None, save=False, lims=None):

    try:
        lower = lims[0]
        upper = lims[1]
    except:
        lower = [0]
        upper = [-1]
    
    try:
        data_lbl = os.path.split(file_name)[1]
    except:
        data_lbl = None

    fig, ax = mp.subplots(figsize=(8.5))
    ax.grid(True, color='silver', linewidth=0.5)
    try:
        ax.set_title(axis_lbls[0])
        ax.set(xlabel=axis_lbls[1], ylabel=axis_lbls[2])
    except:
        pass

    ax.plot(x_data[lower:upper], y_data[lower:upper], color=None, marker=None, linestyle='-', alpha=1, label=data_lbl)
    ax.legend(loc='best', fontsize=8)

    if save == True:
        fig.savefig(fname=file_name + '.jpg', dpi='figure', format='jpg', bbox_inches='tight')