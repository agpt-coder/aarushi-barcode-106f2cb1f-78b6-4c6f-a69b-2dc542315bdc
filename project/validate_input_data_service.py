from typing import Dict, List, Union

from pydantic import BaseModel, ValidationError, validator


class ValidationResponse(BaseModel):
    """
    Conveys the results of the product data validation process, including any errors found. This ensures the caller receives detailed feedback on the validity of their submission.
    """

    is_valid: bool
    errors: List[str]


class ProductDataModel(BaseModel):
    """
       Validates each product's data against predefined schemas.
    class includes valid fields such as SKU, UPC, EAN, etc.
    """

    sku: str
    upc: Union[str, None] = None
    ean: Union[str, None] = None
    name: str
    description: Union[str, None] = None

    @validator("sku", "upc", "ean")
    def product_codes_must_be_non_empty_strings(cls, v):
        if v is not None and (not v.strip()):
            raise ValueError("Field must be a non-empty string.")
        return v


def validate_input_data(
    data_format: str, product_data: Union[Dict, List[Dict], str]
) -> ValidationResponse:
    """
    Validates incoming product data for barcode generation.

    Args:
        data_format (str): Specifies the format of the incoming data (e.g., "JSON", "CSV").
        product_data (Union[Dict, List[Dict], str]): Contains the product information for validation. Its type is dynamic, based on the 'data_format' field: 'str' for CSV format (as CSV data will be provided as a single string), and 'dict' or 'list[dict]' for JSON (depending on whether a single product or multiple products are submitted).

    Returns:
        ValidationResponse: Conveys the results of the product data validation process, including any errors found. This ensures the caller receives detailed feedback on the validity of their submission.
    """
    errors = []
    if data_format.lower() == "json":
        if isinstance(product_data, (dict, list)):
            try:
                if isinstance(product_data, dict):
                    ProductDataModel(**product_data)
                if isinstance(product_data, list):
                    for pd in product_data:
                        ProductDataModel(**pd)
            except ValidationError as e:
                errors.extend([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        else:
            errors.append("Invalid JSON data format received.")
    elif data_format.lower() == "csv":
        if isinstance(product_data, str):
            for row in product_data.splitlines():
                if not row.strip():
                    errors.append("Empty row found.")
        else:
            errors.append("Invalid CSV data format received.")
    else:
        errors.append(f"Unsupported data format: {data_format}")
    is_valid = len(errors) == 0
    return ValidationResponse(is_valid=is_valid, errors=errors)
