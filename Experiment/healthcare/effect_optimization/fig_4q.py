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

color = ['C1', 'C0', 'C7', 'C6']
label = ['PS-prov', "PS-search", "PS-prov\_no\_opt", "PS-search\_no\_opt"]

f_size = (20, 10)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()


input_path = r'time_4q.csv'
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
    if count > 10:
        break
    items = line.strip().split(',')
    x_list.append(items[0])
    execution_timeps1.append(float(items[1]))
    execution_timebl1.append(float(items[2]))
    # if items[4] != '':
    #     execution_timebl1.append(float(items[5]))
    #     execution_timebl2.append(float(items[6]))
    # else:
    #     execution_timebl1.append(0)
    #     execution_timebl2.append(0)



index = np.arange(len(x_list))
bar_width = 0.45

fig, ax = plt.subplots(1, 1, figsize=f_size)

plt.bar(index, execution_timeps1, bar_width, color=color[1], label=label[1])
# plt.bar(index, execution_timeps2, bar_width, bottom=execution_timeps1,
#         color=color[1], label=label[1])
plt.bar(index + bar_width, execution_timebl1, bar_width, color=color[3], label=label[3])
# plt.bar(index + bar_width, execution_timebl2, bar_width, bottom=execution_timebl1,
#         color=color[3], label=label[3])

# x_list = ['\\boldmath$Q^H_1$\n\\boldmath$C^H_1$', '\\boldmath$Q^H_1$\n\\boldmath$C^H_2$',
#           '\\boldmath$Q^H_2$\n\\boldmath$C^H_1$', '\\boldmath$Q^H_2$\n\\boldmath$C^H_2$']
x_list = ['\\boldmath$Q^H_1$\n\\boldmath$C^H_1$', '\\boldmath$Q^H_1$\n\\boldmath$C^H_2$',
          '\\boldmath$Q^H_2$\n\\boldmath$C^H_1$', '\\boldmath$Q^H_2$\n\\boldmath$C^H_2$',
          '\\boldmath$Q^H_3$\n\\boldmath$C^H_4$', '\\boldmath$Q^H_3$\n\\boldmath$C^H_5$',
          '\\boldmath$Q^H_4$\n\\boldmath$C^H_7$', '\\boldmath$Q^H_4$\n\\boldmath$C^H_8$',
          ]

plt.xticks(np.arange(0, 8) + bar_width/2, x_list, rotation=0, fontsize=65)
plt.yticks(fontsize=75, weight='bold')

plt.xlabel('Query and Constraint', fontsize=75, weight='bold', labelpad=-0)

plt.yscale('log')

plt.tight_layout()
lgnd = plt.legend(loc='upper left', bbox_to_anchor=(0, 1.2), fontsize=70, ncol=2, labelspacing=0.1,
                  handletextpad=0.2, markerscale=0.2, columnspacing=0.2, frameon=False)

# lgnd = plt.legend(loc='upper right', bbox_to_anchor=(1.03, 1.05), fontsize=70, ncol=2, labelspacing=0.2,
#                   handletextpad=0.2, markerscale=0.2, columnspacing=0.4)


plt.savefig("healthcare_optimization_effect_4q.png", bbox_inches='tight')
plt.show()
