#include "iostream"          // Input/Output stream
#include "numpy/npy_math.h"  // Math functions from NumPy
using namespace std;         // So we don't have to use 'std' every time
                             // Program Starts
bool firebolt_portal = true; // Firebolt Portal connection
                             // Add all your variables here
int main() {                 // Define main function
    cout << "[INFO: shared/import.cc] C++ works!";
    if (firebolt_portal = true) {
        return firebolt_portal;
    } else {
        cout << "[WARN: shared/import.cc] Failed to connect to Firebolt Portal. Please try again.";
    }
    return 0;
}
