---
date: 2024-04-16T10:22:56.793742
author: AutoGPT <info@agpt.co>
---

# aarushi-barcode-1

The project's objective is to develop a system that accepts product data such as SKU, UPC, EAN, etc., and generates barcode images in the specified formats which include EAN-13 and Code 128 due to their extensive usage in the retail and logistics sectors. Although the user initially inquired about customizing the size, color, and resolution of the barcodes, they stated no requirement for such customizations. Yet, information collected demonstrated the capability to customize barcodes using Python libraries, suggesting flexibility in the implementation if needed in the future.

The product data will be provided through structured data formats like JSON or CSV files, ensuring a seamless and error-free data transfer process for barcode generation. Python, with its rich ecosystem of libraries, will be leveraged for this development. The 'python-barcode' library is identified as suitable for generating the barcode images. Additionally, for instances where customization might be required, the 'Pillow' library could be used to adjust the size, color, and resolution of the generated barcode images. Instructions and examples were provided on installing necessary libraries, generating barcodes, customizing, and saving them as image files using Python.

This system plays a crucial role in various applications, streamlining operations and enhancing efficiency in product identification and logistics management. Its development within the specified tech stack, utilizing Python, FastAPI for API creation, PostgreSQL as the database, and Prisma as the ORM, will ensure a robust and scalable solution to meet the user's needs.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-barcode-1'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
