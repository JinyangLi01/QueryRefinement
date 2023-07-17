import matplotlib.pyplot as plt
import numpy as np

# Create some data to plot
x = np.arange(5)
y = [2, 5, 3, 8, 10]

# Set the xticks with labels that include LaTeX and \n
xticks = [r'Label 1', r'Label$_{2}\n$with superscript $x^2$', r'Label 3', r'Label$_{4}$', r'Label 5']
plt.plot(x, y)
plt.xticks(x, xticks, rotation=0)

# Enable LaTeX rendering
plt.rc('text', usetex=True)

# Show the plot
plt.show()
