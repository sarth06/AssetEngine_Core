# generate_asset.py
print("Generating mathematical binary matrix...")
with open("true_binary.ppm", "wb") as f:
    width, height = 400, 400
    # Write the P6 Magic Number Header
    f.write(f"P6\n{width} {height}\n255\n".encode())

    # Write the raw RGB bytes
    for y in range(height):
        for x in range(width):
            r = int((x / width) * 255)
            g = int((y / height) * 255)
            b = 150
            f.write(bytes([r, g, b]))

print("SUCCESS: true_binary.ppm is ready for the engine.")