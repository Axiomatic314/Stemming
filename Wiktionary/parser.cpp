#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
using namespace std;

struct block{
    int seekBytes;
    int totalBytes;
    vector<int> articleIDs;
};

vector<block> getArticleList(set<string> dict){
    vector<block> blockList;
    string line;
    string indexFilePath = "enwiktionary-20230401-pages-articles-multistream-index.txt";
    fstream indexFile(indexFilePath, fstream::in);
    if(!indexFile.is_open()){
        fprintf(stderr, "Error opening article index!\n");
        return blockList;
    }
    while(getline(indexFile, line)){
        string delim = ":";
        string token;
        vector<string> lineSegments;
        size_t next = 0;
        size_t last = 0;
        while((next = line.find(delim, last)) != string::npos){
            token = line.substr(last, next-last);
            last = next + 1;
            lineSegments.push_back(token);
        }
        //process contents of line
    }

}

int main(){

    //get a set of valid English words
    set<string> dict; 
    string word;
    string wordFilePath = "words.txt";
    fstream wordFile(wordFilePath, fstream::in);
    if(!wordFile.is_open()){
        fprintf(stderr, "Error opening word list!\n");
        exit(EXIT_FAILURE);
    }
    while(getline(wordFile, word)){
        dict.insert(word);
    }
    wordFile.close();

    //parse index for info on relevant articles
    vector<block> articleList = getArticleList(dict);


    return EXIT_SUCCESS;
}