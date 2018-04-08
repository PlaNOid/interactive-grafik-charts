from flask import Blueprint, render_template

mod = Blueprint('root', __name__)


@mod.route('/')
def root_view():
    return render_template('base.html')


@mod.route('/simple_chart')
def chart():
    legend = 'Monthly Data'
    labels = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август']
    values = [1, 5, 6, 4, 7, 8, 3, 15]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

