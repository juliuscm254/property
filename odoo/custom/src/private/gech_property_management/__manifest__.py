##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Property Management",
    "version": "16.0.0.0.0",
    "summary": "This module is used to manage properties and link it to a partner.",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Sales",
    "description": """
    This module is used to manage properties and link it to a partner. \n
    User creates a Property and adds stakeholders (res.partner), their role and percentage. \n
    User can also add an agent to the list of stakeholders if the property has an agent. \n

    Here is the link to how it works: https://www.loom.com/share/36bf5bd5f7774d68be75243feb7144b9\n

    """,
    #'sequence': '1',
    "author": "Julius",
    # "website": "https://vertel.se/apps/odoo-property/property_mgmt",
    # "images": ["static/description/banner.png"],  # 560x280 px.
    "license": "AGPL-3",
    "contributor": "",
    "maintainer": "Julius",
    # "repository": "https://github.com/vertelab/odoo-property",
    # Any module necessary for this one to work correctly
    "depends": ["base", "contacts", "gech_digital_twin", "account", "contract"],
    "data": [
        "security/ir.model.access.csv",
        # "security/property_security.xml",
        # 'views/property_designation_view.xml',
        # 'views/property_history_view.xml',
        # "views/res_partner_view.xml",
        "wizards/tenant_contract_rental_unit_wizard.xml",
        "views/tenant_contract.xml",
        "views/building.xml",
        "views/rental_unit.xml",
        "views/owner_contract.xml",
        "views/owner_payment.xml",
        "views/account_payment_view.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "gech_property_management/static/src/js/contract_save_dialog.js",
        ],
        # "web.assets_frontend": ["contract/static/src/scss/frontend.scss"],
        # "web.assets_tests": ["contract/static/src/js/contract_portal_tour.js"],
    },
    "application": False,
    "installable": True,
}
