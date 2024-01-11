import argparse
import os
from PIL import Image
import io
import base64

OUTPUT_LQUIP_FILE = './lqips.txt'
OUTPUT_DIR = '../posts-compressed'

def convert_to_webp(input_file, output_dir):
    filename = os.path.basename(input_file)
    base, ext = os.path.splitext(filename)
    output_file = os.path.join(output_dir, f"{base}.webp")

    image = Image.open(input_file)
    image.save(output_file, format='WEBP')

    return output_file

# Global variable for the output file

def generate_lqip(image_path):
    # Open the image file.
    img = Image.open(image_path)

    # Resize the image to a smaller size.
    img.thumbnail((100, 100))

    # Convert the image to grayscale.
    img = img.convert('L')

    # Save the image to a BytesIO object.
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='WEBP')

    # Get the base64 representation of the image.
    img_base64 = base64.b64encode(byte_arr.getvalue()).decode()

    # Append the LQIP to the output file.
    with open(OUTPUT_LQUIP_FILE, 'a') as f:
        f.write("%s,%s\n" % (image_path, img_base64))

def main():
    parser = argparse.ArgumentParser(description='Convert images to .webp format and generate LQIP.')
    parser.add_argument('-i', '--input', type=str, help='Input image file')
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if args.input:
        input_files = [args.input]
    else:
        input_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    for input_file in input_files:
        output_file = convert_to_webp(input_file, OUTPUT_DIR)
        print(f"Converted {input_file} to {output_file}")

        lqip = generate_lqip(output_file)
        print(f"Generated LQIP for {output_file}: {lqip}")

if __name__ == "__main__":
    main()
