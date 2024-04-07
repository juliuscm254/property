from odoo import fields, models


class ValuationBuilding(models.Model):
    _name = "valuation.building"  # Descriptive name
    _description = "Valuation Building Link"

    valuation_id = fields.Many2one(
        comodel_name="valuation.valuation",
        string="Valuation",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the valuation this building is associated with.",
    )

    building_id = fields.Many2one(
        comodel_name="building.building",
        string="Building",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the building included in this valuation.",
    )

    # Optional additional fields for the relationship (e.g., valuation share, specific details)
    # ...
