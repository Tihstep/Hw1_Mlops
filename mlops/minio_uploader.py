import os
from dvc.repo import Repo
from minio import Minio
from minio.error import S3Error

class Minio_client:
    def __init__(self, bucket_name="data"):
        self.minio_client = Minio(
            endpoint="minio:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False,
        )
        self.bucket_name = bucket_name
        
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Ошибка при создании бакета: {e}")


    def upload_to_minio(self, data: dict, filename: str):
        """
        Сохраняет данные локально, добавляет в DVC и отправляет в MinIO.
        
        Args:
            data (dict): Данные для сохранения.
            filename (str): Название файла.
            
        Returns:
            str: Путь к загруженному файлу в MinIO.
        """
        local_path = f"./{self.bucket_name}/{filename}"
        os.makedirs(f"./{self.bucket_name}", exist_ok=True)
        
        with open(local_path, "w") as f:
            f.write(str(data))

        if not os.path.exists('.dvc'):
            repo = Repo.init()

        repo = Repo()
        repo.add(local_path)
        repo.push(targets=[local_path])

        return f"s3://{self.bucket_name}/{filename}"