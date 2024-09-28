# -*- coding: utf-8 -*-
from odoo import models, fields, api


class cs_battery_size(models.Model):
    _name = 'fleet.vehicle.battery.size'
    _rec_name = "battery_size"

    _sql_constraints = [
        (
            'unique_battery_size',
            'unique(battery_size)',
            'Battery Size must be unique'
        ),
    ]

    battery_size = fields.Integer(
        string='Size',
        required=True,
        index=True
    )
