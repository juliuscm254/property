from odoo import api, fields, models


class Portfolio(models.Model):
    _name = "portfolio.portfolio"  # Descriptive name
    _description = "Grouping of real estate assets"

    PORTFOLIO_TYPE = [
        ("opening_control", "Opening Control"),  # method action_pos_session_open
        ("opened", "In Progress"),  # method action_pos_session_closing_control
        ("closing_control", "Closing Control"),  # method action_pos_session_close
        ("closed", "Closed & Posted"),
    ]

    # Unique identifier (consider using a sequence)
    # portfolio_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('portfolio.portfolio.manual'),
    #                            help="Unique identifier for this portfolio.")
    portfolio_id = fields.Char(
        string="ID",
        required=True,
        default=lambda self: self._get_next_portfolio_id(),
        help="Unique identifier for this portfolio.",
    )

    # Name of the portfolio
    name = fields.Char(string="Name", required=True, help="Name of the portfolio.")

    # User-specific portfolio code (optional)
    portfolio_code = fields.Char(
        string="Portfolio Code",
        help="Optional user-specific code for the portfolio (e.g., MR003).",
    )

    type = fields.Selection(
        PORTFOLIO_TYPE,
        string="Type",
        required=True,
        default="opening_control",
        help="Select the type of portfolio.",
    )

    # Type of the portfolio
    type = fields.Selection(
        string="Type", required=True, selection=[], help="Select the type of portfolio."
    )  # Replace with relevant options

    # Asset category (optional)
    asset_category = fields.Char(
        string="Asset Category",
        help="Optional field to describe the asset category of the portfolio.",
    )

    # Ownership type (optional)
    ownership_type = fields.Char(
        string="Ownership Type",
        help="Optional field to describe the ownership structure of the portfolio.",
    )

    # Valid from date (required)
    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Date the portfolio was set up (yyyy-mm-dd hh:mm:ss).",
    )

    # Valid until date (optional)
    valid_until = fields.Datetime(
        string="Valid Until",
        help="Optional date the portfolio's maturity is reached (yyyy-mm-dd hh:mm:ss).",
    )

    # Primary usage type (optional)
    primary_usage_type = fields.Char(
        string="Primary Usage Type",
        help="Optional definition of the primary usage type/asset class of the portfolio.",
    )

    # Secondary usage type (optional)
    secondary_usage_type = fields.Char(
        string="Secondary Usage Type",
        help="Optional definition of the secondary usage type/asset class of the portfolio.",
    )

    # Market value (optional)
    market_value = fields.Float(
        string="Market Value",
        digits=(28, 4),
        help="Optional field for the current market value of the portfolio.",
    )

    # Main currency (optional)
    currency = fields.Char(
        string="Currency",
        help="Optional field for the main/default currency of the portfolio.",
    )

    # Reporting date (optional)
    reporting_date = fields.Datetime(
        string="Reporting Date", help="Optional reporting date (yyyy-mm-dd hh:mm:ss)."
    )

    # Reporting cycle (optional)
    reporting_cycle = fields.Selection(
        string="Reporting Cycle",
        selection=[],
        help="Optional selection for the reporting cycle (used to determine next reporting date).",
    )  # Replace with relevant options

    @api.model  # Decorator to define a model method
    def _get_next_portfolio_id(self):
        # Define the prefix for your portfolio ID pattern (PF-)
        prefix = "PF-"
        # Get the next sequence number for the 'portfolio.portfolio' sequence
        sequence_value = self.env["ir.sequence"].next_by_code("portfolio.portfolio")
        # Format the sequence number with leading zeros (01, 02, 03, etc.)
        sequence_str = str(sequence_value).zfill(2)
        # Combine prefix and sequence number to form the portfolio ID
        return prefix + sequence_str

    @api.model_create
    def create(self, vals):
        vals = vals.copy()
        if not vals.get("portfolio_id"):
            vals["portfolio_id"] = self._get_next_portfolio_id()
        return super(Portfolio, self).create(vals)
