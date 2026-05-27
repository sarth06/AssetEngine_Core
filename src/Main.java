public class Main {
    public static void main(String[] args) {
        System.out.println("--- ENGINE STARTING: LOAD TEST ---");

        // 1. INGESTION BENCHMARK
        long startTime = System.currentTimeMillis();
        Image myImage = new Image("assets/high_res.ppm");
        long ingestionTime = System.currentTimeMillis();
        System.out.println("Ingestion Phase: " + (ingestionTime - startTime) + " ms");

        // 2. COMPUTE BENCHMARK
        Filter.applyGrayscale(myImage);
        long computeTime = System.currentTimeMillis();
        System.out.println("Compute Phase: " + (computeTime - ingestionTime) + " ms");

        // 3. EXPORT BENCHMARK
        myImage.export("assets/high_res_output.ppm");
        long exportTime = System.currentTimeMillis();
        System.out.println("Export Phase: " + (exportTime - computeTime) + " ms");

        System.out.println("Total Execution Time: " + (exportTime - startTime) + " ms");
    }
}