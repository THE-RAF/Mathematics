from scipy.integrate import odeint
from scipy.optimize import fsolve
import numpy as np
import itertools
import matplotlib.pyplot as plt
from colorlines import colorline
from matplotlib import style



class PhaseDiagram:
    def __init__(self, system):
        self.system = system
        self.fig, self.ax = plt.subplots(1, 1)

    def steady_states(self, search_space, discretization=5):
        linspaces = [np.linspace(axis[0], axis[1], discretization) for axis in search_space]

        guesses = list(itertools.product(*linspaces))
        ss_system = lambda x: self.system(x, 0)

        results = []
        for guess in guesses:
            calc_result, _, convergence_success, info = fsolve(ss_system, guess, full_output=True)

            if convergence_success:
                if len(results) == 0:
                    results.append(calc_result)

                else:
                    new_guess = True

                    for result in results:
                        if all(np.isclose(calc_result, result, atol=1e-2)):
                            new_guess = False

                    if new_guess:
                        results.append(calc_result)
            else:
                print('convergence failure')

        return results

    def plot_trajectory(self, x0, time_sequence, ax, fade=0.1, linewidth=1):
        r = odeint(f, x0, time_sequence)
        colorline(x=r[:,0], y=r[:,1], ax=ax, cmap='bone_r', fade=fade, linewidth=linewidth)
        # plt.plot(r[:,0], r[:,1])

    def random_paths(self, n, time_sequence, x_rand_interval, y_rand_interval, fade=0.1, linewidth=1):
        self.fig.subplots_adjust(
            top=0.981,
            bottom=0.043,
            left=0.029,
            right=0.981,
            hspace=0.2,
            wspace=0.2
        )

        for _ in range(n):
            x_random = np.random.uniform(x_rand_interval[0], x_rand_interval[1])
            y_random = np.random.uniform(y_rand_interval[0], y_rand_interval[1])
            self.plot_trajectory([x_random, y_random], time_sequence=time_sequence, ax=self.ax, fade=fade, linewidth=linewidth)
        plt.show()


def f(x, t):
    y = np.zeros(shape=2)
    y[0] = x[0] - x[1]*x[0]
    y[1] = x[0]*x[1] - x[1]
    return y

PD = PhaseDiagram(f)
steady_states = PD.steady_states(search_space=[[-10,40],[-10,40]])
print(steady_states)

time_sequence=np.linspace(0.1,2.5,1000)
PD.random_paths(n=150, time_sequence=time_sequence, x_rand_interval=[-.4, 1.5], y_rand_interval=[0, 2], fade=1.0)

# PD.fig.savefig('PD1.png', dpi=300)
