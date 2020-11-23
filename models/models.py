# -*- coding: utf-8 -*-
import random
import string

from odoo import models, fields, api

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


class player(models.Model):
    _name = 'game.player'
    _description = 'Jugador'

    name = fields.Char(default=name_generator)
    photo = fields.Image(max_width=150, max_heigth=150)
    level = fields.Integer()
    points = fields.Integer()

    barcos = fields.One2many('game.barco', 'player')
    islas = fields.One2many('game.isla', 'player')
    viajes = fields.One2many('game.viaje', 'player')
    levels = fields.One2many('game.levels', 'player')

    archipielagos = fields.Many2many('game.archipielago')

class barco(models.Model):
    _name = 'game.barco'
    _description = 'Barco'

    name = fields.Char()

    player = fields.Many2one('game.player')
    isla = fields.Many2one('game.isla')



class isla(models.Model):
    _name = "game.isla"
    _description = "Isla"

    photo = fields.Image(default=image_generator, max_width=100, max_heigth=100)
    name = fields.Char(default=name_generator)
    level = fields.Integer(default=random.randint(1, 100))

    #Recursos por defecto, cada dia se reinician, depende de los dias que estes tendras mas recursos
    #depende del nivel de la isla tendra unso recursos o otros
    madera = fields.Integer(default=random.randint(500, 800))
    bronce = fields.Integer(default=random.randint(400, 700))
    hierro = fields.Integer(default=random.randint(300, 600))
    plata = fields.Integer(default=random.randint(200, 500))
    oro = fields.Integer(default=random.randint(100, 400))
    adamantium = fields.Integer(default=random.randint(0, 300))

    player = fields.Many2one('game.player')
    archipielago = fields.Many2one('game.archipielago')

    barcos = fields.One2many('game.barco', 'isla')


class archipielago(models.Model):
    _name = "game.archipielago"
    _description = "Archipiélago"

    photo = fields.Image(max_width=100, max_heigth=100)
    name = fields.Char(default=name_generator)

    islas = fields.One2many('game.isla', 'archipielago')
    players = fields.Many2many('game.player')

class viaje(models.Model):
    _name = "game.viaje"
    _description = "Viaje"

    name = fields.Char(compute='_get_name')
    fecha = fields.Datetime()
    finish = fields.Date()
    horas = fields.Integer()

    player = fields.Many2one('game.player')

    origen_isla = fields.Many2one('game.isla')
    destino_isla = fields.Many2one('game.isla')
    launch_time = fields.Datetime(default=lambda t: fields.Datetime.now())

    @api.depends('origen_isla', 'destino_isla', 'player')
    def _get_name(self):
        for t in self:
            t.name = str(t.player.name) + " " + str(t.origen_isla.name) + " -> " + str(t.destino_isla.name)

class levels(models.Model):
    _name = 'game.levels'

    player = fields.Many2one('game.player')
    date = fields.Char(default=lambda self: fields.Datetime.now())
    levels = fields.Integer()


class template(models.Model):
    _name = 'game.template'
    _description = 'Templates of the game'

    name = fields.Char()
    photo = fields.Image()