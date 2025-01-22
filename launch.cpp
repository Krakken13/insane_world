#include <iostream>
#include <cstdlib>
using namespace std;
int main() {
    string pythonFile = "main.py";
    string command = "python " + pythonFile;
    int result = system(command.c_str());
    return 0;
}