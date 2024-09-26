#!/usr/bin/env python3

import concurrent.futures
import csv
import gc
import logging
import math
import operator
import os
import pathlib
import subprocess
import sys
import time

from Bio import SeqIO
from igraph import *
from tqdm import tqdm

from metacoag.metacoag_utils import (feature_utils, graph_utils, label_prop_utils,
                            marker_gene_utils, matching_utils)
from metacoag.metacoag_utils.bidirectionalmap import BidirectionalMap

__author__ = "Vijini Mallawaarachchi and Yu Lin"
__copyright__ = "Copyright 2020, MetaCoAG Project"
__license__ = "GPL-3.0"
__version__ = "1.2.2"
__maintainer__ = "Vijini Mallawaarachchi"
__email__ = "vijini.mallawaarachchi@anu.edu.au"
__status__ = "Stable Release"

# Set global paramters
# ---------------------------------------------------

MAX_WEIGHT = sys.float_info.max


def run(args):

    # Get arguments
    # ------------------------------------------------------------------------

    assembler = args.assembler
    graph = args.graph
    contigs = args.contigs
    abundance = args.abundance
    paths = args.paths
    output = args.output
    hmm = args.hmm
    prefix = args.prefix
    min_length = args.min_length
    p_intra = args.p_intra
    p_inter = args.p_inter
    d_limit = args.d_limit
    depth = args.depth
    n_mg = args.n_mg
    no_cut_tc = args.no_cut_tc
    mg_threshold = args.mg_threshold
    bin_mg_threshold = args.bin_mg_threshold
    min_bin_size = args.min_bin_size
    delimiter = args.delimiter
    nthreads = args.nthreads

    contigs_file = contigs
    assembly_graph_file = graph
    contig_paths_file = paths
    abundance_file = abundance
    output_path = output

    # Setup logger
    # ------------------------------------------------------------------------

    logger = logging.getLogger(f"MetaCoaAG {__version__}")
    logger.setLevel(logging.DEBUG)
    logging.captureWarnings(True)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    consoleHeader = logging.StreamHandler()
    consoleHeader.setFormatter(formatter)
    consoleHeader.setLevel(logging.INFO)
    logger.addHandler(consoleHeader)

    # Setup output path for log file
    fileHandler = logging.FileHandler(f"{output_path}/{prefix}metacoag.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    # Set thresholds
    bin_threshold = -math.log(p_intra, 10)
    break_threshold = -math.log(p_inter, 10)

    n_bins = 0

    # Validate prefix
    if prefix != "":
        if not prefix.endswith("_"):
            prefix = f"{prefix}_"

    # Validate files
    # ------------------------------------------------------------------------

    # Check if paths file is provided when the assembler type is SPAdes
    if assembler.lower() == "spades" and contig_paths_file is None:
        logger.error("Please make sure to provide the path to the contigs.paths file.")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    # Check if paths file is provided when the assembler type is Flye
    if assembler.lower() == "flye" and contig_paths_file is None:
        logger.error("Please make sure to provide the path to the assembly_info.txt file.")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    # Skip paths file when the assembler type is MEGAHIT
    if assembler.lower() == "megahit":
        contig_paths_file = "None"

    # Validate min_bin_size
    if min_bin_size <= 0:
        logger.error("Please enter a valid number for min_bin_size")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)
    
    # Validate depth
    if depth <= 0:
        logger.error("Please enter a valid number for depth")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    # Validate d_limit
    if d_limit <= 0:
        logger.error("Please enter a valid number for d_limit")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)
    
    # Validate number of threads
    if nthreads <= 0:
        logger.error("Please enter a valid number for the number of threads")
        logger.error("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    # Start MetaCoAG
    # ------------------------------------------------------------------------

    logger.info(
        "Welcome to MetaCoAG: Binning Metagenomic Contigs via Composition, Coverage and Assembly Graphs."
    )

    logger.info("Input arguments: ")
    logger.info(f"Assembler used: {assembler}")
    logger.info(f"Contigs file: {contigs_file}")
    logger.info(f"Assembly graph file: {assembly_graph_file}")
    logger.info(f"Contig paths file: {contig_paths_file}")
    logger.info(f"Abundance file: {abundance_file}")
    logger.info(f"Final binning output file: {output_path}")
    logger.info(f"Marker gene file hmm: {hmm}")
    logger.debug(f"Number of marker genes in hmm file: {n_mg}")
    logger.info(f"Minimum length of contigs to consider: {min_length}")
    logger.info(f"Depth to consider for label propagation: {depth}")
    logger.info(f"p_intra: {p_intra}")
    logger.info(f"p_inter: {p_inter}")
    logger.debug(f"bin_threshold: {bin_threshold}")
    logger.debug(f"break_threshold: {break_threshold}")
    logger.info(f"Do not use --cut_tc: {no_cut_tc}")
    logger.info(f"mg_threshold: {mg_threshold}")
    logger.info(f"bin_mg_threshold: {bin_mg_threshold}")
    logger.info(f"min_bin_size: {min_bin_size} base pairs")
    logger.info(f"d_limit: {d_limit}")
    logger.info(f"Number of threads: {nthreads}")
    
    logger.info("MetaCoAG started")
    start_time = time.time()


    # Get links of the assembly graph
    # ------------------------------------------------------------------------

    # try:
    if assembler == "spades":
        # Get paths, segments, links and contigs of the assembly graph
        (
            paths,
            segment_contigs,
            node_count,
            contigs_map,
            contig_names,
        ) = graph_utils.get_segment_paths_spades(contig_paths_file)

        # Get reverse mapping of contig map
        contigs_map_rev = contigs_map.inverse

        # Get reverse mapping of contig identifiers
        contig_names_rev = contig_names.inverse

    if assembler == "megahit":
        original_contigs = {}
        contig_descriptions = {}

        # Get mapping of original contig identifiers with descriptions
        for index, record in enumerate(SeqIO.parse(contigs_file, "fasta")):
            original_contigs[record.id] = str(record.seq)
            contig_descriptions[record.id] = record.description

        # Get links and contigs of the assembly graph
        (
            node_count,
            graph_contigs,
            links,
            contig_names,
        ) = graph_utils.get_links_megahit(assembly_graph_file)

        # Get reverse mapping of contig identifiers
        contig_names_rev = contig_names.inverse

    if assembler == "flye":
        # Get contigs map
        contig_names = graph_utils.get_flye_contig_map(contigs_file)

        # Get reverse mapping of contig identifiers
        contig_names_rev = contig_names.inverse

        # Get links and contigs of the assembly graph
        (
            paths,
            segment_contigs,
            node_count,
            contigs_map,
        ) = graph_utils.get_links_flye(contig_paths_file, contig_names_rev)

        # Get reverse mapping of contig map
        contigs_map_rev = contigs_map.inverse

    if assembler == "megahitc":

        # Get links and contigs of the assembly graph
        (
            node_count,
            links,
            contig_names,
        ) = graph_utils.get_links_megahit_custom(assembly_graph_file)

        # Get reverse mapping of contig identifiers
        contig_names_rev = contig_names.inverse

    if assembler == "custom":

        # Get links and contigs of the assembly graph
        (
            node_count,
            links,
            contig_names,
        ) = graph_utils.get_links_custom(assembly_graph_file)

        # Get reverse mapping of contig identifiers
        contig_names_rev = contig_names.inverse

    # except:
    #     logger.error(
    #         "Please make sure that the correct path to the contig paths file is provided."
    #     )
    #     logger.info("Exiting MetaCoAG... Bye...!")
    #     sys.exit(1)

    # Construct the assembly graph
    # -------------------------------

    all_contigs = [x for x in range(node_count)]

    try:
        # Create graph
        assembly_graph = Graph()

        # Add vertices
        assembly_graph.add_vertices(node_count)
        logger.info(f"Total number of contigs available: {node_count}")

        # Name vertices with contig identifiers
        for i in range(node_count):
            assembly_graph.vs[i]["id"] = i
            assembly_graph.vs[i]["label"] = contig_names[i]

        # Get list of edges
        if assembler == "spades":
            edge_list = graph_utils.get_graph_edges_spades(
                assembly_graph_file=assembly_graph_file,
                contigs_map=contigs_map,
                contigs_map_rev=contigs_map_rev,
                paths=paths,
                segment_contigs=segment_contigs,
            )

        if assembler == "flye":
            edge_list = graph_utils.get_graph_edges_flye(
                assembly_graph_file=assembly_graph_file,
                contigs_map=contigs_map,
                contigs_map_rev=contigs_map_rev,
                paths=paths,
                segment_contigs=segment_contigs,
            )

        if assembler == "megahit" or assembler == "megahitc" or assembler == "custom":
            edge_list = graph_utils.get_graph_edges_megahit(
                links=links, contig_names_rev=contig_names_rev
            )
        

        # Add edges to the graph
        assembly_graph.add_edges(edge_list)

        # Simplify the graph
        assembly_graph.simplify(multiple=True, loops=False, combine_edges=None)

        logger.info(f"Total number of edges in the assembly graph: {len(list(assembly_graph.es))}")

    except:
        logger.error(
            "Please make sure that the correct path to the assembly graph file is provided."
        )
        logger.info("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    if assembler == "megahit":
        # Map original contig identifiers to contig identifiers of MEGAHIT assembly graph
        graph_to_contig_map = BidirectionalMap()

        for (n, m), (n2, m2) in zip(graph_contigs.items(), original_contigs.items()):
            if m == m2:
                graph_to_contig_map[n] = n2

        graph_to_contig_map_rev = graph_to_contig_map.inverse

    # Get isolated contigs with no neighbours
    isolated = graph_utils.get_isolated(node_count, assembly_graph)

    logger.info(f"Total isolated contigs in the assembly graph: {len(isolated)}")

    # Get the number of samples and the length and coverage of contigs
    # ------------------------------------------------------------------------

    logger.info("Obtaining lengths and coverage values of contigs")

    if assembler == "megahit":
        (
            sequences,
            coverages,
            contig_lengths,
            n_samples,
        ) = feature_utils.get_cov_len_megahit(
            contigs_file=contigs_file,
            contig_names_rev=contig_names_rev,
            graph_to_contig_map_rev=graph_to_contig_map_rev,
            min_length=min_length,
            abundance_file=abundance_file,
        )

    else:
        sequences, coverages, contig_lengths, n_samples = feature_utils.get_cov_len(
            contigs_file=contigs_file,
            contig_names_rev=contig_names_rev,
            min_length=min_length,
            abundance_file=abundance_file,
        )

    isolated_long = []

    my_long = 0

    for contig in contig_lengths:
        if contig_lengths[contig] >= min_length:
            my_long += 1

    for contig in isolated:
        if contig_lengths[contig] >= min_length:
            isolated_long.append(contig)

    logger.info(f"Total long contigs: {my_long}")
    logger.info(f"Total isolated long contigs in the assembly graph: {len(isolated_long)}")

    # Set intra weight and inter weight
    # ------------------------------------------------------------------------

    w_intra = bin_threshold * (n_samples + 1)
    w_inter = break_threshold * (n_samples + 1)

    logger.debug(f"w_intra: {w_intra}")
    logger.debug("w_inter: {w_inter}")

    # Get tetramer composition of contigs
    # ------------------------------------------------------------------------

    logger.info("Obtaining tetranucleotide frequencies of contigs")

    normalized_tetramer_profiles = feature_utils.get_tetramer_profiles(
        output_path=output_path,
        sequences=sequences,
        contigs_file=contigs_file,
        contig_lengths=contig_lengths,
        min_length=min_length,
        nthreads=nthreads,
    )

    del sequences
    gc.collect()

    # Get contigs with marker genes
    # -----------------------------------------------------

    logger.info("Scanning for single-copy marker genes")

    if not os.path.exists(f"{contigs_file}.hmmout"):
        # Check if FragGeneScan is installed
        try:
            p = subprocess.run(["which", "run_FragGeneScan.pl"], capture_output=True)
            if p.returncode != 0:
                raise Exception("Command does not exist")
        except:
            logger.error(
                "FragGeneScan does not exist. Please install from https://omics.informatics.indiana.edu/FragGeneScan/"
            )
            sys.exit(1)

        # Check if HMMER is installed
        try:
            p = subprocess.run(["which", "hmmsearch"], capture_output=True)
            if p.returncode != 0:
                raise Exception("Command does not exist")
        except:
            logger.error(
                "hmmsearch does not exist. Please install from http://hmmer.org/"
            )
            sys.exit(1)

        # Run FragGeneScan and HMMER if .hmmout file is not present
        logger.info("Obtaining hmmout file")
        marker_gene_utils.scan_for_marker_genes(
            contigs_file=contigs_file,
            nthreads=nthreads, 
            markerURL=hmm,
            no_cut_tc = no_cut_tc
        )
    else:
        logger.info(".hmmout file already exists")

    logger.info("Obtaining contigs with single-copy marker genes")

    # Get contigs with single-copy marker genes and count of contigs for each single-copy marker gene
    if assembler == "megahit":
        (
            marker_contigs,
            marker_contig_counts,
            contig_markers,
        ) = marker_gene_utils.get_contigs_with_marker_genes_megahit(
            contigs_file=contigs_file,
            contig_names_rev=contig_names_rev,
            graph_to_contig_map_rev=graph_to_contig_map_rev,
            mg_length_threshold=mg_threshold,
            contig_lengths=contig_lengths,
            min_length=min_length,
        )

    else:
        (
            marker_contigs,
            marker_contig_counts,
            contig_markers,
        ) = marker_gene_utils.get_contigs_with_marker_genes(
            contigs_file=contigs_file,
            contig_names_rev=contig_names_rev,
            mg_length_threshold=mg_threshold,
            contig_lengths=contig_lengths,
            min_length=min_length,
        )

        all_contig_markers = marker_gene_utils.get_all_contigs_with_marker_genes(
            contigs_file=contigs_file,
            contig_names_rev=contig_names_rev,
            mg_length_threshold=mg_threshold,
        )

    logger.info(f"Number of contigs containing single-copy marker genes: {len(contig_markers)}")

    # Check if there are contigs with single-copy marker genes
    if len(contig_markers) == 0:
        logger.info(
            "Could not find contigs that contain single-copy marker genes. The dataset cannot be binned."
        )
        logger.info("Exiting MetaCoAG... Bye...!")
        sys.exit(1)

    # Get single-copy marker gene counts to make bins
    # -----------------------------------------------------

    logger.info("Determining contig counts for each single-copy marker gene")

    # Get the count of contigs for each single-copy marker gene
    my_gene_counts = list(marker_contig_counts.values())

    # Sort the counts in the descending order
    my_gene_counts.sort(reverse=True)

    logger.debug("Contig counts of single-copy marker genes: ")
    logger.debug(str(my_gene_counts))

    # Get contigs containing each single-copy marker gene for each iteration
    # -----------------------------------------------------

    smg_iteration = {}

    n = 0

    unique_my_gene_counts = list(set(my_gene_counts))
    unique_my_gene_counts.sort(reverse=True)

    # Get contigs for each iteration of single-copy marker gene
    for g_count in unique_my_gene_counts:
        # Get the single-copy marker genes with maximum count of contigs and
        # sort them in the descending order of the total marker genes contained

        total_contig_mgs = {}

        for item in marker_contig_counts:
            if marker_contig_counts[item] == g_count:
                total_contig_lengths = 0

                for contig in marker_contigs[item]:
                    contig_mg_counts = len(contig_markers[contig])
                    total_contig_lengths += contig_mg_counts

                total_contig_mgs[item] = total_contig_lengths

        total_contig_mgs_sorted = sorted(
            total_contig_mgs.items(), key=operator.itemgetter(1), reverse=True
        )

        for item in total_contig_mgs_sorted:
            smg_iteration[n] = marker_contigs[item[0]]
            n += 1

    # Initialise bins
    # -----------------------------------------------------

    bins = {}
    bin_of_contig = {}
    bin_markers = {}

    binned_contigs_with_markers = []

    logger.info("Initialising bins")

    # Initialise bins with the contigs having the first single-copy
    # marker gene according to the ordering

    for i in range(len(smg_iteration[0])):
        binned_contigs_with_markers.append(smg_iteration[0][i])
        contig_num = smg_iteration[0][i]

        bins[i] = [contig_num]
        bin_of_contig[contig_num] = i

        bin_markers[i] = contig_markers[contig_num]

    logger.debug(f"Number of initial bins detected: {len(smg_iteration[0])}")
    logger.debug("Initialised bins: ")
    logger.debug(bins)

    # Assign contigs with single-copy marker genes to bins
    # -----------------------------------------------------

    logger.info("Matching and assigning contigs with single-copy marker genes to bins")

    # Matching contigs to bins
    (
        bins,
        bin_of_contig,
        n_bins,
        bin_markers,
        binned_contigs_with_markers,
    ) = matching_utils.match_contigs(
        smg_iteration=smg_iteration,
        bins=bins,
        n_bins=n_bins,
        bin_of_contig=bin_of_contig,
        binned_contigs_with_markers=binned_contigs_with_markers,
        bin_markers=bin_markers,
        contig_markers=contig_markers,
        contig_lengths=contig_lengths,
        contig_names=contig_names,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
        coverages=coverages,
        assembly_graph=assembly_graph,
        w_intra=w_intra,
        w_inter=w_inter,
        d_limit=d_limit,
    )

    logger.debug(f"Number of bins after matching: {len(bins)}")

    logger.debug("Bins with contigs containing seed marker genes")

    for b in bins:
        logger.debug(f"{b}: {bins[b]}")

    logger.debug(f"Number of binned contigs with single-copy marker genes: {len(bin_of_contig)}")

    del smg_iteration
    del my_gene_counts
    del unique_my_gene_counts
    del marker_contigs
    del marker_contig_counts
    del total_contig_mgs
    gc.collect()

    # Further assign contigs with seed marker genes
    # -------------------------------------------------

    # Get contigs with single-copy marker genes which are not matched to bins
    unbinned_mg_contigs = list(
        set(contig_markers.keys()) - set(binned_contigs_with_markers)
    )

    unbinned_mg_contig_lengths = {}

    # Get the lengths of the unmatched contigs
    for contig in unbinned_mg_contigs:
        contigid = contig
        unbinned_mg_contig_lengths[contig] = contig_lengths[contigid]

    # Sort the unmatched in the the descending order of their contig lengths
    unbinned_mg_contig_lengths_sorted = sorted(
        unbinned_mg_contig_lengths.items(), key=operator.itemgetter(1), reverse=True
    )

    logger.debug(f"Number of unbinned contigs with single-copy marker genes: {len(unbinned_mg_contigs)}")

    logger.info("Further assigning contigs with single-copy marker genes")

    # Further assigning unmatched contigs to bins
    (
        bins,
        bin_of_contig,
        n_bins,
        bin_markers,
        binned_contigs_with_markers,
    ) = matching_utils.further_match_contigs(
        unbinned_mg_contigs=unbinned_mg_contig_lengths_sorted,
        min_length=min_length,
        bins=bins,
        n_bins=n_bins,
        bin_of_contig=bin_of_contig,
        binned_contigs_with_markers=binned_contigs_with_markers,
        bin_markers=bin_markers,
        contig_markers=contig_markers,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
        coverages=coverages,
        w_intra=w_intra,
    )

    # Get remaining contigs with single-copy marker genes which are not assigned to bins
    unbinned_mg_contigs = list(
        set(contig_markers.keys()) - set(binned_contigs_with_markers)
    )

    logger.debug(f"Remaining number of unbinned MG seed contigs: {len(unbinned_mg_contigs)}")
    logger.debug(f"Number of binned contigs with single-copy marker genes: {len(bin_of_contig)}")

    del unbinned_mg_contigs
    del unbinned_mg_contig_lengths
    del unbinned_mg_contig_lengths_sorted
    gc.collect()

    # Get seed bin counts and profiles
    # -----------------------------------------------------

    smg_bin_counts = []

    # Get the count of contigs with single-copy marker genes in each bin
    for i in bins:
        smg_bin_counts.append(len(bins[i]))

    # Get composition and coverage profiles for each bin
    # based on contigs with single-copy marker genes
    (
        bin_seed_tetramer_profiles,
        bin_seed_coverage_profiles,
    ) = feature_utils.get_bin_profiles(
        bins=bins,
        coverages=coverages,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
    )

    # Get binned and unbinned contigs
    # -----------------------------------------------------

    binned_contigs = list(bin_of_contig.keys())

    unbinned_contigs = list(set([x for x in range(node_count)]) - set(binned_contigs))

    logger.debug(f"Number of binned contigs: {len(binned_contigs)}")
    logger.debug(f"Number of unbinned contigs: {len(unbinned_contigs)}")
    logger.debug(f"Number of binned contigs with markers: {len(binned_contigs_with_markers)}")

    # Get components without labels
    # -----------------------------------------------------

    # Get connected contigs within the labelled components
    non_isolated = graph_utils.get_non_isolated(
        node_count=node_count,
        assembly_graph=assembly_graph,
        binned_contigs=binned_contigs,
        nthreads=nthreads
    )

    logger.debug(f"Number of non-isolated contigs: {len(non_isolated)}")

    # Propagate labels to vertices of unlabelled long contigs
    # -----------------------------------------------------

    logger.info("Propagating labels to connected vertices of unlabelled long contigs")

    # Label propagation on connected vertices of unlabelled long contigs
    (
        bins,
        bin_of_contig,
        bin_markers,
        binned_contigs_with_markers,
    ) = label_prop_utils.label_prop(
        bin_of_contig=bin_of_contig,
        bins=bins,
        contig_markers=contig_markers,
        bin_markers=bin_markers,
        binned_contigs_with_markers=binned_contigs_with_markers,
        smg_bin_counts=smg_bin_counts,
        non_isolated=non_isolated,
        contig_lengths=contig_lengths,
        min_length=min_length,
        assembly_graph=assembly_graph,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
        coverages=coverages,
        depth=1,
        weight=w_intra,
    )

    logger.debug(f"Total number of binned contigs: {len(bin_of_contig)}")

    # Further propagate labels to vertices of unlabelled long contigs
    # --------------------------------------------------------------------------------

    # Further label propagation on connected vertices of unlabelled long contigs
    (
        bins,
        bin_of_contig,
        bin_markers,
        binned_contigs_with_markers,
    ) = label_prop_utils.label_prop(
        bin_of_contig=bin_of_contig,
        bins=bins,
        contig_markers=contig_markers,
        bin_markers=bin_markers,
        binned_contigs_with_markers=binned_contigs_with_markers,
        smg_bin_counts=smg_bin_counts,
        non_isolated=non_isolated,
        contig_lengths=contig_lengths,
        min_length=min_length,
        assembly_graph=assembly_graph,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
        coverages=coverages,
        depth=depth,
        weight=w_inter,
    )

    logger.debug(f"Total number of binned contigs: {len(bin_of_contig)}")

    # Get binned and unbinned contigs
    # -----------------------------------------------------

    binned_contigs = list(bin_of_contig.keys())

    unbinned_contigs = list(set([x for x in range(node_count)]) - set(binned_contigs))

    logger.debug(f"Number of binned contigs: {len(binned_contigs)}")
    logger.debug(f"Number of unbinned contigs: {len(unbinned_contigs)}")

    # Propagate labels to vertices of unlabelled long contigs in isolated components
    # -----------------------------------------------------------------------------------------------

    logger.info("Further propagating labels to vertices of unlabelled long contigs")

    # Get long unbinned contigs
    long_unbinned = list(
        filter(
            lambda contig: contig not in bin_of_contig
            and contig_lengths[contig] >= min_length,
            all_contigs,
        )
    )

    # Starting propagation of labels to vertices of unlabelled long contigs

    assigned = [None for itr in long_unbinned]

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=nthreads)

    # Thread function for workers

    def thread_function(
        n,
        contig,
        coverages,
        normalized_tetramer_profiles,
        bin_seed_tetramer_profiles,
        bin_seed_coverage_profiles,
    ):
        bin_result = label_prop_utils.assign_long(
            contigid=contig,
            coverages=coverages,
            normalized_tetramer_profiles=normalized_tetramer_profiles,
            bin_tetramer_profiles=bin_seed_tetramer_profiles,
            bin_coverage_profiles=bin_seed_coverage_profiles,
        )
        assigned[n] = bin_result

    exec_args = []

    for n, contig in enumerate(long_unbinned):
        exec_args.append(
            (
                n,
                contig,
                coverages,
                normalized_tetramer_profiles,
                bin_seed_tetramer_profiles,
                bin_seed_coverage_profiles,
            )
        )

    for itr in tqdm(
        executor.map(lambda p: thread_function(*p), exec_args), total=len(long_unbinned)
    ):
        pass

    executor.shutdown(wait=True)

    # End propagation of labels to vertices of unlabelled long contigs

    put_to_bins = [x for x in assigned if x is not None]

    if len(put_to_bins) == 0:
        logger.debug("No further contigs were binned")
    else:
        # Add contigs to bins according to assignment
        (
            bins,
            bin_of_contig,
            bin_markers,
            binned_contigs_with_markers,
        ) = label_prop_utils.assign_to_bins(
            put_to_bins=put_to_bins,
            bins=bins,
            bin_of_contig=bin_of_contig,
            bin_markers=bin_markers,
            binned_contigs_with_markers=binned_contigs_with_markers,
            contig_markers=contig_markers,
            contig_lengths=contig_lengths,
        )

    logger.debug(f"Total number of binned contigs: {len(bin_of_contig)}")

    #  Further propagate labels to vertices of unlabelled long contigs
    # --------------------------------------------------------------------------------

    logger.info(
        "Further propagating labels to connected vertices of unlabelled long contigs"
    )

    # Further label propagation on connected vertices of unlabelled long contigs
    (
        bins,
        bin_of_contig,
        bin_markers,
        binned_contigs_with_markers,
    ) = label_prop_utils.final_label_prop(
        bin_of_contig=bin_of_contig,
        bins=bins,
        contig_markers=contig_markers,
        bin_markers=bin_markers,
        binned_contigs_with_markers=binned_contigs_with_markers,
        smg_bin_counts=smg_bin_counts,
        contig_lengths=contig_lengths,
        min_length=min_length,
        assembly_graph=assembly_graph,
        normalized_tetramer_profiles=normalized_tetramer_profiles,
        coverages=coverages,
        depth=depth,
        weight=MAX_WEIGHT,
    )

    logger.debug(f"Total number of binned contigs: {len(bin_of_contig)}")

    # Get elapsed time
    # -----------------------------------

    # Determine elapsed time
    elapsed_time = time.time() - start_time

    # Print elapsed time for the process
    logger.info(f"Elapsed time: {elapsed_time} seconds")

    # Get bin sizes
    # -----------------------------------

    bin_size = {}

    for b in bins:
        bin_size[b] = 0
        for contig in bins[b]:
            bin_size[b] += contig_lengths[contig]

    # Merge bins
    # -----------------------------------

    # Create graph
    bins_graph = Graph()

    # Add vertices
    bins_graph.add_vertices(len(bins))

    # Name vertices with contig identifiers
    for i in range(len(bins)):
        bins_graph.vs[i]["id"] = i
        bins_graph.vs[i]["label"] = "bin " + str(i + 1)

    bins_to_rem = []

    for b in bins:
        possible_bins = []

        no_possible_bins = True

        logger.debug(
            f"Bin {b}: # contigs: {len(bins[b])}, bin size: {bin_size[b]}bp, # markers: {len(bin_markers[b])}"
        )

        min_pb = -1
        min_pb_weight = MAX_WEIGHT

        for pb in bin_markers:
            common_mgs = list(set(bin_markers[pb]).intersection(set(bin_markers[b])))

            if len(common_mgs) == 0:
                tetramer_dist = matching_utils.get_tetramer_distance(
                    bin_seed_tetramer_profiles[b], bin_seed_tetramer_profiles[pb]
                )
                prob_comp = matching_utils.get_comp_probability(tetramer_dist)
                prob_cov = matching_utils.get_cov_probability(
                    bin_seed_coverage_profiles[pb], bin_seed_coverage_profiles[b]
                )
                prob_product = prob_comp * prob_cov
                log_prob = 0

                if prob_product > 0.0:
                    log_prob = -(math.log(prob_comp, 10) + math.log(prob_cov, 10))
                else:
                    log_prob = MAX_WEIGHT

                if log_prob <= w_intra:
                    prob_cov1 = matching_utils.get_cov_probability(
                        bin_seed_coverage_profiles[pb], bin_seed_coverage_profiles[b]
                    )
                    prob_product1 = prob_comp * prob_cov1
                    log_prob1 = 0

                    if prob_product1 > 0.0:
                        log_prob1 = -(math.log(prob_comp, 10) + math.log(prob_cov1, 10))
                    else:
                        log_prob1 = MAX_WEIGHT

                    if log_prob1 <= w_intra:
                        possible_bins.append(pb)

                        if log_prob < min_pb_weight:
                            min_pb_weight = log_prob
                            min_pb = pb

        if min_pb != -1:
            bins_graph.add_edge(b, min_pb)
            no_possible_bins = False

        if no_possible_bins and len(bin_markers[b]) < n_mg * bin_mg_threshold:
            bins_to_rem.append(b)

    bin_cliques = bins_graph.maximal_cliques()

    # Get bin clique sizes
    # -----------------------------------

    bin_clique_size = {}

    for bin_clique in bin_cliques:
        bin_name = "_".join(str(x) for x in list(bin_clique))

        bin_clique_size[bin_name] = 0

        for b in bin_clique:
            bin_clique_size[bin_name] += bin_size[b]

    # Get final list of bins and write result to output file
    # ----------------------------------------------------------

    # Get output path
    output_bins_path = f"{output_path}/{prefix}bins"
    lq_output_bins_path = f"{output_path}/{prefix}low_quality_bins"

    # Create output directory for bin files
    if not os.path.isdir(output_bins_path):
        subprocess.run(f"mkdir -p {output_bins_path}", shell=True)
    if not os.path.isdir(lq_output_bins_path):
        subprocess.run(f"mkdir -p {lq_output_bins_path}", shell=True)

    final_bins = {}
    lowq_bins = {}

    final_bin_count = 0

    with open(f"{output_path}/{prefix}contig_to_bin.tsv", mode="w") as out_file:
        output_writer = csv.writer(
            out_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        for bin_clique in bin_cliques:
            bin_name = "_".join(str(x) for x in list(bin_clique))

            can_write = True

            if len(bin_clique) == 1 and bin_clique[0] in bins_to_rem:
                can_write = False

            if can_write and bin_clique_size[bin_name] >= min_bin_size:
                final_bin_count += 1

                for b in bin_clique:
                    for contig in bins[b]:
                        final_bins[contig] = bin_name

                        if assembler == "megahit":
                            output_writer.writerow(
                                [
                                    contig_descriptions[
                                        graph_to_contig_map[contig_names[contig]]
                                    ],
                                    "bin_" + bin_name,
                                ]
                            )
                        else:
                            output_writer.writerow(
                                [contig_names[contig], "bin_" + bin_name]
                            )

            else:
                for b in bin_clique:
                    for contig in bins[b]:
                        lowq_bins[contig] = bin_name

    logger.info("Writing the Final Binning result to file")

    bin_files = {}

    for bin_name in set(final_bins.values()):
        bin_files[bin_name] = open(
            f"{output_bins_path}/{prefix}bin_{bin_name}.fasta", "w+"
        )

    for bin_name in set(lowq_bins.values()):
        bin_files[bin_name] = open(
            f"{lq_output_bins_path}/{prefix}bin_{bin_name}_seqs.fasta", "w+"
        )

    for n, record in tqdm(
        enumerate(SeqIO.parse(contigs_file, "fasta")),
        desc="Splitting contigs into bins",
    ):
        if assembler == "megahit":
            contig_num = contig_names_rev[graph_to_contig_map_rev[record.id]]
        else:
            contig_num = contig_names_rev[record.id]

        if contig_num in final_bins:
            bin_files[final_bins[contig_num]].write(
                f">{str(record.id)}\n{str(record.seq)}\n"
            )

        elif contig_num in lowq_bins:
            bin_files[lowq_bins[contig_num]].write(
                f">{str(record.id)}\n{str(record.seq)}\n"
            )

    # Close output files
    for c in set(final_bins.values()):
        bin_files[c].close()

    for c in set(lowq_bins.values()):
        bin_files[c].close()

    logger.info(f"Producing {final_bin_count} bins...")
    logger.info(f"Final binning results can be found in {output_bins_path}")


    # Exit program
    # -----------------------------------

    logger.info("Thank you for using MetaCoAG!")

    logger.removeHandler(fileHandler)
    logger.removeHandler(consoleHeader)


def main(args):
    run(args)


if __name__ == "__main__":
    main()