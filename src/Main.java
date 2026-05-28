public class Main {
    public static void main(String[] args) {
        System.out.println("--- ENGINE STARTING: CONCURRENCY TEST ---");

        // 1. HARDWARE RECONNAISSANCE (This is the variable your IDE couldn't find!)
        int cores = Runtime.getRuntime().availableProcessors();
        System.out.println("Hardware Recon: JVM mapping tasks to " + cores + " active CPU cores.");

        // 2. INGESTION
        long startTime = System.currentTimeMillis();
        Image myImage = new Image("assets/high_res.ppm");
        long ingestionTime = System.currentTimeMillis();
        System.out.println("Ingestion Phase: " + (ingestionTime - startTime) + " ms");

        // 3. COMPUTE (Passing the 'cores' variable we just created above)
        Filter.applyGrayscale(myImage, cores);
        long computeTime = System.currentTimeMillis();
        System.out.println("Compute Phase: " + (computeTime - ingestionTime) + " ms");

        // 4. EXPORT
        myImage.export("assets/high_res_output.ppm");
        long exportTime = System.currentTimeMillis();
        System.out.println("Export Phase: " + (exportTime - computeTime) + " ms");

        System.out.println("Total Execution Time: " + (exportTime - startTime) + " ms");
    }
}