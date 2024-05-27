import numpy  as np
import matplotlib.pyplot as mpl
from matplotlib import cm

# Generating data
x = np.linspace(-1.25, 1.25, 100)
y = np.linspace(-0.5, 1.25, 100)
X, Y = np.meshgrid(x, y)
Z = 0.01 * (1.0 + 30*(Y - X*X)**2 + (1-X)**2)

# Contour plot of lewis function
fig, ax = mpl.subplots()

cs = ax.contourf(X,Y,Z,50, cmap=cm.jet)
fig.colorbar(cs)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

fig.suptitle('Lewis function')
fig.tight_layout()

fig.savefig('lewis_function.pdf')
