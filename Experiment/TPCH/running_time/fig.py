import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
from matplotlib.dates import AutoDateLocator, AutoDateFormatter, date2num

sns.set_palette("Paired")
# sns.set_palette("deep")
sns.set_context("poster", font_scale=2)
sns.set_style("whitegrid")
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 4
plt.rcParams['xtick.bottom'] = True
plt.rcParams['ytick.left'] = True

#
# plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
# plt.rc('text.latex', preamble=r'\usepackage{boldmath}')

color = ['C1', 'C0', 'C3', 'C2']
label = ['PS-prov', "PS-search", "BL-prov", "BL-search"]

plt.rc('text', usetex=True)
plt.rc('font', size=70, weight='bold')

f_size = (20, 12)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()

input_path_prefix = r'running_time_q'
constraints = ['relax1', 'contract1', 'refine1']

def run(q):
    baseline_fig = False
    x_list = []
    file_path = input_path_prefix + str(q) + ".csv"
    running_time = pd.read_csv(file_path)
    execution_timeps1 = running_time['PS_prov'].tolist()
    execution_timeps2 = running_time['PS_search'].tolist()
    execution_timebl1 = running_time['BL_prov'].tolist()
    execution_timebl2 = running_time['BL_search'].tolist()

    print(execution_timeps1, execution_timeps2, execution_timebl1, execution_timebl2)

    index = np.arange(len(execution_timeps1))
    bar_width = 0.45

    fig, ax = plt.subplots(1, 1, figsize=f_size)

    ax.xaxis.set_major_locator(ticker.FixedLocator(index))
    # format date
    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(AutoDateFormatter(locator))

    plt.bar(index, execution_timeps1, bar_width, color=color[0], label=label[0])
    plt.bar(index, execution_timeps2, bar_width, bottom=execution_timeps1,
            color=color[1], label=label[1])
    # plt.bar(index + bar_width, execution_timebl1, bar_width, color=color[2], label=label[2])
    # plt.bar(index + bar_width, execution_timebl2, bar_width, bottom=execution_timebl1,
    #         color=color[3], label=label[3])

    # x_list = [r"\boldmath$C^T_1$\n\textbf{100M}",
    #           '$C^T_1$\n1G', '$C^T_1$\n10G', '$C^T_2$\n100M', '$C^T_2$\n1G', '$C^T_2$\n10G',
    #           '$C^T_3$\n100M', '$C^T_3$\n1G', '$C^T_3$\n10G']
    x_list = ['\\boldmath$C^T_1$\n\\textbf{100M}', '\\boldmath$C^T_1$\n\\textbf{1G}','\\boldmath$C^T_1$\n\\textbf{10G}',
              '\\boldmath$C^T_2$\n\\textbf{100M}', '\\boldmath$C^T_2$\n\\textbf{1G}', '\\boldmath$C^T_2$\n\\textbf{10G}',
                '\\boldmath$C^T_3$\n\\textbf{100M}', '\\boldmath$C^T_3$\n\\textbf{1G}', '\\boldmath$C^T_3$\n\\textbf{10G}']

    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], x_list, fontsize=55, weight='bold')
    plt.yticks(fontsize=80, weight='bold')
    plt.yscale('log')
    plt.xlabel(r'Constraint and Dataset Size', fontsize=80, weight='bold')
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4), fontsize=50, ncol=2, labelspacing=0.25,
    #            handletextpad=0.1, markerscale=0.5, columnspacing=0.3, frameon=False)

    lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.45, 1.3), fontsize=54, ncol=4, labelspacing=0.25,
                      handletextpad=0.1, markerscale=0.5, columnspacing=0.3, frameon=False)

    plt.tight_layout()
    fig_path = "running_time_" + str(q) + ".png"

    plt.savefig(fig_path, bbox_inches='tight')
    plt.show()


run(12)
