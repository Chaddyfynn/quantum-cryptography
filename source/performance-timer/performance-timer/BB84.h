#pragma once

#include<cstdlib>
#include<iostream>

class BB84
{
public:
	// Default Constructor
	BB84(){ 
		_seed = std::time(NULL);
		srand((unsigned)time(NULL));
	}

	// Generate Keys
	int* genBin(int len) {
		int* arr = new int[len];
		for (int i = 0; i < len; i++) {
			arr[i] = rand() % 2;
		}
		return arr;
	}

	// Receive Key
	int* genSharedKey(int* initKey, int* sendBase, int* receiveBase) {
		int len = sizeof(*initKey) / sizeof(initKey[0]);
		int* arr = new int[len];
			for (int i = 0; i < len; i++) {
			if (sendBase[i] == receiveBase[i]) {
				arr[i] = initKey[i];
			}
		}
			return arr;
	}

	// Encode Data

	// Decode Data

	// Representation
	char* toString(int* arr) {
		int len = sizeof(*arr) / sizeof(arr[0]);
		char* str = new char[len];
		for (int i = 0; i < len; i++) {
			/*if (arr[i] == NULL) {
				str[i] = 'N';
			}
			else {*/
				str[i] = char(arr[i]);
			/*}*/
		}
		return str;
	}

private:
	int _seed;
};

