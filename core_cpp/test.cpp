#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main() {
	Point2f lonlat(0,0);

	vector<Point2f> array1 = { Point2f(330,250),  Point2f(50,370),  Point2f(945,395),  Point2f(815,245)};
	vector<Point2f> array2 = { Point2f(-73.984976, 40.759271),  Point2f(-73.985132, 40.759316), 
		Point2f(-73.985201, 40.759196),  Point2f(-73.985035,40.759104)};


	Mat M = getPerspectiveTransform(array1, array2);
	cout << M;
}