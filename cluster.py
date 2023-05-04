from nltk.metrics import jaccard_distance
from sklearn.metrics.cluster import adjusted_mutual_info_score, adjusted_rand_score

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
    return stem_clusters, stem_pairs

def measure_cluster_accuracy(wikt_pairs, wikt_clusters, stem_pairs, stem_clusters):
    wikt_labels = list()
    stem_labels = list()
    labels = dict()
    temp_clusters = stem_clusters.copy()
    #find the appropriate labels for the clusters
    curr_label = 0
    for ref_cluster in wikt_clusters.keys():
        curr_label+=1
        best_cluster = ""
        best_distance = 1.00
        count = 0
        for cluster in temp_clusters.keys():
            count+=1
            print(f"Processing {count}/{len(temp_clusters.keys())}")
            distance = jaccard_distance(wikt_clusters[ref_cluster], stem_clusters[cluster])
            if distance < best_distance:
                best_distance = distance
                best_cluster = cluster
        if best_distance < 1.00:
            temp_clusters.pop(best_cluster)
            labels[best_cluster] = curr_label
        labels[ref_cluster] = curr_label
    #make lists of the stems as labels
    for word, stem in wikt_pairs:
        wikt_labels.append(labels[stem])
    for word, stem in stem_pairs:
        if stem in labels.keys():
            stem_labels.append(labels[stem])
        else:
            stem_labels.append(0)
    #find the ami
    print(f"AMI: {adjusted_mutual_info_score(wikt_labels, stem_labels)}")
    print(f"ARI: {adjusted_rand_score(wikt_labels, stem_labels)}")




def main():
    #todo: check if the necessary files are actually there
    wikt_file = "Wiktionary/replacements.txt"
    #Todo: change the stemmer file to be given via command line?
    stemmer_file = "Stemmers/Snowball/snowballOutput.txt"

    # Get the clusters from word->stem files
    wikt_clusters, wikt_pairs = create_clusters(wikt_file)
    stem_clusters, stem_pairs = create_clusters(stemmer_file)

    measure_cluster_accuracy(wikt_pairs, wikt_clusters, stem_pairs, stem_clusters)

if __name__ == "__main__":
    main()