import pandas as pd
import sys

# Read dataset.csv, fighters.txt, and graph.txt

# This adjacency matrix is really sparse...
# For a bigger dataset it would probably be betterto use an adjacency matrix per weight class

fights = pd.read_csv('dataset.csv')
with open("fighters.txt", 'r') as f:
    fighters = f.read().split('\n')
with open("graph.txt", 'r') as f:
    adjacency_rows = f.read().split('\n')
    matchups = []
    for row in adjacency_rows:
        if len(row) == 0:
            continue
        weights = [int(item) for item in row.split(",")]
        matchups.append(weights)

def get_fighter_id(fighter_name):
    # For large enough datasets, it would probably be better to binary search a *sorted* list
    return fighters.index(fighter_name)

def get_fighter_name(fighter_id):
    return fighters[fighter_id]

def get_fights_between_ordered(fighter1, fighter2):
    fights_R = fights[fights["R_fighter"].isin([fighter1])]
    fights_between = fights_R[fights_R["B_fighter"].isin([fighter2])]
    return fights_between.values.tolist()

def get_fights_between(fighter1_id, fighter2_id):
    fighter1 = get_fighter_name(fighter1_id)
    fighter2 = get_fighter_name(fighter2_id)
    fights_between = get_fights_between_ordered(fighter1, fighter2) + get_fights_between_ordered(fighter2, fighter1)
    return fights_between

def min_dist(Q, dist):
    min_dist = sys.maxsize
    u = None
    for x in Q:
        if dist[x] < min_dist:
            min_dist = dist[x]
            u = x
    return u
def dijkstra(G, src, tgt):
    Q = []
    V = len(fighters) - 1
    dist = [sys.maxsize] * len(fighters)
    prev = [None] * len(fighters)
    for v in range(V):
        Q.append(v)
    dist[src] = 0
    while len(Q) > 0:
        U = min_dist(Q, dist)
        print("min_dist: %s" % (get_fighter_name(U)))
        Q = Q.remove(U)
        if U == tgt:
            break
        for v in range(V):
            if G[v][U] > 0:
                print("%s %s" % (get_fighter_name(v), get_fighter_name(U)))
                alt = dist[U] + G[v][U]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = U
    S = []
    u = tgt
    if prev[u] is not None or u == src:
        while u is not None:
            S.insert(0, get_fighter_name(u))
            u = prev[u]
    return S

def get_shortest_path(fighter1_id, fighter2_id):
    from1 = dijkstra(matchups, fighter1_id, fighter2_id)
    print(from1)
    return None

# To find the degrees of bacon value,
#   - Get the fighter #'s of both fighters
#   - Find the shortest path (if one exists) in graph.txt
#   - Use dataset.csv to find metadata about the fights (the edges in the graph) using lookups for fighter #
#   - Construct a list of tuples for the chain
#   - DONE

def degrees_of_bacon(fighter1, fighter2):
    fighter1_id = get_fighter_id(fighter1)
    fighter2_id = get_fighter_id(fighter2)
    fighter_chain = get_shortest_path(fighter1_id, fighter2_id)
    if fighter_chain is None:
        return None
    else:
        fight_chain = []
        for i in range(len(fighter_chain) - 1):
            fight_chain.append(get_fights_between(fighter_chain[i], fighter_chain[i + 1]))
        return fight_chain


degrees_of_bacon("Miesha Tate", "Ronda Rousey")
