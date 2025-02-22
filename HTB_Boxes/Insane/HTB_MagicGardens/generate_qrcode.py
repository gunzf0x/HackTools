#!/usr/bin/python3
import qrcode
import argparse


def parse_arguments()->argparse.Namespace:
    """
    Get arguments from user
    """
    parser = argparse.ArgumentParser(description="Generate a QR code from input content.")
    parser.add_argument("content", type=str, help="The content to encode in the QR code.")
    qr_default: str = 'qrcode.png'
    parser.add_argument("-o", "--output",type=str, default=qr_default, 
                        help=f"Output file name for the QR code image (default: {qr_default}).")
    return parser.parse_args()


def create_qr_code(content: str, output_file:str)->None:
    """
    Create and save a QR code with the specified content.
    """
    print(f"[+] Appending the following content in QR Code:\n{content}\n")
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size in boxes
    )
    qr.add_data(content)
    qr.make(fit=True)
    # Generate and save the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"[+] QR code saved as {output_file!r}")


def main()->None:
    # Get arguments from user
    args: argparse.Namespace = parse_arguments()
    # Create QR Code
    create_qr_code(args.content, args.output)


if __name__ == "__main__":
    main()
