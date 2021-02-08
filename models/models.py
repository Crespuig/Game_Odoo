# -*- coding: utf-8 -*-
import math
import random
import string
from datetime import datetime, timedelta

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
    _inherit = "res.partner"
    _name = 'res.partner'
    _description = 'Jugador'

    #name = fields.Char(default=name_generator)
    is_player = fields.Boolean(default=True)
    is_premium = fields.Boolean(default=False)
    photo = fields.Image(max_width=150, max_heigth=150)
    level = fields.Integer()
    points = fields.Integer()

    barcos = fields.One2many('game.barco', 'player')
    islas = fields.One2many('game.isla', 'player')
    viajes = fields.One2many('game.viaje', 'player')
    levels = fields.One2many('game.levels', 'player')
    combates = fields.One2many('game.challenge', 'player')

    archipielagos = fields.Many2many('game.archipielago')

    photo_small = fields.Image(max_width=50, max_heigth=50, related='photo', store=True)
    photo_medium = fields.Image(max_width=200, max_heigth=200, related='photo', store=True)

    #_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre ya existe, prueba con otro'), ]



    '''def assign_random_isla(self):
        for p in self:
            islas = self.env['game.isla'].search([('player', '=', False)]).ids
            isla = self.env['game.isla'].browse(random.choice(islas))
            isla.write({'player': p.id})
            life_support = self.env['terraform.building'].create({
                'isla': isla.id
            })'''


class barco(models.Model):
    _name = 'game.barco'
    _description = 'Barco'

    name = fields.Char(default=name_generator)
    photo = fields.Image(max_width=150, max_heigth=150)
    vida = fields.Integer(default=50, readonly=True)
    defensa = fields.Integer(default=random.randint(10, 25), readonly=True)
    ataque = fields.Integer(default=random.randint(10, 25), readonly=True)
    level = fields.Integer(default=1, readonly=True)
    #esquivar = fields.Integer(default=random.randint(0, 20))

    player = fields.Many2one('res.partner')
    isla = fields.Many2one('game.isla')

    photo_small = fields.Image(max_width=50, max_heigth=50, related='photo', store=True)
    photo_medium = fields.Image(max_width=200, max_heigth=200, related='photo', store=True)

    #_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre ya existe, prueba con otro'), ]


class isla(models.Model):
    _name = "game.isla"
    _description = "Isla"

    photo = fields.Image(default=image_generator, max_width=100, max_heigth=100)
    name = fields.Char(default=name_generator)
    level = fields.Integer(default=random.randint(1, 100))
    n_isla = fields.Integer()
    cambios_isla = fields.One2many('game.cambios_isla', 'isla')
    #construction_buildings = fields.Many2many('game.construccion', compute='_get_barcos_disponibles')

    #Recursos por defecto, cada dia se reinician, depende de los dias que estes tendras mas recursos
    #depende del nivel de la isla tendra unso recursos o otros
    madera = fields.Integer(default=random.randint(500, 800))
    bronce = fields.Integer(default=random.randint(400, 700))
    hierro = fields.Integer(default=random.randint(300, 600))
    plata = fields.Integer(default=random.randint(200, 500))
    oro = fields.Integer(default=random.randint(100, 400))
    adamantium = fields.Integer(default=random.randint(0, 300))
    pos_x = fields.Integer(default=lambda self: self.random_generator(-100, 100))
    pos_y = fields.Integer(default=lambda self: self.random_generator(-100, 100))

    player = fields.Many2one('res.partner')
    archipielago = fields.Many2one('game.archipielago', ondelete='cascade', required=True)

    barcos = fields.One2many('game.barco', 'isla')

    photo_small = fields.Image(max_width=50, max_heigth=50, related='photo', store=True)
    photo_medium = fields.Image(max_width=100, max_heigth=100, related='photo', store=True)

    @api.model
    def random_generator(self, a, b):
        return random.randint(a, b)

    #_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre ya existe, prueba con otro'), ]


    def calculate_production(self):
        for p in self:
            date = fields.Datetime.now()

            if p.player:

                new_madera = p.madera * 0.01
                new_bronce = p.bronce * 0.01
                new_hierro = p.hierro * 0.01
                new_plata = p.plata * 0.01
                new_oro = p.oro * 0.01
                new_adamantium = p.adamantium * 0.01

                final_madera = p.madera + new_madera
                final_bronce = p.bronce + new_bronce
                final_hierro = p.hierro + new_hierro
                final_plata = p.plata + new_plata
                final_oro = p.oro + new_oro
                final_adamantium = p.adamantium + new_adamantium


                p.write({
                    'madera': final_madera,
                    'bronce': final_bronce,
                    'hierro': final_hierro,
                    'plata': final_plata,
                    'oro': final_oro,
                    'adamantium': final_adamantium
                })

                if p.player:
                    cambios_isla = p.env['game.cambios_isla'].create(
                        {'isla': p.id, 'time': date, 'name': p.name + " " + str(date)})

                    cambios_isla.write({
                        'madera': p.madera
                    })


    @api.model
    def update_resources(self):
        islas = self.env['game.isla'].search([])
        islas.calculate_production()
        print("Recurso actualizado")

    def cambios_islas(self):
        records = self.browse(self.env.context.get('active_ids'))
        for p in records:
            p.write({'madera': 1000})

    def open_player(self):
        for b in self:
            if b.player:
                return {
                    "type": "ir.actions.act_window",
                    "res_model": "res.partner",
                    "views": [[self.env.ref('game.player_form').id, "form"]],
                    "res_id": b.player.id,
                    "target": "new"
                }


class archipielago(models.Model):
    _name = "game.archipielago"
    _description = "Archipiélago"

    photo = fields.Image(max_width=100, max_heigth=100)
    name = fields.Char(default=name_generator)

    islas = fields.One2many('game.isla', 'archipielago')
    players = fields.Many2many('res.partner')

    photo_small = fields.Image(max_width=50, max_heigth=50, related='photo', store=True)
    photo_medium = fields.Image(max_width=100, max_heigth=100, related='photo', store=True)

    #_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre ya existe, prueba con otro'), ]

class viaje(models.Model):
    _name = "game.viaje"
    _description = "Viaje"

    name = fields.Char(compute='_get_viaje_name')
    fecha = fields.Datetime()
    finish = fields.Date()
    horas = fields.Integer()

    player = fields.Many2one('res.partner')

    origen_isla = fields.Many2one('game.isla')
    destino_isla = fields.Many2one('game.isla')
    duracion_viaje = fields.Integer(default=0, compute='_get_duracion_viaje')
    launch_time = fields.Datetime(default=lambda t: fields.Datetime.now())

    #_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre ya existe, prueba con otro'), ]

    @api.depends('origen_isla', 'destino_isla', 'player')
    def _get_viaje_name(self):
        for t in self:
            if t.player.name is False or t.origen_isla.name is False or t.destino_isla.name is False:
                t.name = "Viaje nombre"
            else:
                t.name = str(t.player.name) + " " + str(t.origen_isla.name) + " -> " + str(t.destino_isla.name)

    @api.depends('origen_isla', 'destino_isla')
    def _get_duracion_viaje(self):
        for t in self:
            t.duracion_viaje = ((((t.destino_isla.pos_x - t.origen_isla.pos_x) ** 2) + (
                        (t.destino_isla.pos_y - t.origen_isla.pos_y) ** 2)) ** 0.5)

            if t.duracion_viaje < 100:
                t.duracion_viaje = 100

class viaje_wizard(models.TransientModel):
    _name = 'game.viaje_wizard'

    def _default_player(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.
    player = fields.Many2one('res.partner', required=True, default=_default_player , domain="[('is_player', '=', True)]", readonly=True)
    origen_isla = fields.Many2one('game.isla', ondelete='cascade', required=True)
    destino_isla = fields.Many2one('game.isla', ondelete='cascade', required=True)


    #distance = fields.Float(compute='_get_distance')  # Distancia en temps

    @api.onchange('player')
    def onchange_player(self):
        return {
            'domain': {'origen_isla': [('player', '=', self.player.id)]},
        }

    @api.onchange('origen_isla')
    def onchange_isla(self):
        return {
            'domain': {'destino_isla': [('id', '!=', self.origen_isla.id)]},
        }

    '''
    @api.depends('origen_isla', 'destino_isla')
    def _get_distance(self):
        for t in self:
            if (t.origen_isla and t.destino_isla):
                distance = abs(int(t.origen_isla.sun.coordinates) - int(t.destiny_planet.sun.coordinates)) + 0.1
                t.distance = distance
            else:
                t.distance = 0
    '''


    def crear_viaje(self):
        viaje = self.env['game.viaje'].create({
            'player': self.player.id,
            'origen_isla': self.origen_isla.id,
            'destino_isla': self.destino_isla.id
        })

        return {
            'name': 'Nuevo viaje',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.viaje',
            'res_id': viaje.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

class levels(models.Model):
    _name = 'game.levels'

    player = fields.Many2one('res.partner')
    date = fields.Char(default=lambda self: fields.Datetime.now())
    levels = fields.Integer()


class template(models.Model):
    _name = 'game.template'
    _description = 'Templates of the game'

    name = fields.Char()
    photo = fields.Image()

class challenge(models.Model):
    _name = 'game.challenge'
    _description = 'Player challenges'
    # Main fields
    player = fields.Many2one('res.partner', readonly=True)
    nombre = fields.Char()

    finished = fields.Boolean(default=False)
    player_1 = fields.Many2one('res.partner', required=True, ondelete='restrict')
    player_2 = fields.Many2one('res.partner', required=True, ondelete='restrict')
    isla_1 = fields.Many2one('game.isla', required=True, ondelete='restrict')
    isla_2 = fields.Many2one('game.isla', required=True, ondelete='restrict')
    barco_1 = fields.Many2one('game.barco', required= True, ondelete='restrict')
    barco_2 = fields.Many2one('game.barco', required=True, ondelete='restrict')
    ### Challenge objective
    playerUpgradeLevel = fields.Many2one('res.partner')
    winner = fields.Many2one('res.partner', ondelete='restrict', readonly=True)


    player_1_avatar = fields.Image(related='player_1.photo')
    player_2_avatar = fields.Image(related='player_2.photo')
    isla_1_image = fields.Image(related='isla_1.photo')
    isla_2_image = fields.Image(related='isla_2.photo')
    barco_1_image = fields.Image(related='barco_1.photo')
    barco_2_image = fields.Image(related='barco_2.photo')

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
                           'player_2': [('id', '!=', self.player_1.id)],
                           'barco_1': [('player', '=', self.player_1.id)]},
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
                           'player_1': [('id', '!=', self.player_2.id)],
                           'barco_2': [('player', '=', self.player_2.id)]},
        }

    @api.onchange('target_goal')
    def _onchange_goal(self):
        if self.target_goal < 0:
            self.target_goal = 0

    @api.model
    def calcularCombatesCron(self):
        self.calcularCombates()

    def calcularCombates(self):
        combates = self.search([('finished','=',False)])
        for c in combates:
            barco1 = c.barco_1
            ataque1 = c.barco_1.ataque
            defensa1 = c.barco_1.defensa
            vida1 = c.barco_1.vida
            vidaInicial1 = c.barco_1.vida
            level1 = c.barco_1.level

            barco2 = c.barco_2
            ataque2 = c.barco_2.ataque
            defensa2 = c.barco_2.defensa
            vida2 = c.barco_2.vida
            vidaInicial2 = c.barco_2.vida
            level2 = c.barco_2.level

            turno = 1

            while vida1 > 0 and vida2 > 0:
                if turno == 1:
                    if(random.randint(0, 100) > 20):
                        vida2 = vida2 - ((ataque1 + 10) - defensa2)
                        print(barco2.name, vida2)
                    else:
                        print("esquivado")
                    turno = 0
                if turno == 0:
                    if (random.randint(0, 100) > 20):
                        vida1 = vida1 - ((ataque2 + 10) - defensa1)
                        print(barco1.name, vida1)
                    else:
                        print("esquivado")
                    turno = 1

            if vida1 <= 0:
                winner = barco2.player.id
                nameWinner = barco2.player.name
                playerUpgradeLevel = barco2.player.level = barco2.player.level + 1
                if (barco2.player.level > 100):
                    barco2.player.level = 100
                barcoUpgradeVida = c.barco_2.vida = vidaInicial2 + (random.randint(1, 5))
                barcoUpgradeAtaque = c.barco_2.ataque = ataque2 + (random.randint(1,5))
                barcoUpgradeDefensa = c.barco_2.defensa = defensa2 + (random.randint(1,5))
                barcoUpgradeLevel = c.barco_2.level = level2 + (random.randint(1,5))
            else:
                winner = barco1.player.id
                nameWinner = barco1.player.name
                playerUpgradeLevel = barco1.player.level = barco1.player.level + 1
                if(barco1.player.level > 100):
                    barco1.player.level = 100

                barcoUpgradeVida = c.barco_1.vida = vidaInicial1 + (random.randint(1, 5))
                barcoUpgradeAtaque = c.barco_1.ataque = ataque1 + (random.randint(1, 5))
                barcoUpgradeDefensa = c.barco_1.defensa = defensa1 + (random.randint(1, 5))
                barcoUpgradeLevel = c.barco_1.level = level1 + (random.randint(1, 5))

            c.write({'finished': True, 'winner': winner})
            print("Ganador: " + nameWinner)
            print("Level " + nameWinner + " + " + str(playerUpgradeLevel))
            print(barcoUpgradeVida, barcoUpgradeAtaque, barcoUpgradeDefensa, barcoUpgradeLevel)
            print("Combate finalizado")


#si un jugador no tiene un todas las islas de un archipilago otro jugador puede entrar para conquistar islas, pero si un jugador tiene todas las islas
#de un archipielago si otro intenta entrar se crea una guerra con toda la flota, el que gane se queda con todas las islas

