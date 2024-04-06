from odoo import fields, models


class Space(models.Model):
    _name = "space.space"  # Descriptive name
    _description = "A space represents an area or volume bounded actually or theoretically. Spaces are areas or volumes that provide for certain functions within a building"

    # Unique identifier (consider using a sequence)
    space_id = fields.Char(
        string="Space ID",
        required=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("space.space"),
        help="Unique identifier for the space. This can be generated automatically using a sequence or defined manually.",
    )

    # Many2one field referencing the Floor model
    floor_id = fields.Many2one(
        comodel_name="floor.floor",
        string="Floor",
        required=True,
        ondelete="cascade",
        help="Reference to the Floor which the space belongs to.",
    )

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the space. This can be a descriptive name, e.g., Office 101, Meeting Room A.",
    )

    space_code = fields.Char(
        string="Space Code",
        help="Optional user-specific Space Code for internal reference.",
    )

    space_number = fields.Float(
        string="Space Number",
        help="Optional space number for additional identification.",
    )

    # Selection field for space type (if there are predefined options)
    type = fields.Selection(
        string="Type",
        required=True,
        selection=[
            ("office", "Office"),
            ("factory", "Factory"),
            ("warehouse", "Warehouse"),
            ("residential", "Residential"),
            ("other", "Other"),
        ],
        default="residential",
        help="The type of space, e.g., Office, Meeting Room, Storage Room, etc.",
    )

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        help="The date from which the space record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="The date until which the space record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    space_height_usable = fields.Float(
        string="Usable Height",
        help="The usable height of the space, excluding any features that may obstruct movement or use.",
    )

    space_height = fields.Float(
        string="Actual Height",
        help="The actual height of the space from floor to ceiling.",
    )

    space_volume_gross = fields.Float(
        string="Gross Volume",
        help="The gross volume of the space, including the volume of surrounding walls.",
    )

    space_volume_net = fields.Float(
        string="Net Volume",
        help="The net volume of the space, excluding the volume of surrounding walls.",
    )

    primary_floor_material = fields.Char(
        string="Primary Floor Material",
        help="The primary material used for the floor in the space.",
    )

    primary_wall_material = fields.Char(
        string="Primary Wall Material",
        help="The primary material used for the walls in the space.",
    )

    primary_ceiling_material = fields.Char(
        string="Primary Ceiling Material",
        help="The primary material used for the ceiling in the space.",
    )

    rentable = fields.Boolean(
        string="Rentable",
        help="Indicates whether the space is available for rent (Y/N).",
    )

    effect_zones_heating = fields.Float(
        string="Heated Area", help="The area within the space that is actively heated."
    )

    effect_zones_cooling = fields.Float(
        string="Cooled Area", help="The area within the space that is actively cooled."
    )

    effect_zones_ventilation = fields.Float(
        string="Ventilated Area",
        help="The area within the space that is actively ventilated.",
    )

    climate_heated = fields.Boolean(
        string="Climate Heated",
        help="Indicates whether the space has a heating system (Y/N).",
    )

    climate_cooled = fields.Boolean(
        string="Climate Cooled",
        help="Indicates whether the space has a cooling system (Y/N).",
    )

    co_use_area = fields.Boolean(
        string="Co-Use Area",
        help="Indicates whether the space is used by multiple tenants (Y/N).",
    )

    maximum_occupancy = fields.Integer(
        string="Maximum Occupancy",
        help="The maximum number of people allowed to occupy the space safely.",
    )

    ventilation_type = fields.Char(
        string="Ventilation Type",
        help="The type of ventilation system used in the space, e.g., exhaust, supply, balanced, or heat-recovery.",
    )
