import pandas as pd

do_slim_columns = False

if do_slim_columns:
    raw_dataset = pd.read_csv('ufc-master.csv')
    slim_dataset = raw_dataset[["R_fighter", "B_fighter", "Winner", "finish", "finish_details", "weight_class"]]
    slim_dataset.to_csv('dataset.csv')

do_fighter_index = False

if do_fighter_index:
    slim_dataset = pd.read_csv('dataset.csv')
    fighters = slim_dataset["R_fighter"].tolist() + slim_dataset["B_fighter"].tolist()
    fighters = set(fighters) # Remove duplicate names
    with open("fighters.txt", 'w') as f:
        for fighter in fighters:
            f.write("%s\n" % (fighter))
        f.close()

do_fighter_adjacency = False

if do_fighter_adjacency:
    # Get the list of vertices in the graph
    slim_dataset = pd.read_csv('dataset.csv')
    fighters = slim_dataset["R_fighter"].tolist() + slim_dataset["B_fighter"].tolist()
    fighters = list(set(fighters)) # Remove duplicate names
    # Adjacency graph format: row_index = fighter_A_id, column_index = fighter_B_id
    #                           edge_weight = 1 if they fought
    with open("fighters.txt", 'w') as f:
        for fighter in fighters:
            f.write("%s\n" % (fighter))
        f.close()
    fighter_pairs = slim_dataset[["R_fighter", "B_fighter"]]
    with open("graph.txt", 'w') as f:
        for A in range(len(fighters)):
            # Find all B_fighter where R_fighter = fighters[A] and find all R_fighter where B_fighter = fighters[A]
            # Convert the results to lists and combine into one single list of people who fought fighters[A]
            who_fought_A = fighter_pairs[fighter_pairs["R_fighter"].isin([fighters[A]])]["B_fighter"].tolist() + fighter_pairs[fighter_pairs["B_fighter"].isin([fighters[A]])]["R_fighter"].tolist()
            for B in range(len(fighters)):
                have_we_fought = 1 if fighters[B] in who_fought_A else 0
                delimeter = "," if B < len(fighters)-1 else "\n"
                f.write("%d%s" % (have_we_fought, delimeter))
        f.close()
