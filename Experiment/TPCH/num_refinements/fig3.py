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


color = ['C4', 'C10', 'tan', 'C2']
label = ['PS', "PS-search", "total-number", "BL-search"]

plt.rc('text', usetex=True)
plt.rc('font', size=70, weight='bold')

f_size = (17, 7)

x_list = list()
x_naive = list()
execution_timeps = list()
execution_timeall = list()
execution_timebl1 = list()
execution_timebl2 = list()

input_path_prefix = r'num_refinements_q'
constraints = ['relax1', 'contract1', 'refine1']

def run(q):
    baseline_fig = False
    x_list = []
    file_path = input_path_prefix + str(q) + ".csv"
    running_time = pd.read_csv(file_path)
    execution_timeps = running_time['PS'].tolist()
    execution_timeall = running_time['all'].tolist()

    print(execution_timeps, execution_timeall)

    index = np.arange(len(execution_timeps))
    bar_width = 0.45

    fig, ax = plt.subplots(1, 1, figsize=f_size)

    ax.xaxis.set_major_locator(ticker.FixedLocator(index))
    # format date
    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(AutoDateFormatter(locator))

    plt.bar(index, execution_timeps, bar_width, color=color[0], label=label[0])
    plt.bar(index + bar_width, execution_timeall, bar_width, color=color[2], label=label[2])

    # x_list = [r"\boldmath$C^{T,3}_1$\n\textbf{100M}",
    #           '$C^{T,3}_1$\n1G', '$C^{T,3}_1$\n10G', '$C^{T,3}_2$\n100M', '$C^{T,3}_2$\n1G', '$C^{T,3}_2$\n10G',
    #           '$C^{T,3}_3$\n100M', '$C^{T,3}_3$\n1G', '$C^{T,3}_3$\n10G']
    x_list = ['\\boldmath$C^{T,3}_1$\n\\textbf{100M}', '\\boldmath$C^{T,3}_1$\n\\textbf{1G}','\\boldmath$C^{T,3}_1$\n\\textbf{10G}',
              '\\boldmath$C^{T,3}_2$\n\\textbf{100M}', '\\boldmath$C^{T,3}_2$\n\\textbf{1G}', '\\boldmath$C^{T,3}_2$\n\\textbf{10G}',
                '\\boldmath$C^{T,3}_3$\n\\textbf{100M}', '\\boldmath$C^{T,3}_3$\n\\textbf{1G}', '\\boldmath$C^{T,3}_3$\n\\textbf{10G}']

    plt.xticks([0.25, 1.25, 2.2, 3.3, 4.3, 5.2, 6.3, 7.3, 8.25], x_list, fontsize=45, weight='bold')
    plt.yticks([1000, 100000], fontsize=70, weight='bold')
    plt.yscale('log')
    plt.ylim(10, 100000000)
    plt.tight_layout()
    plt.xlabel(r'Constraint and Dataset Size', fontsize=65, weight='bold', labelpad=0)
    # plt.legend(loc='upper center', bbox_to_anchor=(0.45, 1.3), fontsize=54, ncol=4, labelspacing=0.3,
    #                   handletextpad=0.1, markerscale=0.2, columnspacing=0.3, frameon=False)
    plt.legend(loc='upper center', bbox_to_anchor=(0.45, 1.3), fontsize=57, ncol=2, labelspacing=0.2,
               handletextpad=0.2, markerscale=0.3, columnspacing=1, frameon=False)

    fig_path = "TPCH_num_refinements_" + str(q) + ".png"

    plt.savefig(fig_path, bbox_inches='tight')
    plt.show()


run(3)
