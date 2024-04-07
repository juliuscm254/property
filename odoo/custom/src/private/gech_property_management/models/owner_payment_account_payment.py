from odoo import fields, models


class RentalUnitBuilding(models.Model):
    _name = "rental.unit.building"  # Descriptive name
    _description = "Rental Unit - Building Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_building_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.building'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the Building model
    building_id = fields.Many2one(
        comodel_name="building.building",
        string="Building",
        required=True,
        ondelete="cascade",
    )

    # Additional fields (consider if needed)
    # Example: primary_usage = fields.Char(string='Primary Usage')  # If a unit has different uses in different buildings
