import os
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from pipelines import (
    standardize_docling,
    # standardize_markitdown,
    # html_to_md_docling,
    get_job_name,
    # pdf_to_md_docling,
    clean_temp_files
)

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Welcome to the PDF/URL Parser API!"}
#
# @app.post("/processurl/", status_code=status.HTTP_200_OK)
# async def process_url(request: URLRequest):
#     clean_temp_files()
#     try:
#         url = request.url
#         job_name = get_job_name()
#         markdown_output = html_to_md_docling(url, job_name)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     return FileResponse(markdown_output, media_type='application/octet-stream',filename=f'{job_name}.md')
#
#
# @app.post("/processpdf/", status_code=status.HTTP_200_OK)
# async def process_pdf(file: UploadFile):
#     if file.content_type != 'application/pdf':
#         raise HTTPException(status_code=400, detail="File must be a PDF")
#     clean_temp_files()
#     contents = await file.read()
#     output = Path("./temp_processing/output/pdf")
#     os.makedirs(output, exist_ok=True)
#     job_name = get_job_name()
#     try:
#         file_path = output / f'{job_name}.pdf'
#         with open(file_path, 'wb') as f:
#             f.write(contents)
#             await file.close()
#         markdown_output = pdf_to_md_docling(file_path, job_name)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         await file.close()
#     return FileResponse(markdown_output, media_type='application/octet-stream', filename=f'{file.filename}.md')
#
#
@app.post('/standardizedocling/', status_code=status.HTTP_200_OK)
async def standardizedocling(file: UploadFile, background_tasks: BackgroundTasks):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    background_tasks.add_task(my_background_task)
    contents = await file.read()
    output = Path("./temp_processing/output/pdf")
    os.makedirs(output, exist_ok=True)
    job_name = get_job_name()
    try:
        file_path = output / f'{job_name}.pdf'
        with open(file_path, 'wb') as f:
            f.write(contents)
            await file.close()
        standardized_output = standardize_docling(file_path, job_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()
    return FileResponse(standardized_output, media_type='application/octet-stream', filename=f'{file.filename}.md')

#
# @app.post('/standardizemarkitdown/', status_code=status.HTTP_200_OK)
# async def standardizemarkitdown(file: UploadFile, background_tasks: BackgroundTasks):
#     if file.content_type != 'application/pdf':
#         raise HTTPException(status_code=400, detail="File must be a PDF")
#     background_tasks.add_task(my_background_task)
#     contents = await file.read()
#     output = Path("./temp_processing/output/pdf")
#     os.makedirs(output, exist_ok=True)
#     job_name = get_job_name()
#     try:
#         file_path = output / f'{job_name}.pdf'
#         with open(file_path, 'wb') as f:
#             f.write(contents)
#             await file.close()
#         standardized_output = standardize_markitdown(file_path, job_name)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         await file.close()
#     return FileResponse(standardized_output, media_type='application/octet-stream', filename=f'{file.filename}.md')

def my_background_task():
    clean_temp_files()
    print("Performed cleanup of temp files.")