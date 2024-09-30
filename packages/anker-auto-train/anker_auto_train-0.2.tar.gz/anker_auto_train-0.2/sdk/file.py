from pathlib import Path

import requests
from typing import Dict, Any
from pydantic import BaseModel, Field

class UploadfileResponse(BaseModel):
    url: str = Field(..., description="上传文件链接")
    bucket: str = Field(..., description="桶名")
    object_name: str = Field(..., description="文件名")
    storage_id: str = Field(..., description="存储id")


class AutoTrainSDK:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_presigned_upload_url(self, directory: str, file_name: str) -> Dict[str, Any]:
        url = f"{self.base_url}/get_upload_url"
        params = {
            "directory": directory,
            "file_name": file_name
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def upload_file(self, presigned_url: str, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.put(presigned_url, files=files)
            response.raise_for_status()
        return file_path

    def upload_file_to_directory(self, directory: str, file_path: str) -> int:
        file_name = Path(file_path).name
        presigned_data = self.get_presigned_upload_url(directory, file_name)
        presigned_url = presigned_data['url']
        self.upload_file(presigned_url, file_path)
        return UploadfileResponse(**presigned_data)

    def get_presigned_download_url(self, storage_id: str, bucket: str, object_name: str) -> Dict[str, Any]:
        url = f"{self.base_url}/get_download_url"
        params = {
            "storage_id": storage_id,
            "bucket": bucket,
            "object_name": object_name
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def download_file(self, storage_id: str, bucket: str, object_name: str, file_path: str) -> str:
        url = self.get_presigned_download_url(storage_id, bucket, object_name)['url']
        response = requests.get(url)
        response.raise_for_status()
        # 判断路径是否存在
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path