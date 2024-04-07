from odoo import fields, models


class OperationalMeasurementRentalUnit(models.Model):
    _name = "operational.measurement.rental.unit"  # Descriptive name
    _description = "Operational Measurement Rental Unit Link"

    operational_measurement_id = fields.Many2one(
        comodel_name="operational.measurement",
        string="Operational Measurement",
        required=True,
        ondelete="restrict",
        help="Globally unique identifier (GUID) of the operational measurement associated with the rental unit.",
    )

    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the rental unit this operational measurement applies to.",
    )

    # Optional additional fields for the relationship (e.g., allocation percentage)
    # ...
