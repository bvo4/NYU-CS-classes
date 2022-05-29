#include "types.h"
#include "stat.h"
#include "user.h"

int Gettime = 2;

int ReturnXor(int mod)
{
	/* Xorshift PRNG Generator */
	Gettime ^= Gettime << 4;
	Gettime ^= Gettime >> 9;
	Gettime ^= Gettime << 8;

	if(Gettime < 0)
		Gettime *=-1;

	return Gettime%mod;

}

int main(int argc, char *argv[])
{
	int mod = 100;

	if(argc >= 2)
	{
		mod = atoi(argv[1]);
	}
	if(argc >= 3)
	{
		Gettime = atoi(argv[2]);
	}
	else
	{
		/* Use the system time as the seed */
		Gettime = uptime();
	}

	//generate a bmp picture
	int i = 0;
	for(i = 0; i < 10; i++)
	{
		printf(1, "Number is %d\n", ReturnXor(mod));
	}
	exit();
}