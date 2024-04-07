from odoo import fields, models


class RentalPayment(models.Model):
    _inherit = "account.payment"
    _name = "rental.payment"  # Optional, if you want a different model name

    # Your custom fields for property management
    # property_id = fields.Many2one(comodel_name='property.property', string='Property', required=True)
    rental_contract_id = fields.Many2one(
        comodel_name="rental.contract", string="Rental Contract", required=True
    )
    # Starting date of the payment period (format: yyyy-mm-dd)
    valid_from = fields.Date(string="Valid From", required=True)
    # Ending date of the payment period (format: yyyy-mm-dd)
    valid_until = fields.Date(string="Valid Until", required=True)
    # Discount percentage applied to the payment (optional)
    discount_percentage = fields.Float(string="Discount (%)")
    # Reference to the index table (optional)
    index_id = fields.Char(string="Index Reference")
    # Yearly payment amount (optional)
    yearly_amount = fields.Monetary(string="Yearly Amount")
    # Type of lease payment (e.g., monthly rent, late fee)
    payment_type = fields.Selection(
        string="Payment Type",
        selection=[("rent", "Rent"), ("late_fee", "Late Fee"), ("other", "Other")],
        required=True,
    )
