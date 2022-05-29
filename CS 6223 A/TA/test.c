#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <math.h>

unsigned int xorbuf(unsigned int *buffer, int size) {
    unsigned int result = 0;
	int i = 0;
    for (i = 0; i < size; i++) {
        result ^= buffer[i];
    }
    return result;
}

int main(int argc, char* argv[]){
	
	return 0;
}

/*
int main(int argc, char* argv[]){
	int block_count = 1;
	unsigned int buffer_size = 1024;
	unsigned int result = 0;
	int fd = open(argv[1], 0), n;
	unsigned int buffer[buffer_size];
	while((n = read(fd, buffer, sizeof(unsigned int))) > 0){
  result ^= xorbuf(buffer, 8);
		block_count++;
	}
	close(fd);
	printf("XOR result is %08x\n", result);
	return 0;
}

*/