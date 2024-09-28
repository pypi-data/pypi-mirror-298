# -*- coding: utf-8 -*-
from odoo import models, fields, api


class cs_battery_maximum_charge(models.Model):
    _name = 'fleet.vehicle.battery.maximum.charge'
    _rec_name = "maximum_charge"

    _sql_constraints = [
        (
            'unique_maximum_charge',
            'unique(maximum_charge)',
            'Battery Maximum Charge must be unique'
        ),
    ]

    maximum_charge = fields.Float(
        string='Max Charge',
        required=True,
        index=True,
        digits=(16, 2)
    )
