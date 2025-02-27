from odoo import http
# import xlwt
import xlsxwriter
import io
import datetime
# from odoo.exceptions import 
from odoo.exceptions import UserError


class InventoryAgingController(http.Controller):
    
    @http.route('/inventoryaging_lot/excel', type='http', auth='user')
    def generate_excel_report(self,product_ids,category_ids,location_ids,lot_ids, date_from, date_to):
        # try:
            
            query = (f"""
                     
                        SELECT 
                     -- distinct
                    product,
                    uom,
                    cost,
                    category,
                    location,
                    style,
                    current_stock,
                    SUM(sq.x_studio_value) AS total_value,
                    SUM(sq.quantity) AS total_quantity,
                    -- Quantity breakdown by days
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) = 0 THEN sq.quantity
                        ELSE 0
                    END) AS "0_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 1 AND 30 THEN sq.quantity
                        ELSE 0
                    END) AS "1-30_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 31 AND 60 THEN sq.quantity
                        ELSE 0
                    END) AS "31-60_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 61 AND 90 THEN sq.quantity
                        ELSE 0
                    END) AS "61-90_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 91 AND 120 THEN sq.quantity
                        ELSE 0
                    END) AS "91-120_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 121 AND 150 THEN sq.quantity
                        ELSE 0
                    END) AS "121-150_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 151 AND 180 THEN sq.quantity
                        ELSE 0
                    END) AS "151-180_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 181 AND 270 THEN sq.quantity
                        ELSE 0
                    END) AS "181-270_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 271 AND 365 THEN sq.quantity
                        ELSE 0
                    END) AS "271-365_days_quantity",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) > 365 THEN sq.quantity
                        ELSE 0
                    END) AS "more_than_365_days_quantity",

                    -- Value breakdown by days
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) = 0 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "0_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 1 AND 30 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "1-30_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 31 AND 60 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "31-60_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 61 AND 90 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "61-90_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 91 AND 120 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "91-120_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 121 AND 150 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "121-150_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 151 AND 180 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "151-180_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 181 AND 270 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "181-270_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) BETWEEN 271 AND 365 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "271-365_days_value",
                    SUM(CASE 
                        WHEN DATE_PART('day', CURRENT_DATE - sq.create_date) > 365 THEN sq.x_studio_value
                        ELSE 0
                    END) AS "more_than_365_days_value"

                    FROM 
                    (SELECT 
                        sq.product_id,
                        (SELECT SUM(sqq.quantity) 
                        FROM stock_quant sqq 
                        WHERE sqq.inventory_date IS NOT NULL 
                        AND sqq.product_id = sq.product_id and sqq.lot_id = sq.lot_id) AS current_stock,
                        pt.name ->> 'en_US' AS product,
                        pc.name as category,
                        st.complete_name as location,
                        prop.value_float as cost,
                        uom.name ->> 'en_US' as uom,
                        sq.create_date,
                        sl.name as style,
                        sq.quantity,
                        sq.x_studio_value  -- Make sure sq.x_studio_value exists here
                    FROM 
                        stock_quant sq
                    INNER JOIN 
                        product_product pp ON sq.product_id = pp.id 
                    INNER JOIN 
                        product_template pt ON pp.product_tmpl_id = pt.id
                    INNER JOIN 
                        product_category pc ON pt.categ_id = pc.id
                    INNER JOIN 
                        stock_location st ON sq.location_id = st.id
                    left JOIN 
                        ir_property prop ON prop.res_id = 'product.product,' || pp.id 
                    INNER JOIN 
                        uom_uom uom ON pt.uom_id = uom.id
					left join 
                        stock_lot sl on sl.id = sq.lot_id
                    WHERE 
                        st.usage = 'internal'
                    
                """)
            



            env = http.request.env
            if date_from != False and date_to != False:
                
                query += " AND sq.create_date >= '%s' AND sq.create_date <= '%s'" % (date_from,date_to)

            product_name_list = ""
            if product_ids and product_ids!='[]':
                product_ids_str = product_ids.split('[')[-1].split(']')[0]
                products = env['product.product'].browse(int(product_ids_str))
                product_names = {product.id: product.display_name for product in products}
                product_name_list = list(product_names.values())
                query += " and sq.product_id in (%s)" % product_ids_str

            category_name_list = ""
            if category_ids and category_ids!='[]':
                category_ids_str = category_ids.split('[')[-1].split(']')[0]
                category = env['product.category'].browse(int(category_ids_str))
                category_names = {category.id: category.display_name for category in category}
                category_name_list = list(category_names.values())
                
                query += " AND pc.id in (%s)" % category_ids_str
            location_name_list = ""
            if location_ids and location_ids!='[]':
                location_ids_str = location_ids.split('[')[-1].split(']')[0]
                locations = env['stock.location'].browse(int(location_ids_str))
                location_names = {location.id: location.display_name for location in locations}
                location_name_list = list(location_names.values())
                query += " AND st.id in (%s)" % location_ids_str
            lot_name_list = ""
            if lot_ids and lot_ids!='[]':
                lot_ids_str = lot_ids.split('[')[-1].split(']')[0]

                lots = env['stock.lot'].browse(int(lot_ids_str))
                lot_names = {lot.id: lot.display_name for lot in lots}
                lot_name_list = list(lot_names.values())

                query += " AND sl.id in (%s)" % lot_ids_str





            query += """ ) AS sq
                    GROUP BY product, style, current_stock,
                    category, location, cost, uom;"""
            env.cr.execute(query)
            records = env.cr.dictfetchall()

            # env.cr.execute(query)
            # records = env.cr.dictfetchall()

            # data=env.cr.fetchall()
            """
            worksheet.write(ROW, COLUMN, VALUE)

            """
            # raise UserError(len(records))
            output = io.BytesIO()
            # workbook.value
            workbook = xlsxwriter.Workbook(output, {'in_memory': False})
            worksheet = workbook.add_worksheet()
            # worksheet.fo
            
            merge_format = workbook.add_format(
                        {
                            "bold": 1,
                            "border": 1,
                            "align": "center",
                            "valign": "vcenter",
                            "fg_color": "gray",
                            # "font_color": 'red'
                        }
                    )
            merge_format2 = workbook.add_format(
                        {
                            "bold": 1,
                            "border": 1,
                            "align": "center",
                            "valign": "vcenter",

                        }
                    )
            

            # Header for the Inventory Age Breakdown Report
            worksheet.merge_range("A1:AA2", "Inventory Age Breakdown Report", merge_format)

            # Product, Category, and Location Filters
            worksheet.merge_range('B4:C4', 'Products', merge_format)
            if product_ids and product_ids != "[]":
                worksheet.merge_range('D4:F4', str(product_name_list), merge_format2)

            worksheet.merge_range('G4:H4', 'Category', merge_format)
            if category_ids and category_ids != "[]":
                worksheet.merge_range('I4:K4', str(category_name_list), merge_format2)

            worksheet.merge_range('L4:M4', 'Location', merge_format)
            if location_ids and location_ids != "[]":
                worksheet.merge_range('N4:O4', str(location_name_list), merge_format2)

            worksheet.merge_range('P4:Q4', 'Lots/Serial', merge_format)
            if lot_ids and lot_ids != "[]":
                worksheet.merge_range('S4:T4', str(lot_name_list), merge_format2)



            # Table headers
            worksheet.write('A7', 'Product Name', merge_format2)
            worksheet.write("B7", "Product Category", merge_format)
            worksheet.write("C7", "Lot/Style", merge_format2)
            worksheet.write("D7", "Style", merge_format)  # New column for Style
            worksheet.write("E7", "Location", merge_format)
            worksheet.write("F7", "UOM", merge_format2)
            worksheet.write("G7", "Total Quantity", merge_format)
            worksheet.write("H7", "Total Value", merge_format2)


            # Add merged headers for day-based breakdown
            worksheet.merge_range("I7:J7", "0 Days", merge_format)        # Columns I-J
            worksheet.write("I8", "Qty", merge_format)                   # Column I
            worksheet.write("J8", "Value", merge_format)                 # Column J

            worksheet.merge_range("K7:L7", "1 to 30 Days", merge_format2) # Columns K-L
            worksheet.write("K8", "Qty", merge_format2)                  # Column K
            worksheet.write("L8", "Value", merge_format2)                # Column L

            worksheet.merge_range("M7:N7", "31 to 60 Days", merge_format) # Columns M-N
            worksheet.write("M8", "Qty", merge_format)                   # Column M
            worksheet.write("N8", "Value", merge_format)                 # Column N

            worksheet.merge_range("O7:P7", "61 to 90 Days", merge_format2)# Columns O-P
            worksheet.write("O8", "Qty", merge_format2)                  # Column O
            worksheet.write("P8", "Value", merge_format2)                # Column P

            worksheet.merge_range("Q7:R7", "91 to 120 Days", merge_format)# Columns Q-R
            worksheet.write("Q8", "Qty", merge_format)                   # Column Q
            worksheet.write("R8", "Value", merge_format)                 # Column R

            worksheet.merge_range("S7:T7", "121 to 150 Days", merge_format2)# Columns S-T
            worksheet.write("S8", "Qty", merge_format2)                  # Column S
            worksheet.write("T8", "Value", merge_format2)                # Column T

            worksheet.merge_range("U7:V7", "151 to 180 Days", merge_format)# Columns U-V
            worksheet.write("U8", "Qty", merge_format)                   # Column U
            worksheet.write("V8", "Value", merge_format)                 # Column V

            worksheet.merge_range("W7:X7", "181 to 270 Days", merge_format2)# Columns W-X
            worksheet.write("W8", "Qty", merge_format2)                  # Column W
            worksheet.write("X8", "Value", merge_format2)                # Column X

            worksheet.merge_range("Y7:Z7", "271 to 365 Days", merge_format)# Columns Y-Z
            worksheet.write("Y8", "Qty", merge_format)                   # Column Y
            worksheet.write("Z8", "Value", merge_format)                 # Column Z

            worksheet.merge_range("AA7:AB7", "More than 365 Days", merge_format2)# Columns AA-AB
            worksheet.write("AA8", "Qty", merge_format2)                 # Column AA
            worksheet.write("AB8", "Value", merge_format2)               # Column AB

            # Set the column widths dynamically
            product_name_len = len('Product Name')
            category_name_len = len("Product Category")
            lot_style_len = len("Lot/Style")
            style_len = len("Style")
            location_len = len("Location")
            uom_len = len("UOM")
            total_qty_len = len("Total Quantity")
            total_value_len = len("Total Value")



            # # Iterate through records and write the data
            for row, record in enumerate(records, start=9):
                worksheet.write(f'A{row}', record['product'])                # Column A
                worksheet.write(f'B{row}', record['category'])               # Column B
                worksheet.write(f'C{row}', record['style'])              # Column C
                worksheet.write(f'D{row}', record['total_value'])                  # Column D (New)
                worksheet.write(f'E{row}', record['location'])               # Column E
                worksheet.write(f'F{row}', record['uom'])                    # Column F
                worksheet.write(f'G{row}', record['total_quantity'])         # Column G
                worksheet.write(f'H{row}', record['total_value'])            # Column H

                worksheet.write(f'I{row}', record['0_days_quantity'])         # Column I
                worksheet.write(f'J{row}', record['0_days_value'])           # Column J

                worksheet.write(f'K{row}', record['1-30_days_quantity'])     # Column K
                worksheet.write(f'L{row}', record['1-30_days_value'])        # Column L

                worksheet.write(f'M{row}', record['31-60_days_quantity'])    # Column M
                worksheet.write(f'N{row}', record['31-60_days_value'])       # Column N

                worksheet.write(f'O{row}', record['61-90_days_quantity'])    # Column O
                worksheet.write(f'P{row}', record['61-90_days_value'])       # Column P

                worksheet.write(f'Q{row}', record['91-120_days_quantity'])   # Column Q
                worksheet.write(f'R{row}', record['91-120_days_value'])      # Column R

                worksheet.write(f'S{row}', record['121-150_days_quantity'])  # Column S
                worksheet.write(f'T{row}', record['121-150_days_value'])     # Column T

                worksheet.write(f'U{row}', record['151-180_days_quantity'])  # Column U
                worksheet.write(f'V{row}', record['151-180_days_value'])     # Column V

                worksheet.write(f'W{row}', record['181-270_days_quantity'])  # Column W
                worksheet.write(f'X{row}', record['181-270_days_value'])     # Column X

                worksheet.write(f'Y{row}', record['271-365_days_quantity'])  # Column Y
                worksheet.write(f'Z{row}', record['271-365_days_value'])     # Column Z

                worksheet.write(f'AA{row}', record['more_than_365_days_quantity']) # Column AA
                worksheet.write(f'AB{row}', record['more_than_365_days_value'])   # Column AB


            # Adjust column widths
            worksheet.set_column(0, 0, max(product_name_len, len('Product Name')))
            worksheet.set_column(1, 1, max(category_name_len, len('Product Category')))
            worksheet.set_column(2, 2, max(lot_style_len, len('Lot/Style')))
            worksheet.set_column(3, 3, max(style_len, len('Style')))
            worksheet.set_column(4, 4, max(location_len, len('Location')))
            worksheet.set_column(5, 5, max(uom_len, len('UOM')))
            worksheet.set_column(6, 6, total_qty_len)
            worksheet.set_column(7, 7, total_value_len)

            workbook.close()
            #region DO NOT TOUCH
            output.seek(0)

            response = http.request.make_response(output.read(), 
                                                headers=[
                                                    ("content_type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                                                    ("Content-Disposition","attachment; filename=inventory-aging.xlsx")
                                                    ])
            

            output.close()

            return response
        # except Exception as e:
            
            # raise UserError(str(e))
        

