#include "NumCpp.hpp"

using namespace std;

int main(){
    
    nc::NdArray<double> arr = { 0.038, 0.194, 0.425};
    nc::NdArray<double> arr1 = { 0.05, 0.127, 0.094};
    
    nc::NdArray<double> dp = nc::dot(arr, arr1);
    
    cout<<"This is the dot product: "<<dp<<endl;
    
    return 0;
}