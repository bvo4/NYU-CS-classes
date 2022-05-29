#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

char buffer [4096];

void tail(int fd, char* file, int line)
{
	int n = 0;
	int lines = 0;
	int counter = 1;
	int i = 0;
	
	//Create a temporary file to hold the input.
	int temp  = open("temp", O_CREATE | O_RDWR);
	
	/*******READ FILE*********/
	
	//Read out the file
	while ((n=read(fd, buffer, sizeof(buffer))) > 0)
	{
		//Write into temporary file
		write(temp, buffer, n);
		
		//Check for newlines
		while(i < n)
		{
			if(buffer[i] == '\n')
				lines++;
			
			i++;
		}
	}
	
	temp = open("temp", 0);
	i = 0;
	/*******PRINT FILE*********/

	while((n = read(pointer, buffer, sizeof(buffer))) > 0)
	{
		//Take the file stream and read out for every \n
		while(i <= n)
		{
			if(counter > print)
			{
				printf(1, "GREATER\n");
				printf(1, "%c", buffer[i]);
			}
			//Newline
			if(buffer[i]=='\n')
				counter++;

			i++;
		}
	}
		// delete the file before closing the function
		unlink("temp");
		close(temp);
}

int main(int argc, char *argv[])
{
	int sub = 10;
	int fd = 0;
	int i;
	int k = 0;

	//Default case, print out the last 10 lines
	if(argc < 1)
	{
		tail(0, sub);
		exit();
	}

	for(i = 1; i< argc; i++)
	{
		//Assign the value to a
		a = *argv[i];
		
		if(a == '-')
		{
			argv[i]++;
			x = atoi(argv[i]++);
		}
		else
		{
			if((fd = open(argv[i], 0)) < 0)
			{
				printf(1, "Tail:  Cannot open %s\n", argv[i]);
				exit();
			}
		}
	}
	tail(fd, file, x);
	close(fd);
	exit();
}