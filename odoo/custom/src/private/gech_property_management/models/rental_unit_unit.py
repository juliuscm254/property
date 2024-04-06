from odoo import fields, models


class RentalUnitUom(models.Model):
    _name = "rental.unit.uom"  # Descriptive name
    _description = "Rental Unit - Unit of Measure Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_uom_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.uom'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the 'uom.uom' model
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        required=True,
        ondelete="restrict",
    )

    # Optional fields for additional data (consider if needed)
    # Example: default_uom_factor = fields.Float(string='Default Conversion Factor')

    # You can add constraints or validations on the UoM selection based on your use case
