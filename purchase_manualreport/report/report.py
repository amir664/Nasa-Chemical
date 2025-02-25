from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.purchase_manualreport.purchase_manualreports"
    _description = "Purchase Report"


    def _get_report_values(self, docids, data=None):
        
        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        vendor_ids = data['vendor_ids']
        po_no = data['po_no']
        grn = data['grn']
        invoice_no = data['invoice_no']
        po_no1 = data.get('po_no', '')



        other_details.update({
                'from_date': date_from,
                'to_date': date_to,
                'product_ids': product_ids,
                'vendor_ids': vendor_ids,
                'po_no': po_no,
                'grn': grn,
                'invoice_no':invoice_no,
            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))


        cr = self._cr
        where_clauses = []
        params = []

        if date_from and date_to:
            where_clauses.append("po.date_order BETWEEN %s AND %s")
            params.extend([tuple(date_from), tuple(date_to)])

        if product_ids:
            where_clauses.append(f"pt.id IN ({', '.join(map(str, product_ids))})")


        if vendor_ids:
            where_clauses.append(f"rs.id IN ({', '.join(map(str, vendor_ids))})")
        
        if po_no != "purchase.order()":  
            raise UserError(po_no)
            po_numbers = po_no.replace("purchase.order(", "").replace(")", "").strip()
            
            if po_numbers:  
                # formatted_po_no = ", ".join(f"'{po.strip()}'" for po in po_numbers.split(','))  
                po_values = ', '.join(f"'{name}'" for name in po_numbers)
                raise UserError([po_numbers,po_values])
                where_clauses.append(f"po.name IN (({', '.join(map(str, po_numbers))})")
                
        
        if grn != "stock.picking()":  
            po_numbers = grn.replace("stock.picking(", "").replace(")", "").strip()
            
            if po_numbers:  
                formatted_po_no = ", ".join(f"'{po.strip()}'" for po in po_numbers.split(','))  
                where_clauses.append(f"sp.name IN ({formatted_po_no})")

        if invoice_no != "account.move()":  
            po_numbers = invoice_no.replace("account.move(", "").replace(")", "").strip()
            
            if po_numbers:  
                formatted_po_no = ", ".join(f"'{po.strip()}'" for po in po_numbers.split(','))  
                where_clauses.append(f"sp.name IN ({formatted_po_no})")
            # params.append(vendor_ids)
        # raise UserError(po_no)
        # raise UserError([po_no,grn,invoice_no,vendor_ids,product_ids,date_from])
        # if po_no and isinstance(po_no, models.BaseModel):  # Ensure it's a recordset
        #     po_no_names = [po.name for po in po_no if po.name]  # Extract valid names
        #     if po_no_names:
        #         where_clauses.append("po.name IN %s")
        #         params.append(tuple(po_no_names))
        # raise UserError(po_no.id)
        # if po_no.id:
        #     where_clauses.append("po.name IN %s")
        #     params.append((po_no.id))

        # if grn and isinstance(grn, models.BaseModel):
        #     grn_names = [grn.name for grn in grn if grn.name]
        #     if grn_names:
        #         where_clauses.append("sp.name IN %s")
        #         params.append(tuple(grn_names))

        # if invoice_no and isinstance(invoice_no, models.BaseModel):
        #     invoice_no_names = [invoice.name for invoice in invoice_no if invoice.name]
        #     if invoice_no_names:
        #         where_clauses.append("am.name IN %s")
        #         params.append(tuple(invoice_no_names))




        # Combine WHERE clauses
        where_clause = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = (f"""
                SELECT 
                    pr.name AS PurchaseRequest,
                    po.date_order AS Date,
                    rs.name AS Vendor,                    
                    pt.name ->> 'en_US' AS Item,
                    po.name AS PONo,
                    sp.name AS GRN,
                    am.name AS InvoiceNo,
                    sw.name AS Location,
                    pol.product_qty AS Qty,
                    mm.name ->> 'en_US' AS Unit,
                    pol.price_unit AS Price, 
                    pol.price_total AS Amount
                FROM purchase_order_line pol 
                INNER JOIN purchase_order po ON po.id = pol.order_id
                INNER JOIN product_product pp ON pp.id = pol.product_id
                INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
                INNER JOIN res_partner rs ON rs.id = po.partner_id
                LEFT JOIN stock_picking sp ON sp.origin = po.name   
                LEFT JOIN account_move am ON am.invoice_origin = po.name
                INNER JOIN stock_picking_type spt ON spt.id = po.picking_type_id
                INNER JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
                INNER JOIN uom_uom mm ON mm.id = pol.product_uom
                LEFT JOIN purchase_request pr ON pr.id = po.purchase_request_id -- Assuming this is the correct relationship
                {where_clause}
                ORDER BY po.name;

                
                """
        
         )
        raise UserError(query)

        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
            'total_qty': sum(item['qty'] for item in data),
            'total_price': sum(item['price'] for item in data),
            
            'total_amount': sum(item['amount'] for item in data),
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }


        
