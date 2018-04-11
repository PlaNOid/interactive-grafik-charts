from flask import Blueprint, render_template, url_for, redirect
from flask_builder import db
from .models import Chart, Point
from lib.utils import ujsonify, dataschema
from voluptuous import Schema, Optional, Required
from psycopg2 import IntegrityError
from datetime import datetime
import pytz


mod = Blueprint('charts', __name__, url_prefix='/charts')


@mod.route('/')
def list_view():
    c = Chart.query
    total = c.count()
    return ujsonify(result=[b.to_dict() for b in c], total=total)


@mod.route('/', methods=['POST'])
@dataschema(Schema({
    Required('chart_name'): str,
    Optional('chart_legend'): str,
    Optional('fmt'): str,
    Optional('point_x'): str,
    Optional('point_y'): str,
}))
def add_view(chart_name, fmt='%d-%m-%Y %H:%M', chart_legend='', point_y=None):
    if point_y:
        c = Chart.query.filter_by(name=chart_name).one()
        point_x = datetime.now(pytz.timezone("Europe/Moscow")).strftime(c.date_format)
        p = Point(chart_id=c.id, x_coord=point_x, y_coord=point_y)
        db.session.add(p)
        db.session.commit()
    else:
        c = Chart(name=chart_name, legend=chart_legend, date_format=fmt)
        db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'this chart name is already exist'
    return redirect('/charts/show/'+str(c.id))


@mod.route('/point/', methods=['POST'])
@dataschema(Schema({
    Required('point_id'): str,
    Required('point_y'): str,
}))
def update_view(point_id, point_y):
    point_id = int(point_id)
    p = Point.query.filter_by(id=point_id).first_or_404()
    p.y_coord = point_y
    db.session.add(p)
    db.session.commit()
    return redirect('/charts/show/'+str(p.chart_id))


@mod.route('/<int:chart_id>', methods=['POST'])
def delete_view(chart_id):
    c = Chart.query.filter_by(id=chart_id).first_or_404()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('root.root_view'))


@mod.route('/show/<int:chart_id>')
def build_view(chart_id):
    c = Chart.query.filter_by(id=chart_id).first_or_404()
    points = c.points
    x_coord = []
    y_coord = []
    point_ids = []
    for p in points:
        x_coord.append(p.x_coord)
        y_coord.append(p.y_coord)
        point_ids.append(p.id)
    coord_dict = dict(zip(x_coord, y_coord))
    points_list = list(zip(point_ids, x_coord, y_coord))
    return render_template(
        'chart.html',
        labels=x_coord,
        values=y_coord,
        chart_name=c.name,
        legend=c.legend,
        points=coord_dict,
        points_list=points_list,
        chart_id=c.id
    )
