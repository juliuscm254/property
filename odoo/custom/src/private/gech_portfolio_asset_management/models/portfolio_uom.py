from odoo import fields, models


class PortfolioUom(models.Model):
    _name = "portfolio.uom"  # Descriptive name
    _description = "Portfolio Unit of Measure Link"

    portfolio_id = fields.Many2one(
        comodel_name="portfolio.portfolio",
        string="Portfolio",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the portfolio this unit applies to.",
    )

    unit_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        required=True,
        ondelete="restrict",
        help="Unit of measure associated with this portfolio.",
    )

    # Optional additional fields for the relationship (e.g., is_primary)
    is_primary = fields.Boolean(
        string="Is Primary",
        default=False,
        help="Indicates if this is the primary unit of measure for the portfolio.",
    )
