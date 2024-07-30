import sys
import os.path

def getWords(wordListFile):
    words = list()
    with open(wordListFile, "r") as f:
        for line in f:
            words.append(line[:-1])
    return words

def getStems(numWords, stemListFile):
    lines = list()
    with open(stemListFile, "r") as f:
        for line in f:
            lines.append(line)
    if lines[0].startswith("This"): lines.pop(0)
    stems = [""] * numWords
    stem = ""
    for line in lines:
        if line[0][0].isalpha():
            stem = line[:-2]
        elif line[0][0] == "<":
            docid = int(line[1:line.find(",")])
            stems[docid] = stem
        else:
            return stems
        
def printResults(words, stems, outputFile):
    with open(outputFile, "w") as f:
        for i in range(0,len(words)):
            f.write(words[i] + " -> " + stems[i] + "\n")
    return

def main():

    if len(sys.argv) != 2:
        print("Usage: python wordToStem.py <stemmer>")
        return
    
    wordListFile = f"Data/clueweb/stems/{sys.argv[1]}Doclist.aspt"
    stemListFile = f"Data/clueweb/stems/{sys.argv[1]}Dictionary"

    outputFile = f"Data/clueweb/stems/{sys.argv[1]}Stems"

    if not os.path.exists(wordListFile) and not os.path.exists(stemListFile):
        print("Please ensure the files are there!")

    print("Processing doclist...")
    words = getWords(wordListFile)
    print("Processing dictionary...")
    stems = getStems(len(words), stemListFile)
    print("Printing results to file...")
    printResults(words, stems, outputFile)
    print("Complete!")

if __name__ == "__main__":
    main()