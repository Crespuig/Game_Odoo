# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'game.game'
    _description = 'Game'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float()
    description = fields.Text()

class player(models.Model):
    _name = 'game.player'
    _description = 'Jugador'

    photo = fields.Image(max_width='200')
    name = fields.Char()
    level = fields.Integer()
    points = fields.Integer()
    description = fields.Text()
    base = fields.Integer()

class base(models.Model):
    _name = 'game.base'
    _description = 'Base'

    photo = fields.Image(max_width='200')
    level = fields.Integer()
    resources = fields.Integer()


