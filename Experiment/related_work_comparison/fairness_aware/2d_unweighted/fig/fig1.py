import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np


sns.set_palette("Paired")
# sns.set_palette("deep")
sns.set_context("poster", font_scale=2)
sns.set_style("whitegrid")
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 4
plt.rcParams['xtick.bottom'] = True
plt.rcParams['ytick.left'] = True

plt.rc('text', usetex=True)
plt.rc('font', size=70, weight='bold')

color = ['plum', 'darkorchid', 'darkgrey', 'dimgrey']
label = ["PVL-first,$x,y\in$[400,600]", "PVL-first,$x,y\in$[550,700]", "[15],$x,y\in$[400,600]","[15],$x,y\in$[550,700]"]

f_size = (14.5, 5.9)

disparity = list()
num_refinements = list()
execution_time_per = list()
execution_time_total = list()
execution_time_competitior1 = list()
execution_time_competitior2 = list()
execution_time_first1 = list()
execution_time_first2 = list()


input_path = r'competitior_q1.csv'
input_file = open(input_path, "r")
Lines = input_file.readlines()
# Strips the newline character
for line in Lines:
    items = line.strip().split(',')
    disparity.append(int(items[0]))
    execution_time_competitior1.append(float(items[1]))




input_path = r'competitior_q2.csv'
input_file = open(input_path, "r")
Lines = input_file.readlines()
# Strips the newline character
for line in Lines:
    items = line.strip().split(',')
    # disparity.append(int(items[0]))
    execution_time_competitior2.append(float(items[1]))



input_path = r'constraint_change_q1.csv'
input_file = open(input_path, "r")
Lines = input_file.readlines()
# Strips the newline character
for line in Lines:
    items = line.strip().split(',')
    num_refinements.append(int(items[1]))
    execution_time_first1.append(float(items[4]))



input_path = r'constraint_change_q2.csv'
input_file = open(input_path, "r")
Lines = input_file.readlines()
# Strips the newline character
for line in Lines:
    items = line.strip().split(',')
    num_refinements.append(int(items[1]))
    execution_time_first2.append(float(items[4]))


print(execution_time_per, execution_time_total)


x = [0, 2, 4, 6, 8, 10, 12]
x_pos = np.arange(len(disparity))
fig, ax = plt.subplots(1, 1, figsize=f_size)

barWidth = 0.21
r1 = np.arange(len(x))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# plt.bar(r1, execution_time_total, width=bar_width, label=label[0], color=color[0])
plt.bar(r1, execution_time_first1, width=barWidth, label=label[0], color=color[0], alpha=0.8)
plt.bar(r2, execution_time_competitior1, width=barWidth, label=label[2], color=color[2], alpha=1)
plt.bar(r3, execution_time_first2, width=barWidth, label=label[1], color=color[1], alpha=0.8)
plt.bar(r4, execution_time_competitior2, width=barWidth, label=label[3], color=color[3], alpha=1)


plt.ylim(0.0001, 500)

plt.xticks([r + 1.5 *  barWidth for r in range(len(x))], [90, 80, 70, 60, 50, 40, 30], fontsize=67, weight='bold')
plt.yticks( fontsize=65, weight='bold')

plt.tight_layout()
plt.xlabel('target disparity: \% of the original', fontsize=67, weight='bold', labelpad=-10).set_position((0.43, 1))
# plt.ylabel('Running time (s)')
plt.yscale('log')

handles, labels = plt.gca().get_legend_handles_labels()
order = [0, 2, 1, 3]
lgnd = plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],
                  loc='upper center', bbox_to_anchor=(0.42, 1.6), fontsize=45, ncol=2, labelspacing=0.06,
                  handletextpad=0.2, markerscale=0.2, columnspacing=0.1, handlelength=1.3, handleheight=0.6, frameon=False)

plt.savefig("comparision_2d_q1q2.png", bbox_inches='tight')
plt.show()
