#!/usr/bin/python3

#PBS -l nodes=1:ppn=1:lxxii-core

import os
import sys

if "PBS_O_WORKDIR" in os.environ:
  os.chdir(os.environ["PBS_O_WORKDIR"])

import numpy as np
import pandas as pd
import random
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp
import networkx as nx
import EoN
from collections import defaultdict
import csv

# ----------------------------------------------------------------

df = pd.read_csv('../TRUMP_CHANTING_VERIFIED.csv')
df = df[:400]

yData = np.cumsum(df['total_tweets'])
xData = np.arange(0, len(df), 1)

tSpan = [0, len(df)]

I0 = yData[0]

# ----------------------------------------------------------------

def seiz(t, y, S0, E0, Z0, beta, b, ro, p, e, l):
    S = y[0]
    E = y[1]
    I = y[2]
    Z = y[3]
    
    N = S0 + E0 + I0 + Z0
    
    dS = -1 * beta * S * (I / N) - b * S * (Z / N)
    dE = (1 - p) * beta * S * (I / N) + (1 - l) * b * S * (Z / N) - ro * E * (I / N) - e * E
    dI = p * beta * S * (I / N) + ro * E * (I / N) + e * E
    dZ = l * b * S * (Z / N)

    return [dS, dE, dI, dZ]

def solve_seiz(x, *args):
    initialValues = [args[0], args[1], I0, args[2]]
    
    return solve_ivp(seiz, tSpan, initialValues, method='BDF', t_eval=x, args=args).y

def fit_seiz(x, *args):
    return solve_seiz(x, *args)[2]

initial_guess = [100, 100, 100, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10]
bounds = (0, [9e8, 9e8, 9e8, 100, 100, 100, 1, 1, 1])

popt, pcov = curve_fit(fit_seiz, xData, yData, initial_guess, bounds=bounds)

N = round(popt[0] + popt[1] + I0 + popt[2])

S0 = round(popt[0])
E0 = round(popt[1])
I0 = round(I0)
Z0 = round(popt[2])

beta = popt[3]
b = popt[4]
ro = popt[5]
p = popt[6]
e = popt[7]
l = popt[8]

# ----------------------------------------------------------------

I_simulations = []
simulation_count = 100

for i in range(simulation_count):
    degrees = []

    in_degrees = []
    out_degrees = []

    for i in range(N):
        n = np.random.uniform(1, 330*1e6)

        follower_count = 1e7*((1 / n)**0.62)

        degrees.append(round(follower_count))

    in_degrees = random.sample(degrees, len(degrees))
    out_degrees = random.sample(degrees, len(degrees))

    average_degree = (np.array(out_degrees).sum() / N)

    scaler = (N - 1) / average_degree

    beta_ntw = (beta * scaler) / N
    b_ntw = (b * scaler) / N
    ro_ntw = (ro * scaler) / N
    
    G = nx.directed_configuration_model(in_degrees, out_degrees)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    def return_combined_rates(G, node, status, list_nbr, list_rates):
        combined_rate = 0

        for i in range(len(list_nbr)):
            nbr_status = list_nbr[i]
            rate = list_rates[i]  

            neighbours = len([nbr for nbr in G.neighbors(node) if status[nbr] == nbr_status])

            combined_rate += (rate * neighbours)

        return combined_rate

    def rate_function(G, node, status, parameters):
        beta_ntw, b_ntw, ro_ntw, p, e, l = parameters

        if status[node] == 'E':
            return e + return_combined_rates(G, node, status, ['I'], [ro_ntw])

        elif status[node] == 'S':
            return return_combined_rates(G, node, status, ['I', 'Z'], [beta_ntw, b_ntw])
        else:
            return 0

    def transition_choice(G, node, status, parameters):
        beta_ntw, b_ntw, ro_ntw, p, e, l = parameters

        if status[node] == 'E':
            return 'I'
        elif status[node] == 'S':

            rate_of_infection = return_combined_rates(G, node, status, ['I'], [beta_ntw])
            rate_of_skeptisim = return_combined_rates(G, node, status, ['Z'], [b_ntw])

            combined_rate = rate_of_infection + rate_of_skeptisim

            prob_of_infection = rate_of_infection / combined_rate
            prob_of_skeptisim = rate_of_skeptisim / combined_rate

            if np.random.choice(['I', 'Z'], p=[prob_of_infection, prob_of_skeptisim]) == 'I':
                return np.random.choice(['I', 'E'], p=[p, 1 - p])
            else:
                return np.random.choice(['E', 'Z'], p=[1 - l, l])

    def get_influence_set(G, node, status, parameters):
        return G.predecessors(node)

    parameters = (beta_ntw, b_ntw, ro_ntw, p, e, l)

    IC = defaultdict(lambda: 'S')

    for node in range(E0):
        IC[node] = 'E'

    for node in range(I0):
        IC[node + I0] = 'I'

    for node in range(round(Z0)):
        IC[node + (E0 + I0)] = 'Z'


    t, S, E, I, Z = EoN.Gillespie_complex_contagion(G, rate_function,
                               transition_choice, get_influence_set, IC,
                               return_statuses=('S', 'E', 'I', 'Z'),
                               parameters=parameters, tmax=400)
    
    x_common = np.linspace(0, 400, 400)
    
    I_simulations.append(np.interp(x_common, t, I))

# ----------------------------------------------------------------

with open('simulations.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for row in I_simulations:
        spamwriter.writerow(row)