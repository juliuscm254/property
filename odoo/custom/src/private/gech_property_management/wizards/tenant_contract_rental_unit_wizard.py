from odoo import fields, models


class TenantContractRentalUnitWizard(models.TransientModel):
    _name = "tenant.contract.rental.unit.wizard"

    building_id = fields.Many2one("building.building", string="Building", required=True)
    rental_unit_id = fields.Many2one(
        "rental.unit",
        string="Rental Unit",
        domain="[('building_id', '=', building_id), ('rented_out', '=', False)]",
        required=True,
    )

    def action_add_rental_unit(self):
        tenant_contract = self.env.context.get("active_id")
        print(self.env.context)
        tenant_contract_m = self.env.context.get("active_model")
        tenant_contract_m = self.env[tenant_contract_m].browse(tenant_contract)

        if not self.rental_unit_id.rented_out:  # Check if rented_out is False
            new_record = self.env["tenant.contract.rental.unit"].create(
                {
                    "tenant_contract_rental_unit_id": self.rental_unit_id.id,
                    "tenant_contract_id": tenant_contract,
                    # ... other fields based on wizard input
                }
            )
            print(tenant_contract_m)
            new_record_2 = self.env["tenant.contract.line"].create(
                {
                    # 'contract_id': self.rental_unit_id.id,
                    "contract_id": tenant_contract_m.contract_id.id,
                    "product_id": tenant_contract_m.rent_product_id.id,
                    "recurring_interval": 1,
                    "recurring_invoicing_type": "pre-paid",
                    "recurring_rule_type": "monthly",
                    "date_start": fields.Date.today(),
                    "name": "New Contract Line",
                    "quantity": 1.0,
                    # ... other fields based on wizard input
                }
            )
            return {"type": "ir.actions.act_window_close"}
        else:
            # Handle case where unit is rented out (error message, warning)
            return {
                "type": "ir.actions.act_window_close",
                "warning": {
                    "title": "Error!",
                    "message": "Selected rental unit is already rented out.",
                },
            }

    # def action_add_rental_unit(self):
    #     tenant_contract = self.env.context.get('active_id')
    #     self.env['tenant.contract.rental.unit'].create({
    #         'tenant_contract_rental_unit_id': self.rental_unit_id.id,
    #         'tenant_contract_id': tenant_contract,
    #         # ... other fields based on wizard input
    #     })

    #     return {'type': 'ir.actions.act_window_close'}
