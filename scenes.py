import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from python_femm import Scene

from model import MyModel


class RotorCenter(Scene):

    model = MyModel
    iterations = 8
    mode = '2D'
    save_as = 'rotorcenter'

    def run_2d(self):
        ...

    def display_results_2d(self):
        ...

    def run_3d(self):
        ...

    def display_results_3d(self):
        ...

    def run(self, x_iteration, y_iteration):
        model = self.model()
        # Setup the model.
        model.start()
        # Define what we want to vary.
        rotor_center_x = self.vary(0.5 * np.sin(np.pi / 16), 0.5 * -np.sin(np.pi / 16), x_iteration)
        rotor_center_y = self.vary(0.5 * -np.cos(np.pi / 16), 0.5 * np.cos(np.pi / 16), x_iteration)
        # Draw the model and analyse it.
        model.pre(rotor_center=[rotor_center_x, rotor_center_y])
        model.session.pre.save_as(f'{self.save_as}_{x_iteration}_{y_iteration}.fem')
        model.solve()
        return model.post()

    def display_results(self, results):
        if self.mode == '2D':
            plt.plot(self.get_axis(-0.5, 0.5), results[0])
        if self.mode == '3D':
            figure = plt.figure()
            ax = Axes3D(figure)
            ax.plot_trisurf(self.get_axis(60, 59), self.get_axis(60, 61), results)
        plt.show()


class PoleWidth(Scene):

    model = MyModel()
    iterations = 16
    mode = '2D'

    def run(self, x_iteration, y_iteration):
        self.model.start()
        pole_width = self.vary(2, 18, x_iteration)
        pole_angle = self.vary(20, 30, x_iteration)
        self.model.pre(
            pole_width=pole_width,
            pole_angle=pole_angle,
            save_as=f'pole_width_{pole_width}.fem'
        )
        self.model.solve()
        res = self.model.post()
        self.model.close()
        return res

    def display_results(self, results):
        plt.plot(self.get_axis(10, 18), results[0])
        plt.show()
