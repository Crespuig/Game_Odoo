from odoo import models, fields, api
# herència de classe
from odoo.exceptions import ValidationError



class player_premium(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'Player Premium'
    # Main fields
    is_premium = fields.Boolean()

    def _get_consume_recursos(self):
        for c in self:
            super(player_premium, self)._get_consume_recursos()
            if c.isla.madera < 200 or c.isla.bronce < 100 or c.isla.hierro < 50 or c.isla.plata < 25 or c.isla.oro < 10 or c.isla.adamantium < 5:
                raise ValidationError("No hay suficientes recursos para construir el barco en esta isla")

