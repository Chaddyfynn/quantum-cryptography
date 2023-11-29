// performance-timer.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string>
#include <vector>
#include "BB84.h"
#include <chrono>

int main()
{
    /*std::string input;
    std::cout << "How many bits?";
    std::cin >> input;*/
    /*int len = std::stoi(input);*/
    std::string bb84;
    std::cout << "BB84?";
    std::cin >> bb84;
    bool b92 = false;
    if (bb84 == "n") {
        b92 = true;
    }

    std::string num;
    std::cout << "How many runs?";
    std::cin >> num;
    int run = std::stoi(num);

    std::string start;
    std::cout << "Start?";
    std::cin >> start;
    int startBit = std::stoi(start);

    std::string end;
    std::cout << "End?";
    std::cin >> end;
    int endBit = std::stoi(end);

    std::vector<int> aveTimes;
    std::vector<int> devTimes;
    std::vector<int> bits;
    int step;
    if (b92) {
        startBit *= 4;
        endBit *= 4;
        step = 4;
    }
    else {
        startBit *= 2;
        endBit *= 2;
        step = 2;
    }

    for (int j = startBit; j <= endBit; j+= step) {
        std::vector<std::chrono::microseconds> times;
        bits.push_back(j/step);

        for (int i = 0; i < run; i++) {


            auto start = std::chrono::high_resolution_clock::now();
            BB84* qkd = new BB84();

            std::vector<int> initialKey;
            initialKey = qkd->genBin(j);

            std::vector<int> encryptBasis;
            encryptBasis = qkd->genBin(j);

            std::vector<int> decryptBasis;
            decryptBasis = qkd->genBin(j);

            std::vector<int> sharedKey;
            sharedKey = qkd->genSharedKey(initialKey, encryptBasis, decryptBasis);

            for (int i = 0; i < sharedKey.size() / 2; i++) {
            }

            auto stop = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(2 * (stop - start));
            times.push_back(duration);
        }

        std::chrono::microseconds ave = times[0];
        for (int i = 1; i < times.size(); i++) {
            ave += times[i];
        }
        ave /= times.size();
        std::cout << "Time taken by function: "
            << ave.count() << " microseconds" << std::endl;
        aveTimes.push_back(ave.count());

        int std = pow(times[0].count() - ave.count(),2);
        for (int i = 1; i < times.size(); i++) {
            std += pow(times[i].count() - ave.count(), 2);
        }
        std /= times.size();
        std = sqrt(std);
        devTimes.push_back(std);
    }

    

    for (int i = 0; i < bits.size(); i++) {
        std::cout << "Time for " << bits[i] << " bits was " << aveTimes[i] << " +- " << devTimes[i] << "microseconds." << std::endl;
    }

    std::cout << std::endl;

    for (int i = 0; i < bits.size(); i++) {
        std::cout << bits[i] << "," << aveTimes[i] << "," << devTimes[i] << std::endl;
    }

    std::cout << "Type anything to close" << std::endl;
    std::string empty;
    std::cin >> empty;

    return 0;
}

