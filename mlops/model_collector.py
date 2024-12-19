import os
from minio.error import S3Error
import pickle
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ModelCollector:
    def __init__(self, minio_client, bucket_name):
        """
        Args:
            minio_client: Minio клиент.
            bucket_name: Имя MinIO бакета.
            models: Словарь хранящихся моделей и их послежних версий 
        """
        self.minio_client = minio_client
        self.bucket_name = bucket_name
        self._models = {}
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if self.minio_client.bucket_exists(self.bucket_name):
            objects = self.minio_client.list_objects(self.bucket_name, recursive=True)
            for obj in objects:
                data = self.minio_client.get_object(obj.bucket_name, obj.object_name)
                object_data = data.data
                self._models[obj.object_name] = object_data
        else:
            self.minio_client.make_bucket(self.bucket_name)
            self._models = {}

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, value):
        if not isinstance(value, dict):
            raise TypeError("Models must be a dictionary")
        self._models = value

    def add_model(self, model_id, model_path):
        """Add or update a model in MinIO with versioning."""
        self.minio_client.fput_object(self.bucket_name, model_id, model_path)
        print(f"Uploaded {model_path} to {self.bucket_name}/{model_id}")

        with open(model_path,'rb') as f:
            model = pickle.load(f)
        self._models[model_id] = model

    def get_model(self, model_id, model_path):
        "Download model from MinIO."

        try:
            if model_id in self._models:
                os.makedirs("./models/", exist_ok=True)
                with open(model_path,'wb') as f:
                    pickle.dump(self._models[model_id],f)
                    return model_path
            self.minio_client.fget_object(self.bucket_name, model_id, model_path)
            print(f"Downloaded {self.bucket_name}/{model_id} to {model_path}")
            return model_path
        except S3Error as e:
            raise ValueError(f"Failed to fetch model: {e}")
    
    def delete_model(self, model_id):
        "Delete model"

        try:
            # Тут можно удалять из minio, но будем считать 
            # что с моделями у нас логика insert only
            #model_collector.minio_client.remove_object(model_collector.bucket_name, model_id)
            logger.info(f"Model {model_id} deleted from MinIO.")
        except Exception as e:
            logger.error(f"Failed to delete model {model_id} from MinIO: {e}")
            raise NameError(f"Failed to delete model: {e}")



