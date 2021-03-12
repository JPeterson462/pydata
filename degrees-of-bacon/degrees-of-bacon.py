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
    try:
    # For large enough datasets, it would probably be better to binary search a *sorted* list
        return fighters.index(fighter_name)
    except:
        return None

def get_fighter_name(fighter_id):
    try:
        return fighters[fighter_id]
    except:
        return None

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
        if U is None:
            return None # No path found
        Q.remove(U)
        if U == tgt:
            break
        for v in range(V):
            if G[v][U] > 0:
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
    fight_path = dijkstra(matchups, fighter1_id, fighter2_id)
    if fight_path is None:
        return None
    named_fight_path = [get_fighter_id(name) for name in fight_path]
    result = []
    for i in range(len(named_fight_path) - 1):
        edge_start = named_fight_path[i]
        edge_end = named_fight_path[i + 1]
        fights = get_fights_between(edge_start, edge_end)
        result_matchups = []
        for fight in fights:
            _, red_corner, blue_corner, winner, win_type, win_details, weight_class = fight
            did_they_win = (red_corner == fight_path[i] and winner == 'Red') or (blue_corner == fight_path[i] and winner == 'Blue')
            result_matchups.append((fight_path[i], fight_path[i + 1], did_they_win, win_type, win_details, weight_class))
        result.append(result_matchups)
    return result

# To find the degrees of bacon value,
#   - Get the fighter #'s of both fighters
#   - Find the shortest path (if one exists) in graph.txt
#   - Use dataset.csv to find metadata about the fights (the edges in the graph) using lookups for fighter #
#   - Construct a list of tuples for the chain
#   - DONE

win_type_lookup = {
    "SUB": ["Submission", True],
    "U-DEC": ["Unanimous Decision", False],
    "S-DEC": ["Split Decision", False],
    "M-DEC": ["Majority Decision", False],
    "KO/TKO": ["KO/TKO", True],
    "DQ": ["Disqualification", True],
    "Overturned": ["Overturned", True],
}
def format_fight_result(win_type, win_details):
    win_type, has_details = win_type_lookup.get(win_type, ["(unknown)", False])
    if has_details:
        return "%s (%s)" % (win_type, win_details)
    else:
        return win_type

def format_fight(fight):
    edge_start, edge_end, did_they_win, win_type, win_details, weight_class = fight
    did_they_win_formatted = "beat" if did_they_win else "lost to"
    return "%s %s %s by %s at %s" % (edge_start, did_they_win_formatted, edge_end, format_fight_result(win_type, win_details), weight_class)

def format_matchup(fight_list):
    first_fight_for_reference = list(fight_list[0])
    matchup_formatted = "%s -> %s\n" % (first_fight_for_reference[0], first_fight_for_reference[1])
    for fight in fight_list:
        matchup_formatted = matchup_formatted + "\t" + format_fight(fight) + "\n"
    return matchup_formatted

def degrees_of_bacon(fighter1, fighter2):
    fighter1_id = get_fighter_id(fighter1)
    fighter2_id = get_fighter_id(fighter2)
    if fighter1_id is None:
        return "Fighter %s does not exist in this dataset" % (fighter1)
    if fighter2_id is None:
        return "Fighter %s does not exist in this dataset" % (fighter2)
    fighter_chain = get_shortest_path(fighter1_id, fighter2_id) if fighter1_id != fighter2_id else []
    if fighter_chain is None or len(fighter_chain) == 0:
        return "%s and %s have a bacon number of infinity" % (fighter1, fighter2)
    bacon_number = "%s and %s have a bacon number of %d\n\n" % (fighter1, fighter2, len(fighter_chain))
    formatted_matchup_list = [format_matchup(fight_pair) for fight_pair in fighter_chain]
    fighter_chain_formatted = bacon_number + "\n".join(formatted_matchup_list)
    return fighter_chain_formatted

if len(sys.argv) < 3:
    sys.exit(1)

degrees = degrees_of_bacon(sys.argv[1], sys.argv[2])
print(degrees)
