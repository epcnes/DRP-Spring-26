import numpy as np
from numpy.random import rand, randint
import gurobipy as gp
from gurobipy import GRB

# https://docs.gurobi.com/

# --- API --- #
params = {
"WLSACCESSID": "bf9a9974-82e7-4745-8a9c-d853d1d65926",
"WLSSECRET": "a9bbbc67-d3f4-4958-8aa2-c2e5a7b0a357",
"LICENSEID": 2773076,
}
env = gp.Env(params=params)

# --- Setup --- #
scenes = ["Scene1", "Scene2", "Scene3", "Scene4", "Scene5", "Scene6", "Scene7", "Scene8", "Scene9"]
actors = ["Actor1", "Actor2", "Actor3", "Actor4", "Actor5", "Actor6", "Actor7", "Actor8", "Actor9"]
n = len(scenes)
m = len(actors)
holdingCost=[760, 620, 850, 920, 760, 720, 870, 650, 820]
durations = [50, 50, 30, 40, 30, 50, 20, 50, 40]
sceneDuration = dict(zip(scenes, durations))
actorHolding = dict(zip(actors, holdingCost))
W = 120

# Table 1
T =np.matrix([
    [1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1, 0]
])

availability = {
    (w, s): T[j, i] for i, s in enumerate(scenes) for j, w in enumerate(actors) if T[j, i] == 1
}

# Table 2
S = np.matrix([
    [0, 2, 4, 3, 1, 1, 3, 4, 5],
    [9, 0, 9, 4, 6, 10, 7, 6, 6],
    [1, 6, 0, 5, 7, 1, 4, 6, 2],
    [4, 7, 5, 0, 1, 9, 6, 3, 5],
    [2, 4, 5, 2, 0, 1, 10, 5, 2],
    [2, 6, 8, 3, 2, 0, 1, 3, 10],
    [4, 9, 10, 5, 2, 1, 0, 8, 9],
    [10, 5, 8, 3, 2, 7, 6, 0, 10],
    [10, 6, 1, 7, 4, 1, 7, 5, 0]
])

# ---  Computational Comparison --- #
# Number of scenes 𝑛 ∈ {10, 15, 20, 30, 40, 50, 60};
# Number of actors 𝑚 ∈ {10, 20};
# Capacity 𝑊 ∈ {50, 75};
# Density 𝜌 ∈ {0.3, 0.5} controls the probability for an actor to be present in a scene:
#   if the real number randomly drawn in [0, 1] is smaller than or equal to 𝜌, then 𝑡
#   𝑖,𝑗 = 1; 0, otherwise;
# Duration 𝓁𝑗 was randomly sampled from the integer uniform distribution [1, 20];
# Changeover time 𝑠𝑖,𝑗 was randomly sampled from the integer uniform distribution [1, 10].

# scenes = [10, 15, 20, 30, 40, 50, 60]
# actors = [10, 20]
# W = [50, 75]
# p = [0.3, 0.5]
# durations = list(randint(1, 21, (1, i)) for i in scenes)
# S = list(randint(1, 11, (i, i)) for i in scenes)
# T = list((rand(i, j) <= x).astype(int) for i in actors for j in scenes for x in p)

