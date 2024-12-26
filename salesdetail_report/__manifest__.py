{
    'name': 'Sales Detail Report',
    # 'version': '14.0.1',
    'version': '17.0.1.0.0',

    'depends': ['base','sale'],
    
    'data': [
             'wizard/wizard.xml',
             'security/ir.model.access.csv',
             'report/report.xml',
             'report/report_template.xml',

             ],
    
    # "images" : [
    #          'img/header.png'
    #          'img/footer.jpeg'
    #         #  'static/description/footer.jpeg',
    #             ],
    
    'installable': True,
    'auto_install': False,
    'application': False,
}




# <?xml version="1.0" encoding="utf-8"?>
# <odoo>
#     <template id="salesdetail_reports">
#         <t t-call="web.html_container">
#             <t t-call="web.external_layout">
#                 <div class="page" style="font-family:Segoe UI;">
#                     <div class="row mt-5 mb-3">
#                         <div class="col-12">
#                             <table style="border-collapse:collapse;" class="table-bordered">
#                                 <thead>
#                                     <tr>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:100px; background-color:#A9A9A9;">Registration No.</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Name</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Invoice Type</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Invoice No</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:200px; background-color:#A9A9A9;">Invoice Date</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">HS Code</th>
                                        
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Rate</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Quantity</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:200px; background-color:#A9A9A9;">Value of Sales Excl. ST</th>
#                                         <th style="text-align:left;border-bottom:1px solid black;padding:10px;width:400px; background-color:#A9A9A9;">Sales Tax/ FED in ST Mode</th>
#                                     </tr>
#                                 </thead>
#                                 <tbody>
#                                     <t t-set="total_quantity" t-value="0"/>
#                                     <t t-set="total_exclamount" t-value="0"/>
#                                     <t t-set="total_tax" t-value="0"/>

#                                     <t t-foreach="data" t-as="value">
#                                         <t t-set="total_quantity" t-value="total_quantity + value['quantity']"/>
#                                         <t t-set="total_exclamount" t-value="total_exclamount + value['exclamount']"/>
#                                         <t t-set="total_tax" t-value="total_tax + value['tax']"/>
#                                     </t>

#                                     <t t-foreach="data" t-as="value">                                        
#                                         <tr>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['registration']"/></td>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['name']"/></td>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['type']"/></td>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['invno']"/></td>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['invdate']"/></td>
#                                             <td style="text-align:left; padding:4px;"><span t-esc="value['code']"/></td>
#                                             <td style="text-align:right; padding:4px;">
#                                                 <!-- <span t-esc="value['code']"/> -->
#                                             </td>
#                                             <td style="text-align:right; padding:4px;"><span t-esc="value['quantity']"/></td>
#                                             <td style="text-align:right; padding:4px;"><span t-esc="value['exclamount']"/></td>
#                                             <td style="text-align:right; padding:4px;"><span t-esc="value['tax']"/></td>                                                                            
#                                         </tr>
#                                     </t>

#                                     <tr> 
#                                         <td colspan="7" class="total-cell" style="text-align:right; padding:4px;">
#                                             <b>Totals</b>
#                                         </td>
#                                         <td class="total-cell" style="text-align:right; padding:4px;">
#                                             <b><span t-esc="total_quantity" t-options="{&quot;widget&quot;: &quot;float&quot;, &quot;precision&quot;: 2, &quot;thousands_sep&quot;: &quot;,&quot;}"/></b>
#                                         </td>
#                                         <td class="total-cell" style="text-align:right; padding:4px;">
#                                             <b><span t-esc="total_exclamount" t-options="{&quot;widget&quot;: &quot;float&quot;, &quot;precision&quot;: 2, &quot;thousands_sep&quot;: &quot;,&quot;}"/></b>
#                                         </td>
#                                         <td class="total-cell" style="text-align:right; padding:4px;">
#                                             <b><span t-esc="total_tax" t-options="{&quot;widget&quot;: &quot;float&quot;, &quot;precision&quot;: 2, &quot;thousands_sep&quot;: &quot;,&quot;}"/></b>
#                                         </td>
#                                     </tr>
#                                 </tbody>

#                             </table>
#                         </div>
#                     </div>
                    
#                 </div>
#             </t>
#         </t>

#     </template>
# </odoo>
