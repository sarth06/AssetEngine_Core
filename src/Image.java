import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.BufferedInputStream;
import java.io.InputStream;

public class Image {
    // 1. The State
    public String format;
    public int width;
    public int height;
    public int maxColor;
    public int[][][] imageMatrix;

    public Image() {
        this("assets/high_res.ppm");
    }

    // --- NEW HELPER: THE TOKEN EXTRACTOR ---
    // Reads individual text words safely from a raw byte stream
    private String readToken(InputStream stream) throws IOException {
        StringBuilder token = new StringBuilder();
        int b;
        // Skip all leading whitespace
        while ((b = stream.read()) != -1 && Character.isWhitespace(b)) {}

        // Read characters until the next whitespace
        if (b != -1) token.append((char) b);
        while ((b = stream.read()) != -1 && !Character.isWhitespace(b)) {
            token.append((char) b);
        }
        return token.toString();
    }

    // 2. The Core Ingestion Engine (Hybrid Binary/Text Reader)
    public Image(String path) {
        try (BufferedInputStream inputStream = new BufferedInputStream(new FileInputStream(new File(path)))) {
            // --- STEP 1: PARSE THE TEXT HEADER ---
            this.format = readToken(inputStream);
            this.width = Integer.parseInt(readToken(inputStream));
            this.height = Integer.parseInt(readToken(inputStream));
            this.maxColor = Integer.parseInt(readToken(inputStream));

            System.out.println("Engine Status: Memory Allocated for " + width + "x" + height + " matrix.");

            // Allocate RAM
            this.imageMatrix = new int[height][width][3];

            // --- STEP 2: PARSE THE RAW MACHINE BYTES ---
            // Because inputStream.read() pulls exactly 1 byte (0-255),
            // it perfectly matches our RGB color requirements.
            for (int row = 0; row < height; row++) {
                for (int col = 0; col < width; col++) {
                    this.imageMatrix[row][col][0] = inputStream.read(); // Red
                    this.imageMatrix[row][col][1] = inputStream.read(); // Green
                    this.imageMatrix[row][col][2] = inputStream.read(); // Blue
                }
            }

        } catch (FileNotFoundException e) {
            throw new IllegalStateException("System Error: Asset not found at " + path, e);
        } catch (IOException e) {
            throw new IllegalStateException("System Error: Corrupted binary stream.", e);
        }
    }

    // 3. The Export Layer
    public void export(String outputPath) {
        try (PrintWriter writer = new PrintWriter(new File(outputPath))) {

            // CRITICAL OVERRIDE: We read a P6 (Binary) file, but we are exporting
            // a P3 (Text) file so you can easily view the output text.
            writer.println("P3");
            writer.println(width + " " + height);
            writer.println(maxColor);

            // Unload the Matrix to the Hard Drive
            for (int row = 0; row < height; row++) {
                for (int col = 0; col < width; col++) {
                    int r = imageMatrix[row][col][0];
                    int g = imageMatrix[row][col][1];
                    int b = imageMatrix[row][col][2];
                    writer.print(r + " " + g + " " + b + "  ");
                }
                writer.println();
            }

            System.out.println("Engine Status: Asset successfully compiled to " + outputPath);
        } catch (FileNotFoundException e) {
            System.out.println("System Error: Asset export destination not found.");
        }
    }
}