from odoo import api, fields, models


class ValuationAccount(models.Model):
    _name = "valuation.account"  # Descriptive name
    _description = "Valuation Account Link"

    valuation_id = fields.Many2one(
        comodel_name="valuation.valuation",
        string="Valuation",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the valuation this account is associated with.",
    )

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        ondelete="restrict",
        help="Unique identifier of the account considered in this valuation.",
    )

    # Optional additional fields for the relationship
    # ...

    # Leverage Odoo account features (consider these examples)
    debit = fields.Float(
        string="Debit",
        help="Debit amount associated with this account in the valuation.",
    )
    credit = fields.Float(
        string="Credit",
        help="Credit amount associated with this account in the valuation.",
    )
    balance = fields.Float(
        string="Balance",
        compute="_compute_balance",
        store=True,
        help="Calculated balance (debit - credit).",
    )

    @api.depends("debit", "credit")
    def _compute_balance(self):
        for record in self:
            record.balance = record.debit - record.credit
