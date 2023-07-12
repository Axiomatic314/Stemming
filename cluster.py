import os
import sys
from tqdm import tqdm
from nltk.metrics import f_measure
import numpy as np

def create_clusters(filename):
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
    stem_clusters = dict(sorted(stem_clusters.items()))
    return stem_clusters, stem_pairs

def print_best_clusters(wikt_clusters, stem_clusters, filename):
    with open(filename, "w") as f:
        count = 0
        for ref_cluster in wikt_clusters.values():
            count+=1
            best_cluster = list()
            best_fmeasure = 0.00
            for cluster in stem_clusters.values():
                fmeasure = f_measure(ref_cluster, cluster)
                if fmeasure > best_fmeasure:
                        best_fmeasure = fmeasure
                        best_cluster = cluster
            f.write(f"wiktionary: {ref_cluster} | stemmer: {best_cluster}\n")
            if count == 32:
                return
    

def print_clusters(filename, clusters):
    with open(filename, "w") as f:
        for stem in clusters.keys():
            f.write(stem)
            for word in clusters[stem]:
                f.write(" " + word)
            f.write("\n")

def main():
    wikt_file = "Wiktionary/replacements.txt"
    if not os.path.exists(wikt_file):
        print(f"{wikt_file} is missing!", file=sys.stderr)
        return
    if len(sys.argv) not in (3,4):
        print("Usage: python cluster.py <directory> <stemmer> [y]")
        return
    stemmer_dir = sys.argv[1]
    stemmer = sys.argv[2]
    stemmer_file = stemmer + "Stems"
    stemmer_file = os.path.join(stemmer_dir, stemmer_file)
    if not os.path.exists(stemmer_file):
        print(f"{stemmer_file} is missing!")
        return
    output_file = stemmer + "Clusters"
    output_file = os.path.join(stemmer_dir, output_file)
    BEST = False
    if len(sys.argv) == 4 and sys.argv[3] == "y":
        BEST = True

    # Get the clusters from word->stem files
    stem_clusters, stem_pairs = create_clusters(stemmer_file)
    wikt_clusters, wikt_pairs = create_clusters(wikt_file)
    # Print out all the clusters and their corresponding stem
    print_clusters(output_file, stem_clusters)
    print_clusters("Wiktionary/temp.txt", wikt_clusters)
    if BEST:
        # Print out the best clusters for each wikt cluster
        output_file = stemmer + "BestClusters"
        output_file = os.path.join(stemmer_dir, output_file)
        print_best_clusters(wikt_clusters, stem_clusters, output_file)

    

if __name__ == "__main__":
    main()