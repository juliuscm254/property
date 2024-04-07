from odoo import fields, models


class OwnerContractBuilding(models.Model):
    _name = "owner.contract.building"  # Descriptive name
    _description = "Owner Contract Building Link"  # Clearer description

    # Many2one field referencing the RentalContract model
    owner_contract_id = fields.Many2one(
        comodel_name="owner.contract",
        string="Property Owner Contract",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the RentalUnit model (if it exists)
    building_id = fields.Many2one(
        comodel_name="building.building",
        string="Building",
        required=True,
        ondelete="cascade",
    )

    # Optional additional fields for the junction table (consider these based on your needs)
    # Example: square_footage = fields.Float(string='Square Footage')
    # Example: rent_amount = fields.Monetary(string='Rent Amount')
