from datetime import datetime

from sqlalchemy import Index

from app import db


class PropertyPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer,
                            db.ForeignKey('property.id',
                                          ondelete='CASCADE'),
                            nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    is_best = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    __table_args__ = (
        Index('ix_property_photo_property_id_is_best', property_id, is_best,
              unique=True,
              postgresql_where=is_best),
        Index('ix_property_photo_property_id', 'property_id'),
    )
