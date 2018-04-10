from flask import Blueprint, render_template
from flask_builder import db
from .models import Chart, Point
from lib.utils import ujsonify


mod = Blueprint('charts', __name__, url_prefix='/charts')


@mod.route('/')
def list_view():
    return render_template('chart.html')


@mod.route('/', methods=['POST'])
def add_chart_view(chart_name):
    chart = Chart(name=chart_name)
    db.session.add(chart)
    db.session.commit()
    return ujsonify(**chart.to_dict())


@mod.route('/', methods=['POST'])
def add_point_view(point_x, point_y, point_chart=None):
    if point_chart:
        chart = Chart(name=point_chart)
        db.session.add(chart)
        point = Point(
            x_coord=point_x,
            y_coord=point_y,
        )
        db.session.add(point)
        db.session.commit()
    else:
        point = Point(
            x_coord=point_x,
            y_coord=point_y
        )
        db.session.add(point)
        db.session.commit()

    return ujsonify(**point.to_dict())


@mod.route('/<int:chart_id>', methods=['PUT'])
def update_view(chart_id):
    pass


@mod.route('/<int:chart_id>', methods=['DELETE'])
def delete_view(chart_id):
    pass


@mod.route('/<int:chart_id>')
def one_view():
    pass
