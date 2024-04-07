from odoo import fields, models


class RentalUnitFloor(models.Model):
    _name = "rental.unit.floor"  # Descriptive name
    _description = "Rental Unit - Floor Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_floor_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.floor'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the Floor model
    floor_id = fields.Many2one(
        comodel_name="floor.floor", string="Floor", required=True, ondelete="cascade"
    )

    # Additional fields (consider if needed)
    # Example: primary_usage = fields.Char(string='Primary Usage')  # If a unit has different uses on different floors
