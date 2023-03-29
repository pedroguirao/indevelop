# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class GesgruImporter(models.Model):
    _inherit = 'gesgru.importer'


    last_connection_date = fields.Datetime('Last connection')
    ocr_transactions_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='company_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )

    def get_purchase_order_data(self):
        #Abrimos DBF e iteramos por cada fila
        #Comprobamos si el servicio ya está definido en Odoo buscando en el modelo purchase.order por el nombre de servicio
        po = self.env['modelo'].search(["|",('partner_ref', '=', key),], limit=1)

        #Si no está creado lo creamos con fecha y ref
        po = self.env['modelo'].create({
            #'state': transactions_by_state['FACTURAS'][i]['status'],
            #'type': type_doc,
        })

