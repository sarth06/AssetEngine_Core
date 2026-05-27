public class Filter {

    // A static method means we don't need to instantiate a "Filter" object.
    // We just pass an Image into it, and it alters the image's matrix.
    public static void applyGrayscale(Image img) {

        // Loop through the image's height and width
        for (int row = 0; row < img.height; row++) {
            for (int col = 0; col < img.width; col++) {

                // Extract current RGB values from the object
                int r = img.imageMatrix[row][col][0];
                int g = img.imageMatrix[row][col][1];
                int b = img.imageMatrix[row][col][2];

                // Calculate the grayscale average
                int average = (r + g + b) / 3;

                // Overwrite the original pixel in-place
                img.imageMatrix[row][col][0] = average;
                img.imageMatrix[row][col][1] = average;
                img.imageMatrix[row][col][2] = average;
            }
        }
        System.out.println("Filter Status: Grayscale successfully applied in-place.");
    }
}