from odoo import models, fields, api
# herència de classe
class player_premium(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'Player Premium'
    # Main fields
    is_premium = fields.Boolean()

    def _get_duracion_viaje(self):
        for t in self:
            super(player_premium, self)._get_duracion_viaje()
            t.duracion_viaje = ((((t.destino_isla.pos_x - t.origen_isla.pos_x) ** 2) + (
                    (t.destino_isla.pos_y - t.origen_isla.pos_y) ** 2)) ** 0.5)

            if t.duracion_viaje < 50:
                t.duracion_viaje = 50