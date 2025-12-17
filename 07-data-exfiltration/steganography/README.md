# Image Steganography Toolkit

Hide data inside images using LSB (Least Significant Bit) encoding.

## Features

- Hide text or files inside images
- LSB encoding for minimal visual impact
- Automatic capacity checking
- Support for PNG, JPEG, and other image formats
- Binary data encoding/decoding
- Image capacity calculator

## Installation
```bash
pip install Pillow numpy
```

## Usage

### Hide Text in Image
```bash
# Encode secret text
python3 steganography.py --encode carrier.png \
  --data "secret message" --output encoded.png

# Decode and display text
python3 steganography.py --decode encoded.png --text
```

### Hide File in Image
```bash
# Encode file
python3 steganography.py --encode vacation.jpg \
  --data passwords.txt --output photo.jpg

# Decode file
python3 steganography.py --decode photo.jpg --output recovered.txt
```

### Check Image Capacity
```bash
# See how much data an image can hold
python3 steganography.py --capacity myimage.png
```

### Calculate Required Image Size
```bash
# Calculate minimum image size for 1MB of data
python3 steganography.py --calc-size 1000000
```

## Module Usage
```python
from steganography import ImageSteganography

# Initialize
stego = ImageSteganography()

# Encode data
stego.encode_data('carrier.png', 'secret message', 'encoded.png')

# Encode file
stego.encode_file('carrier.png', 'passwords.txt', 'encoded.png')

# Decode data
data = stego.decode_data('encoded.png')

# Decode file
stego.decode_file('encoded.png', 'recovered.txt')

# Check capacity
capacity = stego.check_capacity('carrier.png')
print(f"Max capacity: {capacity['max_mb']:.2f} MB")
```

## How It Works

LSB (Least Significant Bit) steganography works by:

1. Converting data to binary representation
2. Adding 4-byte length header
3. Modifying the least significant bit of each pixel
4. Changes are imperceptible to human eye
5. Data can be extracted by reading LSBs

## Capacity

Image capacity = (Width × Height × Channels) ÷ 8 bytes

Example: 1920×1080 RGB image = 777,600 bytes (~759 KB)

## Architecture

- `core.py` - Main ImageSteganography interface
- `encoder.py` - Data encoding operations
- `decoder.py` - Data decoding operations
- `binary_ops.py` - Binary conversion utilities
- `image_ops.py` - Image processing operations
- `cli.py` - Command-line interface

## Security Notes

- LSB steganography is detectable with statistical analysis
- Use for obfuscation, not strong security
- Combine with encryption for sensitive data
- PNG format better than JPEG (no compression artifacts)
- Larger images = more capacity

## Limitations

- JPEG compression may damage hidden data
- Some image editors strip LSB data
- Maximum capacity limited by image size
- Visual quality degradation with high data density