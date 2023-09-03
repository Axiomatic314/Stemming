import sys
from nltk.metrics import edit_distance, jaccard_distance, f_measure, precision, recall
import numpy as np
from tqdm import tqdm
import os.path

def create_clusters(filename):
    # cluster_list = list()
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
    # #Get list of the clusters
    # for stem in stem_clusters:
    #     cluster = stem_clusters[stem]
    #     cluster_list.append(cluster)
    return stem_clusters, stem_pairs

def trim_clusters(wikt_clusters, stem_clusters):
    clusters = set(wikt_clusters.keys())
    for cluster in clusters:
        if len(wikt_clusters[cluster]) == 1:
            wikt_clusters.pop(cluster)
    clusters = set(stem_clusters.keys())
    for cluster in clusters:
        if len(stem_clusters[cluster]) == 1:
            stem_clusters.pop(cluster)
    return wikt_clusters, stem_clusters

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
    cluster_sizes = list()
    for cluster in clusters.values():
        size = len(cluster)
        cluster_sizes.append(size)
    cluster_sizes = np.array(cluster_sizes, dtype="int")
    np.savetxt(filename, cluster_sizes)

def write_clusters(clusters, filename, includeStem):
    with open(filename, "w", encoding="utf-8") as f:
        for stem in clusters.keys():
            if includeStem: 
                f.write(stem + ": ")
            for word in clusters[stem]:
                f.write(word + " ")
            f.write("\n")

def write_word_distances(wikt_pairs, stem_pairs, filename):
    distances = list()
    for i in tqdm(range (0, len(stem_pairs))):
        distance = edit_distance(wikt_pairs[i][1], stem_pairs[i][1], substitution_cost=1)
        distances.append(distance)
    print("Average distance between stems from wiktionary and the stemming algorithm:", file=sys.stderr)
    print(f"Mean: {np.mean(distances)}\nMedian: {np.median(distances)}", file = sys.stderr)
    distances = np.array(distances, dtype="int")
    np.savetxt(filename, distances)

def measure_cluster_accuracy(wikt_clusters, stem_clusters):
    ref_clusters = set()
    test_clusters = set()
    for cluster in wikt_clusters.values():
        temp = " ".join(cluster)
        ref_clusters.add(temp)
    for cluster in stem_clusters.values():
        temp = " ".join(cluster)
        test_clusters.add(temp)
    print(f"Jaccard distance: {jaccard_distance(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"F measure: {f_measure(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"Precision: {precision(ref_clusters, test_clusters)}", file=sys.stderr)
    print(f"Recall: {recall(ref_clusters, test_clusters)}", file=sys.stderr)

def write_cluster_fmeasures(wikt_clusters, stem_clusters, filename):
    cluster_fmeasures = list()
    for ref_cluster in tqdm(stem_clusters.values()):
        # best_cluster = list()
        best_fmeasure = 0.00
        for cluster in wikt_clusters.values():
            fmeasure = f_measure(ref_cluster, cluster)
            if fmeasure > best_fmeasure:
                best_fmeasure = fmeasure
                # best_cluster = cluster
        cluster_fmeasures.append(best_fmeasure)
        # if best_fmeasure == 0.00:
        #     print(f"Best wiktionary match: {best_cluster} for the stemmer cluster {ref_cluster}", file=sys.stderr)
    cluster_fmeasures = np.array(cluster_fmeasures)
    print("Average F measure between the two sets of clusters:", file=sys.stderr)
    print(f"Mean: {np.mean(cluster_fmeasures)}\nMedian: {np.median(cluster_fmeasures)}", file=sys.stderr)
    np.savetxt(filename, cluster_fmeasures) 

def write_cluster_distances(wikt_clusters, stem_clusters, filename):
    temp_clusters = list(stem_clusters.values())
    cluster_distances = list()
    for ref_cluster in tqdm(wikt_clusters.values()):
        best_cluster = list()
        best_distance = 1.00
        for cluster in temp_clusters:
            distance = jaccard_distance(ref_cluster, cluster)
            if distance < best_distance:
                best_distance = distance
                best_cluster = cluster
        if best_distance < 1.00:
            temp_clusters.remove(best_cluster)
        cluster_distances.append(best_distance)
    cluster_distances = np.array(cluster_distances)
    print(f"Remaining clusters: {len(temp_clusters)}", file=sys.stderr)
    print("Average jaccard distance between the two sets of clusters:", file=sys.stderr)
    print(f"Mean: {np.mean(cluster_distances)}\nMedian: {np.median(cluster_distances)}", file=sys.stderr)
    np.savetxt(filename, cluster_distances) 

def main():
    wikt_file = "Wiktionary/wordToStem.txt"
    if not os.path.exists(wikt_file):
        print(f"{wikt_file} is missing!", file=sys.stderr)
        return
    if len(sys.argv) != 3:
        print("Usage: python compare.py <directory> <stemmer>")
        return
    stemmer_dir = sys.argv[1]
    stemmer = sys.argv[2]
    stemmer_file = stemmer + "Stems"
    stemmer_file = os.path.join(stemmer_dir, stemmer_file)
    if not os.path.exists(stemmer_file):
        print(f"{stemmer_file} is missing!")
        return
    data_dir = os.path.join("Data", "wikt")

    # Get the clusters from word->stem files
    wikt_clusters, wikt_pairs = create_clusters(wikt_file)
    stem_clusters, stem_pairs = create_clusters(stemmer_file)
    print(f"Total clusters for the stemmer: {len(stem_clusters)}", file=sys.stderr)
    print(f"Total clusters for the wiktionary: {len(wikt_clusters)}", file=sys.stderr)

    # Get the distribution of cluster sizes 
    write_size_distribution(stem_clusters, os.path.join(data_dir, stemmer + "_distribution.csv"))
    write_size_distribution(wikt_clusters, os.path.join(data_dir, "wikt" + "_distribution.csv"))

    # Get the maximum fmeasure for each stemmer cluster
    write_cluster_fmeasures(wikt_clusters, stem_clusters, os.path.join(data_dir, stemmer + "_cluster_fmeasures.csv"))

    # #Removing single clusters
    # wikt_clusters, stem_clusters = trim_clusters(wikt_clusters, stem_clusters)
    # print(f"Clusters for the stemmer with length > 1: {len(stem_clusters)}", file=sys.stderr)
    # print(f"Clusters for the wiktionary with length > 1: {len(wikt_clusters)}", file=sys.stderr)
    # write_cluster_fmeasures(wikt_clusters, stem_clusters, os.path.join(data_dir, stemmer + "_after_cluster_fmeasures.csv"))

    # Get the edit distances between the wiktionary stems and those from the stemming algorithm
    write_word_distances(wikt_pairs, stem_pairs, os.path.join(data_dir, stemmer + "_word_distances.csv"))

    #Testing comparing both clusterings as sets themselves - and using jaccard distance
    # print("Before removing singles:", file=sys.stderr)
    # measure_cluster_accuracy(wikt_clusters, stem_clusters)
    #Removing single clusters
    # wikt_clusters, stem_clusters = trim_clusters(wikt_clusters, stem_clusters)
    # print(f"Clusters for the stemmer with length > 1: {len(stem_clusters)}", file=sys.stderr)
    # print(f"Clusters for the wiktionary with length > 1: {len(wikt_clusters)}", file=sys.stderr)
    # print("After removing singles:", file=sys.stderr)
    # measure_cluster_accuracy(wikt_clusters, stem_clusters)
    # write_cluster_distances(wikt_clusters, stem_clusters, "Data/cluster_distances.csv")


if __name__ == "__main__":
    main()