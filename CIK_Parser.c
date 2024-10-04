#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//Helpful Resource: https://www.geeksforgeeks.org/how-to-read-from-a-file-in-c/

int main() {
    FILE * iptr;
    FILE * optr;

    iptr = fopen("CIK-File-6-input.txt", "r");
    optr = fopen("output2.txt", "w");
    char str[50];
    char subA[50];
    char subB[50];

    char *ptr;
    int index;

    if(NULL == iptr) {
        printf("file can't be opened \n");
    }


    fprintf(optr, "[\n");

    while(fgets(str, 50, iptr) != NULL) {
        for(int i = 0; i < strlen(str); i++) {
            if(str[i] == ':') {
                index = i;
                break;
            }
        }
        //strncpy(subA, str, index);
        //fprintf(optr, "\t\"%s\",\n", subA);
        strncpy(subA, str+(index+1), 8);
        if(strlen(subA) != 0) {
            fprintf(optr, "\t\"%s\",\n", subA);
        }
        

    }

    fprintf(optr, "]");

    fclose(iptr);
    fclose(optr);
    return 0;
}