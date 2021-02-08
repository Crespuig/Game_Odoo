from odoo import models, fields, api

class cambios_isla(models.Model):
    _name = 'game.cambios_isla'
    _description = 'Cambios en las islas durante un periodo de tiempo'

    name = fields.Char()
    isla = fields.Many2one('game.isla', ondelete='cascade', required=True)
    time = fields.Char()

    madera = fields.Integer()
    bronce = fields.Integer()
    hierro = fields.Integer()
    plata = fields.Integer()
    oro = fields.Integer()
    adamantium = fields.Integer()


    madera_reduction = fields.Integer(digits=(12, 4))
    madera_increment = fields.Integer(digits=(12, 4))

    bronce_reduction = fields.Integer(digits=(12, 4))
    bronce_increment = fields.Integer(digits=(12, 4))

    hierro_reduction = fields.Integer(digits=(12, 4))
    hierro_increment = fields.Integer(digits=(12, 4))

    plata_reduction = fields.Integer(digits=(12, 4))
    plata_increment = fields.Integer(digits=(12, 4))

    oro_reduction = fields.Integer(digits=(12, 4))
    oro_increment = fields.Integer(digits=(12, 4))

    adamantium_reduction = fields.Integer(digits=(12, 4))
    adamantium_increment = fields.Integer(digits=(12, 4))
