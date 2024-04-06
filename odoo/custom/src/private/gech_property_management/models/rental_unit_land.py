from odoo import fields, models


class RentalUnitLand(models.Model):
    _name = "rental.unit.land"  # Descriptive name
    _description = "Rental Unit - Land Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_land_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.land'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the Land model
    land_id = fields.Many2one(
        comodel_name="land.land", string="Land", required=True, ondelete="cascade"
    )

    # Additional fields (consider if needed)
    # Example: purpose = fields.Char(string='Purpose')  # If a unit has access to specific land for a reason (e.g., parking)
