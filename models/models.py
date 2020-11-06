# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'game.player'
    _description = 'Jugador'

    name = fields.Char()
    photo = fields.Image(max_width=100, max_heigth=100)
    level = fields.Integer()
    points = fields.Integer()

    barcos = fields.One2many('game.barco', 'player')
    islas = fields.One2many('game.isla', 'player')
    viajes = fields.One2many('game.viaje', 'player')

    archipielagos = fields.Many2many('game.archipielago', 'player')


class barco(models.Model):
    _name = 'game.barco'
    _description = 'Barco'

    name = fields.Char()

    player = fields.Many2one('game.player')
    isla = fields.Many2one('game.isla')



class isla(models.Model):
    _name = "game.isla"
    _description = "Isla"

    photo = fields.Image(max_width=100, max_heigth=100)
    name = fields.Char()
    level = fields.Integer()
    madera = fields.Integer()
    bronce = fields.Integer()
    hierro = fields.Integer()
    plata = fields.Integer()
    oro = fields.Integer()
    adamantium = fields.Integer()

    player = fields.Many2one('game.player')
    archipielago = fields.Many2one('game.archipielago')

    barcos = fields.One2many('game.barco', 'isla')

class archipielago(models.Model):
    _name = "game.archipielago"
    _description = "Archipiélago"

    photo = fields.Image(max_width=100, max_heigth=100)
    name = fields.Char()

    islas = fields.One2many('game.isla', 'archipielago')
    players = fields.Many2many('game.player', 'archipielago')

class viaje(models.Model):
    _name = "game.viaje"
    _description = "Viaje"

    name = fields.Char()
    fecha = fields.Datetime()
    finish = fields.Date()
    horas = fields.Integer()

    player = fields.Many2one('game.player')






