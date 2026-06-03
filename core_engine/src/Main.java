import java.io.File;

public class Main {
    public static void main(String[] args) {
        // 1. HEADLESS ARGUMENT VALIDATION
        if (args.length < 3) {
            System.err.println("[CRITICAL ERROR] Engine requires 3 arguments.");
            System.exit(1);
        }

        String inputPath = args[0];
        String outputPath = args[1];
        String mode = args[2].toLowerCase();

        System.out.println("========================================");
        System.out.println("⚡ AeroCanvas Native Core Initialized");
        System.out.println("========================================");
        System.out.println("[ENGINE] Input Target : " + inputPath);
        System.out.println("[ENGINE] Output Target: " + outputPath);
        System.out.println("[ENGINE] Filter Mode  : " + mode);

        // 2. FILE SYSTEM CHECK
        File inputFile = new File(inputPath);
        if (!inputFile.exists()) {
            System.err.println("[ERROR] Input file does not exist at path: " + inputPath);
            System.exit(1);
        }

        // 3. EXECUTE COMPUTATIONAL PIPELINE
        try {
            long startTime = System.nanoTime();

            // Load the raw binary image into memory
            Image img = new Image(inputPath);

            // Route to the exact method names found in your Image.java file
            switch (mode) {
                case "invert":
                    img.applyInversion();
                    break;
                case "blur":
                    img.applyBlur();
                    break;
                case "edge":
                    img.applyEdgeDetection();
                    break;
                case "sharpen":
                    img.applySharpen();
                    break;
                case "grayscale":
                    img.applyGrayscale();
                    break;
                default:
                    System.err.println("[ERROR] Unknown filter mode requested: " + mode);
                    System.exit(1);
            }

            // Flush the processed memory buffer back to disk using your save() method
            img.save(outputPath);

            long endTime = System.nanoTime();
            double executionTimeMs = (endTime - startTime) / 1_000_000.0;

            System.out.println("[ENGINE] Execution Complete!");
            System.out.printf("[ENGINE] Compute Latency: %.2f ms\n", executionTimeMs);

        } catch (Exception e) {
            System.err.println("[CRITICAL EXCEPTION] The native compute core crashed.");
            e.printStackTrace();
            System.exit(1);
        }
    }
}