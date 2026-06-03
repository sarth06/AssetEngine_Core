import java.io.*;

public class Image {
    private int width;
    private int height;
    private int maxColorVal;
    private byte[] pixels;

    public Image(String filePath) throws IOException {
        readPPM(filePath);
    }

    private void readPPM(String filePath) throws IOException {
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(filePath))) {
            char c1 = (char) bis.read();
            char c2 = (char) bis.read();
            if (c1 != 'P' || c2 != '6') throw new IOException("Invalid PPM format. Expected P6 Binary.");
            bis.read();

            width = Integer.parseInt(nextString(bis));
            height = Integer.parseInt(nextString(bis));
            maxColorVal = Integer.parseInt(nextString(bis));

            pixels = new byte[width * height * 3];
            bis.read(pixels);
        }
    }

    private String nextString(BufferedInputStream bis) throws IOException {
        StringBuilder sb = new StringBuilder();
        int b;
        while ((b = bis.read()) != -1) {
            if (b == '#') {
                while ((b = bis.read()) != '\n' && b != '\r' && b != -1) ;
                continue;
            }
            if (Character.isWhitespace(b)) {
                if (sb.length() > 0) break;
            } else {
                sb.append((char) b);
            }
        }
        return sb.toString();
    }

    public void save(String filePath) throws IOException {
        try (BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(filePath))) {
            String header = "P6\n" + width + " " + height + "\n" + maxColorVal + "\n";
            bos.write(header.getBytes());
            bos.write(pixels);
        }
    }

    // --- FILTER: Inversion ---
    public void applyInversion() {
        for (int i = 0; i < pixels.length; i++) {
            int val = pixels[i] & 0xFF;
            pixels[i] = (byte) (255 - val);
        }
    }

    // --- FILTER: Box Blur (Restored to actual blurring) ---
    public void applyBlur() {
        byte[] temp = new byte[pixels.length];
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int r = 0, g = 0, b = 0, count = 0;
                for (int dy = -1; dy <= 1; dy++) {
                    for (int dx = -1; dx <= 1; dx++) {
                        int ny = y + dy, nx = x + dx;
                        if (ny >= 0 && ny < height && nx >= 0 && nx < width) {
                            int index = (ny * width + nx) * 3;
                            r += pixels[index] & 0xFF;
                            g += pixels[index + 1] & 0xFF;
                            b += pixels[index + 2] & 0xFF;
                            count++;
                        }
                    }
                }
                int outIndex = (y * width + x) * 3;
                temp[outIndex] = (byte) (r / count);
                temp[outIndex + 1] = (byte) (g / count);
                temp[outIndex + 2] = (byte) (b / count);
            }
        }
        pixels = temp;
    }

    // --- FILTER: Grayscale ---
    public void applyGrayscale() {
        for (int i = 0; i < pixels.length; i += 3) {
            int r = pixels[i] & 0xFF;
            int g = pixels[i + 1] & 0xFF;
            int b = pixels[i + 2] & 0xFF;
            int avg = (r + g + b) / 3;
            pixels[i] = (byte) avg;
            pixels[i + 1] = (byte) avg;
            pixels[i + 2] = (byte) avg;
        }
    }
    // --- FILTER: Sharpen ---
    public void applySharpen() {
        int[] sharpenKernel = { 0, -1, 0, -1, 5, -1, 0, -1, 0 };
        applyConvolution(sharpenKernel);
    }

    // --- FILTER: Edge Detection ---
    public void applyEdgeDetection() {
        int[] edgeKernel = { -1, -1, -1, -1, 8, -1, -1, -1, -1 };
        applyConvolution(edgeKernel);
    }

    // --- HELPER: Matrix Math Engine ---
    private void applyConvolution(int[] kernel) {
        byte[] temp = new byte[pixels.length];
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int r = 0, g = 0, b = 0;
                int kernelIndex = 0;
                for (int dy = -1; dy <= 1; dy++) {
                    for (int dx = -1; dx <= 1; dx++) {
                        int ny = Math.min(Math.max(y + dy, 0), height - 1);
                        int nx = Math.min(Math.max(x + dx, 0), width - 1);
                        int pixelIndex = (ny * width + nx) * 3;
                        int weight = kernel[kernelIndex++];
                        r += (pixels[pixelIndex] & 0xFF) * weight;
                        g += (pixels[pixelIndex + 1] & 0xFF) * weight;
                        b += (pixels[pixelIndex + 2] & 0xFF) * weight;
                    }
                }
                int outIndex = (y * width + x) * 3;
                temp[outIndex] = (byte) Math.min(Math.max(r, 0), 255);
                temp[outIndex + 1] = (byte) Math.min(Math.max(g, 0), 255);
                temp[outIndex + 2] = (byte) Math.min(Math.max(b, 0), 255);
            }
        }
        pixels = temp;
    }
}

// --- FILTER: Sharpen