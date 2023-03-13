import matplotlib.pyplot as plt
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

color = ['C1', 'C0', 'C3', 'C2']
label = ['PS-prov', "PS-search", "BL-prov", "BL-search"]

plt.rc('text', usetex=True)
plt.rc('font', size=70, weight='bold')

f_size = (14, 10)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()

input_path_prefix = r'result_'
constraints = ['relax1', 'contract1', 'refine1']

def run(queries, size):
    baseline_fig = False
    x_list = []
    for query in queries:
        x_list.append("Q_{" + str(query) + "}C_1")
        x_list.append("Q_{" + str(query) + "}C_2")
        x_list.append("Q_{" + str(query) + "}C_3")
        for constraint in constraints:
            input_path = input_path_prefix + "q" + str(query) + constraint + ".csv"
            input_file = open(input_path, "r")
            Lines = input_file.readlines()
            line = Lines[2]
            items = line.strip().split(',')
            execution_timeps1.append(float(items[2]))
            execution_timeps2.append(float(items[3]))
            if Lines[3] != '\n':
                baseline_fig = True
                line = Lines[3]
                items = line.strip().split(',')
                execution_timebl1.append(float(items[2]))
                execution_timebl2.append(float(items[3]))
            else:
                execution_timebl1.append(0)
                execution_timebl2.append(0)

    print(x_list, execution_timeps1, execution_timeps2, execution_timebl1, execution_timebl2)

    index = np.arange(len(execution_timeps1))
    bar_width = 0.4

    fig, ax = plt.subplots(1, 1, figsize=f_size)

    ax.xaxis.set_major_locator(ticker.FixedLocator(index))
    # format date
    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(AutoDateFormatter(locator))

    plt.bar(index, execution_timeps1, bar_width, color=color[0], label=label[0])
    plt.bar(index, execution_timeps2, bar_width, bottom=execution_timeps1,
            color=color[1], label=label[1])
    if baseline_fig:
        plt.bar(index + bar_width, execution_timebl1, bar_width, color=color[2], label=label[2])
        plt.bar(index + bar_width, execution_timebl2, bar_width, bottom=execution_timebl1,
                color=color[3], label=label[3])
    #
    # plt.xticks(np.arange(0, 8, 2) + bar_width / 2, x_list, rotation=0, fontsize=70)
    x_list = ['Q1C1', "Q1C3", "Q2C2"]
    plt.xticks(np.arange(0, len(queries) * 3, 2) + bar_width / 2, x_list, fontsize=70, weight='bold')
    plt.yticks(fontsize=70, weight='bold')

    plt.xlabel(r'Query and Constraint')
    # plt.ylabel('Running time (s)')
    plt.legend(loc='upper right', bbox_to_anchor=(1.03, 0.80), fontsize=45, ncol=2)
    plt.yscale("log")
    plt.tight_layout()
    fig_path = "running_time_" + size + ".png"

    plt.savefig(fig_path, bbox_inches='tight')
    plt.show()


run([3, 12], '100M')
