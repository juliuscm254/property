from odoo import fields, models


class Site(models.Model):
    _name = "site.site"  # Descriptive name
    _description = "Grouping of multiple buildings and lands"

    # Unique identifier (consider using a sequence)
    site_id = fields.Char(
        string="Site ID",
        required=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("site.site"),
        help="Unique identifier for the site. This can be generated automatically using a sequence or defined manually.",
    )

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the site. This can be a descriptive name, e.g., Headquarters, Production Facility, etc.",
    )

    site_code = fields.Char(
        string="Site Code",
        help="Optional user-specific Site Code for internal reference.",
    )

    # Selection field for site type (if there are predefined options)
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
        help="The type of site, e.g., Office, Factory, Warehouse, etc.",
    )

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        help="The date from which the site record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="The date until which the site record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    status = fields.Char(
        string="Status",
        help="Optional field to describe the current status of the site.",
    )
