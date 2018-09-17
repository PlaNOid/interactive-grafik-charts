from flask_builder import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


class TsResponsible(db.Model, SerializerMixin):
    __tablename__ = 'ts_resposibles'

    id = db.Column(db.Integer, primary_key=True)

    id_ts = db.Column(db.Integer, db.ForeignKey('ts.id', ondelete='CASCADE'))
    associate_id = db.Column(db.Integer, db.ForeignKey('associates.id', ondelete='CASCADE'))
    parrent_id = db.Column(db.Integer, db.ForeignKey('ts_resposibles.id', ondelete='CASCADE'), nullable=True)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    is_delete = db.Column(db.Boolean, default=False)


class TS(db.Model, SerializerMixin):
    __tablename__ = 'ts'

    id = db.Column(db.Integer, primary_key=True)

    reg_num = db.Column(db.String(25))
    decomission_date = db.Column(db.DateTime)

    is_delete = db.Column(db.Boolean, default=False)


class Associate(db.Model, SerializerMixin):
    __tablename__ = 'associates'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    patronymic = db.Column(db.String(255))

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    is_delete = db.Column(db.Boolean, default=False)
