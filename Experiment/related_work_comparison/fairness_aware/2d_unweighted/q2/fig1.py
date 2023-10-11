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

color = ['darkorchid', 'plum', 'slategrey']
label = ["PVL-avg", "PVL-first", "[15]",]

f_size = (14, 6)



disparity = list()
num_refinements = list()
execution_time_per = list()
execution_time_total = list()
execution_time_competitior = list()
execution_time_first = list()



input_path = r'competitior_1d_q2.csv'
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


input_path = r'constraint_change_q2.csv'
input_file = open(input_path, "r")

Lines = input_file.readlines()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if line == '\n':
        continue
    items = line.strip().split(',')
    num_refinements.append(int(items[1]))
    execution_time_total.append(float(items[2]))
    execution_time_per.append(float(items[3]))
    execution_time_first.append(float(items[4]))

print(execution_time_per, execution_time_total)

bar_width = 0.28

x = [0, 2, 4, 6, 8, 10, 12]
x_pos = np.arange(len(disparity))
fig, ax = plt.subplots(1, 1, figsize=f_size)

# Position of the bars on the x-axis
r1 = x_pos - bar_width
r2 = x_pos
r3 = x_pos + bar_width
r4 = x_pos + 2 * bar_width

# plt.bar(r1, execution_time_total, width=bar_width, label=label[0], color=color[0])
plt.bar(r1, execution_time_per, width=bar_width, label=label[0], color=color[0], alpha=.7)
plt.bar(r2, execution_time_first, width=bar_width, label=label[1], color=color[1], alpha=0.8)
plt.bar(r3, execution_time_competitior, width=bar_width, label=label[2], color=color[2])


plt.ylim(0.0001, 300)


# x_list = ['\\boldmath$Q^H_1$\\boldmath$C^H_1$', '\\boldmath$Q^H_1$\\boldmath$C^H_2$',
#           '\\boldmath$Q^H_1$\\boldmath$C^H_3$',
#           '\\boldmath$Q^H_2$\\boldmath$C^H_1$', '\\boldmath$Q^H_2$\\boldmath$C^H_2$',
#           '\\boldmath$Q^H_2$\\boldmath$C^H_3$']


plt.xticks(r2, [90, 80, 70, 60, 50, 40, 30], fontsize=67, weight='bold')
plt.yticks(fontsize=65, weight='bold')

plt.tight_layout()
plt.xlabel('target disparity: \% of the original', fontsize=67, weight='bold', labelpad=-10).set_position((0.43, 1))
# plt.ylabel('Running time (s)')
plt.yscale('log')

lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.46, 1.45), fontsize=50, ncol=4, labelspacing=0.2,
                  handletextpad=0.2, markerscale=0.2, columnspacing=0.2, frameon=False)

plt.savefig("comparision_2d_q2.png", bbox_inches='tight')
plt.show()
