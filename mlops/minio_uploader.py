import os
from dvc.repo import Repo
from minio import Minio
from minio.error import S3Error

minio_client = Minio(
    endpoint="minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

bucket_name = "data"

try:
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
except S3Error as e:
    print(f"Ошибка при создании бакета: {e}")


def upload_to_minio(data: dict, filename: str):
    """
    Сохраняет данные локально, добавляет в DVC и отправляет в MinIO.
    
    Args:
        data (dict): Данные для сохранения.
        filename (str): Название файла.
        
    Returns:
        str: Путь к загруженному файлу в MinIO.
    """
    local_path = f"./{bucket_name}/{filename}"
    os.makedirs(f"./{bucket_name}", exist_ok=True)
    
    with open(local_path, "w") as f:
        f.write(str(data))

    if not os.path.exists('.dvc'):
        repo = Repo.init()

    repo = Repo()
    repo.add(local_path)
    repo.push(targets=[local_path])

    
    #minio_client.fput_object(bucket_name, filename, local_path)

    return f"s3://{bucket_name}/{filename}"