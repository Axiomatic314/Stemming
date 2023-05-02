import sys

def create_cluster_list(filename):
    #todo: change this to use the word -> stem file, so can get rid of cluster.py entirely?
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

def main():
    stemmer_file = "Stemmers/Snowball/snowballClusters.txt"
    wikt_file = "Wiktionary/reducedGroupings.txt"

    #Get the clusters
    stem_clusters = create_cluster_list(stemmer_file)
    wikt_clusters = create_cluster_list(wikt_file)
    print(f"Total clusters for the stemmer: {len(stem_clusters)}", file=sys.stderr)
    print(f"Total clusters for the wiktionary: {len(wikt_clusters)}", file=sys.stderr)

    print_size_distribution(stem_clusters, "stem_distribution")
    print_size_distribution(wikt_clusters, "wikt_distribution")

    #Remove clusters with only one element
    stem_clusters[:] = [x for x in stem_clusters if len(x) > 1]
    wikt_clusters[:] = [x for x in wikt_clusters if len(x) > 1]
    print(f"Clusters for the stemmer with length > 1: {len(stem_clusters)}", file=sys.stderr)
    print(f"Clusters for the wiktionary with length > 1: {len(wikt_clusters)}", file=sys.stderr)

    print_clusters(wikt_clusters, "wikt_clusters.txt")
    print_clusters(stem_clusters, "stem_clusters.txt")

if __name__ == "__main__":
    main()