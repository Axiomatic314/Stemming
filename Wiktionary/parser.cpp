#include <iostream>
#include <vector>
#include <string>
using namespace std;

/**
 * Creates a list of relevant articles from the Wiktionary.
*/
vector<string> relevantArticles(vector<string> validWords, vector<string> articleIndex){
    vector<string> results;
    string currentWord = validWords.at(0);
    int currentWordIndex = 0;
    
    for(string entry: articleIndex){
        string currentEntry;
        //find the article title - note that some languages are right to left, so may need to revist this
        size_t found = entry.rfind(":");
        if(found != string::npos){
            currentEntry = entry.substr(found+1);
        }
        int compareResults = currentEntry.compare(currentWord);
        if(compareResults == 0){ //the entry is in our list of valid words
            results.push_back(entry);
            currentWordIndex++;
        }else if(compareResults > 0){ //the entry is greater than our current valid word
            while(compareResults >= 0 && currentWordIndex+1 <= validWords.size()){
                currentWord = validWords.at(currentWordIndex++);
                compareResults = currentEntry.compare(currentWord);
                if(compareResults == 0){ //the entry is in our list of valid words
                    results.push_back(entry);
                    currentWordIndex++;
                    break;
                }
            }
        }
    }

}