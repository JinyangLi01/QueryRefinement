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

f_size = (13, 8)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()

input_path_prefix = r'constraint_change_q'

def run(query, constraint):
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
    # x_list = [19941230, 19950115, 19950130, 19950215, 19950230, 19950315, 19950330, 19950415]
    x_list = [110, 120, 130, 140, 150, 160]

    print(x_list, execution_timeps1, execution_timeps2)

    index = np.arange(len(execution_timeps1))
    bar_width = 0.5

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
    #

    plt.xticks(np.arange(0, 6, 1), x_list, rotation=0, fontsize=70)
    plt.yticks(fontsize=80, weight='bold')

    plt.xlabel(r'\{race=race3\} $>=$ (\%)',
               fontsize=85, weight='bold', labelpad=-10).set_position((0.41, -0.1))
    plt.tight_layout()
    plt.legend(loc='upper right', bbox_to_anchor=(0.98, 0.8), fontsize=65,
               ncol=1, labelspacing=0.1, handletextpad=0.2, markerscale=0.3,
               columnspacing=0.2, borderpad=0.2, frameon=True)

    fig_path = "healthcare_constraint_change_q" + str(query) + "_" + constraint + ".png"

    plt.savefig(fig_path, bbox_inches='tight')
    plt.show()


run(1, "1")
