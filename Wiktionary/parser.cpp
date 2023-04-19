#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <filesystem>
using namespace std; namespace fs = filesystem;

struct Block{
    int seekBytes;
    int totalBytes;
    vector<int> articleIDs;
    vector<string> articleTitles;
};

Block createBlock(){
    Block block;
    block.seekBytes = 0;
    block.totalBytes = 0;
    return block;
}

vector<Block> getArticleList(set<string> dict, string indexFilePath, string dumpFilePath){
    vector<Block> blockList;
    string line;
    fstream indexFile(indexFilePath, fstream::in);
    if(!indexFile.is_open()){
        fprintf(stderr, "Error opening article index!\n");
        return blockList;
    }
    int currSeekBytes = 0;
    Block currBlock = createBlock();
    while(getline(indexFile, line)){
        string delim = ":";
        string token;
        vector<string> lineSegments; // seekBytes, articleID, articleTitle
        size_t next = 0;
        size_t last = 0;
        while((next = line.find(delim, last)) != string::npos){
            token = line.substr(last, next-last);
            last = next + 1;
            lineSegments.push_back(token);
        }
        lineSegments.push_back(line.substr(last));
        int seekBytes = stoi(lineSegments.at(0),nullptr,10);
        int articleID = stoi(lineSegments.at(1),nullptr,10);
        string articleTitle = lineSegments.at(2);
        //check if we are on a new block
        if(currSeekBytes < seekBytes){ //we are on a new block
            if(currBlock.seekBytes != 0){ //there was a previous block
                currBlock.totalBytes = seekBytes - currBlock.seekBytes;
                blockList.push_back(currBlock);
                currBlock = createBlock();
            }
            currBlock.seekBytes = seekBytes;
            currSeekBytes = seekBytes;
        }
        //add article if applicable
        if(dict.count(articleTitle) != 0){ //articleTitle is in the list
            currBlock.articleIDs.push_back(articleID);
            currBlock.articleTitles.push_back(articleTitle);
        }
    }
    //update final block
    currBlock.totalBytes = fs::file_size(dumpFilePath) - currSeekBytes;
    blockList.push_back(currBlock);
    return blockList;
}

void printArticleList(vector<Block>  articleList){
    for(int block = 0; block < articleList.size(); block++){
        printf("Block %i: seekBytes = %i, totalBytes = %i, articleList:\n", block, articleList.at(block).seekBytes, articleList.at(block).totalBytes);
        // for(int article = 0; article < articleList.at(block).articleIDs.size(); article++){
        //     printf("%s\n", articleList.at(block).articleTitles.at(article).c_str());
        // }
    }
}

// void extractArticles(vector<Block> articleList, string outputFilePath, string dumpFilePath){

// }

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

    //set up Wiktionary dump files
    string indexFilePath = "enwiktionary-20230401-pages-articles-multistream-index.txt";
    string dumpFilePath = "enwiktionary-20230401-pages-articles-multistream.xml.bz2";

    //parse index for info on relevant articles
    vector<Block> articleList = getArticleList(dict, indexFilePath, dumpFilePath);

    printArticleList(articleList);


    return EXIT_SUCCESS;
}