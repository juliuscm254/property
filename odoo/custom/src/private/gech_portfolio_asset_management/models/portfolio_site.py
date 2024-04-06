from odoo import fields, models


class PortfolioSite(models.Model):
    _name = "portfolio.site"  # Descriptive name
    _description = "Portfolio Site Link"

    portfolio_id = fields.Many2one(
        comodel_name="portfolio.portfolio",
        string="Portfolio",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the portfolio this site belongs to.",
    )

    site_id = fields.Many2one(
        comodel_name="site.site",
        string="Site",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the site associated with this portfolio.",
    )

    # Optional additional fields for the relationship (e.g., investment share, ownership details)
    # ...
