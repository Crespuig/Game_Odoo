from odoo import models, fields, api
import random
import string


def name_generator(self):
    letters = list(string.ascii_lowercase)
    first = list(string.ascii_uppercase)
    vocals = ['a','e','i','o','u','y','']
    name = random.choice(first)
    for i in range(0,random.randint(3,5)):
        name = name+random.choice(letters)+random.choice(vocals)
    return name

def image_generator(self):
    images = self.env['game.template'].search([]).mapped('photo')
    image = random.choice(images)

    return image

class wizard_isla(models.TransientModel):
    _name = 'game.wizard_isla'

    name = fields.Char(default=name_generator, required=True)
    player = fields.Many2one('res.partner', domain="[('is_player', '=', True)]")
    #n_isla = fields.Integer()

    def _default_archipielago(self):
        return self.env['game.archipielago'].browse(self._context.get('active_id'))

    archipielago = fields.Many2one('game.archipielago', default=_default_archipielago, readonly=True)
    image = fields.Image(max_width=200, max_height=200)
    madera = fields.Integer()
    bronce = fields.Integer()
    hierro = fields.Integer()
    plata = fields.Integer()
    oro = fields.Integer()
    adamantium = fields.Integer()

    state = fields.Selection([('global', 'Global'),
                              ('enviroment', 'Recursos')],
                             default='global')
    '''
    @api.depends('archipielago')
    def get_n_isla(self):
        if self.archipielago:
            n_isla = max(self.archipielago.islas.mapped('n_isla')) + 1
            self.n_isla = n_isla
    '''


    @api.onchange('templates')
    def onchange_template(self):
        img = self.template.image
        self.image = img
        print(img)

    @api.onchange('name')
    def onchange_name(self):
        name = self.name
        if len(self.env['game.isla'].search([('name', '=', name)])) > 0:
            self.name = name + "_new"
            return (
            {'warning': {'title': "Name Repeated", 'message': "The name is repeated", 'type': 'notification'}, })


    def next(self):
        if self.state == 'global':
            self.state = 'enviroment'
        return {
            'name': "Isla Wizard",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.wizard_isla',
            'res_id': self.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def previous(self):
        if self.state == 'enviroment':
            self.state = 'global'
        return {
            'name': "Isla Wizard",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.wizard_isla',
            'res_id': self.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def crear_isla(self):
        nueva_isla = {}
        nueva_isla['name'] = self.name
        nueva_isla['player'] = self.player.id
        nueva_isla['photo'] = self.image
#        nueva_isla['n_isla'] = self.n_isla
        nueva_isla['archipielago'] = self.archipielago.id
        nueva_isla['madera'] = self.madera
        nueva_isla['bronce'] = self.bronce
        nueva_isla['hierro'] = self.hierro
        nueva_isla['plata'] = self.plata
        nueva_isla['oro'] = self.oro
        nueva_isla['adamantium'] = self.adamantium

        isla = self.env['game.isla'].create(nueva_isla)

        return {
            'name': 'Nueva Isla',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.isla',
            'res_id': isla.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }







