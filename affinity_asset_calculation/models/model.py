from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from datetime import datetime
import qrcode
import base64
from io import BytesIO


class AccountMove(models.Model):
    _inherit = "account.move"

    custom_depreciation = fields.Float(string="Custom Depreciation Calculation")

    @api.depends(
        "asset_id",
        "depreciation_value",
        "asset_id.total_depreciable_value",
        "asset_id.already_depreciated_amount_import",
    )
    def _compute_depreciation_cumulative_value(self):
        for i in self:
            if i.asset_remaining_value == 0:
                for asset in i.asset_id:
                    depri = 0
                    deprication = asset.original_value - asset.salvage_value
                    method = asset.method_progress_factor
                    # if asset.state == 'draft':
                    for move in asset.depreciation_move_ids.sorted(
                        lambda mv: (mv.date, mv._origin.id)
                    ):
                        depri += deprication * (method / 12)
                        if (
                            asset.depreciation_move_ids.sorted(
                                lambda mv: (mv.date, mv._origin.id)
                            )[-1]
                            == move
                        ):
                            # move.depreciation_value = ((deprication / 12) / method)
                            move.asset_depreciated_value = depri
                            move.asset_remaining_value = 0
                        else:
                            # move.depreciation_value = ((deprication / 12) / method)
                            move.asset_remaining_value = deprication
                            move.asset_depreciated_value = depri
                            deprication = round(
                                (deprication - (deprication * (method / 12))), 2
                            )
                    # else:
                    #     i.asset_remaining_value = i.asset_remaining_value
                    #     i.asset_depreciated_value = i.asset_depreciated_value


class AccountAsset(models.Model):
    _inherit = "account.asset"

    serial_no = fields.Char(string="Serial No")
    model_part_no = fields.Char(string="Model Part No")
    owner_company = fields.Char(string="Owner/Company Name")
    quantity = fields.Float(string="Quantity")
    purchase_lease_details = fields.Char(string="Purchase Lease Details")
    # location_id = fields.Char(string="Location")
    location_name = fields.Char(string="Location")
    location_id = fields.Many2one("account.asset.location", string="Location")
    department_id = fields.Many2one("hr.department", string="Department")
    brand_id = fields.Many2one("account.asset.brand", string="Brand")
    category_id = fields.Many2one("account.asset.category", string="Category")
    responsible_person = fields.Many2one("hr.employee", string="Responsible Person")
    vendor_id = fields.Many2one("res.partner", string="Vendor")
    warranty_id = fields.Many2one("account.asset.warranty", string="Warranty")
    qrcode = fields.Binary(string="QR code")

    def _recompute_board(self, start_depreciation_date=False):
        new_depreciation_moves_data = super(AccountAsset, self)._recompute_board()
        deprication = self.original_value - self.salvage_value
        method = self.method_progress_factor
        self['qrcode'] = self.generateCode()
        for i in new_depreciation_moves_data:
            if i == new_depreciation_moves_data[-1]:
                i.update(
                    {
                        "depreciation_value": (deprication * (method / 12)),
                    }
                )
            else:
                i.update(
                    {
                        "depreciation_value": (deprication * (method / 12)),
                    }
                )
            deprication = round((deprication - (deprication * (method / 12))), 2)

        return new_depreciation_moves_data

    def generateCode(self, data=False):
        for i in self:
            if not data:
                data = {
                    "Asset Name": self.name,
                    "Asset ID": self.id,
                    "Asset Location": (
                        self.location_id.id if self.location_id else "None"
                    ),
                    "Asset Value": self.original_value,
                }
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue())


class AccountAssetLocations(models.Model):
    _name = "account.asset.location"

    name = fields.Char(string="Name")
    parent_location_id = fields.Many2one(
        "account.asset.location", string="Parent Locations"
    )


class AccountAssetBrand(models.Model):
    _name = "account.asset.brand"

    name = fields.Char(string="Name")


class AccountAssetCategory(models.Model):
    _name = "account.asset.category"

    name = fields.Char(string="Name")


class AccountAssetWarranty(models.Model):
    _name = "account.asset.warranty"

    name = fields.Char(string="Name")
    warranty_from = fields.Date(string="Start Date")
    warranty_to = fields.Date(string="End Date")
    details = fields.Char(string="Details")
