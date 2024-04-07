{
    "name": "Digital Twin",
    "version": "16.0.0.0.0",
    "summary": "Manages physical assets and their digital representations.",
    "category": "Operations",
    "description": """
    This module introduces the concept of Digital Twins within Odoo. A Digital Twin represents the digital counterpart of a physical asset in the real world. It allows you to:

    * Create and manage Digital Twins for various asset types.
    * Link physical assets (e.g., equipment, buildings) to their corresponding Digital Twins.
    * Associate relevant data and information with each Digital Twin, providing a comprehensive view of the physical asset's state and behavior.
    * Leverage the Digital Twin for various purposes, such as:
        * Monitoring and analysis of asset performance.
        * Predictive maintenance scheduling based on real-time and historical data.
        * Simulation and optimization of asset operations.
    """,
    "author": "Julius",
    "license": "AGPL-3",
    "contributor": "",
    "maintainer": "Julius",
    # "depends": ["base", "contacts", "gech_digital_twin"],
    "data": [
        "security/ir.model.access.csv",
        # "views/menu.xml",
        # "views/owner_payment.xml"
    ],
    "application": False,
    "installable": True,
}
