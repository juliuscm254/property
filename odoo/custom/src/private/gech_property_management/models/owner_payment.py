from odoo import api, fields, models


class OwnerPayment(models.Model):
    _name = "owner.payment"  # Optional, if you want a different model name
    _inherits = {"account.payment": "payment_id"}
    _inherit = ["mail.thread"]
    _description = "Model for tracking owner payments related to property contracts."

    # Your custom fields for property management
    # property_id = fields.Many2one(comodel_name='property.property', string='Property', required=True)
    owner_contract_id = fields.Many2one(
        comodel_name="owner.contract", string="Owner Contract", required=True
    )
    # Starting date of the payment period (format: yyyy-mm-dd)
    valid_from = fields.Date(string="Payment Period From", required=True)
    # Ending date of the payment period (format: yyyy-mm-dd)
    valid_until = fields.Date(string="Payment Period Until", required=True)
    # Discount percentage applied to the payment (optional)
    discount_percentage = fields.Float(string="Discount (%)")
    # Reference to the index table (optional)
    index_id = fields.Char(string="Index Reference")
    # Yearly payment amount (optional)
    yearly_amount = fields.Monetary(string="Yearly Amount")
    # Type of lease payment (e.g., monthly rent, late fee)
    owner_payment_type = fields.Selection(
        string="Owner Payment Type",
        selection=[
            ("commission", "Commission"),
            ("late_fee", "Late Fee"),
            ("other", "Other"),
        ],
        required=True,
    )

    message_main_attachment_id = fields.Many2one(groups="base.group_user")
    payment_id = fields.Many2one(
        comodel_name="account.payment",
        string="Payment",
        ondelete="restrict",
        required=True,
    )  # Optional: ondelete='cascade' if deleting owner.payment should cascade delete account.payment

    # @api.constrains('valid_from', 'valid_until', 'owner_contract_id')
    # def _validate_payment_period(self):
    #     for record in self:
    #         contract = record.owner_contract_id
    #         if contract:
    #             if record.valid_from < contract.valid_from or record.valid_until > contract.valid_until:
    #                 raise ValidationError("Payment period should be within the contract's valid date range.")
    #             if self.env['owner.payment'].search_count([
    #                 ('id', '!=', record.id),
    #                 ('owner_contract_id', '=', contract.id),
    #                 ('valid_from', '<=', record.valid_until),
    #                 ('valid_until', '>=', record.valid_from)
    #             ]):
    #                 raise ValidationError("Payment period overlaps with an existing payment for the same contract.")

    # @api.model
    # def update_rent_period(self):
    #     for record in self:
    #         if record.owner_contract_id:
    #             contract = record.owner_contract_id
    #             payment_frequency = contract.payment_frequency
    #             new_end_date = record.valid_until + self._get_period_delta(payment_frequency, record.valid_from, record.valid_until)
    #             contract.write({
    #                 'rent_begin_date': record.valid_until,
    #                 'rent_end_date': new_end_date
    #             })

    # @api.model
    # def _get_period_delta(self, payment_frequency, start_date, end_date):
    #     if payment_frequency == 'monthly':
    #         return timedelta(days=(end_date.replace(day=1) - start_date.replace(day=1)).days + 1)
    #     elif payment_frequency == 'quarterly':
    #         return timedelta(days=(end_date.replace(day=1) - start_date.replace(day=1)).days + 92)
    #     elif payment_frequency == 'biannually':
    #         return timedelta(days=(end_date.replace(day=1) - start_date.replace(day=1)).days + 183)
    #     else:  # annual
    #         return timedelta(days=365)

    @api.model
    def create(self, vals):
        if vals.get("payment_id"):
            payment = self.env["account.payment"].browse(vals["payment_id"])
            payment.write(
                {
                    "payment_type": "outbound",
                    "partner_type": "supplier",
                }
            )
        else:
            payment_vals = {
                "payment_type": "outbound",
                "partner_type": "supplier",
                # 'partner_id': self.env.user.partner_id.id,
            }
            payment = self.env["account.payment"].create(payment_vals)
            vals["payment_id"] = payment.id
        return super(OwnerPayment, self).create(vals)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     payments = super(OwnerPayment, self).create(vals_list)
    #     for payment in payments:
    #         account_payment_vals = self._prepare_account_payment_vals(payment)
    #         payment.write({'payment_id': self.env['account.payment'].create(account_payment_vals).id})
    #     return payments

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Create owner.payment records
    #     # payments = super(OwnerPayment, self).create(vals_list)

    #     print(vals_list)

    #     # Create linked account.payment records for each owner.payment
    #     account_payments = []
    #     for payment in vals_list:
    #         account_payment_vals = self._prepare_account_payment_vals(vals_list)
    #         account_payments.append(self.env['account.payment'].create(account_payment_vals))

    #     # Update rent period based on owner.payment records (if needed)
    #     # payments.update_rent_period()

    #     return account_payments

    # def _prepare_account_payment_vals(self, owner_payment):
    #     # Prepare dictionary with values for account.payment record
    #     vals = {
    #         'payment_type': 'outbound',  # Adjust payment type as needed
    #         'partner_type': 'supplier',  # Adjust partner type as needed
    #         # 'partner_id': owner_payment.owner_contract_id.partner_id.id,  # Link to partner from owner.contract
    #         # 'amount': owner_payment.yearly_amount / 12,  # Assuming yearly_amount is divided by 12 for monthly payments
    #         # 'currency_id': owner_payment.owner_contract_id.currency_id.id,  # Use currency from owner.contract
    #         # 'payment_method_id': owner_payment.owner_contract_id.payment_method_id.id,  # Use payment method from owner.contract
    #         # 'date': owner_payment.valid_from,  # Use payment start date
    #     }
    #     # You can add other relevant fields from owner_payment to account.payment here
    #     return vals

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Call the original create method to create payment records
    #     payments = super(OwnerPayment, self).create(vals_list)

    #     for payment in payments:
    #         # Retrieve the corresponding move_id
    #         move_id = payment.move_id

    #         # Update the payment_id on account_move_line with the correct ID
    #         move_id.line_ids.write({'payment_id': payment.id})  # Use payment.id to reference OwnerPayment record

    #     return payments

    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super(OwnerPayment, self).create(vals_list)
    #     records.update_rent_period()
    #     return records

    # def write(self, vals):
    #     result = super(OwnerPayment, self).write(vals)
    #     self.update_rent_period()
    #     return result

    # def post(self):
    #     result = super(OwnerPayment, self).post()
    #     for payment in self:
    #         # Access the generated journal entry (move_id)
    #         move_id = payment.move_id
    #         # Do something with the move_id (e.g., print it, use it for reports)
    #         print(f"Payment ID: {payment.id}, Journal Entry ID: {move_id.id}")
    #     return result

    # @api.model.update
    # def write(self, vals):
    #     result = super(OwnerPayment, self).write(vals)
    #     for record in self:
    #         if record.owner_contract_id:
    #             contract = record.owner_contract_id
    #             # Update rent_begin_date and rent_end_date based on new payment period (Option 1)
    #             contract.write({
    #                 'rent_begin_date': record.valid_until,
    #                 'rent_end_date': record.valid_until + timedelta(days=contract.payment_frequency == 'monthly' and 30 or (
    #                     contract.payment_frequency == 'quarterly' and 30 * 3 or (
    #                         contract.payment_frequency == 'biannually' and 30 * 6 or 365
    #                     )
    #                 ))
    #             })
    #     return result

    # def action_post(self):
    #     ''' draft -> posted '''
    #     self.move_id._post(soft=False)

    #     self.filtered(
    #         lambda pay: pay.is_internal_transfer and not pay.paired_internal_transfer_payment_id
    #     )._create_paired_internal_transfer_payment()

    # def action_cancel(self):
    #     ''' draft -> cancelled '''
    #     self.move_id.button_cancel()

    # def action_draft(self):
    #     ''' posted -> draft '''
    #     self.move_id.button_draft()

    # def action_open_destination_journal(self):
    #     ''' Redirect the user to this destination journal.
    #     :return:    An action on account.move.
    #     '''
    #     self.ensure_one()

    #     action = {
    #         'name': _("Destination journal"),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.journal',
    #         'context': {'create': False},
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'res_id': self.destination_journal_id.id,
    #     }
    #     return action
