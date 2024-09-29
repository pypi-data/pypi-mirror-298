# -*- coding: utf-8 -*-

"""
Created on Thu Sep 27 13:30:00 2024

@author: Yuriy Izotov
@user: izotov93
"""

import random
from itertools import repeat
# from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool
import numpy as np
from LogNNet.mlp_evaluation import evaluate_mlp_mod


class Particle:
    """
    The class describes one particle in the particle swarm method
    """

    def __init__(self, start_position, model_config):
        self.position = start_position

        self.w = 0.5
        self.c1, self.c2 = 2, 2
        # [w, c1, c2, r1, r2]
        self.coef_velocity = [self.w, self.c1, self.c2, random.random(), random.random()]

        self.model = PSO_fit_model(**model_config)

        self.velocity = [0] * len(start_position)
        self.best_position = self.position
        self.best_value = -1
        self.is_random_velocity = False

    def update_velocity(self, global_best_position):
        r1 = random.random()
        r2 = random.random()

        for i in range(len(self.velocity)):
            self.velocity[i] = self.w * self.velocity[i] + \
                               self.c1 * r1 * (self.best_position[i] - self.position[i]) + \
                               self.c2 * r2 * (global_best_position[i] - self.position[i])

    def update_position(self, bounds):
        for i in range(len(self.position)):
            self.position[i] = self.position[i] + self.velocity[i]

            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]
                self.velocity[i] = 0
            elif self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]
                self.velocity[i] = 0

    def update_stat_particle(self, error):
        if self.best_value == -1 or error > self.best_value:
            self.best_position = list(self.position)
            self.best_value = error


class PSO_fit_model(object):
    def __init__(self, X: np.ndarray, y: np.ndarray, shuffle=True, random_state=42, target='Regressor'):
        self.X, self.y = X, y

        self.shuffle = shuffle
        self.random_state = random_state
        self.target = target

    def pso_fitness(self, num_rows_W=10, Zn0=100, Cint=45,
                    Bint=-43, Lint=3025, prizn=123, n_f=100, ngen=100, noise=0):

        """
        self._param_ranges = {
            'num_rows_W': validate_param(input_layer_neurons, int,
                                         check_limits=True, name_param='input_layer_neurons'),
            'Zn0': (-499, 499),
            'Cint': (-499, 499),
            'Bint': (-499, 499),
            'Lint': (100, 10000),
            'first_layer_neurons': validate_param(first_layer_neurons, int,
                                                  check_limits=True, name_param='first_layer_neurons'),
            'hidden_layer_neurons': validate_param(hidden_layer_neurons, int,
                                                   check_limits=True, name_param='hidden_layer_neurons'),
            'learning_rate': validate_param(learning_rate, float,
                                            check_limits=True, name_param='learning_rate'),
            'epochs': validate_param(n_epochs, int, check_limits=True, name_param='n_epochs'),
            'prizn': (0, 1),
            'n_f': n_f,
            'ngen': validate_param(ngen, int, check_limits=True, name_param='ngen'),
            'noise': validate_param(noise, float, check_limits=True, name_param='noise'),
        }
        """

        metrics, model, input_layers_data = evaluate_mlp_mod(X=self.X, y=self.y, params=params, num_folds=num_folds,
                                                             num_rows_W=num_rows_W, Zn0=Zn0, Cint=Cint, Bint=Bint,
                                                             Lint=Lint, prizn=prizn, n_f=n_f, ngen=ngen,
                                                             shuffle=self.shuffle, random_state=self.random_state,
                                                             target=self.target, noise=noise)
        return metrics, model, input_layers_data


def train_particle(particle: Particle):
    """
    Single particle training function
        :param particle: Particle instance
        :return: Accuracy value for given hyperparameters
    """

    return particle.model.pso_fitness(particle.position)


def PSO(X: np.ndarray, y: np.ndarray, num_folds: int, param_ranges: dict,
        selected_metric: str, selected_metric_class: (int, None), dimensions: int,
        num_particles: int, num_iterations: int, num_threads=5,
        random_state=42, shuffle=True, target='Regressor',
        static_features=(list, None)) -> (np.ndarray, float, object, dict):
    """
    Function for searching for optimal parameters using the Particle Swarm Optimization (PSO)

        :param X: (np.ndarray): The input features of the dataset, where rows represent samples
            and columns represent features.
        :param y: (np.ndarray): The target values corresponding to the input features.
        :param num_folds: (int): The number of folds to use for cross-validation during the
            evaluation of particle fitness.
        :param param_ranges: (dict): A dictionary defining the ranges for the hyperparameters to
            optimize for each model.
        :param selected_metric: (str): A string representing the metric to be used for evaluating the
            fitness of particles.
        :param selected_metric_class: (int, None): For classification tasks, this defines the class to optimize.
        :param dimensions: (int): The number of hyperparameters to optimize, corresponding to the number of
            dimensions in the particle space.
        :param num_particles: (int): The number of particles in the swarm that will explore the hyperparameter space.
        :param num_iterations: (int): The number of iterations for the optimization process.
        :param num_threads: (int, optional): he number of threads to use for parallel execution.
            Default is the number of CPU cores.
        :param random_state: (int, optional): Seed for random number generation to ensure reproducibility.
            Default is 42.
        :param shuffle: (bool, optional):  Whether to shuffle the data before splitting into folds
            for cross-validation. Default is True.
        :param target: (str, optional): The type of  task: 'Regressor' for regression or
            'Classifier' for classification. Default is 'Regressor'.
        :param static_features: (None or list, optional): -
        :return: (tuple): A tuple containing the params:
            - global_best_position: (np.ndarray): The best set of hyperparameters found during optimization.
            - global_best_fitness: (float): The fitness value of the best hyperparameter set.
            - global_best_model: (object) The best-trained model corresponding to the best hyperparameter set.
            - input_layers_data : (dict): Data related to the input layers,
                including weights W and other normalization parameters.
    """

    list_limit = [param_ranges[item] for item in param_ranges.keys()]

    global_best_value = float('-inf')
    global_best_position = []

    model_config = {'X': X,
                    'y': y,
                    'shuffle': shuffle,
                    'random_state': random_state,
                    'target': target}

    start_data = [[random.uniform(limit[0], limit[1]) for limit in list_limit] for _ in range(num_particles)]

    with Pool(processes=num_threads) as pool:
        swarm = pool.starmap(Particle, zip(start_data, repeat(model_config)))

        for iterations in range(num_iterations):
            value_positions = pool.imap_unordered(train_particle, swarm)

            for i, (value, particle) in enumerate(zip(value_positions, swarm)):
                particle.update_stat_particle(value)

                if global_best_value == -1 or value > global_best_value:
                    global_best_position = list(particle.position)
                    global_best_value = value

            for particle in swarm:
                if particle.is_random_velocity:
                    particle.position = [random.uniform(limit[0], limit[1]) for limit in list_limit]
                else:
                    particle.update_velocity(global_best_position)
                    particle.update_position(list_limit)

                particle.is_random_velocity = False

            print(f"Iteration {iterations + 1}/{num_iterations}, Best Fitness in fold: {round(global_best_value, 4)}")

    pool.close()
    pool.join()



    return best_position, global_best_fitness, global_best_model, input_layers_data


if __name__ == '__main__':
    pass