from odoo import fields, models


class TenantContractExpense(models.Model):
    _name = "tenant.contract.expense"
    _description = "Expense Line Items for Tenant Contracts"

    name = fields.Char(string="Expense Name", required=True)
    contract_id = fields.Many2one(
        comodel_name="tenant.contract",
        string="Contract",
        required=True,
        ondelete="cascade",
    )
    expense_type = fields.Selection(
        selection=[("percentage", "Percentage"), ("fixed", "Fixed Amount")],
        string="Expense Type",
        required=True,
    )
    expense_value = fields.Float(string="Expense Value", required=True)
    description = fields.Text(string="Description")
