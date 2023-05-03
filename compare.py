import sys
import os
import nltk.metrics.distance as distance

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
            stem_clusters[stem] = list()
        stem_clusters[stem].append(word)
    #Get list of the clusters
    for stem in stem_clusters:
        cluster = list()
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
            cluster_list.append(cluster)
    return cluster_list

def print_size_distribution(clusters, filename):
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

def print_clusters(clusters, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for cluster in clusters:
            for word in cluster:
                f.write(word + " ")
            f.write("\n")

def measure_word_accuracy(wikt_pairs, stem_pairs):
    scores = list()
    for i in range (0, len(stem_pairs)):
        #may want to add more of a penalty to substitions??
        scores.append(distance.edit_distance(wikt_pairs[i][1], stem_pairs[i][1]))
    #return an average
    


def measure_cluster_accuracy(wikt_clusters, stem_clusters):
    #determine the accuracy of the clusters....
    return 0

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
    print_size_distribution(stem_clusters, "stem_distribution")
    print_size_distribution(wikt_clusters, "wikt_distribution")

    #Remove clusters with only one element
    stem_clusters[:] = [x for x in stem_clusters if len(x) > 1]
    wikt_clusters[:] = [x for x in wikt_clusters if len(x) > 1]
    print(f"Clusters for the stemmer with length > 1: {len(stem_clusters)}", file=sys.stderr)
    print(f"Clusters for the wiktionary with length > 1: {len(wikt_clusters)}", file=sys.stderr)

    #Included for testing
    print_clusters(wikt_clusters, "wikt_clusters.txt")
    print_clusters(stem_clusters, "stem_clusters.txt")



if __name__ == "__main__":
    main()