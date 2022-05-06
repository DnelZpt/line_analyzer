import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth, square

class DataGen():

    def __init__(self, seed):
        F = 60
        Ts = 1/(100*F)
        N = int(5/(F*Ts))
        t = np.linspace(0.0, N*Ts, N, endpoint=False)
        self.rs = np.random.RandomState(seed)
        self.__voltages = self.__get_voltages(F, t)
        self.__currents = self.__get_currents(F, t)

    def get_data(self):
        return self.__voltages, self.__currents

    def plot(self):
        col_labels = ["Voltaje", "Corriente"]
        row_labels = ["Fase A", "Fase B", "Fase C"]
        fig, axs = plt.subplots(3, 2, figsize=(15, 8))
        for i in range(3):
            axs[i, 0].plot(self.__voltages[i])
            axs[i, 0].grid()
            axs[i, 1].plot(self.__currents[i])
            axs[i, 1].grid()
        for ax, col in zip(axs[0], col_labels):
            ax.set_title(col)

        for ax, row in zip(axs[:,0], row_labels):
            ax.set_ylabel(row, rotation=0, size='large')

        fig.tight_layout()
        plt.show()


    def __hrect(self, t, *args):
        fun = np.heaviside(np.sin(t), 1) * np.sin(t)
        return fun

    def __frect(self, t, *args):
        fun = np.sign(np.sin(t)) * np.sin(t)
        return fun

    def __get_voltages(self, F, t):
        v = list([0, 0, 0])
        n_harmonics = 5
        amplitude = [0, 220, 0, 20, 0, 8]
        for k, amp in zip(range(n_harmonics+1), amplitude):
            v[0] += amp * np.sin(k*(2*np.pi*F*t))
            v[1] += amp * np.sin(k*(2*np.pi*F*t+240*np.pi/180))
            v[2] += amp * np.sin(k*(2*np.pi*F*t+120*np.pi/180))
        return v

    def __get_currents(self, F, t):
        func = self.rs.choice([square, sawtooth,
                               self.__hrect, self.__frect])
        i = list([0, 0, 0])
        d = self.rs.rand()
        a = 220 * d
        i[0] = a * func(2*np.pi*F*t, d)
        i[1] = a * func(2*np.pi*F*t+240*np.pi/180, d)
        i[2] = a * func(2*np.pi*F*t+120*np.pi/180, d)

        return i
