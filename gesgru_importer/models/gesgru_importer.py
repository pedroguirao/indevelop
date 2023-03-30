# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import logging

from dbfread import DBF
from pandas import DataFrame
import json

_logger = logging.getLogger(__name__)


class GesgruImporter(models.Model):
    _inherit = 'res.company'

    last_connection_date = fields.Datetime('Last connection')

    def getDbf(self):
        return DBF('/opt/odoo/servicio.dbf', ignore_missing_memofile=True, load=True)

    def getDataFrame(self, dbf):
        return DataFrame(dbf)

    def getListOfTypes(self, record, dbf):
        listTypes = {}
        listKey = self.getDataFrame(dbf).keys()
        for field in listKey:
            listTypes[field] = str(type(record[field])).replace('<class \'', '').replace('\'>', '')

        return listTypes

    def setJson(self, dbf):
        listKey = self.getDataFrame(dbf).keys()
        superdict = []

        for reg in dbf.records:
            dict = {}
            for field in listKey:
                if str(field) == "FECHASERV" or str(field) == "IDSERVICIO":
                    dict[str(field)] = str(reg[field])
            superdict.append(dict)
        return json.loads(json.dumps(superdict))

    def parseDbf(self, dbf):
            for i in range(len(dbf.records)):

                self.env.cr.commit()

                try:
                    po = self.env['purchase.order'].search([('partner_ref', '=', str(dbf.records[i]["IDSERVICIO"]))], limit=1)

                    if not po:
                        fechaserv = str(dbf.records[i]["FECHASERV"])
                        partnerref = int(dbf.records[i]["IDSERVICIO"])

                        if(fechaserv == "None"):
                            fechaserv = '2001-01-01 00:00:00'

                        po = self.env['purchase.order'].create({
                                'name': "Prueba",
                                'partner_id': 2,
                                'date_order': fechaserv,
                                'partner_ref': partnerref
                        })

                except Exception as ex:
                    template = "- An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message + " - " + str(dbf.records[i]["FECHASERV"]) + " --- " + str(dbf.records[i]["IDSERVICIO"]))

    def insertBBDD(self, dbf):
        self.parseDbf(dbf)

    def test_action_button(self):
        dbf = self.getDbf()
        # json = self.setJson(dbf)
        # print(json)

        #self.parseDbf(dbf)
        self.insertBBDD(dbf)

    # def get_purchase_order_data(self):
    # Abrimos DBF e iteramos por cada fila
    # Comprobamos si el servicio ya está definido en Odoo buscando en el modelo purchase.order por el nombre de servicio
    # po = self.env['modelo'].search(["|",('partner_ref', '=', key),], limit=1)

    # Si no está creado lo creamos con fecha y ref
    # po = self.env['modelo'].create({
    # 'state': transactions_by_state['FACTURAS'][i]['status'],
    # 'type': type_doc,
    # })
