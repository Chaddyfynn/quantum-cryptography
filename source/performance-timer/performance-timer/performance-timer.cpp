// performance-timer.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string>
#include "BB84.h"

int main()
{
    std::string input;
    std::cout << "How many bits?";
    std::cin >> input;
    int len = std::stoi(input);

    BB84 *qkd = new BB84();

    int* initialKey = new int[len];
    initialKey = qkd->genBin(len);
    
    std::cout << qkd->toString(initialKey);

}

