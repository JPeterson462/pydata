# MMA Degrees of Bacon
This program was tested with (and by default uses) the [Ultimate UFC Dataset](https://www.kaggle.com/mdabbert/ultimate-ufc-dataset). This implementation uses Djikstra shortest path to find the shortest path between two fighters in an undirected, unweighted graph of fights.

## Preprocessing Data
*preprocess.py* performs incremental preprocessing to convert data to a normalized *dataset.csv* with supporting files *fighters.txt* an *graph.txt* (an adjacency matrix indexed by *fighters.txt*)
