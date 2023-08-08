#include <iostream>
#include <zlib.h>


void readGZ(char *filename){
    gzFile inputFileGZ = gzopen(filename, "rb");
    if(inputFileGZ == NULL){
        printf("Error! Could not open %s.\n", filename);
        exit(EXIT_FAILURE);
    }
    int bufSize = 8192;
    char buffer[bufSize];
    int bytesRead = 0;
    while(true){
        bytesRead = gzread(inputFileGZ, buffer, bufSize);
        if (bytesRead > 0){
            //deal with data in the buffer
            printf("%s\n", buffer);
        }else{
            break;
        }
    }
    gzclose(inputFileGZ);
}

int main(){
    char filename[] = "test.gz";
    //read and ungzip file
    readGZ(filename);
    //extract nth warc and write to new file
   

}

