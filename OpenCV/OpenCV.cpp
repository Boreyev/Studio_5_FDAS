#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

int main()
{
	string xmlPath = "C:/users/Boreyev/Documents/libraries/opencv/build/etc/haarcascades//haarcascade_frontalface_alt.xml";
	string referenceImage = "D:/Desktop/bryv/image/newimg/Camera Roll/WIN_20220307_01_06_17_Pro";

	double scale = 1; //Scales frame resolution (higher = quicker, 1.0 = default)

	//Importing cascade dependencies
	CascadeClassifier faceCascade;
	faceCascade.load(xmlPath);

	//Capture video frame from webcam
	VideoCapture cap(0);
	if (!cap.isOpened())
		return -1;

	//While true:
	for (;;)
	{
		Mat frame;
		cap >> frame;

		//Convert captured frames to grayscale. Haar Cascade face detection requires a grayscale image.
		Mat grayscale;
		cvtColor(frame, grayscale, COLOR_BGR2GRAY);
		//Resize the image by dividing the width/height by the scale.
		resize(grayscale, grayscale, Size(grayscale.size().width / scale, grayscale.size().height / scale));

		//Create rectangle vector, Set for detectMultiScale method parameters:
		//Image matrix, rectangle vect, scale factor, min neighbours, flags, min object size, max object size.
		vector<Rect> faceArea;
		faceCascade.detectMultiScale(grayscale, faceArea, 1.1, 3, 0, Size(5, 50));

		//For area in faceArea: set colour-range to 255 (grayscale)
		//Creates rectangle around detected face
		for (Rect area : faceArea) {
			Scalar drawColor = Scalar(255, 0, 0);
			rectangle(frame, Point(cvRound(area.x * scale), cvRound(area.y * scale)),
				Point(cvRound((area.x + area.width - 1) * scale), cvRound((area.y + area.height - 1) * scale)), drawColor);
		}

		//Displays webcam frame to user.
		imshow("Webcam", frame);

		//If user presses key, exit software
		if (waitKey(30) > -0)
			break;
	}

	return 0;
}