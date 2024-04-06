from odoo import fields, models


class ValuationOperationalMeasurement(models.Model):
    _name = "valuation.operational.measurement"  # Descriptive name
    _description = "Valuation Operational Measurement Link"

    valuation_id = fields.Many2one(
        comodel_name="valuation.valuation",
        string="Valuation",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the valuation this measurement is associated with.",
    )

    operational_measurement_id = fields.Many2one(
        comodel_name="operational.measurement",
        string="Operational Measurement",
        required=True,
        ondelete="restrict",
        help="Globally unique identifier (GUID) of the operational measurement considered in this valuation.",
    )

    # Optional additional fields for the relationship (e.g., weighting factor, specific details)
    # ...
