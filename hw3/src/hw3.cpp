#include <opencv/cv.h>
#include <opencv/highgui.h>

void doSobel(cv::Mat input) {
  int scale = 1;
  int delta = 0;
  int ddepth = CV_16S;
  cv::Mat grad_x, grad_y;
  cv::Mat abs_grad_x, abs_grad_y;
  cv::Mat grad;
  
  cv::Mat blurred;
  cv::blur(input, blurred, cv::Size(3,3));
  
  //   Gradient X with kernel size 3
  cv::Sobel(blurred, grad_x, ddepth, 1, 0, 3, scale, delta, cv::BORDER_DEFAULT);
  //   Gradient Y with kernel size 3
  cv::Sobel(blurred, grad_y, ddepth, 0, 1, 3, scale, delta, cv::BORDER_DEFAULT);
  
  //   Convert back to CV_8U
  cv::convertScaleAbs(grad_x, abs_grad_x);
  cv::convertScaleAbs(grad_y, abs_grad_y);
  
  //   Adding gradients together
  cv::addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, grad);
  
  cv::imshow("Sobel Edge Detection", grad);
  
  //   Do the Hough Transform
  cv::Mat cdst;
  cv::cvtColor(grad, cdst, CV_GRAY2BGR);
  
  std::vector<cv::Vec4i> lines;
  HoughLinesP(grad, lines, 1, CV_PI/180, 50, 50, 10 );
  for( size_t i = 0; i < lines.size(); i++ )
  {
    cv::Vec4i l = lines[i];
    cv::line( cdst, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, CV_AA);
  }
  
  cv::imshow("Sobel Edge Detection with Hough Transform", cdst);
}

void doLaplace(cv::Mat input) {
  cv::Mat dst;
  int kernel_size = 3;
  int scale = 1;
  int delta = 0;
  int ddepth = CV_16S;
  
  // Smooth the image
  cv::GaussianBlur( input, input, cv::Size(3,3), 0, 0, cv::BORDER_DEFAULT );
  
  Laplacian( input, dst, ddepth, kernel_size, scale, delta, cv::BORDER_DEFAULT );
  
  cv::Mat abs_dst;
  
  convertScaleAbs( dst, abs_dst );
  
  // cv::imshow("Laplace Edge Detection", abs_dst);
  
  //   Do Hough Transform
  cv::Mat color_laplace_hough;
  cv::cvtColor(abs_dst, color_laplace_hough, CV_GRAY2BGR);
  
  std::vector<cv::Vec4i> lines_canny;
  cv::HoughLinesP(abs_dst, lines_canny, 1, CV_PI/180, 500, 50, 10 );
  for( size_t i = 0; i < lines_canny.size(); i++ )
  {
    cv::Vec4i l = lines_canny[i];
    cv::line( color_laplace_hough, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, CV_AA);
  }
  
  cv::imshow("Laplace Edge Detection with Hough Transform", color_laplace_hough);
}

void doCanny(cv::Mat input) {
  cv::Mat detected_edges;
  
  cv::Canny(input, detected_edges, 50, 200, 3);
  
  cv::imshow("Canny Edge Detection", detected_edges);
  
  //   Do Hough Transform
  cv::Mat color_canny_hough;
  cv::cvtColor(detected_edges, color_canny_hough, CV_GRAY2BGR);
  
  std::vector<cv::Vec4i> lines_canny;
  cv::HoughLinesP(detected_edges, lines_canny, 1, CV_PI/180, 50, 50, 10 );
  for( size_t i = 0; i < lines_canny.size(); i++ )
  {
    cv::Vec4i l = lines_canny[i];
    cv::line( color_canny_hough, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, CV_AA);
  }
  
  cv::imshow("Canny Edge Detection with Hough Transform", color_canny_hough);
}

void doCannyWithNoise(cv::Mat input) {
  // Create some noise
  cv::Mat noise, noisy_input;
  noise = input.clone();
  noisy_input = input.clone();
  cv::randn(noise, cv::Scalar::all(0.0), cv::Scalar::all(25.0));
  cv::add(input, noise, noisy_input);
  
  cv::imshow("Original Image with Noise", noisy_input);
  
  cv::Mat detected_edges;
  
  cv::Canny(noisy_input, detected_edges, 50, 200, 3);
  
  cv::imshow("Canny Edge Detection with Noise", detected_edges);
  
  //   Do Hough Transform
  cv::Mat color_canny_hough;
  cv::cvtColor(detected_edges, color_canny_hough, CV_GRAY2BGR);
  
  std::vector<cv::Vec4i> lines_canny;
  cv::HoughLinesP(detected_edges, lines_canny, 1, CV_PI/180, 50, 50, 10 );
  for( size_t i = 0; i < lines_canny.size(); i++ )
  {
    cv::Vec4i l = lines_canny[i];
    cv::line( color_canny_hough, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, CV_AA);
  }
  
  cv::imshow("Canny Edge Detection with Noise and Hough Transform", color_canny_hough);
}

void doSIFT(cv::Mat input) {
  cv::SiftFeatureDetector detector;
  std::vector<cv::KeyPoint> keypoints;
  detector.detect(input, keypoints);
  
  // Add results to image and save.
  cv::Mat output;
  cv::drawKeypoints(input, keypoints, output);
  cv::imshow("SIFT Features", output);
}

int main(int argc, const char* argv[])
{
  // Load original Image
  cv::Mat input = cv::imread("hallway.jpg", 0); // Load as grayscale
  
  // Show it
  cv::imshow("Original Image", input);
  
  // Do Sobel edge detection
  // doSobel(input);
  
  // Do Laplace edge detection
  // doLaplace(input);
  
  // Do canny edge detection
  doCanny(input);
  
  // Do canny edge detection with noise
  doCannyWithNoise(input);
  
  // Do SIFT detection
  // doSIFT(input);
  
  // Wait for key
  cv::waitKey();
}