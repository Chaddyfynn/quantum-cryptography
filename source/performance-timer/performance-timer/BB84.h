#pragma once

#include<cstdlib>
#include<iostream>
#include<vector>

class BB84
{
public:
	// Default Constructor
	BB84(){ 
		_seed = std::time(NULL);
		srand((unsigned)time(NULL));
	}

	// Generate Keys
	std::vector<int> genBin(int len) {
		std::vector<int> arr;
		for (int i = 0; i < len; i++) {
			arr.push_back(rand() % 2);
		}
		return arr;
	}

	// Receive Key
	std::vector<int> genSharedKey(std::vector<int> initKey, std::vector<int> sendBase, std::vector<int> receiveBase) {
		int len = initKey.size();
		std::vector<int> arr;
			for (int i = 0; i < len; i++) {
			if (sendBase[i] == receiveBase[i]) {
				arr.push_back(initKey[i]);
			}
		}
			return arr;
	}

	// Encode Data

	// Decode Data

	// Representation
	std::string toString(std::vector<int> arr) {
		int len = arr.size();
		std::string str;
		for (int i = 0; i < len; i++) {
			str.push_back(48 + arr[i]); // Do not let arr contain values greater than 1, or less than 0
		}
		return str;
	}

private:
	int _seed;
};

