from flask import Flask, jsonify, request
from ingreedypy import Ingreedy
from pint import UnitRegistry

app = Flask(__name__)
pint = UnitRegistry()


def parse_quantity(description):
    total = 0
    quantities = Ingreedy().parse(description)['quantity']
    for quantity in quantities:
        total += pint.Quantity(quantity['amount'], quantity['unit'])

    base_units = get_base_units(total) or total.units
    total = total.to(base_units)
    magnitude = round(total.magnitude, 2)
    units = None if total.dimensionless else pint.get_symbol(str(total.units))
    return magnitude, units


def get_base_units(quantity):
    dimensionalities = {
        None: pint.Quantity(1),
        'length': pint.Quantity(1, 'cm'),
        'volume': pint.Quantity(1, 'ml'),
        'weight': pint.Quantity(1, 'g'),
    }
    dimensionalities = {
        v.dimensionality: pint.get_symbol(str(v.units)) if k else None
        for k, v in dimensionalities.items()
    }
    return dimensionalities.get(quantity.dimensionality)


@app.route('/', methods=['POST'])
def root():
    descriptions = request.form.getlist('descriptions[]')
    descriptions = [d.strip() for d in descriptions]

    results = {}
    for description in descriptions:
        magnitude, units = parse_quantity(description)
        results[description] = {
            'magnitude': magnitude,
            'units': units,
        }
    return jsonify(results)
