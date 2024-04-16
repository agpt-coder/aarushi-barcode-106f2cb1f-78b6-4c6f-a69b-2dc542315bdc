import logging
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Union

import prisma
import prisma.enums
import project.generate_barcode_service
import project.validate_input_data_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-barcode-1",
    lifespan=lifespan,
    description="The project's objective is to develop a system that accepts product data such as SKU, UPC, EAN, etc., and generates barcode images in the specified formats which include EAN-13 and Code 128 due to their extensive usage in the retail and logistics sectors. Although the user initially inquired about customizing the size, color, and resolution of the barcodes, they stated no requirement for such customizations. Yet, information collected demonstrated the capability to customize barcodes using Python libraries, suggesting flexibility in the implementation if needed in the future.\n\nThe product data will be provided through structured data formats like JSON or CSV files, ensuring a seamless and error-free data transfer process for barcode generation. Python, with its rich ecosystem of libraries, will be leveraged for this development. The 'python-barcode' library is identified as suitable for generating the barcode images. Additionally, for instances where customization might be required, the 'Pillow' library could be used to adjust the size, color, and resolution of the generated barcode images. Instructions and examples were provided on installing necessary libraries, generating barcodes, customizing, and saving them as image files using Python.\n\nThis system plays a crucial role in various applications, streamlining operations and enhancing efficiency in product identification and logistics management. Its development within the specified tech stack, utilizing Python, FastAPI for API creation, PostgreSQL as the database, and Prisma as the ORM, will ensure a robust and scalable solution to meet the user's needs.",
)


@app.post(
    "/validate/data",
    response_model=project.validate_input_data_service.ValidationResponse,
)
async def api_post_validate_input_data(
    data_format: str, product_data: Union[Dict, List[Dict], str]
) -> project.validate_input_data_service.ValidationResponse | Response:
    """
    Validates incoming product data for barcode generation.
    """
    try:
        res = project.validate_input_data_service.validate_input_data(
            data_format, product_data
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate/barcode",
    response_model=project.generate_barcode_service.GenerateBarcodeResponse,
)
async def api_post_generate_barcode(
    sku: Optional[str],
    upc: Optional[str],
    ean: Optional[str],
    format: prisma.enums.BarcodeFormat,
    size: Optional[str],
    color: Optional[str],
    resolution: Optional[int],
) -> project.generate_barcode_service.GenerateBarcodeResponse | Response:
    """
    Generates a barcode image from the provided product data.
    """
    try:
        res = await project.generate_barcode_service.generate_barcode(
            sku, upc, ean, format, size, color, resolution
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
