from odoo import fields, models


class ValuationLand(models.Model):
    _name = "valuation.land"  # Descriptive name
    _description = "Valuation Land Link"

    valuation_id = fields.Many2one(
        comodel_name="valuation.valuation",
        string="Valuation",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the valuation this land is associated with.",
    )

    land_id = fields.Many2one(
        comodel_name="land.land",
        string="Land",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the land included in this valuation.",
    )

    # Optional additional fields for the relationship (e.g., land area, valuation share)
    # ...
