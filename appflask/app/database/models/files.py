from datetime import datetime
from pathlib import Path

from marshmallow import fields, ValidationError
from sqlalchemy import func

from app import db
from app.case_management.mixins import BaseMixin
from app.settings.models import BaseSchema


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime)


class DataMappers(db.Model, BaseMixin, TimestampMixin):
    __tablename__ = 'data_mappers'

    # the name of data mapper, for example 'petition'
    name = db.Column(db.String, primary_key=True)

    # mapped key-value columns
    fields = db.Column(db.JSON)

    # the name of petition data mapper
    PETITION = "petition"

    # required columns
    required_columns = ('apn',)

    def clean_fields(self):
        """
        Clean data mapper fields. Remove empty fields from data mapper.
        """
        mapper_fields = {}
        for k, v in self.fields.items():
            if v == '' or v is None:
                continue
            mapper_fields[k] = v

        return mapper_fields


class Files(db.Model, BaseMixin):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    extension = db.Column(db.String)

    @classmethod
    def create_from_file(cls, file):

        file_name = '_'.join([datetime.now().strftime("%H_%M_%S_%d_%m_%Y"), file.filename])
        new_file = FilesSchema().load(
            dict(
                name=file_name,
                data=file.read(),
                extension=Path(file.filename).suffix
            )
        )
        new_file.save()
        return new_file


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')


class FilesSchema(BaseSchema):
    class Meta:
        model = Files

    data = BytesField(allow_none=True)


class DataMapperSchema(BaseSchema):
    class Meta:
        model = DataMappers
