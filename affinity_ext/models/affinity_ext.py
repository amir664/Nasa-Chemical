from odoo import fields, models, api
from odoo.exceptions import UserError



class ResPartnerInherited(models.Model):
    _inherit = "res.partner"

    legal_status = fields.Selection([('individual', 'Individual'), ('partnership', 'Partnership'), ('aop', 'AOP'), ('company', 'Company')], required = True)
    company_reg = fields.Char("Company Registration", required = True)
    artical = fields.Char("Article of Association and Memorandom", required = True)
    strn_no = fields.Char("STRN", required = True)
    cnic_no = fields.Char("CNIC Number", required = True)
    vendor_status = fields.Selection([('active', 'Active'), ('non_active', 'Non Active')], string = "Status")
    major_client = fields.Selection([('a','A Category'), ('b', 'B Category'), ('c', 'C Category')]) 
    region = fields.Char(string="Region")
    status = fields.Char(string="Status")
    town = fields.Char(string="Town")

class ResPartnerBankInherited(models.Model):
    
    _inherit = "res.partner.bank"
    
    bank_iban_num = fields.Char('IBAN Number')



class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)', default=10.00)


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'


    # Override the write method to check purchase tolerance before saving the record
    @api.model
    def write(self, vals):
        res =  super(StockPickingInherited, self).write(vals)
        high_perc_qty = 0
        for rec in self:
            if rec.picking_type_id.name == 'Receipts':
                for line in rec.move_ids_without_package:
                    if line.quantity and line.product_uom_qty:
                        
                        high_perc_qty =  line.product_uom_qty + ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100) 
                    if line.quantity >= high_perc_qty:
                        raise UserError('You have violated the purchase tolerance limit')

        # Proceed with the default write behavior after the checks
        return res



class PurchaseOrderInherited(models.Model):
    _inherit = "purchase.order"


    
    notes = fields.Html(
        string="Terms and Condition" 
    )

    @api.model
    def default_get(self, fields_list):
        res = super(PurchaseOrderInherited, self).default_get(fields_list)
        res['notes'] = """<strong>Purchase Order Terms and Conditions:</strong>
                            <ul>
                                <li><b>Acceptance:</b> By accepting this Purchase Order, the Supplier agrees to all terms and conditions stated herein. Any modifications must be approved in writing by the Buyer.</li>
                                <li><b>Pricing and Payment:</b> Prices are fixed and include all charges. Payment will be due in 30/60 days after receipt of invoice and goods or services.</li>
                                <li><b>Delivery:</b> Timely delivery is essential. NASA Chemicals reserves the right to reject late deliveries or cancel the order if deadlines are missed. Delivery timings are 8am-3:00 pm. Any deliveries earlier or later than this time may be cancelled or returned.</li>
                                <li><b>Delivery Tolerance:</b> The Supplier is allowed to deliver no more than 10% extra material beyond the quantity specified in the purchase order. Any delivery exceeding the 10% allowance must be pre-approved by the Buyer in writing. Failure to obtain approval may result in the return of excess material at the Supplier's expense.</li>
                                <li><b>Content Of Document</b></li>
                                    <ul>
                                        <li><b>Product Specifications Sheet:</b> Must include detailed information such as product dimensions, materials used, performance characteristics, and compliance with relevant industry standards.</li>
                                        <li><b>Technical Data Sheet (TDS): </b>Should provide comprehensive technical information, including product properties, recommended applications, handling instructions, and safety data.</li>
                                        <li><b>Certificate of Analysis (CoA): </b>Must include test results confirming that the product meets the agreed-upon specifications, including any relevant batch or lot numbers.</li>
                                    </ul>
                                <li><b>Inspection: <b/>Goods/services are subject to inspection. Non-conforming items may be rejected and returned at the Supplier’s expense.</li>
                                <li><b>Warranty: </b>The Supplier warrants that goods/services are free of defects, conform to specifications, and are fit for purpose. In case any damaged goods are identified during the production process, the goods will be rejected, and company will have the right to deduct payment and send the rejected material back to the vendor, at the vendor’s expense.</li>
                                <li><b>Damages: <b/>Any damages to our finished goods resulting from leakages/damages in suppliers’ material will be fully covered by the supplier, including all associated costs and losses.</li>
                                <li><b>Changes: </b>The Buyer may request changes to the order. Price or schedule adjustments require mutual agreement.</li>
                                <li><b>Termination: </b>The Buyer may terminate this order for convenience or cause. In the case of termination for cause, no further payment is due.</li>
                                <li><b>Liability: </b>The Supplier agrees to indemnify the Buyer for any damages arising from defective goods/services.</li>
                                <li><b>Compliance: </b>Supplier must comply with all applicable laws and regulations.</li>
                                <li><b>Governing Law: </b>This order is governed by the laws of PPRA. </li>
                            </ul>"""
        return res
    

class PurchaseRerquestLineInherited(models.Model):
    _inherit = 'purchase.request.line'

    minimum_stock_level = fields.Float('Minimum Stock Level')
    forecasting_stock = fields.Float('Forecasting Stock')
    on_hand_qty = fields.Float('On Hand Quantity')
    
    
    @api.onchange('product_id')
    def _on_change_product_id(self):
        for rec in self:
            
            order = rec.env['stock.warehouse.orderpoint'].search([('product_id', '=', rec.product_id.id)])
            # Search for the stock quant for the product
            quant = rec.env['stock.quant'].search([('product_id', '=', rec.product_id.id), ('location_id.usage', '=', 'internal')])
            
            # If a warehouse orderpoint is found
            if rec.product_id:
                if rec.product_id == order.product_id:
                    # Set minimum stock level and forecasting stock from orderpoint
                    rec['minimum_stock_level'] = order.product_min_qty
                    rec['forecasting_stock'] = order.qty_forecast

            # If a stock quant is found in an internal location
            if quant:
                for quan in quant:
                    if rec.product_id == quan.product_id:
                        # Set on hand quantity from quant
                        rec['on_hand_qty'] = quan.inventory_quantity_auto_apply



class QualityCheckInherited(models.Model):
    _inherit = "quality.check"

    methods = fields.Char(string="Method")


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    delivery_address = fields.Char(string="Delivery Address", compute="_compute_delivery_address", readonly=False)

    def _compute_delivery_address(self):
        for record in self:
            record.delivery_address = record.partner_id.contact_address


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

   
    discount = fields.Float(string="Discount (%)", compute="_compute_discount_percentage", store=True)
    discount_in_amount = fields.Float(string="Discount in Amount")


    @api.depends('discount_in_amount', 'price_unit', 'product_uom_qty', 'tax_id')
    def _compute_discount_percentage(self):
        for line in self:
            subtotal = (line.price_unit * line.product_uom_qty)  
            if subtotal > 0:
                line.discount = (line.discount_in_amount / subtotal) * 100
            else:
                line.discount = 0.0
    # @api.depends('price_unit', 'product_uom_qty', 'discount_in_amount', 'tax_id')
    # def _compute_amount(self):
    #     for line in self:
    #         super(SaleOrderLineInherit, line)._compute_amount()  
    #         line['discount'] = (line.discount_in_amount/line.price_subtotal)*100
