#!/usr/bin/env python3

import logging
import os
import pathlib

__author__ = "Vijini Mallawaarachchi and Yu Lin"
__copyright__ = "Copyright 2020, MetaCoAG Project"
__license__ = "GPL-3.0"
__version__ = "1.2.2"
__maintainer__ = "Vijini Mallawaarachchi"
__email__ = "vijini.mallawaarachchi@anu.edu.au"
__status__ = "Stable Release"


# create logger
logger = logging.getLogger(f"MetaCoaAG {__version__}")


# Modified from SolidBin
def scan_for_marker_genes(contigs_file, nthreads, markerURL, no_cut_tc, hard=0):

    fragScanURL = "run_FragGeneScan.pl"
    hmmExeURL = "hmmsearch"

    if markerURL == "auxiliary/marker.hmm":
        software_path = pathlib.Path(__file__).parent.absolute()
        markerURL = os.path.join(software_path, "auxiliary", "marker.hmm")

    logger.info("Using marker file: " + markerURL)

    fragResultURL = f"{contigs_file}.frag.faa"
    hmmResultURL = f"{contigs_file}.hmmout"
    if not (os.path.exists(fragResultURL)):
        fragCmd = (
            fragScanURL
            + " -genome="
            + contigs_file
            + " -out="
            + contigs_file
            + ".frag -complete=0 -train=complete -thread="
            + str(nthreads)
            + " 1>"
            + contigs_file
            + ".frag.out 2>"
            + contigs_file
            + ".frag.err"
        )
        logger.debug(f"exec cmd: {fragCmd}")
        os.system(fragCmd)

    if os.path.exists(fragResultURL):
        use_cut_tc = ""
        if not no_cut_tc:
            use_cut_tc = "--cut_tc"

        if not (os.path.exists(hmmResultURL)):
            hmmCmd = (
                hmmExeURL
                + " --domtblout "
                + hmmResultURL
                + " "
                + use_cut_tc
                + " --cpu "
                + str(nthreads)
                + " "
                + markerURL
                + " "
                + fragResultURL
                + " 1>"
                + hmmResultURL
                + ".out 2>"
                + hmmResultURL
                + ".err"
            )
            logger.debug(f"exec cmd: {hmmCmd}")
            os.system(hmmCmd)

        else:
            logger.debug(f"HMMER search failed! Path: {hmmResultURL} does not exist.")
    else:
        logger.debug(f"FragGeneScan failed! Path: {fragResultURL} does not exist.")


# Get contigs containing marker genes
def get_all_contigs_with_marker_genes(
    contigs_file, contig_names_rev, mg_length_threshold
):
    contig_markers = {}

    with open(f"{contigs_file}.hmmout", "r") as myfile:
        for line in myfile.readlines():
            if not line.startswith("#"):
                strings = line.strip().split()

                contig = strings[0]

                # Marker gene name
                marker_gene = strings[3]

                # Marker gene length
                marker_gene_length = int(strings[5])

                # Mapped marker gene length
                mapped_marker_length = int(strings[16]) - int(strings[15])

                name_strings = contig.split("_")
                name_strings = name_strings[: len(name_strings) - 3]

                # Contig name
                contig_name = "_".join(name_strings)

                contig_num = contig_names_rev[contig_name]

                if mapped_marker_length > marker_gene_length * mg_length_threshold:
                    # Get marker genes in each contig
                    if contig_num not in contig_markers:
                        contig_markers[contig_num] = [marker_gene]
                    else:
                        if marker_gene not in contig_markers[contig_num]:
                            contig_markers[contig_num].append(marker_gene)

    return contig_markers


# Get contigs containing marker genes
def get_contigs_with_marker_genes(
    contigs_file, contig_names_rev, mg_length_threshold, contig_lengths, min_length
):
    marker_contigs = {}
    marker_contig_counts = {}
    contig_markers = {}

    with open(f"{contigs_file}.hmmout", "r") as myfile:
        for line in myfile.readlines():
            if not line.startswith("#"):
                strings = line.strip().split()

                contig = strings[0]

                # Marker gene name
                marker_gene = strings[3]

                # Marker gene length
                marker_gene_length = int(strings[5])

                # Mapped marker gene length
                mapped_marker_length = int(strings[16]) - int(strings[15])

                name_strings = contig.split("_")
                name_strings = name_strings[: len(name_strings) - 3]

                # Contig name
                contig_name = "_".join(name_strings)

                contig_num = contig_names_rev[contig_name]
                contig_length = contig_lengths[contig_num]

                if (
                    contig_length >= min_length
                    and mapped_marker_length > marker_gene_length * mg_length_threshold
                ):
                    marker_repeated_in_contig = False

                    # Get marker genes in each contig
                    if contig_num not in contig_markers:
                        contig_markers[contig_num] = [marker_gene]
                    else:
                        if marker_gene not in contig_markers[contig_num]:
                            contig_markers[contig_num].append(marker_gene)

                    # Get contigs containing each marker gene
                    if marker_gene not in marker_contigs:
                        marker_contigs[marker_gene] = [contig_num]
                    else:
                        if contig_num not in marker_contigs[marker_gene]:
                            marker_contigs[marker_gene].append(contig_num)
                        else:
                            marker_repeated_in_contig = True

                    # Get contig counts for each marker
                    if marker_gene not in marker_contig_counts:
                        marker_contig_counts[marker_gene] = 1
                    else:
                        if not marker_repeated_in_contig:
                            marker_contig_counts[marker_gene] += 1

    return marker_contigs, marker_contig_counts, contig_markers


# Get contigs containing marker genes
def get_contigs_with_marker_genes_megahit(
    contigs_file,
    contig_names_rev,
    graph_to_contig_map_rev,
    mg_length_threshold,
    contig_lengths,
    min_length,
):
    marker_contigs = {}
    marker_contig_counts = {}
    contig_markers = {}

    with open(f"{contigs_file}.hmmout", "r") as myfile:
        for line in myfile.readlines():
            if not line.startswith("#"):
                strings = line.strip().split()

                contig = strings[0]

                # Marker gene name
                marker_gene = strings[3]

                # Marker gene length
                marker_gene_length = int(strings[5])

                # Mapped marker gene length
                mapped_marker_length = int(strings[16]) - int(strings[15])

                name_strings = contig.split("_")
                name_strings = name_strings[: len(name_strings) - 3]

                # Contig name
                contig_name = "_".join(name_strings)

                contig_num = contig_names_rev[graph_to_contig_map_rev[contig_name]]
                contig_length = contig_lengths[contig_num]

                if (
                    contig_length >= min_length
                    and mapped_marker_length > marker_gene_length * mg_length_threshold
                ):
                    marker_repeated_in_contig = False

                    # Get marker genes in each contig
                    if contig_num not in contig_markers:
                        contig_markers[contig_num] = [marker_gene]
                    else:
                        if marker_gene not in contig_markers[contig_num]:
                            contig_markers[contig_num].append(marker_gene)

                    # Get contigs containing each marker gene
                    if marker_gene not in marker_contigs:
                        marker_contigs[marker_gene] = [contig_num]
                    else:
                        if contig_num not in marker_contigs[marker_gene]:
                            marker_contigs[marker_gene].append(contig_num)
                        else:
                            marker_repeated_in_contig = True

                    # Get contig counts for each marker
                    if marker_gene not in marker_contig_counts:
                        marker_contig_counts[marker_gene] = 1
                    else:
                        if not marker_repeated_in_contig:
                            marker_contig_counts[marker_gene] += 1

    return marker_contigs, marker_contig_counts, contig_markers


def count_contigs_with_marker_genes(marker_contig_counts):
    marker_frequencies = {}

    for marker in marker_contig_counts:
        if marker_contig_counts[marker] not in marker_frequencies:
            marker_frequencies[marker_contig_counts[marker]] = 1
        else:
            marker_frequencies[marker_contig_counts[marker]] += 1

    return marker_frequencies
