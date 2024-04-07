from odoo import api, fields, models

# from .contract_line_constraints import get_allowed


class TenantContractLine(models.Model):
    _name = "tenant.contract.line"
    _description = "Tenant Agreement Line"
    _inherits = {"contract.line": "contract_line_id"}

    tenant_contract_id = fields.Many2one(
        comodel_name="tenant.contract",
        string="Contract",
        required=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
    )

    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        # required=True,
        ondelete="cascade",
    )

    # @api.model
    # def create(self, vals_list):
    #     records = self.env[self._name]
    #     for vals in vals_list:
    #         tenant_contract_id = vals.get("tenant_contract_id")
    #         if isinstance(tenant_contract_id, str):
    #             try:
    #                 tenant_contract_id = int(tenant_contract_id)
    #             except ValueError:
    #                 tenant_contract_id = self.env["tenant.contract"].search([("name", "=", tenant_contract_id)], limit=1).id

    #         tenant_contract = self.env["tenant.contract"].browse(tenant_contract_id)
    #         contract_values = {
    #             "contract_id": tenant_contract.contract_id.id,
    #             "recurring_interval": vals.get("recurring_interval", 1),
    #             "recurring_invoicing_type": vals.get("recurring_invoicing_type", "pre-paid"),
    #             "recurring_rule_type": vals.get("recurring_rule_type", "monthly"),
    #             "date_start": vals.get("date_start", fields.Date.today()),
    #             "name": vals.get("name", "New Contract Line"),
    #             "quantity": vals.get("quantity", 1.0),
    #         }
    #         vals.update(contract_values)
    #         records |= super(TenantContractLine, self).create(vals)
    #     return records

    @api.model
    def create(self, vals):
        print(vals, "CONTRACTLINE!!!!")
        if "tenant_contract_id" in vals:
            tenant_contract = self.env["tenant.contract"].browse(
                vals["tenant_contract_id"]
            )
            # vals['contract_id'] = tenant_contract.contract_id.id
            contract_values = {
                "contract_id": tenant_contract.contract_id.id,
                "product_id": tenant_contract.rent_product_id.id,
                "recurring_interval": vals.get("recurring_interval", 1),
                "recurring_invoicing_type": vals.get(
                    "recurring_invoicing_type", "pre-paid"
                ),
                "recurring_rule_type": vals.get("recurring_rule_type", "monthly"),
                "date_start": vals.get("date_start", fields.Date.today()),
                "name": vals.get("name", "New Contract Line"),
                "quantity": vals.get("quantity", 1.0),
            }
            vals.update(contract_values)
        return super(TenantContractLine, self).create(vals)
