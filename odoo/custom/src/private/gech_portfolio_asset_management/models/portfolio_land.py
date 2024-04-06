from odoo import fields, models


class PortfolioBuilding(models.Model):
    _name = "portfolio.land"  # Descriptive name (consider 'portfolio_building')
    _description = "Portfolio Land Link"

    portfolio_id = fields.Many2one(
        comodel_name="portfolio.portfolio",
        string="Portfolio",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the portfolio this building belongs to.",
    )

    land_id = fields.Many2one(
        comodel_name="land.land",
        string="Land",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the land associated with this portfolio.",
    )

    # Optional additional fields for the relationship (e.g., investment share, ownership details)
    # ...
