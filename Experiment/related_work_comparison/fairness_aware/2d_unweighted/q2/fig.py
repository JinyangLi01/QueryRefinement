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

color = ['darkorchid', 'mediumorchid', 'plum', 'slategrey']
label = ['PVL-total', "PVL-avg", "PVL-first", "[15]",]

f_size = (18, 10.3)


disparity = list()
num_refinements = list()
execution_time_per = list()
execution_time_total = list()
execution_time_competitior = list()
execution_time_first = list()



input_path = r'competitior_q3.csv'
input_file = open(input_path, "r")
Lines = input_file.readlines()
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if count < 3:
        continue
    items = line.strip().split(',')
    disparity.append(int(items[0]))
    execution_time_competitior.append(float(items[1]))


input_path = r'constraint_change_q3.csv'
input_file = open(input_path, "r")

Lines = input_file.readlines()

count = 0
# Strips the newline character
for line in Lines:
    items = line.strip().split(',')
    num_refinements.append(int(items[1]))
    execution_time_total.append(float(items[2]))
    execution_time_per.append(float(items[3]))
    execution_time_first.append(float(items[4]))

print(execution_time_per, execution_time_total)

bar_width = 0.22

x = [0, 2, 4, 6, 8, 10, 12]
x_pos = np.arange(len(disparity))
fig, ax = plt.subplots(1, 1, figsize=f_size)

# Position of the bars on the x-axis
r1 = x_pos - bar_width
r2 = x_pos
r3 = x_pos + bar_width
r4 = x_pos + 2 * bar_width

plt.bar(r1, execution_time_total, width=bar_width, label=label[0], color=color[0])
plt.bar(r2, execution_time_per, width=bar_width, label=label[1], color=color[0], alpha=.7)
plt.bar(r3, execution_time_first, width=bar_width, label=label[2], color=color[2], alpha=0.8)
plt.bar(r4, execution_time_competitior, width=bar_width, label=label[3], color=color[3])


plt.ylim(0.001, 100)


# x_list = ['\\boldmath$Q^H_1$\\boldmath$C^H_1$', '\\boldmath$Q^H_1$\\boldmath$C^H_2$',
#           '\\boldmath$Q^H_1$\\boldmath$C^H_3$',
#           '\\boldmath$Q^H_2$\\boldmath$C^H_1$', '\\boldmath$Q^H_2$\\boldmath$C^H_2$',
#           '\\boldmath$Q^H_2$\\boldmath$C^H_3$']

plt.xticks(x_pos + 0.5 * bar_width, [80, 70, 60, 50, 40, 30, 20], fontsize=70, weight='bold')
plt.yticks(fontsize=65, weight='bold')

plt.xlabel('target disparity: \% of the original', fontsize=70, weight='bold').set_position((0.44, 0))
# plt.ylabel('Running time (s)')
plt.yscale('log')
# plt.legend(loc='upper right', bbox_to_anchor=(1, 1.05), ncol=2, fontsize=40)
lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.46, 1.44), fontsize=55, ncol=4, labelspacing=0.1,
                  handletextpad=0.1, handlelength=1.7, markerscale=0.05, columnspacing=0.1, frameon=False)

plt.tight_layout()
plt.savefig("comparision_q3.png", bbox_inches='tight')
plt.show()
