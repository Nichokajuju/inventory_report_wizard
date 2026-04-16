# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DeliveryReportWizard(models.TransientModel):
    _name = 'delivery.report.wizard'
    _description = 'Delivery Report Wizard'

    # ── Date Range ──────────────────────────────────────────────────────
    date_from = fields.Date(
        string='From Date',
        required=True,
        default=fields.Date.context_today,
    )
    date_to = fields.Date(
        string='To Date',
        required=True,
        default=fields.Date.context_today,
    )

    # ── Operation Type ───────────────────────────────────────────────────
    operation_type_ids = fields.Many2many(
        'stock.picking.type',
        string='Operation Type(s)',
        help='Leave empty to include all operation types.',
    )

    # ── Source Location ──────────────────────────────────────────────────
    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        domain=[('usage', 'in', ['internal', 'transit'])],
        help='Filter by source/warehouse location. Leave empty for all.',
    )

    # ── Destination Location ─────────────────────────────────────────────
    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        domain=[('usage', 'in', ['internal', 'transit', 'customer'])],
        help='Filter by destination (e.g. Kitchen). Leave empty for all.',
    )

    # ── Partner ──────────────────────────────────────────────────────────
    partner_id = fields.Many2one(
        'res.partner',
        string='Delivery Address (Contact)',
        help='Filter by contact/partner. Leave empty for all.',
    )

    # ── Status ───────────────────────────────────────────────────────────
    state = fields.Selection(
        selection=[
            ('all', 'All'),
            ('done', 'Done'),
            ('assigned', 'Ready'),
            ('waiting', 'Waiting'),
            ('confirmed', 'Confirmed'),
        ],
        string='Status',
        default='done',
        required=True,
    )

    # ────────────────────────────────────────────────────────────────────
    def _build_domain(self):
        self.ensure_one()

        if self.date_from > self.date_to:
            raise UserError(_('From Date cannot be later than To Date.'))

        domain = [
            ('scheduled_date', '>=', fields.Datetime.to_datetime(self.date_from)),
            ('scheduled_date', '<=',
             fields.Datetime.to_datetime(self.date_to).replace(
                 hour=23, minute=59, second=59)),
        ]

        if self.state != 'all':
            domain.append(('state', '=', self.state))

        if self.operation_type_ids:
            domain.append(('picking_type_id', 'in', self.operation_type_ids.ids))

        if self.location_id:
            domain.append(('location_id', '=', self.location_id.id))

        if self.location_dest_id:
            domain.append(('location_dest_id', '=', self.location_dest_id.id))

        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))

        return domain

    # ────────────────────────────────────────────────────────────────────
    def action_generate_report(self):
        self.ensure_one()
        domain = self._build_domain()
        pickings = self.env['stock.picking'].search(
            domain, order='scheduled_date asc'
        )

        if not pickings:
            raise UserError(_(
                'No deliveries found for the selected filters. '
                'Please adjust your date range or filter criteria.'
            ))

        return self.env.ref(
            'delivery_report_wizard.action_delivery_report_pdf'
        ).report_action(pickings)