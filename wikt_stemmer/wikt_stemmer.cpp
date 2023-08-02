#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
using namespace std;


string getStem(string term, unordered_map<string,string> lookupTable){
    auto search = lookupTable.find(term);
    if(search == lookupTable.end()){
        return term;
    }
    return search->second;
}

unordered_map<string,string> getLookupTable(string filename){
    unordered_map<string,string> lookupTable;
    string wordToStemFilePath = filename;
    fstream wordToStemFile(wordToStemFilePath, fstream::in);
    if(!wordToStemFile.is_open()){
        fprintf(stderr, "Error opening file!\nNo stemming will be applied.\n");
    }else{
        string line, word, stem;
        while(getline(wordToStemFile, line)){
            string delim = " -> ";
            vector<string> lineSegments;
            word = line.substr(0, line.find(delim));
            stem = line.substr(line.find(delim) + delim.length(), line.length() - delim.length() - word.length());
            lookupTable[word] = stem;
        }
    }
    return lookupTable;
}

int main(){
    unordered_map<string,string> lookupTable = getLookupTable("wordToStem.txt");
    string term;
    while(getline(cin,term)){
    cout << term + " -> " + getStem(term, lookupTable) << endl;
    }
}