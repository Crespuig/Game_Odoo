# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'game.player'
    _description = 'Jugador'

    name = fields.Char()
    photo = fields.Image()
    level = fields.Integer()
    points = fields.Integer()

    #caracters = fields.One2many('game.caracter', 'lider')
    barcos = fields.One2many('game.barco', 'barco')
    islas = fields.One2many('game.isla', 'isla')

#class caracter(models.Model):
    #_name = 'game.caracter'
    #_description = 'Caracter'

    #lider = fields.Many2one('game.player')




class barco(models.Model):
    _name = 'game.barco'
    _description = 'Barco'

    barco = fields.Many2one('game.player')



class isla(models.Model):
    _name = "game.isla"
    _description = "Isla"

    photo = fields.Image()
    name = fields.Char()
    level = fields.Integer()
    resources = fields.Integer()
    madera = fields.Integer()
    bronce = fields.Integer()
    hierro = fields.Integer()
    plata = fields.Integer()
    oro = fields.Integer()
    adamantium = fields.Integer()

    isla = fields.Many2one('game.player')

    #caracters = fields.One2many('game.caracter', 'lider')
    barcos = fields.One2many('game.barco', 'barco')






