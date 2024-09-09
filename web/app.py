from flask import Flask, jsonify, request
from ingreedypy import Ingreedy
from pint import UnitRegistry

app = Flask(__name__)
pint = UnitRegistry()


def normalize_unit(language_code, unit):
    return unit, 1


def parse_quantity(language_code, description):
    total = 0
    quantities = Ingreedy().parse(description)["quantity"]
    for quantity in quantities:
        unit, amount = quantity["unit"], quantity["amount"]
        normalized_unit, conversion_factor = normalize_unit(language_code, unit)
        normalized_amount = amount * conversion_factor
        total += pint.Quantity(normalized_amount, normalized_unit)

    base_units = get_base_units(total) or total.units
    total = total.to(base_units)
    magnitude = round(total.magnitude, 2)
    units = None if total.dimensionless else pint.get_symbol(str(total.units))
    return magnitude, units


def get_base_units(quantity):
    dimensionalities = {
        None: pint.Quantity(1),
        "energy": pint.Quantity(1, "cal"),
        "length": pint.Quantity(1, "cm"),
        "volume": pint.Quantity(1, "ml"),
        "weight": pint.Quantity(1, "g"),
    }
    dimensionalities = {
        v.dimensionality: pint.get_symbol(str(v.units)) if k else None
        for k, v in dimensionalities.items()
    }
    return dimensionalities.get(quantity.dimensionality)


@app.route("/", methods=["POST"])
def root():
    language_code = request.form.get("language_code", type=str, default="en")
    descriptions = request.form.getlist("descriptions[]")
    descriptions = [d.strip() for d in descriptions]

    quantities = []
    for description in descriptions:
        magnitude, units = parse_quantity(language_code, description)
        quantities.append(
            {
                "magnitude": magnitude,
                "units": units,
            }
        )
    return jsonify(quantities)
