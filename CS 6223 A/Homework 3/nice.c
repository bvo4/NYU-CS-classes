#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

int main(int argc, char *argv[])
{

	//read from standard input if no arguments are passed
	if(argc < 1){
		printf(1, "Not enough values\n");
		exit();
	}
	//nice 19 ./test.sh
	int pid;
	int priority;

	pid = atoi(argv[1]);
	priority = atoi(argv[2]);

	printf(1, "PID is %d\n", pid);
	printf(1, "Priority is %d\n", priority);
	ChangeNice(pid, priority);
	exit();
}