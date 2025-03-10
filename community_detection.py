# -*- coding: utf-8 -*-

import pandas as pd
import networkx as nx
import networkx.algorithms.community as nx_comm
#import infomap
from datetime import datetime
import os
from unipath import Path
import sys

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
# @description: -
###

###############################

def _infomap_communities(G, weight='weight', num_trials=100):
    im = infomap.Infomap( silent=True, num_trials=num_trials ) # num_trials (int, optional, Default:1) – Number of outer-most loops to run before picking the best solution.
    mapping = im.add_networkx_graph( G, weight=weight )
    im.run()
    communities = dict()
    for node in im.nodes:
        if node.module_id not in communities:
            communities[node.module_id] = set()
        communities[node.module_id].add( mapping[node.node_id] )
        # print(node.module_id, node.flow, mapping[node.node_id])

    return list(communities.values())

def processing(basepath, input_path, output_filename = None, communities = [], delimiter = " ", verbose = True):
    if verbose:
        print ( "- Data Loading..." )

    G = nx.read_edgelist( input_path, delimiter=delimiter, data=False )
    if verbose:
        print ( "- Network (input): " + str(G.number_of_nodes()) + " nodes and " + str(G.number_of_edges()) + " edges.")

    # Runtime - start timing
    runtime = datetime.now()

    if len(communities) == 0 or 'louvain' in communities:
        if verbose:
            print()
            print ( "- Communities evaluation" )
            print ( ">> louvain_communities..." )
        communities_louvain =  nx_comm.louvain_communities( G, resolution=1, threshold=0.000001, weight='weight' )
        # print ( communities_louvain )
        modularity_louvain = nx_comm.modularity( G, communities_louvain )
        #print ( modularity_louvein )

        if output_filename is not None:
            print ( ">> - Saving data as file..." )
            file = open( basepath + output_filename + '_communities_louvain.txt', "a" )
            file.write( str(communities_louvain) )
            file.close()
    '''
    if len(communities) == 0 or 'infomap' in communities:
        if verbose:
            print ( ">> infomap_communities..." )
        communities_infomap = _infomap_communities( G, weight='weight', num_trials=100 )
        # print ( communities_infomap )
        modularity_infomap = nx_comm.modularity( G, communities_infomap )
        # print ( modularity_infomap )

        if output_filename is not None:
            print ( ">> - Saving data as file..." )
            file = open( basepath + output_filename + '_communities_infomap.txt', "a" )
            file.write( str(communities_infomap) )
            file.close()
    '''

    if len(communities) == 0 or 'greedy' in communities:
        if verbose:
            print ( ">> greedy_communities..." )
        communities_greedy = nx_comm.greedy_modularity_communities( G, weight='weight' )
        # print ( communities_greedy )
        modularity_greedy = nx_comm.modularity( G, communities_greedy )
        # print ( modularity_greedy )
        if output_filename is not None:
            print ( ">> - Saving data as file..." )
            file = open( basepath + output_filename + '_communities_greedy.txt', "a" )
            file.write( str(communities_greedy) )
            file.close()

    '''
    if len(communities) == 0 or 'k_clique' in communities:
        print ( ">> k_clique_communities..." )
        communities_k_clique = nx_comm.k_clique_communities( G, 3 )
        # print ( communities_infomap )
        modularity_k_clique = nx_comm.modularity( G, communities_k_clique )
        # print ( modularity_infomap )
        if len(communities) == 0 or 'greedy' in communities:
            print ( ">> - Saving data as file..." )
            file = open( basepath + output_filename + '_communities_k_clique.txt', "a" )
            file.write( str(communities_k_clique) )
            file.close()
    '''

    #######################

    if output_filename is not None:
        print ( "> Logging..." )

        file = open( basepath + output_filename + '_log.txt', "a" )

        file.write( "***********************************************************************\n" )
        file.write( "* Community Detection                                                 *\n" )
        file.write( "* - Methods: Louvain, Infomap (disabled), Greedy, k-clique (disabled) *\n" )
        file.write( "*                                                                     *\n" )
        file.write( "* Developer: Pietro Cinaglia - cinaglia(at)unicz.it                   *\n" )
        file.write( "* Version: 0.1-alpha                                                  *\n" )
        file.write( "* GitHub: https://github.com/pietrocinaglia/community_detection       *\n" )
        file.write( "***********************************************************************\n" )
        file.write( '\n' )

        file.write( 'Input: ' + input_path )
        file.write( '\n' )
        file.write( 'Network stats: ' + str(G.number_of_nodes()) + ' nodes, ' + str(G.number_of_edges()) + ' edges.' )
        file.write( '\n' )

        if len(communities) == 0 or 'louvain' in communities:
            file.write( '\nNo. of communities (based on Louvain): ' + str(len(communities_louvain)) )
            file.write( '\nModularity (based on Louvain): ' + str(modularity_louvain) )
            file.write( '\n' )

        '''
        if len(communities) == 0 or 'infomap' in communities:
            file.write( '\nNo. of communities (based on InfoMap): ' + str(len(communities_infomap)) )
            file.write( '\nModularity (based on InfoMap): ' + str(modularity_infomap) )
            file.write( '\n' )
        '''

        if len(communities) == 0 or 'greedy' in communities:
            file.write( '\nNo. of communities (based on Greedy): ' + str(len(communities_greedy)) )
            file.write( '\nModularity (based on Greedy): ' + str(modularity_greedy) )
            file.write( '\n' )
        '''
        if len(communities) == 0 or 'k_clique' in communities:
            file.write( '\nNo. of communities (based on k-clique): ' + str(len(communities_k_clique)) )
            file.write( '\nModularity (based on k-clique): ' + str(modularity_k_clique) )
            file.write( '\n' )
        '''
        file.write( '\n' )
        file.write( 'Runtime (total): ' + str((datetime.now() - runtime)) )
        file.close()

#######################

def main():
    print( "***********************************************************************" )
    print( "* Community Detection                                                 *" )
    print( "* - Methods: Louvain, Infomap (disabled), Greedy, k-Clique (disabled) *" )
    print( "*                                                                     *" )
    print( "* Developer: Pietro Cinaglia - cinaglia(at)unicz.it                   *" )
    print( "* Version: 0.1-alpha                                                  *" )
    print( "* GitHub: https://github.com/pietrocinaglia/community_detection       *" )
    print( "***********************************************************************" )

    ###
    # Configuration
    ###
    current_path = os.path.dirname(os.path.realpath(__file__))
    current_path = Path(current_path)
    basepath = str(current_path + "/")
    # Parameters
    input_path = None
    output_filename = None # None: no-store data
    communities = [] # 'all' (or []), 'louvain', 'greedy', 'infomap', 'k_clique'
    # optionals
    delimiter = " "
    verbose = False

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Something was wrong. Check input parameters!")
        print("(Deliminter: single-space; you must change it into the code for other options)")
        exit()
    if len(sys.argv)  == 2:
        input_path = sys.argv[1]
    elif len(sys.argv)  == 3:
        input_path = sys.argv[1]
        output_filename = sys.argv[2]
    elif len(sys.argv)  == 4:
        input_path = sys.argv[1]
        output_filename = sys.argv[2]
        if sys.argv[3] == 'all':
            communities = []
        else:
            communities = sys.argv[3]
        

    print()
    print("It will execute the following methods for community detection:")
    if len(communities) == 0 or None:
        print ( 'louvain', 'greedy' ) # ,'infomap','k_clique' )
    else:
        print( communities )
    print()
    print( "Output: " + basepath + input_path )

    processing(basepath, input_path, output_filename, communities, delimiter)

    print()
    print ( "[ DONE ]" )

## MAIN
if __name__ == "__main__":
    main()
