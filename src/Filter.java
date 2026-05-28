import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Filter {

    // Notice we now pass the 'numCores' dynamically into the method
    public static void applyGrayscale(Image img, int numCores) {

        // 1. The Thread Pool: We spin up exactly 8 workers based on your hardware
        ExecutorService executor = Executors.newFixedThreadPool(numCores);

        // 2. The Chunking Math: Divide the rows evenly among the workers
        int chunkSize = img.height / numCores;

        // 3. The Dispatch Loop
        for (int i = 0; i < numCores; i++) {

            // Define strict boundaries for each thread (these must be 'final' to pass into the lambda)
            final int startRow = i * chunkSize;
            // The last thread picks up any leftover rows if the height isn't perfectly divisible by 8
            final int endRow = (i == numCores - 1) ? img.height : startRow + chunkSize;

            // Submit the mission to the thread pool
            executor.execute(() -> {
                // This is your exact same O(1) algorithm, but restricted to this thread's specific territory
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

        // 4. The Synchronization Barrier
        executor.shutdown(); // Tell the pool no more tasks are coming
        try {
            // Force the main program to stop and wait here until all 8 workers report back
            executor.awaitTermination(1, TimeUnit.MINUTES);
        } catch (InterruptedException e) {
            System.out.println("System Error: Thread execution violently interrupted.");
        }

        System.out.println("Filter Status: Concurrency execution complete. 8 cores successfully synchronized.");
    }
}