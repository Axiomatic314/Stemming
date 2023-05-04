import sys
import os
from nltk.metrics import edit_distance, jaccard_distance, f_measure, precision, recall
import numpy as np

def create_clusters(filename):
    cluster_list = list()
    stem_clusters = dict()
    stem_pairs = list()
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            contents = line.split(sep="->")
            stem_pairs.append((contents[0].strip(), contents[1].strip()))
    #Find which words map to the same stem
    for word, stem in stem_pairs:
        if stem not in stem_clusters.keys():
            stem_clusters[stem] = set()
        stem_clusters[stem].add(word)
    #Get list of the clusters
    for stem in stem_clusters:
        cluster = stem_clusters[stem]
        cluster_list.append(cluster)
    return cluster_list, stem_pairs

def get_clusters(filename):
    cluster_list = list()
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            cluster = list()
            cluster = line.split()
            cluster.pop(0)
            cluster = set(cluster)
            cluster_list.append(cluster)
    return cluster_list

def write_size_distribution(clusters, filename):
    cluster_sizes = dict()
    for cluster in clusters:
        size = len(cluster)
        if size in cluster_sizes.keys():
            cluster_sizes[size]+=1
        else:
            cluster_sizes[size] = 1
    cluster_sizes = dict(sorted(cluster_sizes.items()))
    with open(filename, "w", encoding="utf-8") as f:
        for size in cluster_sizes:
            f.write("(" + str(size) + ", " + str(cluster_sizes[size]) + ")\n")

def write_clusters(clusters, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for cluster in clusters:
            for word in cluster:
                f.write(word + " ")
            f.write("\n")

def write_word_distances(wikt_pairs, stem_pairs, filename):
    distances = list()
    distance_distribution = dict()
    for i in range (0, len(stem_pairs)):
        distance = edit_distance(wikt_pairs[i][1], stem_pairs[i][1], substitution_cost=3)
        distances.append(distance)
        if distance not in distance_distribution.keys():
            distance_distribution[distance] = 0
        distance_distribution[distance]+=1
    distance_distribution = dict(sorted(distance_distribution.items()))
    mean = np.mean(distances)
    median = np.median(distances)
    print("Average distance between stems from wiktionary and the algorithm:", file=sys.stderr)
    print(f"Mean: {mean}\nMedian: {median}", file = sys.stderr)
    with open(filename, "w", encoding="utf-8") as f:
        for distance in distance_distribution:
            f.write("(" + str(distance) + ", " + str(distance_distribution[distance]) + ")\n")

def measure_cluster_accuracy(wikt_clusters, stem_clusters):
    ref_clusters = set()
    test_clusters = set()
    for cluster in wikt_clusters:
        temp = " ".join(cluster)
        ref_clusters.add(temp)
    for cluster in stem_clusters:
        temp = " ".join(cluster)
        test_clusters.add(temp)
    print(f"Jaccard distance: {jaccard_distance(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"F measure: {f_measure(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"Precision: {precision(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"Recall: {recall(ref_clusters, test_clusters)}", file=sys.stderr)

def write_cluster_distances(wikt_clusters, stem_clusters, filename):
    temp_clusters = stem_clusters.copy()
    cluster_distances = list()
    distance_distribution = dict()
    for ref_cluster in wikt_clusters:
        best_cluster = list()
        best_distance = 1.00
        for cluster in temp_clusters:
            distance = jaccard_distance(ref_cluster, cluster)
            # distance = f_measure(ref_cluster, cluster)
            if distance < best_distance:
                best_distance = distance
                best_cluster = cluster
        if best_distance < 1.00:
            temp_clusters.remove(best_cluster)
        cluster_distances.append(best_distance)
        if best_distance not in distance_distribution.keys():
            distance_distribution[best_distance] = 0
        distance_distribution[best_distance]+=1
    distance_distribution = dict(sorted(distance_distribution.items()))
    print(f"Remaining clusters: {len(temp_clusters)}", file=sys.stderr)
    print("Average distance between the clusterings:", file=sys.stderr)
    print(f"Mean: {np.mean(cluster_distances)}\nMedian: {np.median(cluster_distances)}", file=sys.stderr)
    with open(filename, "w", encoding="utf-8") as f:
        for distance in distance_distribution:
            f.write("(" + str(distance) + ", " + str(distance_distribution[distance]) + ")\n")   

def main():
    #todo: check if the necessary files are actually there
    wikt_file = "Wiktionary/replacements.txt"
    #Todo: change the stemmer file to be given via command line?
    stemmer_file = "Stemmers/Snowball/snowballOutput.txt"

    # Get the clusters from a preclustered file
    # wikt_file = "Wiktionary/clusters.txt"
    # wikt_clusters = get_clusters(wikt_cluster_file)

    # Get the clusters from word->stem files
    wikt_clusters, wikt_pairs = create_clusters(wikt_file)
    stem_clusters, stem_pairs = create_clusters(stemmer_file)
    print(f"Total clusters for the stemmer: {len(stem_clusters)}", file=sys.stderr)
    print(f"Total clusters for the wiktionary: {len(wikt_clusters)}", file=sys.stderr)

    # Get the distribution of cluster sizes 
    write_size_distribution(stem_clusters, "stem_distribution")
    write_size_distribution(wikt_clusters, "wikt_distribution")

    #Testing comparing both clusterings as sets themselves
    print("Before removing singles:", file=sys.stderr)
    measure_cluster_accuracy(wikt_clusters, stem_clusters)

    #Remove clusters with only one element
    stem_clusters[:] = [x for x in stem_clusters if len(x) > 1]
    wikt_clusters[:] = [x for x in wikt_clusters if len(x) > 1]
    # print(f"Clusters for the stemmer with length > 1: {len(stem_clusters)}", file=sys.stderr)
    # print(f"Clusters for the wiktionary with length > 1: {len(wikt_clusters)}", file=sys.stderr)

    #Testing
    print("After removing singles:", file=sys.stderr)
    measure_cluster_accuracy(wikt_clusters, stem_clusters)

    #Included for testing
    # write_clusters(wikt_clusters, "wikt_clusters.txt")
    # write_clusters(stem_clusters, "stem_clusters.txt")
    # write_word_distances(wikt_pairs, stem_pairs, "word_distances.txt")

    #Find some measure of accuracy between the two clusterings
    write_cluster_distances(wikt_clusters, stem_clusters, "cluster_distances.txt")

if __name__ == "__main__":
    main()