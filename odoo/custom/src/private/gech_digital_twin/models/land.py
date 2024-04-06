from odoo import fields, models


class Land(models.Model):
    _name = "land.land"  # Descriptive name
    _description = "Land Management"

    # Unique identifier (consider using a sequence)
    # land_id = fields.Char(string='Land ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('land.land'), help="Unique identifier for the land parcel. This can be generated automatically using a sequence or defined manually.")

    # Many2one field referencing the Site model (if applicable)
    site_id = fields.Many2one(
        comodel_name="site.site",
        string="Site",
        help="Reference to the Site which the land belongs to (if applicable).",
    )

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the land parcel. This can be a descriptive name, e.g., Park, Garden, Parking Lot.",
    )

    land_code = fields.Char(
        string="Land Code",
        help="Optional user-specific Land Code for internal reference.",
    )

    # Selection field for land type (if there are predefined options)
    type = fields.Selection(
        string="Type",
        required=True,
        help="The type of land, e.g., Green Area, Building Plot, etc.",
    )

    land_coverage = fields.Char(
        string="Land Coverage",
        help="Optional field to describe the development level of the land (developed, undeveloped, etc.)",
    )

    land_parcel_nr = fields.Char(
        string="Land Parcel Number",
        help="District/Zoning number registered for the plot of land.",
    )

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        help="The date from which the land record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="The date until which the land record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    # Selection field for type of ownership (if there are predefined options)
    type_of_ownership = fields.Selection(
        string="Ownership Type",
        required=True,
        selection=[("owned", "Own"), ("leased", "Lease"), ("other", "Other")],
        default="owned",
        help="Indicates whether the building is owned or leased.",
    )

    self_use = fields.Boolean(
        string="Self Use",
        help="Indicates whether the land is used by the company itself (Y/N).",
    )

    status = fields.Char(
        string="Status",
        help="Optional field to describe the current status of the land.",
    )
