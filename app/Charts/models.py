from sqlalchemy_serializer import SerializerMixin
from flask_builder import db
from datetime import datetime


class Chart(db.Model, SerializerMixin):
    __table_name__ = 'charts'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    points = db.relationship('Point')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Point(db.Model, SerializerMixin):
    __table_name__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'))

    x_coord = db.Column(db.Integer, nullable=False)
    y_coord = db.Column(db.Integer, nullable=False)

