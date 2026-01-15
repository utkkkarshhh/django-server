from django.db import models
from django.db.models.base import ModelBase


class BaseModelMeta(ModelBase):
    def __new__(cls, name, bases, attrs):
        model = super().__new__(cls, name, bases, attrs)
        if not model._meta.abstract:
            fields = model._meta.local_fields
            defined_fields = [f for f in fields if f.name not in ['created_at', 'updated_at']]
            timestamp_fields = [f for f in fields if f.name in ['created_at', 'updated_at']]
            timestamp_fields.sort(key=lambda x: ['created_at', 'updated_at'].index(x.name))
            
            model._meta.local_fields = defined_fields + timestamp_fields
            if hasattr(model._meta, '_expire_cache'):
                model._meta._expire_cache()
        return model


class BaseModel(models.Model, metaclass=BaseModelMeta):
    """
    Abstract base models to provide common fields and methods for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
