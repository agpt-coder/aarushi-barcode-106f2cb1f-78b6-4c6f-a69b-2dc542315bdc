import io
from datetime import datetime
from enum import Enum
from typing import Optional

import barcode
import prisma
import prisma.enums
import prisma.models
from barcode.writer import ImageWriter
from PIL import Image
from pydantic import BaseModel


class GenerateBarcodeResponse(BaseModel):
    """
    The response includes the generated barcode image as a downloadable file or accessible URL, along with potential metadata about the barcode generation.
    """

    barcodeImageURL: str
    format: prisma.enums.BarcodeFormat
    creationDate: str


class BarcodeFormat(Enum):
    EAN_13: str = "ean13"
    UPC_A: str = "upc"
    CODE_128: str = "code128"


async def generate_barcode(
    sku: Optional[str],
    upc: Optional[str],
    ean: Optional[str],
    format: prisma.enums.BarcodeFormat,
    size: Optional[str],
    color: Optional[str],
    resolution: Optional[int],
) -> GenerateBarcodeResponse:
    """
    Generates a barcode image from the provided product data.

    Args:
        sku (Optional[str]): Stock Keeping Unit, identifying the specific item.
        upc (Optional[str]): Universal Product Code, identifying the product in a universal registry.
        ean (Optional[str]): European Article Number, similar to UPC but used internationally.
        format (prisma.enums.BarcodeFormat): The barcode format to generate, e.g., EAN-13 or Code 128.
        size (Optional[str]): The desired size of the barcode image. Format: 'widthxheight' (e.g., '400x200').
        color (Optional[str]): The color of the barcode. Format: HEX color code (e.g., '#000000' for black).
        resolution (Optional[int]): The resolution of the barcode image in DPI (dots per inch).

    Returns:
        GenerateBarcodeResponse: The response includes the generated barcode image as a downloadable file or accessible URL, along with potential metadata about the barcode generation.
    """
    if format not in prisma.enums.BarcodeFormat:
        raise ValueError("Invalid barcode format provided")
    barcode_class = getattr(barcode, format.value.upper(), None)
    if not barcode_class:
        raise ValueError("Unsupported barcode format")
    content = upc or ean or sku
    if not content:
        raise ValueError("At least one of SKU, UPC, or EAN must be provided")
    writer = ImageWriter()
    options = {
        "write_text": False,
        "foreground": color if color else "black",
        "format": "PNG",
    }
    bcode = barcode_class(content, writer=writer)
    buffer = io.BytesIO()
    bcode.write(buffer, options=options)
    if size or resolution:
        img = Image.open(buffer)
        if size:
            width, height = (int(dim) for dim in size.split("x"))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        buffer.seek(0)
        img.save(
            buffer, "PNG", dpi=(resolution, resolution) if resolution else (300, 300)
        )
        buffer.seek(0)
    image_url = f"http://placeholder.image/barcode_{datetime.now().timestamp()}.png"
    barcode_record = await prisma.models.Barcode.prisma().create(
        data={
            "sku": sku,
            "upc": upc,
            "ean": ean,
            "format": format.value,
            "size": size,
            "color": color,
            "resolution": resolution if resolution else 300,
            "image": image_url,
            "userId": "user_id_placeholder",
        }
    )
    return GenerateBarcodeResponse(
        barcodeImageURL=image_url,
        format=format,
        creationDate=datetime.now().isoformat(),
    )
