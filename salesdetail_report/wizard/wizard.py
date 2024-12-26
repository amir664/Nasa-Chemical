from odoo import _, api, fields, models
import datetime

class SalesDetailReportWizard(models.TransientModel):
    _name = 'salesdetail.report'
    _description = 'Sales Detail Report'

    partner_id = fields.Many2one('res.partner', string = "Customer")
    category_id = fields.Many2one('product.category', string = "Item Group")
    partner_tag_id = fields.Many2one('res.partner.category', string = "Sales Type")
    city = fields.Char(string = "City")
    branch = fields.Char(string = "Branch")
    area = fields.Char(string = "Area")
    to_date = fields.Date(string = "To Date")
    from_date = fields.Date(string = "From Date")
    
    def print_report(self):

        # category_id = []
        # if self.category_id:
        #     for id in self.category_id:
        #         category_id.append(id.id)

        # partner_tag_id = []
        # if self.partner_tag_id:
        #     for id in self.partner_tag_id:
        #         partner_tag_id.append(id.id)

        # partner_id = []
        # if self.partner_id:
        #     for id in self.partner_id:
        #         partner_id.append(id.id)


        
        data = {
            'from_date': self.from_date if self.from_date else '01-01-2000',
            'to_date': self.to_date if self.to_date else datetime.datetime.today().date(),
            'partner_tag_id': self.partner_tag_id.id,
            'category_id': self.category_id.id,
            'partner_id': self.partner_id.id,
            'city': self.city,
            'branch': self.branch,
            'area': self.area,
            
        }
        
        return self.env.ref('salesdetail_report.salesdetail_report_pdf').with_context(landscape=True).report_action(self, data = data)
        
    def print_excel_report(self):

        from_date = self.from_date if self.from_date else '01-01-2000',
        to_date = self.to_date if self.to_date else datetime.datetime.today().date(),

        return {
            'type': 'ir.actions.act_url',
            'url': '/salesdetail_report/excel?to_date=%s&from_date=%s&partner_tag_id=%s&category_id=%s&partner_id=%s&city=%s&branch=%s&area=%s'%(to_date, from_date, self.partner_tag_id.id, self.category_id.id or 'false', self.partner_id.id or 'false', self.city, self.branch, self.area),
            'target': 'self',
        }  