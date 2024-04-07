from odoo import fields, models


class PortfolioBuilding(models.Model):
    _name = "portfolio.building"  # Descriptive name (consider 'portfolio_building')
    _description = "Portfolio Building Link"

    portfolio_id = fields.Many2one(
        comodel_name="portfolio.portfolio",
        string="Portfolio",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the portfolio this building belongs to.",
    )

    building_id = fields.Many2one(
        comodel_name="building.building",
        string="Building",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the building associated with this portfolio.",
    )

    # Optional additional fields for the relationship (e.g., investment share, ownership details)
    # ...
