from odoo import fields, models, api
from odoo.exceptions import UserError



class ResPartnerInherited(models.Model):
    _inherit = "res.partner"

    legal_status = fields.Selection([('individual', 'Individual'), ('partnership', 'Partnership'), ('aop', 'AOP'), ('company', 'Company')], required = True)
    company_reg = fields.Char("Company Registration", required = True)
    artical = fields.Char("Article of Association and Memorandom", required = True)
    strn_no = fields.Char("STRN", required = True)
    cnic_no = fields.Char("CNIC Number", required = True)
    vendor_status = fields.Selection([('active', 'Active'), ('non_active', 'Non Active')], string = "Active Status")
    major_client = fields.Selection([('a','A Category'), ('b', 'B Category'), ('c', 'C Category')]) 
    region_id = fields.Many2one('res.customer.region',string="Region",domain=[('type','=','region')])
    sub_region_id = fields.Many2one('res.customer.region',string="Sub-Region",domain=[('type','=','sub-region')])
    status = fields.Selection([('DISTRIBUTOR','DISTRIBUTOR'), ('DEALER', 'DEALER'), ('W.SELLER', 'W.SELLER'), ('WHOLESELLER', 'WHOLESELLER')]) 
    town = fields.Char(string="Town")
    

class ResPartnerBankInherited(models.Model):
    
    _inherit = "res.partner.bank"
    
    bank_iban_num = fields.Char('IBAN Number')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.constrains('product_id')
    def _onchange_product_category(self):
        user_category = self.env.user.x_studio_category.id
        
        if user_category:
            if self.product_id.product_tmpl_id.x_studio_category.id == user_category:
                pass
            else:
                raise UserError("The product category does not match your assigned category. Please review.")




class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)', default=10.00)


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    sampling_id = fields.Char(string="Sampling ID")
    sampling_time = fields.Char(string="Sampling Time (hrs)")
    test_report_no = fields.Char(string="Test Report No.")
    vendor_id = fields.Many2one('res.partner', string="Vendor", compute="_compute_vendor", store=True)
    
    def button_validate(self):
            for rec in self:
                if rec.picking_type_id.id == 41 and rec.location_id.id == 369:
                    if self.env.user.id not in [134, 133]:
                        raise UserError("You are not allowed to validate transfers from Quarantine location.")

            return super().button_validate() 

    @api.depends('origin')
    def _compute_vendor(self):
        for rec in self:
            vendor = False
            if rec.origin:
                po = self.env['purchase.order'].search([('name', '=', rec.origin)], limit=1)
                if po:
                    vendor = po.partner_id
            rec.vendor_id = vendor



class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    # sampling_id = fields.Char(string="Sampling ID")
    # sampling_time = fields.Char(string="Sampling Time (hrs)")  # You can use Float if you want numeric input
    # test_report_no = fields.Char(string="Test Report No.")
    # vendor_id = fields.Many2one('res.partner', string="Vendor", compute="_compute_vendor", store=True)

    # @api.depends('origin')
    # def _compute_vendor(self):
    #     for rec in self:
    #         vendor = False
    #         if rec.origin:
    #             po = self.env['purchase.order'].search([('name', '=', rec.origin)], limit=1)
    #             if po:
    #                 vendor = po.partner_id
    #         rec.vendor_id = vendor

    # @api.constrains('location_id')
    # def check_user_location_access(self):
    #     for rec in self:
    #         allowed_locations = rec.env.user.x_studio_location.ids  
    #         if allowed_locations and rec.location_id.id not in allowed_locations:
    #             raise UserError("This Location is not accessible for you.")



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

    due_date = fields.Date(string="Due Date")
    
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
    salesperson = fields.Char(string="Salesperson")
    source_location = fields.Many2one('stock.location',string="Source Location")

    def _compute_delivery_address(self):
        for record in self:
            record.delivery_address = record.partner_id.contact_address

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        
        for order in self:
            if order.source_location:
                for picking in order.picking_ids:
                    picking.location_id = order.source_location.id
                    for line in picking.move_ids_without_package:
                        line.location_id = order.source_location.id
        return res


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



class CustomerRegion(models.Model):
    _name = "res.customer.region"
    
    name = fields.Char(string="Name",required=True)
    type = fields.Selection([('region','Region'),('sub-region','Sub-Region')],required=True)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                    string="Company",
                                    default=lambda self: self.env.user.company_id.id)

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approved_by = fields.Many2many(
        'res.partner',
        string='Approved By',
        help="Users who have approved this order."
    )

    can_approve = fields.Boolean(
        string="Can Approve",
        compute="_compute_can_approve",
        store=False
    )

    is_fully_approved = fields.Boolean(
        string="Fully Approved",
        compute="_compute_fully_approved",
        store=True
    )

    @api.depends_context('uid')
    def _compute_can_approve(self):
        """Compute if the current user can approve."""
        approved_users = ['Amanullah Khan', 'Fahad Humayoun']
        current_user = self.env.user.partner_id.name
        for order in self:
            order.can_approve = current_user in approved_users

    @api.depends('approved_by')
    def _compute_fully_approved(self):
        """Check if both Amanullah and Fahad have approved."""
        required_approvals = {'Amanullah Khan', 'Fahad Humayoun'}
        for order in self:
            approved_names = set(order.approved_by.mapped('name'))
            order.is_fully_approved = required_approvals.issubset(approved_names)

    def action_approve_order(self):
        """Ensure Amanullah approves first, then Fahad."""
        approval_sequence = ['Amanullah Khan', 'Fahad Humayoun']
        current_user = self.env.user.partner_id

        # Check if the user is allowed to approve
        if current_user.name not in approval_sequence:
            raise UserError(_(f"{current_user.name}: Only Amanullah and Fahad can approve this order."))

        # Get the names of already approved users
        approved_names = self.approved_by.mapped('name')

        # Enforce approval sequence: Amanullah first, then Fahad
        if current_user.name == 'Fahad Humayoun' and 'Amanullah Khan' not in approved_names:
            raise UserError(_("Fahad cannot approve before Amanullah."))

        # If not already approved, add the user to `approved_by`
        if current_user not in self.approved_by:
            self.write({'approved_by': [(4, current_user.id)]})

        approved_names = ", ".join(self.approved_by.mapped('name'))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Approval"),
                'message': _("%s has approved the order." % approved_names),
                'sticky': False,
                'type': 'success',
            }
        }
    
    def action_confirm(self):
        """Confirm order only if both Amanullah and Fahad have approved."""
        exempt_users = ['Administrator', 'Muskan', 'Sana Humayoun','Ali','Azfar Hussain','Bakhtawar','Syed Shahid','Qaiser Mehmood']
        current_user = self.env.user.partner_id.name

        # If the current user is Admin, Muskan, or Asfar, bypass the approval check
        if current_user in exempt_users:
            return super(SaleOrder, self).action_confirm()

        # If not an exempt user, check approval status
        if not self.is_fully_approved:
            raise UserError(_("The order cannot be confirmed until both Amanullah and Fahad have approved it."))

        return super(SaleOrder, self).action_confirm()
    

    
class InheritQualityCheckWizard(models.TransientModel):
    _inherit = 'quality.check.wizard'

    tolerance_min = fields.Float(
        related='current_check_id.point_id.tolerance_min',        
        readonly=True
    )
    tolerance_max = fields.Float(
        related='current_check_id.point_id.tolerance_max',        
        readonly=True
    )
        