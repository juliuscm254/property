from odoo import fields, models


class Floor(models.Model):
    _name = "floor.floor"  # Descriptive name
    _description = "Building Floor Management"

    # Unique identifier (consider using a sequence)
    # floor_id = fields.Char(string='Floor ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('floor.floor'), help="Unique identifier for the floor. This can be generated automatically using a sequence or defined manually.")

    # Many2one field referencing the Building model
    building_id = fields.Many2one(
        comodel_name="building.building",
        string="Building",
        required=True,
        ondelete="cascade",
        help="Reference to the Building which the Floor belongs to.",
    )

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the floor. This can be a descriptive name, e.g., Ground Floor, Floor 1, etc.",
    )

    floor_code = fields.Char(
        string="Floor Code",
        help="Optional user-specific Floor Code for internal reference.",
    )

    floor_number = fields.Integer(
        string="Floor Number",
        required=True,
        help="The floor number within the building.",
    )

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        help="The date from which the floor record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="The date until which the floor record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )
