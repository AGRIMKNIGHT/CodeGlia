#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[100];

    // --- VULNERABILITY: Buffer Overflow ---
    // The strcpy function does not check the size of the input.
    // If 'input' is larger than 100 bytes, it will overwrite
    // memory, which can lead to a crash or code execution.
    strcpy(buffer, input);
    
    printf("Input was: %s\n", buffer);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
    } else {
        printf("Usage: ./vulnerable <input>\n");
    }
    return 0;
}