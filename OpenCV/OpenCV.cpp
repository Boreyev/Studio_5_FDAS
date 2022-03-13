#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include<opencv2/opencv.hpp>

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

int main()
{
	//Add profile and frontal face detect libraries. 
	string xmlPath1 = "C:/users/Boreyev/Documents/libraries/opencv/build/etc/haarcascades//haarcascade_frontalface_alt.xml";
	string xmlPath2 = "C:/users/Boreyev/Documents/libraries/opencv/build/etc/haarcascades//haarcascade_profileface.xml";

	double scale = 3; //Scales frame resolution (higher = quicker, 1.0 = default)

	//Importing cascade dependencies
	CascadeClassifier faceCascade, profileCascade;

	faceCascade.load(xmlPath1);
	profileCascade.load(xmlPath2);

	//Capture video frame from webcam
	VideoCapture cam(0);
	if (!cam.isOpened())
		return -1;
	
	//While true:
	for (;;)
	{
		Mat frame;
		cam >> frame;

		//Convert captured frames to grayscale. Haar Cascade face detection requires a grayscale image.
		Mat grayscale;
		cvtColor(frame, grayscale, COLOR_BGR2GRAY);
		//Resize the image by dividing the width/height by the scale.
		resize(grayscale, grayscale, Size(grayscale.size().width / scale, grayscale.size().height / scale));

		//Create rectangle vector, Set for detectMultiScale method parameters:
		//Image matrix, rectangle vect, scale factor, min neighbours, flags, min object size, max object size.
		vector<Rect> faceArea;
		profileCascade.detectMultiScale(grayscale, faceArea, 1.1, 3, 0, Size(30, 30));
		
		//For area in faceArea: set colour to (0, 255, 0).
		//Creates rectangle around detected face
		for (Rect area : faceArea) {
			Scalar drawColor = Scalar(0, 255, 255);
			rectangle(frame, Point(cvRound(area.x * scale), cvRound(area.y * scale)),
				Point(cvRound((area.x + area.width - 1) * scale), cvRound((area.y + area.height - 1) * scale)), drawColor);
			
			putText(frame, "Face Detected", cv::Point(area.x +100, area.y +60), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(0, 255, 0), 1.5, 8);
		}


		//Displays webcam frame to user.
		imshow("Webcam", frame);

		//If user presses key, exit software
		if (waitKey(30) > -0)
			break;
	}

	return 0;
}