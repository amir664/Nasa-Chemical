from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models
from datetime import datetime


class CustomReport(models.AbstractModel):
    _name = "report.monthly_report.monthly_reports"
    _description = "Purchase Order Month Wise Report"

    def _get_report_values(self, docids, data=None):
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        vendor_ids = data['vendor_ids']
        
        other_details.update({
            'date_from': date_from,
            'date_to': date_to,
            'product_ids': product_ids,
            'vendor_ids': vendor_ids,
        })
        
        cr = self._cr
        
        # Generate the dynamic month columns
        month_query = """
            SELECT to_char(generate_series(
                '%s'::date, 
                '%s'::date, 
                interval '1 month'
            ), 'YYYY_MM') AS month_key
        """ % (date_from, date_to)
        
        cr.execute(month_query)
        months = [row['month_key'] for row in cr.dictfetchall()]
        
        # Construct the dynamic SELECT query
        select_fields = [
            "pt.name AS item",
            "mm.name AS unit"
        ]
        
        for month in months:
            select_fields.append(
                f"COALESCE(SUM(CASE WHEN to_char(po.date_order, 'YYYY_MM') = '{month}' THEN pol.product_qty ELSE 0 END), 0) AS qty_{month}"
            )
            select_fields.append(
                f"COALESCE(SUM(CASE WHEN to_char(po.date_order, 'YYYY_MM') = '{month}' THEN pol.price_subtotal ELSE 0 END), 0) AS amount_{month}"
            )
        
        select_fields.append("COALESCE(SUM(pol.product_qty), 0) AS total_qty")
        select_fields.append("COALESCE(SUM(pol.price_subtotal), 0) AS total_amount")
        
        query = f"""
            SELECT {', '.join(select_fields)}
            FROM purchase_order po
            INNER JOIN purchase_order_line pol ON pol.order_id = po.id
            INNER JOIN product_product pp ON pp.id = pol.product_id
            INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
            INNER JOIN uom_uom mm ON mm.id = pol.product_uom
            WHERE po.date_order >= '{date_from}' AND po.date_order < '{date_to}'
        """
        
        if product_ids:
            product_ids_str = ','.join(map(str, product_ids))
            query += f" AND pt.id IN ({product_ids_str})"
        
        if vendor_ids:
            vendor_ids_str = ','.join(map(str, vendor_ids))
            query += f" AND po.partner_id IN ({vendor_ids_str})"
        
        query += " GROUP BY pt.name, mm.name ORDER BY pt.name;"
        
        cr.execute(query)
        data = cr.dictfetchall()
        for i, item in enumerate(data):
            if 'id' not in item:
                item['id'] = i + 1
        
        # Calculate total quantities and amounts dynamically
        totals = {}
        for month in months:
            totals[f'total_qty_{month}'] = sum(item[f'qty_{month}'] for item in data)
            totals[f'total_amount_{month}'] = sum(item[f'amount_{month}'] for item in data)
        
        totals['total_qty'] = sum(item['total_qty'] for item in data)
        totals['total_amount'] = sum(item['total_amount'] for item in data)

        date_from = datetime.strptime(date_from, "%Y-%m-%d").date() if isinstance(date_from, str) else date_from
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date() if isinstance(date_to, str) else date_to
        # raise UserError(str(data))
        return {
            'doc_ids': docids,
            'date_from': date_from,
            'date_to': date_to,
            'data': data,
            'totals': totals,
            'other': other_details,
        }
        
        # return {
        #     'doc_ids': docids,
        #     'data': data,
        #     'totals': totals,
        #     'other': other_details,
        # }





                
        
