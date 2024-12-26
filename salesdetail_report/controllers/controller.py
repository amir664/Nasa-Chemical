import io
from odoo import http
import xlwt
# import datetime
from odoo.exceptions import UserError, AccessError
from datetime import datetime

class CONSReportController(http.Controller):

    @http.route('/salesdetail_report/excel', type='http', auth='user')
    def generate_excel_report(self, to_date, from_date, partner_tag_id, category_id, partner_id, city, branch, area):
        query = ("""
                        

                    select distinct
                        so.date_order as date,
                        rp.name as customer,
                        rp.id as rp_id,
                        so.user_id as broker,
                        rp.city as city,
                        am.name as invoice_no,
                        --rpc.name ->> 'en_US' as sales_type,
                        sol.name as item,
                        sol.product_uom_qty as quantity,
                        um.name ->> 'en_US' as uom,
                        sol.price_unit as price,
                        sol.price_total as amount
                    from sale_order so
                    inner join res_partner rp on rp.id = so.partner_id
                    inner join sale_order_line sol on sol.order_id = so.id
                    inner join uom_uom um on um.id = sol.product_uom 
                    inner join account_move am on am.invoice_origin = so.name
                    inner join product_template pt on pt.id = sol.product_id
                    where so.id is not null    
                
            """)
        

                    
        
        env = http.request.env
        # partners = []
        
        if to_date != False and from_date != False:
            form_date = from_date.split('datetime.date(')[1].split('),')[0]
            date_to = to_date.split('datetime.date(')[1].split('),')[0]

            query += " and so.date_order between '%s' and '%s'" % (form_date, date_to)

        # raise UserError(str(type(partner_id)) + "--"+ str(type(category_id)))
    

        if partner_id != 'false':
            query += " AND rp.id = %s" % partner_id
            # raise UserError(partner_id)
           
        if category_id != 'false':
        #    raise UserError(category_id)
           query +=  " and pt.categ_id = %s" % category_id
        
        
        if city and city != 'False':
            query += " and rp.city = '%s'" % city
        
        
        if area and area != 'False':
            query += " and rp.street = '%s'" % area
        

        env.cr.execute(query)
        records = env.cr.dictfetchall()    
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sales Detail Report')

        # Title Style
        title_style = xlwt.XFStyle()
        title_font = xlwt.Font()
        title_font.bold = True
        title_style.font = title_font

        title_alignment = xlwt.Alignment()
        title_alignment.horz = xlwt.Alignment.HORZ_CENTER
        title_style.alignment = title_alignment

        # Merge cells for title (0 to 12 for 13 columns)
        sheet.write_merge(0, 0, 0, 11, '', title_style)

        # Header Style (center aligned)
        header_style_center = xlwt.XFStyle()
        header_font = xlwt.Font()
        header_font.bold = True
        header_style_center.font = header_font

        header_alignment_center = xlwt.Alignment()
        header_alignment_center.horz = xlwt.Alignment.HORZ_CENTER
        header_style_center.alignment = header_alignment_center

        # Data Style (center aligned for text)
        data_style_center = xlwt.XFStyle()
        data_alignment_center = xlwt.Alignment()
        data_alignment_center.horz = xlwt.Alignment.HORZ_CENTER
        data_style_center.alignment = data_alignment_center

        # Data Style (right aligned for numbers)
        data_style_right = xlwt.XFStyle()
        data_alignment_right = xlwt.Alignment()
        data_alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
        data_style_right.alignment = data_alignment_right
         	 
        # Bold Center-aligned style
        data_style_bold_center = xlwt.XFStyle()
        bold_font_center = xlwt.Font()
        bold_font_center.bold = True
        data_style_bold_center.font = bold_font_center

        alignment_center_bold = xlwt.Alignment()
        alignment_center_bold.horz = xlwt.Alignment.HORZ_CENTER
        data_style_bold_center.alignment = alignment_center_bold

        # Bold Right-aligned style
        data_style_bold_right = xlwt.XFStyle()
        bold_font_right = xlwt.Font()
        bold_font_right.bold = True
        data_style_bold_right.font = bold_font_right

        alignment_right_bold = xlwt.Alignment()
        alignment_right_bold.horz = xlwt.Alignment.HORZ_RIGHT
        data_style_bold_right.alignment = alignment_right_bold


        # # Title with date range
        # report_title = "Sales Detail Report"

        # # Merge cells for the title row
        # sheet.write_merge(0, 0, 0, 11, report_title, title_style)

        # item_group = ''
        # sales_type = ''
        # cust = ''
        # if category_id != False:
        #     item_group = env['product.category'].search([('id', '=', category_id)])
        # if category_id != False:
        #     sales_type = env['res.partner.category'].search([('id', '=', partner_tag_id)])
        # if category_id != False:
        #     cust = env['res.partner'].search([('id', '=', partner_id)])

        report_title = "Sales Detail Report"

        # Merge cells for the title row
        sheet.write_merge(0, 0, 0, 11, report_title, title_style)

        # # Additional Information Rows
        # additional_info = [
        #     ('Print out date:', datetime.now().strftime('%d/%m/%Y')),
        #     ('Fiscal Year:', f"{from_date}"),  # Replace with actual fiscal year logic if needed
        #     ('Period:', f"{from_date} to {to_date}" if from_date and to_date else ''),
        #     ('Branch:', branch if branch else ''),
        #     ('City:', city if city else ''),
        #     ('Customer:', cust.name if cust.name else ''),
        #     ('Area:', area if area else ''),
        #     ('Items Group:', item_group.complete_name if item_group.complete_name else ''),
        #     ('Sales Type:', sales_type.name if sales_type.name else ''),
        # ]

        # # Write Additional Information Rows
        # row_offset = 1  # Start writing additional info below the title
        # for row, (label, value) in enumerate(additional_info, start=row_offset):
        #     sheet.write(row, 0, label, data_style_bold_center)
        #     sheet.write(row, 1, value, data_style_center)

        # # Adjust the row where headers start
        # header_start_row = row_offset + len(additional_info) + 1  # Avoid overlap with info rows

        # Write headers
        headers = [
            'Date', 'Customer', 'Item', 'Broker', 'Sales Type', 'City',
            'Invoice No', 'Qty', 'Unit', 'Price', 'Amount'
        ]

        # Write headers with the center alignment style
        for col, header in enumerate(headers):
            sheet.write(2, col, header, header_style_center)


        # Write data rows
        for row, record in enumerate(records, start=3):

            user = env['res.users'].search([('id', '=', record['broker'])])

            sheet.write(row, 0, record['date'] if record['date'] else '', data_style_center)
            sheet.write(row, 1, record['customer'] if record['customer'] else '', data_style_center)
            
            sheet.write(row, 2, record['item'] if record['item'] else '', data_style_center)
            sheet.write(row, 3, user.name if user else '', data_style_center)
            sheet.write(row, 4, record['item'] if record['item'] else '', data_style_center)
            sheet.write(row, 5, record['sales_type'] if record['sales_type'] else '', data_style_center)
            sheet.write(row, 6, record['city'] if record['city'] else '', data_style_center)
            sheet.write(row, 7, record['invoice_no'] if record['invoice_no'] else 0.0, data_style_center)
    

            sheet.write(row, 8, record['quantity'] if record['quantity'] else 0.0, data_style_center)
            sheet.write(row, 9, record['uom'] if record['uom'] else 0.0, data_style_center)  # Keeping it empty as per your original code
            sheet.write(row, 10, record['price'] if record['price'] else 0.0, data_style_right)
            sheet.write(row, 11, record['amount'] if record['amount'] else 0.0, data_style_right)

        # Save to stream
        stream = io.BytesIO()
        workbook.save(stream)
        stream.seek(0)

        report_name = 'Sales Detail Report.xls'
        response = http.request.make_response(
            stream.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', http.content_disposition(report_name))
            ]
        )
        response.set_cookie('fileToken', report_name)
        return response


