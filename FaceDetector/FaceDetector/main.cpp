#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"



#include <iostream>
#include <stdio.h>



using namespace std;
using namespace cv;



int main()
{
	double scale = 2.0; //Scales frame resolution (higher = quicker, 1.0 = default)

	//Importing cascade dependencies
	CascadeClassifier faceCascade;
	faceCascade.load("C:/OpenCV4/etc/haarcascades//haarcascade_frontalface_alt.xml");


	VideoCapture cap(0);
	if (!cap.isOpened())
		return -1;

	for (;;)
	{
		Mat frame;
		cap >> frame;

		Mat grayscale;
		cvtColor(frame, grayscale, COLOR_BGR2GRAY);
		resize(grayscale, grayscale, Size(grayscale.size().width / scale, grayscale.size().height / scale));

		vector<Rect> faces;
		faceCascade.detectMultiScale(grayscale, faces, 1.1, 3, 0, Size(30, 30));
		int numFaces = faces.size();//Calculating the number of faces and storing the integer value in x//

		for (Rect area : faces)
		{
			Scalar drawColor = Scalar(255, 0, 0);
			rectangle(frame, Point(cvRound(area.x * scale), cvRound(area.y * scale)),
				Point(cvRound((area.x + area.width - 1) * scale), cvRound((area.y + area.height - 1) * scale)), drawColor);

		}
		cout << "Number of face(s)in the image=" << numFaces << endl;//Displaying the value of x in the console window//
		imshow("Webcam Frame", frame);


//		system("pause");//Pausing the system to visualize the result//

		if (waitKey(30) >= 0)
			break;
	}
	return 0;
}