public class Main {
    public static void main(String[] args) {
        String inputPath = "C:/Users/User/Desktop/AssetEngine_Core/workspace_data/input.ppm";
        String outputPath = "C:/Users/User/Desktop/AssetEngine_Core/workspace_data/high_res_output.ppm";

        String mode = "blur";
        if (args.length > 0) {
            mode = args[0].toLowerCase();
        }

        System.out.println("[ENGINE] Booting Native Image Processor in mode: " + mode);

        try {
            long startTime = System.currentTimeMillis();
            Image img = new Image(inputPath);

            // The Router: Maps Python's command to the correct mathematical matrix
            switch (mode) {
                case "invert":
                    img.applyInversion();
                    break;
                case "grayscale":
                    img.applyGrayscale();
                    break;
                case "sharpen":
                    img.applySharpen();
                    break;
                case "edge": // Matches the value="edge" in your HTML dropdown
                case "edge_detect": // Matches the AI Agent command
                    img.applyEdgeDetection();
                    break;
                case "blur":
                default:
                    img.applyBlur();
                    break;
            }

            img.save(outputPath);
            long endTime = System.currentTimeMillis();
            System.out.println("[ENGINE] Execution Complete. Compute Time: " + (endTime - startTime) + "ms");

        } catch (Exception e) {
            System.err.println("[ERROR] Engine failure: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}