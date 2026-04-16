# -*- coding: utf-8 -*-
{
    'name': 'Delivery Report Wizard',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Generate filtered delivery reports with date range, operation type, and location filters',
    'description': """
        Delivery Report Wizard
        ======================
        Adds a reporting wizard under Inventory > Reporting.

        Features:
        - Filter by Operation Type
        - Filter by Date Range (from / to)
        - Filter by Source and Destination Location
        - Filter by Delivery Address (Contact/Partner)
        - Filter by Status (Done, Ready, Waiting...)
        - Generate printable PDF reports
    """,
    'author': 'Nicholas Mutembei',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/delivery_report_wizard_view.xml',
        'report/delivery_report_template.xml',
        'report/delivery_report_action.xml',
        'views/delivery_report_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}