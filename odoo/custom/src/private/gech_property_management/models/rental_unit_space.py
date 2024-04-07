from odoo import fields, models


class RentalUnitSpace(models.Model):
    _name = "rental.unit.space"  # Descriptive name
    _description = "Rental Unit - Space Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_space_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.space'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the Space model
    space_id = fields.Many2one(
        comodel_name="space.space", string="Space", required=True, ondelete="cascade"
    )

    # Additional fields (consider if needed)
    # Example: primary_usage = fields.Char(string='Primary Usage')  # If a unit has different primary uses in different spaces
