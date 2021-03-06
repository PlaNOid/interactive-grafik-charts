from flask import Blueprint, render_template
from flask_builder import db
from app.charts.models import Chart


mod = Blueprint('root', __name__)


@mod.route('/')
def root_view():
    c = Chart.query
    return render_template('base.html', charts=c)


@mod.route('/simple_chart')
def chart():
    legend = 'Monthly Data'
    labels = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август']
    values = [1, 5, 6, 4, 7, 8, 3, 15]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

