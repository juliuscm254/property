# TODO  Doest not work 3.9
#  from pydantic import ValidationError
import datetime

from odoo import api, fields, models

# from odoo.models import NewId


class TenantContract(models.Model):
    _name = "tenant.contract"
    _description = "Tenant Agreement"
    _inherits = {"contract.contract": "contract_id"}
    PAYMENT_FREQUENCY = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("biannually", "Biannually"),  # Added biannually option
        ("annually", "Annually"),
    ]

    # TODO find a way to limit and default commission product_id

    rent_product_id = fields.Many2one(
        "product.product",
        string="Rent Product",
        # domain=[('type', '=', 'commission')]
    )
    tenant_contract_rental_unit_ids = fields.One2many(
        comodel_name="tenant.contract.rental.unit",
        inverse_name="tenant_contract_id",
        string="Tenant Agreement Units",
        ondelete="restrict",
    )
    rental_unit_ids = fields.One2many(
        comodel_name="rental.unit",
        string="Rental Units",
        compute="_compute_rental_unit_ids",
        ondelete="restrict",
    )

    # Optional reference to a main contract
    main_contract_id = fields.Char(
        string="Main Contract ID",
        help="Optional reference ID for a linked main contract.",
    )

    # Contract name
    contract_name = fields.Char(
        string="Contract Name", help="Optional name for the rental contract."
    )
    # Payment frequency (required)
    # payment_frequency = fields.Selection(
    #     selection=PAYMENT_FREQUENCY,
    #     string="Payment Frequency",
    #     required=True,
    #     help="Select the frequency of rental payments (e.g., monthly, quarterly).",
    # )

    description = fields.Text(
        string="Description",
        help="Optional field for additional details about the rental contract.",
    )

    # Contract group
    contract_group = fields.Char(
        string="Contract Group",
        help="Optional group classification for the rental contract.",
    )

    # TODO current payment period of the contract

    # Rent start date (required)
    rent_begin_date = fields.Date(
        string="Payment Period From Date",
        # required=True,
        help="Date the CURRENT payment period starts.",
    )

    # Rent end date (required)
    rent_end_date = fields.Date(
        string="Payment Period End Date",
        # required=True,
        help="Date the CURRENT payment period ends.",
    )

    # Notice period
    period_of_notice = fields.Char(
        string="Period of Notice",
        help="Required notice period for terminating the contract.",
    )

    # Payment in advance flag
    payment_in_advance = fields.Boolean(
        string="Payment in Advance", help="Flag indicating if rent is paid in advance."
    )

    # Short term lease flag
    short_term_lease = fields.Boolean(
        string="Short Term Lease", help="Flag indicating a short-term lease agreement."
    )

    # Tenant sector
    tenant_sector = fields.Char(
        string="Tenant Sector",
        help="The tenant's industry sector (e.g., retail, technology).",
    )

    # Turnover reporting interval
    turnover_reporting_interval = fields.Char(
        string="Turnover Reporting Interval",
        help="Frequency for reporting tenant turnover.",
    )

    # Valid from date (required)
    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=fields.Datetime.now,
        help="The date from which the building record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )
    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        default=lambda self: datetime.datetime(year=9999, month=12, day=31),
        help="The date until which the building record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    expense_line_ids = fields.One2many(
        "tenant.contract.expense", "contract_id", string="Expense Lines"
    )

    total_monthly_expense = fields.Monetary(
        string="Expenses", compute="_compute_total_expenses", store=True
    )
    total_monthly_rent_occupied = fields.Monetary(
        string="Total Monthly Rent Occupied Units",
        compute="_compute_total_monthly_rent",
        store=True,
    )
    tenant_contract_line_ids = fields.One2many(
        string="Contract lines",
        comodel_name="tenant.contract.line",
        inverse_name="tenant_contract_id",
        copy=True,
        context={"active_test": False},
    )

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print(vals_list, "CREATEEEEEEEE!!!!!!!!")
    #     records = super().create(vals_list)
    #     # for record in records:
    #     #     record.contract_id._set_start_contract_modification()
    #     return records

    # def write(self, vals):
    #     if "tenant_contract_rental_unit_ids" in vals:
    #         print("We Onnnn")

    def action_add_rental_unit(self):
        params = self.id
        print(params, "PARAMMMSSSSSS")
        if params:  # Check if params is not None
            # id = params["id"]
            return {
                "type": "ir.actions.act_window",
                "name": "Add Rental Unit",
                "res_model": "tenant.contract.rental.unit.wizard",
                "view_mode": "form",
                "target": "new",
                # "res_id": params,
            }
        else:
            # Render the custom dialog component
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "component": "gech_property_management.DialogComponent",
                },
            }

    # def write(self, vals):
    #     if "modification_ids" in vals:
    #         res = super(TenantContract, self).write(vals)
    #         for record in self:
    #             record.contract_id._modification_mail_send()
    #     else:
    #         res = super(TenantContract, self).write(vals)
    #     return res

    # @api.model
    # def _set_start_contract_modification(self):
    #     subtype_id = self.env.ref("contract.mail_message_subtype_contract_modification")
    #     for record in self:
    #         if record.contract_line_ids:
    #             date_start = min(record.contract_line_ids.mapped("date_start"))
    #         else:
    #             date_start = record.create_date
    #         record.message_subscribe(
    #             partner_ids=[record.partner_id.id], subtype_ids=[subtype_id.id]
    #         )
    #         record.with_context(skip_modification_mail=True).write(
    #             {
    #                 "modification_ids": [
    #                     (0, 0, {"date": date_start, "description": _("Contract start")})
    #                 ]
    #             }
    #         )

    @api.depends("rental_unit_ids", "rental_unit_ids.monthly_rent")
    def _compute_total_monthly_rent(self):
        pass

    @api.depends("tenant_contract_rental_unit_ids")
    def _compute_rental_unit_ids(self):
        for record in self:
            rental_unit_ids = record.tenant_contract_rental_unit_ids.mapped(
                "tenant_contract_rental_unit_id"
            ).ids
            record.rental_unit_ids = self.env["rental.unit"].search(
                [("id", "in", rental_unit_ids)]
            )

    @api.depends("expense_line_ids")
    def _compute_total_expenses(self):
        pass

    # def _create_contract_line(self):
    #     for record in self:
    #         current_unit_ids = self.env['tenant.contract.rental.unit'].search([
    #             ('tenant_contract_id', '=', record.id)
    #         ])
    #         if record.rent_product_id:  # Only create lines if a rent product is selected
    #             for unit_id in self.tenant_contract_rental_unit_ids:
    #                 # if unit_id not in current_unit_ids:
    #                 self.env['contract.line'].create({
    #                     'contract_id': record.contract_id.id,
    #                     'date_start': record.valid_from,
    #                     'product_id': record.rent_product_id.id,
    #                     # 'name': f"{record.name} - Unit {unit_id.name}",
    #                     'name': "TEST",
    #                     'price_unit': "10000",
    #                 })

    # def _update_contract_line(self):
    #     for record in self:
    #         existing_rental_unit_ids = record.tenant_contract_rental_unit_ids.mapped('rental_unit_id.id')
    #         new_rental_unit_ids = record.tenant_contract_rental_unit_ids.mapped('rental_unit_id').ids
    #         print(existing_rental_unit_ids, "EXCISTING")
    #         print(new_rental_unit_ids, "NEW!!!")

    #         # Create new tenant.contract.rental.unit records and contract.line records for added rental units
    #         added_rental_unit_ids = set(new_rental_unit_ids) - set(existing_rental_unit_ids)
    #         for rental_unit_id in added_rental_unit_ids:
    #             rental_unit = self.env['rental.unit'].browse(rental_unit_id)
    #             new_rental_unit = self.env['tenant.contract.rental.unit'].create({
    #                 'tenant_contract_id': record.id,
    #                 'rental_unit_id': rental_unit.id,
    #             })
    #             self.env['contract.line'].create({
    #                 'contract_id': record.contract_id.id,
    #                 'date_start': record.valid_from,
    #                 'product_id': record.rent_product_id.id,
    #                 'price_unit': "10000",
    #             })

    #         # Remove tenant.contract.rental.unit records and contract.line records for removed rental units
    #         removed_rental_unit_ids = set(existing_rental_unit_ids) - set(new_rental_unit_ids)
    #         for rental_unit_id in removed_rental_unit_ids:
    #             existing_rental_unit = self.env['tenant.contract.rental.unit'].search([
    #                 ('tenant_contract_id', '=', record.id),
    #                 ('rental_unit_id', '=', rental_unit_id)
    #             ])
    #             existing_rental_unit.unlink()
    #             contract_lines = self.env['contract.line'].search([
    #                 ('contract_id', '=', record.contract_id.id),
    #                 ('product_id', '=', record.rent_product_id.id),
    #                 ('name', 'ilike', str(rental_unit_id))  # Assuming contract.line name contains rental_unit_id
    #             ])
    #             contract_lines.unlink()
