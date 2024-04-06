from odoo import fields, models


class RentalContractRentalUnit(models.Model):
    _name = "rental.contract.rental.unit"  # Descriptive name
    _description = "Rental Contract Unit Link"  # Clearer description

    # Many2one field referencing the RentalContract model
    rental_contract_id = fields.Many2one(
        comodel_name="rental.contract",
        string="Rental Contract",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the RentalUnit model (if it exists)
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Optional additional fields for the junction table (consider these based on your needs)
    # Example: square_footage = fields.Float(string='Square Footage')
    # Example: rent_amount = fields.Monetary(string='Rent Amount')
