from odoo import fields, models


class Dunning(models.Model):
    _name = "dunning.dunning"
    _description = "Dunning Management"

    related_rental_payment_id = fields.Many2one(
        comodel_name="rental.payment",
        string="Related Rental Payment",
        compute="_compute_related_rental_payment",
    )
    dunning_level = fields.Selection(
        string="Dunning Level",
        selection=[("1", "1st"), ("2", "2nd"), ("3", "3rd")],
        required=True,
    )
    dunning_amount = fields.Monetary(string="Dunning Amount", required=True)
    currency = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    initial_due_date = fields.Date(string="Initial Due Date", required=True)
    payment_date = fields.Date(string="Payment Date")
    state = fields.Selection(
        string="State", selection=[("open", "Open"), ("paid", "Paid")], default="open"
    )

    def _compute_related_rental_payment(self):
        for record in self:
            try:
                # Access the payment ID from the initial field
                payment_id = record.rental_payment_id
                record.related_rental_payment_id = self.env["rental.payment"].browse(
                    payment_id
                )
            except ValueError:
                # Handle cases where payment_id might not be an integer
                record.related_rental_payment_id = False

    def mark_paid(self):
        self.write({"state": "paid", "payment_date": fields.Date.today()})
