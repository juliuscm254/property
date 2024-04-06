from odoo import fields, models


class Valuation(models.Model):
    _name = "valuation.valuation"  # Descriptive name
    _description = "Valuation"

    # Unique identifier (consider using a sequence)
    valuation_id = fields.Char(
        string="ID",
        required=True,
        default=lambda self: self.env["ir.sequence"].next_by_code(
            "valuation.valuation"
        ),
        help="Unique identifier for this valuation.",
    )

    previous_valuation_id = fields.Char(
        string="Previous Valuation ID",
        help="Unique identifier of the previous valuation (if applicable).",
    )

    name = fields.Char(string="Name", required=True, help="Name of the valuation.")

    type = fields.Selection(
        string="Type", selection=[], help="Select the type of valuation."
    )  # Replace with relevant options

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Date the valuation is valid from (yyyy-mm-dd hh:mm:ss).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        help="Date the valuation needs to be redone (yyyy-mm-dd hh:mm:ss).",
    )

    description = fields.Text(
        string="Description",
        help="Optional description of the valuation implementation.",
    )

    text = fields.Text(string="Text", help="Additional text field (optional).")

    keywords = fields.Char(
        string="Keywords", help="Comma-separated list of important keywords (optional)."
    )

    url = fields.Char(
        string="URL", help="External URL related to the valuation (optional)."
    )

    jurisdiction_type = fields.Selection(
        string="Jurisdiction Type",
        selection=[],
        help="Select the type of jurisdiction (optional).",
    )  # Replace with relevant options

    professional_standard = fields.Char(
        string="Professional Standard",
        help="Name of the professional valuation standard used (optional).",
    )

    accounting_standard = fields.Char(
        string="Accounting Standard",
        help="Name of the accounting standard used (optional).",
    )

    jurisdiction_standard = fields.Char(
        string="Jurisdiction Standard",
        help="Name of the jurisdiction type used (optional).",
    )

    value = fields.Float(
        string="Value", required=True, digits=(28, 4), help="Value of the valuation."
    )

    unit_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        required=True,
        ondelete="restrict",
        help="Unit of measurement associated with the valuation value.",
    )

    assumptions = fields.Text(
        string="Assumptions", help="Concluded assumptions for the valuation (optional)."
    )

    special_assumptions = fields.Text(
        string="Special Assumptions",
        help="Concluded special assumptions for the valuation (optional).",
    )

    constrains = fields.Text(
        string="Constrains",
        help="Existing constrains related to the valuation (optional).",
    )

    approach = fields.Selection(
        string="Valuation Approach",
        selection=[],
        help="Select the valuation approach used (optional).",
    )  # Replace with relevant options

    maintenance_backlog = fields.Boolean(
        string="Maintenance Backlog",
        default=False,
        help="Does a maintenance backlog exist (Y/N)?",
    )

    single_tenant = fields.Boolean(
        string="Single Tenant Building",
        default=False,
        help="Valuation of a single tenant building (Y/N)?",
    )

    discount_rate = fields.Float(
        string="Discount Rate",
        help="Discount rate included in the valuation (optional).",
        digits=(19, 6),
    )

    discount_premiums = fields.Float(
        string="Discount Premiums",
        help="Discount premiums included in the valuation (optional).",
        digits=(19, 6),
    )

    uncertainty = fields.Char(
        string="Uncertainty", help="LoV (Level of Variance) for uncertainty (optional)."
    )

    liquidity = fields.Float(
        string="Liquidity", help="Amount of cash (optional).", digits=(28, 4)
    )

    space_efficiency = fields.Char(
        string="Space Efficiency", help="Space usage efficiency (optional)."
    )

    energy_efficiency = fields.Selection(
        string="Energy Efficiency",
        selection=[],
        help="Energy efficiency class (optional).",
    )  # Replace with relevant options

    document_id = fields.Char(
        string="Document ID",
        help="Unique identifier of a related document (if applicable).",
    )
