from odoo import models, fields, api
from datetime import datetime, timedelta


class wizard_challenge(models.TransientModel):
    _name = 'game.wizard_challenge'

    name = fields.Char()
    player = fields.Many2one('res.partner')

    def _default_player(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))

    nombre = fields.Char(required=True)
    start_date = fields.Datetime(default=fields.Datetime.now)
    end_date = fields.Datetime(default=lambda d: fields.Datetime.to_string(datetime.now() + timedelta(hours=48)))
    finished = fields.Boolean(default=False)
    player_1 = fields.Many2one('res.partner', default=_default_player, domain="[('is_player', '=', True)]", ondelete='restrict', readonly=True)
    player_2 = fields.Many2one('res.partner', ondelete='restrict', domain="[('is_player', '=', True)]")
    isla_1 = fields.Many2one('game.isla', ondelete='restrict')
    isla_2 = fields.Many2one('game.isla', ondelete='restrict')
    ### Challenge objective
    recurso = fields.Selection(
        [('madera', 'Madera'), ('bronce', 'Bronce'), ('hirro', 'Hierro'), ('plata', 'Plata'), ('oro', 'Oro'),
         ('adamantium', 'Adamantium')], required=True)
    target_goal = fields.Float()
    cantidad = fields.Float(required=True)
    #winner = fields.Many2one('res.partner', ondelete='restrict', readonly=True)

    player_1_avatar = fields.Image(related='player_1.photo')
    player_2_avatar = fields.Image(related='player_2.photo')
    isla_1_image = fields.Image(related='isla_1.photo')
    isla_2_image = fields.Image(related='isla_2.photo')

    state = fields.Selection([('global', 'Global'),
                              ('jugadores', 'Jugadores')],
                             default='global')

    def crear_combate(self):
        self.env['game.challenge'].create({
            'nombre': self.nombre,
            'player_1': self.player_1.id,
            'player_2': self.player_2.id,
            'isla_1': self.isla_1.id,
            'isla_2': self.isla_2.id
        })

    @api.onchange('player_1')
    def _onchange_player1(self):
        if self.player_2:
            if self.player_1.id == self.player_2.id:
                self.player_1 = False
                return {
                    'warning': {
                        'title': "Players must be different",
                        'message': "Player 1 is the same as Player 2",
                    }
                }
        return {
            'domain': {'isla_1': [('player', '=', self.player_1.id)],
                       'player_2': [('id', '!=', self.player_1.id)]},
        }

    @api.onchange('player_2')
    def _onchange_player2(self):
        if self.player_1:
            if self.player_1.id == self.player_2.id:
                self.player_2 = False
                return {
                    'warning': {
                        'title': "Players must be different",
                        'message': "Player 1 is the same as Player 2",
                    }
                }
        return {
            'domain': {'isla_2': [('player', '=', self.player_2.id)],
                       'player_1': [('id', '!=', self.player_2.id)]},
        }

    def next(self):
        if self.state == 'global':
            self.state = 'jugadores'
        return {
            'name': "Challenge Wizard",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.wizard_challenge',
            'res_id': self.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def previous(self):
        if self.state == 'jugadores':
            self.state = 'global'
        return {
            'name': "Challenge Wizard",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.wizard_challenge',
            'res_id': self.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }





