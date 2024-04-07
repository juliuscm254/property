from odoo import fields, models


class PortfolioStrategy(models.Model):
    _name = "portfolio.strategy"  # Descriptive name
    _description = "Portfolio Strategy"

    # Unique identifier (consider using a sequence)
    portfolio_strategy_id = fields.Char(
        string="ID",
        required=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("portfolio.strategy"),
        help="Unique identifier for this portfolio strategy.",
    )

    portfolio_id = fields.Many2one(
        comodel_name="portfolio.portfolio",
        string="Portfolio",
        required=True,
        ondelete="restrict",
        help="The portfolio this strategy applies to.",
    )

    name = fields.Char(
        string="Name", required=True, help="Name of the portfolio strategy."
    )

    investment_type = fields.Selection(
        string="Investment Type",
        selection=[],
        help="Select the type of investment strategy.",
    )  # Replace with relevant options

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Date the strategy was implemented (yyyy-mm-dd hh:mm:ss).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        help="Date the strategy needs to be adapted (yyyy-mm-dd hh:mm:ss).",
    )

    # Steering Targets

    strategy_objective_targets_steering = fields.Char(
        string="Steering Target Type",
        help="Steering target type of the portfolio strategy.",
    )
    strategy_objective_values_steering = fields.Float(
        string="Steering Target Value",
        digits=(28, 4),
        help="Target value of the portfolio strategy steering.",
    )
    strategy_objective_unit_steering = fields.Char(
        string="Steering Target Unit",
        help="Unit of the strategy objective steering value.",
    )

    # Target Values

    strategy_objective_targets = fields.Char(
        string="Target Type", help="Target type of the portfolio strategy."
    )
    strategy_objective_values = fields.Float(
        string="Target Value",
        digits=(28, 4),
        help="Target value of the portfolio strategy.",
    )
    strategy_objective_unit = fields.Char(
        string="Target Unit", help="Unit of the strategy objective value."
    )

    source = fields.Char(string="Source", help="Source of the portfolio strategy.")
