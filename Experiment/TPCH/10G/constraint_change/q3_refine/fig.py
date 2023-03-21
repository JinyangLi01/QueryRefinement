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
plt.rc('font', size=80, weight='bold')

f_size = (14, 10)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()

input_path_prefix = r'constraint_change_q'

def run(query, size, constraint):
    input_path = input_path_prefix + str(query) + "_" + constraint + ".csv"
    input_file = open(input_path, "r")

    Lines = input_file.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        if line == '\n':
            continue
        if count < 2:
            continue
        if count > 9:
            break
        items = line.strip().split(',')
        execution_timeps1.append(float(items[2]))
        execution_timeps2.append(float(items[3]))
        if items[4] != '':
            execution_timebl1.append(float(items[5]))
            execution_timebl2.append(float(items[6]))
        else:
            execution_timebl1.append(0)
            execution_timebl2.append(0)
    x_list = [102, 104, 106, 108, 110, 112]

    print(x_list, execution_timeps1, execution_timeps2)

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

    plt.xticks(np.arange(0, 6), x_list, rotation=0, fontsize=80)
    plt.yticks(fontsize=80, weight='bold')

    plt.xlabel(r'\{c\underline{ }nationkey = 12\} $>=$ (\%)', fontsize=75,
               weight='bold').set_position((0.39, -0.1))
    plt.legend(loc='upper right', bbox_to_anchor=(1, 0.8), fontsize=65, ncol=1)
    plt.tight_layout()
    fig_path = "constraint_change_q" + str(query) + "_" + size + "_" + constraint + ".png"

    plt.savefig(fig_path, bbox_inches='tight')
    plt.show()


run(3, "10G", "refine")
