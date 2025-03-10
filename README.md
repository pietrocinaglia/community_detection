# Community Detection

This repo shares an integrated (python) tool for executing community detection methods on network graphs, with no programming skills.

To give a non-exhaustive example, this tool may be used in testing cases... we would like to underline that it is a tool without too many pretensions *:-)*

## How it works

The following parameters need to be defined:

- Path for (input) network graphs

The following parameters can be included (order must be guaranteed):

- Output filename (1): the same is used both for communities files and log
- Community method/s (2): 'all' or one of the following: 'louvain', 'greedy', 'infomap' (disabled), 'k_clique' (disabled)

_(1) the path coincides with the folder where the script is located._

_(2) without quotation marks._


## Example

Basic parameters:
```
python3 community_detection.py /Users/your_username/my_folder/input_graph.txt
```

or, including all parameters:
```
python3 community_detection.py /Users/your_username/my_folder/input_graph.txt my_output louvain
```
