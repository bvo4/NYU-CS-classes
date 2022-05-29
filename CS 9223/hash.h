#include <iostream>
using namespace std;

/*
https://en.wikipedia.org/wiki/Jenkins_hash_function

Altered version of the Jenkin's hash function taken from Wikipedia.

This version was altered to not use the address space of a variable as the hash key.
This is to ensure that the hash function is deterministic.
*/

//Removed the use of the hash key's pointer.
//Changed to use take the 8-byte value of the entire string input as well.
uint jenkinsHash(uint8_t key, size_t length) {
  size_t i = 0;
  uint16_t hash = 0;
  while (i != length) {
    i++;
    hash += key;
    hash += hash << 10;
    hash ^= hash >> 6;
  }
  //cout << "hash: " << unsigned(hash) << endl;
  hash += hash << 3;
  hash ^= hash >> 4;
  hash += hash >> 6;

  //In order to force a fixed length, will forcibly bitshift the hash
  //Until it achieves a specific length of the 16 bit size
  while(to_string(hash).length() < 5)
  {
    //cout<< "Signal : " << to_string(hash).length() << endl;
    hash += hash >> 4;
  }
  /*
  while(to_string(hash).length() > 5)
  {
    //cout<< "Signal :" << hash << endl;
    hash ^= hash >> 1;
  }
  */
  return hash;
}

int main() {

  //The two strings have a hash collision because their lengths are the same.
  string a = "tes443w4wq4244t";
  string b = "2saddas645fasf3";
  
  const size_t length = a.length();
  const size_t length_b = b.length();
  
  uint8_t aa = length;
  uint8_t bb = length_b;
  
  //Output the end result
  cout << jenkinsHash(aa, a.length()) << endl;
  cout << jenkinsHash(bb, b.length()) << endl;

    return 0;
}