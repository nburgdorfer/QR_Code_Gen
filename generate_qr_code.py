"""Script to generate a QR code for a given URL."""

import qrcode
import argparse
from PIL import Image


def generate_qr_code_for_link(
    link: str,
    filename: str,
    version: int,
    fill_color: str,
    back_color: str,
    box_size: int,
    border: int,
    logo_path: str | None,
    logo_size: float,
) -> None:
    """Generates a QR code for a given URL.

    Args:
        link: Link for the QR code.
        filename: Output filename for the QR code image.
        version: Level of detail/complexity/size for the QR code (1-40).
        fill_color: Fill color for the QR code image.
        back_color: Back color for the QR code image.
        box_size: Size of each "box" or pixel in the QR code
        border: Thickness of the border around the QR code
        logo_path: Path to the logo thumbnail to add to the center of the QR code.
        logo_size: Size of the logo (as a percentage) placed in the center of the QR code.
    """

    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # type: ignore
        box_size=box_size,
        border=border,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = (qr.make_image(fill_color=fill_color, back_color=back_color)).convert("RGBA") # type: ignore

    # add logo
    if logo_path is not None:
        logo = Image.open(logo_path).convert("RGBA")
        qr_width, qr_height = img.size
        logo_max_size = int(min(qr_width, qr_height) * logo_size)
        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        logo_width, logo_height = logo.size
        x_center = (qr_width - logo_width) // 2
        y_center = (qr_height - logo_height) // 2
        position = (x_center, y_center)

        # paste background color square first
        #TODO: set color based on background color (need to do string-to-rgb conversion)
        color = (255,255,255)
        bbox_width = ((int(1.05*logo_width) // box_size)+1) * box_size
        bbox_height = ((int(1.05*logo_height) // box_size)+1) * box_size
        bbox_position = ((qr_width - bbox_width) // 2, (qr_height - bbox_height) // 2)
        bbox = Image.new("RGB", (bbox_width, bbox_height), color).convert("RGBA")
        img.paste(bbox, bbox_position, bbox)

        # paste logo
        img.paste(logo, position, logo)

    img.save(filename)
    print(f"QR code for '{link}' saved as '{filename}'")


parser = argparse.ArgumentParser(description="Creates a QR code from a link.")
parser.add_argument("--link", type=str, help="Link for the QR code", required=True)
parser.add_argument(
    "--filename",
    type=str,
    default="qrcode.png",
    help="Output filename for the QR code image",
)
parser.add_argument(
    "--version",
    type=int,
    default=4,
    help="Level of detail/complexity/size for the QR code (1-40)",
)
parser.add_argument(
    "--fill_color", type=str, default="black", help="Fill color for the QR code image"
)
parser.add_argument(
    "--back_color", type=str, default="white", help="Back color for the QR code image"
)
parser.add_argument(
    "--box_size",
    type=int,
    default=25,
    help="Size of each 'box' or pixel in the QR code",
)
parser.add_argument(
    "--border", type=int, default=2, help="Thickness of the border around the QR code"
)
parser.add_argument(
    "--logo_path",
    type=str,
    help="Logo placed in the center of the QR code",
)
parser.add_argument(
    "--logo_size",
    type=float,
    default=0.25,
    help="Size of the logo (as a percentage) placed in the center of the QR code",
)
ARGS = parser.parse_args()


def main() -> None:
    generate_qr_code_for_link(
        link=ARGS.link,
        filename=ARGS.filename,
        version=ARGS.version,
        fill_color=ARGS.fill_color,
        back_color=ARGS.back_color,
        box_size=ARGS.box_size,
        border=ARGS.border,
        logo_path=ARGS.logo_path,
        logo_size=ARGS.logo_size,
    )


if __name__ == "__main__":
    main()
