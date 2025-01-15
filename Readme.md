# ML 24/25-09 Creating Text from images with OCR API

## Overview

This project involves developing an OCR (Optical Character Recognition) solution using the Tesseract SDK. The application preprocesses images (e.g., shifting, rotating, adjusting) and extracts text from them. The goal is to evaluate the impact of preprocessing methods on the quality of text extraction.

The final product is a console application that:

- Accepts various parameters for input and preprocessing methods.
- Outputs extracted text for each preprocessing method.
- Compares the quality of the extracted text between preprocessing methods.

## Architecture

The solution is designed with modular components to ensure scalability and maintainability. Below is an overview of the architecture:

1. **Input Handling**:

   - Reads images from an input folder specified by the user.
   - Supports multiple image formats.

2. **Preprocessing Module**:

   - Applies transformations such as rotation, brightness adjustment, and deskewing to input images.

   - **Methods Used**

     * **Grayscale Coversion**

       * Grayscale image conversion helps streamline the image data and lower the processing requirements for some algorithms.

     * **Binarization**

       * Converting the image to back and white format by thresholding.

     * **Noise Removal**

       * Image filters are used to reduce noise, sharpen details, and overall improve the quality of images before text analysis.

     * **Deskewing**

       * Its important to straighten the read image to extract the exact data from image.

     * **Resizing**

       * Images come in all shapes and sizes, but machine learning algorithms typically require a standard size.
       * Resize and crop the images to square dimensions, often 224x224 or 256x256 pixels.

     * **Normalization**

       * While working with images, it's important to Normalize the pixel values(0 and 1) to have consistent brightness and improve contrast.

3. **OCR Module**:

   - Leverages the Terrasect SDK to extract text from both raw and preprocessed images.

4. **Comparison and Output Module**:
   - Compares extracted text quality across preprocessing methods.
   - Outputs results to specified folders or console.

### Technologies Used

1. **Programming Language**:

   - **C#**: The primary programming language for building the console application.

2. **SDK and Libraries**:

   - **Tesseract SDK**: Used for Optical Character Recognition (OCR) to extract text from images. ([Tesseract by charlesw](https://www.nuget.org/packages/tesseract/))

3. **Framework**:

   - **.NET 9**: Framework for building and running the console application.

4. **Development Tools**:
   - **Visual Studio 2022**: Integrated Development Environment (IDE) for writing, testing, and debugging the code.
   - **MSTest**: Framework for unit testing the application's logic.


## Results
- The results section will include findings on the effectiveness of various preprocessing methods and their impact on text extraction quality. This will be updated as development progresses.



