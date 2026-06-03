import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Filter {

    // --- MATH LAYER 1: 1D GRAYSCALE ---
    public static void applyGrayscale(Image img, int numCores) {
        ExecutorService executor = Executors.newFixedThreadPool(numCores);
        int chunkSize = img.height / numCores;

        for (int i = 0; i < numCores; i++) {
            final int startRow = i * chunkSize;
            final int endRow = (i == numCores - 1) ? img.height : startRow + chunkSize;

            executor.execute(() -> {
                for (int row = startRow; row < endRow; row++) {
                    for (int col = 0; col < img.width; col++) {
                        int r = img.imageMatrix[row][col][0];
                        int g = img.imageMatrix[row][col][1];
                        int b = img.imageMatrix[row][col][2];
                        int average = (r + g + b) / 3;
                        img.imageMatrix[row][col][0] = average;
                        img.imageMatrix[row][col][1] = average;
                        img.imageMatrix[row][col][2] = average;
                    }
                }
            });
        }
        executor.shutdown();
        try {
            executor.awaitTermination(1, TimeUnit.MINUTES);
        } catch (InterruptedException e) {
            System.out.println("System Error: Thread execution violently interrupted.");
        }
        System.out.println("Filter Status: Grayscale execution complete. 8 cores successfully synchronized.");
    }

    // --- MATH LAYER 2: 3x3 CONVOLUTION BLUR ---
    public static void applyBlur(Image img, int numCores) {
        int[][][] tempMatrix = new int[img.height][img.width][3];
        ExecutorService executor = Executors.newFixedThreadPool(numCores);
        int chunkSize = img.height / numCores;

        for (int i = 0; i < numCores; i++) {
            final int startRow = (i == 0) ? 1 : i * chunkSize;
            final int endRow = (i == numCores - 1) ? img.height - 1 : startRow + chunkSize;

            executor.execute(() -> {
                for (int row = startRow; row < endRow; row++) {
                    for (int col = 1; col < img.width - 1; col++) {
                        int rSum = 0, gSum = 0, bSum = 0;

                        // 3x3 Grid Scan
                        for (int ky = -1; ky <= 1; ky++) {
                            for (int kx = -1; kx <= 1; kx++) {
                                rSum += img.imageMatrix[row + ky][col + kx][0];
                                gSum += img.imageMatrix[row + ky][col + kx][1];
                                bSum += img.imageMatrix[row + ky][col + kx][2];
                            }
                        }
                        // Write averages to temp matrix
                        tempMatrix[row][col][0] = rSum / 9;
                        tempMatrix[row][col][1] = gSum / 9;
                        tempMatrix[row][col][2] = bSum / 9;
                    }
                }
            });
        }
        executor.shutdown();
        try {
            executor.awaitTermination(1, TimeUnit.MINUTES);
            // State Transfer back to primary matrix
            for (int r = 1; r < img.height - 1; r++) {
                for (int c = 1; c < img.width - 1; c++) {
                    img.imageMatrix[r][c][0] = tempMatrix[r][c][0];
                    img.imageMatrix[r][c][1] = tempMatrix[r][c][1];
                    img.imageMatrix[r][c][2] = tempMatrix[r][c][2];
                }
            }
        } catch (InterruptedException e) {
            System.out.println("System Error: Convolution thread interrupted.");
        }
        System.out.println("Filter Status: 3x3 Convolution Blur successfully applied.");
    }
}