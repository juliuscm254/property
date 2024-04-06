from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TenantContractRentalUnit(models.Model):
    _name = "tenant.contract.rental.unit"  # Descriptive name
    _description = "Tenant Agreement Contract Rental Unit Link"  # Clearer description

    # Many2one field referencing the RentalContract model
    tenant_contract_id = fields.Many2one(
        comodel_name="tenant.contract",
        string="Tenant Agreement Contract",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the RentalUnit model (if it exists)
    tenant_contract_rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
        unique=True,  # Set this to ensure uniqueness
    )

    # _sql_constraints = [
    #     ('unique_rental_unit', 'UNIQUE(tenant_contract_rental_unit_id)', 'A rental unit can only have one contract throughout its lifetime.'),
    # ]

    @api.onchange("tenant_contract_rental_unit_id")
    def _onchange_rental_unit_id(self):
        # Your logic here
        print("What DI I DO?")
        # if self.tenant_contract_rental_unit_id:
        #     self.tenant_contract_rental_unit_id.rented_out = True
        # else:
        #     self.tenant_contract_rental_unit_id.rented_out = False

    @api.model
    def create(self, vals):
        rental_unit_id = vals.get("tenant_contract_rental_unit_id")
        if rental_unit_id:
            rental_unit = self.env["rental.unit"].browse(
                rental_unit_id
            )  # Fetch rental unit record
            if rental_unit.rented_out:  # Check if rented_out is True
                raise ValidationError(_("Selected rental unit is already rented out."))
            else:
                record = super(TenantContractRentalUnit, self).create(vals)
                rental_unit_id = record.tenant_contract_rental_unit_id
                print(rental_unit_id, "RENTAL UNITTTTTTTT ")
                if rental_unit_id:
                    rental_unit_id.write({"rented_out": True})
                return record

    # @api.model
    # def create(self, vals):
    #     rental_unit_id = vals.get('tenant_contract_rental_unit_id')
    #     if rental_unit_id:
    #         rental_unit = self.env['rental.unit'].browse(rental_unit_id)  # Fetch rental unit record
    #         if rental_unit.rented_out:  # Check if rented_out is True
    #             raise ValidationError('Selected rental unit is already rented out.')
    #     return super(TenantContractRentalUnit, self).create(vals)

    def write(self, vals):
        res = super(TenantContractRentalUnit, self).write(vals)

        print(vals, "RENTAL UNITTTTTTTT ")
        if "tenant_contract_rental_unit_id" in vals:
            for record in self:
                if record.tenant_contract_rental_unit_id:
                    record.tenant_contract_rental_unit_id.rented_out = True
                elif record.rental_unit_id.id in (
                    vals.get("tenant_contract_rental_unit_id") or []
                ):
                    rental_unit_id = self.env["rental.unit"].browse(
                        vals["tenant_contract_rental_unit_id"]
                    )
                    rental_unit_id.rented_out = False
        return res

    def unlink(self):
        rental_unit_ids = self.mapped("tenant_contract_rental_unit_id")
        result = super(TenantContractRentalUnit, self).unlink()

        # Update rented_out field for the related rental.unit records
        for rental_unit in rental_unit_ids:
            rental_unit.rented_out = False
        return result

    # monthly_rent =

    # Optional additional fields for the junction table (consider these based on your needs)
    # Example: square_footage = fields.Float(string='Square Footage')
    # Example: rent_amount = fields.Monetary(string='Rent Amount')
    # def action_add_rental_unit(self):
    #     params = self.tenant_contract_id
    #     print(self.tenant_contract_id.id, "PARAMMMSSSSSS")
    #     if params:  # Check if params is not None
    #         id = params["id"]
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Add Rental Unit',
    #             'res_model': 'tenant.contract.rental.unit.wizard',
    #             'view_mode': 'form',
    #             'target': 'new',
    #             "res_id": self.tenant_contract_id,
    #         }
    #     else:
    #         # Render the custom dialog component
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'component': 'gech_property_management.DialogComponent',
    #             },
    #         }
