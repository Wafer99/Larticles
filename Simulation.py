



from constants import *


def recalc_grid(x, y):
    if x >= constant_grid_size:
        xx = x - constant_grid_size
    elif x < 0:
        xx = constant_grid_size + x
    else:
        xx = int(x)
    if y >= constant_grid_size:
        yy = y - constant_grid_size
    elif y < 0:
        yy = constant_grid_size + y
    else:
        yy = int(y)
    return xx, yy


def recalc_blit(x, y, gx, gy):
    dx = x + gx
    dy = y + gy
    if dx < 0:
        dx = constant_grid_size + dx
    elif dx >= constant_grid_size:
        dx = dx - constant_grid_size
    if dy < 0:
        dy = constant_grid_size + dy
    elif dy >= constant_grid_size:
        dy = dy - constant_grid_size
    dx += 1
    dy += 1
    return dx, dy


class Axon():
    def __init__(self, neuron):
        self.neuron = neuron
        self.weight = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale

def Dendrite_set_weight(axon, weight):
    axon.weight = weight


def Dendrite_get(axon):
    return axon.neuron.name, axon.weight


def Dendrite_fire(axon):
    return axon.weight * Neuron_calculate(axon.neuron)


class Neuron():
    def __init__(self, name):
        self.name = name
        self.dendrites = {}
        self.potential = 0

def Neuron_set_potential(neuron, potential):
    neuron.potential = potential


def Neuron_get_connections(neuron):
    con = []
    for name in neuron.dendrites:
        con.append([neuron.name, name, neuron.dendrites[name].weight])
    return con


def Neuron_connect(neuron1, neuron2, weight=None):
    dendrite = Axon(neuron2)
    if weight != None:
        Dendrite_set_weight(dendrite, weight)
    neuron1.dendrites[neuron2.name] = dendrite
    t = Neuron_test_connection(neuron1, neurons_connectiondepth)
    if not t:
        neuron1.dendrites.pop(neuron2.name)
    return t


def Neuron_disconnect(neuron, name):
    if name in neuron.dendrites:
        neuron.dendrites.pop(name)


def Neuron_test_connection(neuron, connectiondepth):
    n = connectiondepth
    n -= 1
    r = True
    if n >= 0:
        if len(neuron.dendrites) != 0:
            for dendrite in neuron.dendrites:
                t = Neuron_test_connection(neuron.dendrites[dendrite].neuron, n)
                if t == False:
                    r = False
    else:
        r = False
    return r


def sigmoid(potential, derivative=False):
    if not derivative:
        if potential > -100:
            return 1 / (1 + math.exp(-potential))
        else:
            return 0
    else:
        return potential * (1 - potential)


def Neuron_calculate(neuron):
    if len(neuron.dendrites) != 0:
        x = 0
        for dendrite in neuron.dendrites:
            x += Dendrite_fire(neuron.dendrites[dendrite])
        neuron.potential = sigmoid(x)
    return neuron.potential


def Neuron_add_error(neuron, error):
    neuron.error = error


def Neuron_correct(neuron):
    gradient = neuron.error * sigmoid(neuron.potential, derivative=True)
    for dendrite in neuron.dendrites:
        delta_weight = neuron_learningrate * neuron.dendrites[dendrite].neuron.potential * gradient
        neuron.dendrites[dendrite].weight += delta_weight
        Neuron_add_error(neuron.dendrites[dendrite].neuron, gradient * neuron.dendrites[dendrite].weight)
        Neuron_correct(neuron.dendrites[dendrite].neuron)
    neuron.error = 0
    Neuron_calculate(neuron)


def Test_Neuron():
    print(' ')
    print(' ')
    print('Test Neuron')
    print(' ')
    print(' ')
    n1 = Neuron(1)
    n2 = Neuron(2)
    n3 = Neuron(3)
    n1.potential = 0.5
    n2.potential = 0.5
    Neuron_connect(n3, n1, 2)
    Neuron_connect(n3, n2, 3)

    s = 0.1234567890123456789
    for i in range(5001):
        y = Neuron_calculate(n3)
        e = s - y
        Neuron_add_error(n3, e)
        Neuron_correct(n3)
        if i % 500 == 0:
            print(i, n3.potential)
    print('get connections')
    print(Neuron_calculate(n3))
    print(' ')
    print(' ')
    print('End Test Neuron')
    print(' ')
    print(' ')


class Body():
    def __init__(self):
        self.x = 0
        self.y = 0

        self.direction = random.choice(body_directions)

        self.health = int(body_health_bar)
        self.previous_health = self.health
        self.regen = 0
        self.body_drain = 0
        self.regenerating = False
        self.happy = 0

        self.colour = body_colour_newborn

        self.reflect_1 = 0

        self.memory_1 = 0

        self.voice_1 = 0
        self.voice_2 = 0

        self.sound_1 = 0
        self.sound_2 = 0
        self.s1 = 0
        self.s2 = 0


        self.eating = False
        self.talking = False
        self.give_health = False
        self.attacking = False
        self.freezing = False
        self.wall = False

        self.defending = False

        self.frozen = False
        self.freeztime = 0
        self.freezedelay = 0

        self.clock_timer = 0

        self.killer = 0

        self.kills = 0

        self.state = 0

        self.place_counter = 0

def Body_get_properties(body):
    properties = {}
    properties['pos'] = body.x, body.y
    properties['direction'] = body.direction
    properties['health'] = body.health
    properties['regen'] = body.regen
    properties['body drain'] = body.body_drain
    properties['regenerating'] = body.regenerating
    properties['happy'] = body.happy
    properties['colour'] = body.colour
    properties['memory 1'] = body.memory_1
    properties['voice 1'] = body.voice_1
    properties['voice 2'] = body.voice_2
    properties['sound 1'] = body.sound_1
    properties['sound 2'] = body.sound_2
    properties['eating'] = body.eating
    properties['talking'] = body.talking
    properties['giving health'] = body.give_health
    properties['attacking'] = body.attacking
    properties['freezing'] = body.freezing
    properties['freeztime'] = body.freeztime
    properties['killer'] = body.killer
    properties['kills'] = body.kills
    properties['state'] = body.state
    properties['wall'] = body.wall
    properties['freeze delay'] = body.freezedelay
    sx, sy = Body_pos_to_sense(body.x, body.y)
    properties['sense_pos_x'] = sx
    properties['sense_pos_y'] = sy

    return properties


def Body_get_surounding_pos(x, y, direction):
    dx, dy = int(x + direction[0]), int(y + direction[1])
    north = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * direction[0]), int(y + 2 * direction[1])
    northnorth = recalc_grid(dx, dy)

    dx, dy = int(x + 3 * direction[0]), int(y + 3 * direction[1])
    northnorthnorth = recalc_grid(dx, dy)

    dx, dy = int(x - direction[0]), int(y - direction[1])
    south = recalc_grid(dx, dy)

    if direction == (1, 0):
        left = [0, 1]
    elif direction == (0, 1):
        left = [-1, 0]
    elif direction == (-1, 0):
        left = [0, -1]
    else:
        left = [1, 0]

    dx, dy = int(x + left[0]), int(y + left[1])
    west = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0]), int(y + 2 * left[1])
    westwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0]), int(y - left[1])
    east = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0]), int(y - 2 * left[1])
    easteast = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] + direction[0]), int(y + left[1] + direction[1])
    northwest = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0] + direction[0]), int(y + 2 * left[1] + direction[1])
    northwestwest = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] + 2 * direction[0]), int(y + left[1] + 2 * direction[1])
    northnorthwest = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0] + 2 * direction[0]), int(y + 2 * left[1] + 2 * direction[1])
    northnorthwestwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] + direction[0]), int(y - left[1] + direction[1])
    northeast = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0] + direction[0]), int(y - 2 * left[1] + direction[1])
    northeasteast = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] + 2 * direction[0]), int(y - left[1] + 2 * direction[1])
    northnortheast = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0] + 2 * direction[0]), int(y - 2 * left[1] + 2 * direction[1])
    northnortheasteast = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] - direction[0]), int(y + left[1] - direction[1])
    southwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] - direction[0]), int(y - left[1] - direction[1])
    southeast = recalc_grid(dx, dy)

    return {'north': north, 'south': south,
            'west': west, 'westwest': westwest, 'east': east, 'easteast': easteast,
            'northwest': northwest, 'northwestwest': northwestwest,
            'northeast': northeast, 'northeasteast': northeasteast,
            'southwest': southwest, 'southeast': southeast,
            'northnorth': northnorth, 'northnorthnorth': northnorthnorth,
            'northnorthwest': northnorthwest, 'northnorthwestwest': northnorthwestwest,
            'northnortheast': northnortheast, 'northnortheasteast': northnortheasteast}



def Body_sense(surounding):
    potentials = {}
    for name in surounding:
        n = 'sense_' + name
        if surounding[name] != None:
            potentials[n] = 1
        else:
            potentials[n] = 0
    return potentials


def See(larticle_seeing, larticle_seen, none=False):
    d = {}
    d['see_red'] = 0
    d['see_green'] = 0
    d['see_blue'] = 0
    d['see_health'] = 0
    d['see_happyness'] = 0
    d['see_state'] = 0
    d['see_frozen'] = 0
    d['see_attacking'] = 0
    d['see_orientation'] = 1 / 2
    # r g b health happyness state distance
    if not none:
        bodyseeing = larticle_seeing.body
        bodyseen = larticle_seen.body
        colour = bodyseen.colour
        d['see_red'] = colour[0]
        d['see_green'] = colour[1]
        d['see_blue'] = colour[2]
        d['see_health'] = bodyseen.health / bodyseeing.health
        d['see_happyness'] = bodyseen.happy
        d['see_state'] = bodyseen.state
        d['see_frozen'] = int(bodyseen.frozen)
        d['see_attacking'] = int(bodyseen.attacking)
        if int(-bodyseen.direction[0]) == int(bodyseeing.direction[0]):
            if int(-bodyseen.direction[1]) == int(bodyseeing.direction[1]):
                d['see_orientation'] = 0
        if int(bodyseen.direction[0]) == int(bodyseeing.direction[0]):
            if int(bodyseen.direction[1]) == int(bodyseeing.direction[1]):
                d['see_orientation'] = 1

    return d


def Body_see(larticle, surounding):
    # r g b health happyness state distance
    distance = {'see_distance_0': 0, 'see_distance_1': 0, 'see_distance_2': 0}
    if surounding['north'] != None:
        see = See(larticle, surounding['north'])
    else:
        if surounding['northnorth'] != None:
            see = See(larticle, surounding['northnorth'])
            distance['see_distance_0'] = 1
        else:
            if surounding['northnorthnorth'] != None:
                see = See(larticle, surounding['northnorthnorth'])
                distance['see_distance_0'] = 1
                distance['see_distance_1'] = 1
            else:
                see = See(None, None, True)
                distance['see_distance_0'] = 1
                distance['see_distance_1'] = 1
                distance['see_distance_2'] = 1
    d = {}
    for i in see:
        d[i] = see[i]
    for i in distance:
        d[i] = distance[i]
    return d


def Body_move(larticle):
    x = int(larticle.body.direction[0] + larticle.body.x)
    y = int(larticle.body.direction[1] + larticle.body.y)
    dx, dy = recalc_grid(x, y)
    larticle.body.x = dx
    larticle.body.y = dy


def Body_rotate_right(direction):
    if direction == (1, 0):
        d = (0, 1)
    elif direction == (0, 1):
        d = (-1, 0)
    elif direction == (-1, 0):
        d = (0, -1)
    else:
        d = (1, 0)
    return d


def Body_rotate_left(direction):
    if direction == (1, 0):
        d = (0, -1)
    elif direction == (0, -1):
        d = (-1, 0)
    elif direction == (-1, 0):
        d = (0, 1)
    else:
        d = (1, 0)
    return d


def Body_regenerate(larticle, surounding):
    t = body_regenrate

    if surounding['north'] != None:
        if surounding['north'].body.regenerating:
            t += body_regenrate
    if surounding['south'] != None:
        if surounding['south'].body.regenerating:
            t += body_regenrate
    if surounding['west'] != None:
        if surounding['west'].body.regenerating:
            t += body_regenrate
    if surounding['east'] != None:
        if surounding['east'].body.regenerating:
            t += body_regenrate
    larticle.body.health += t

    return t


def Body_eat(larticle_win, larticle_lose):
    if not larticle_lose.body.wall:
        c = body_eat_health_gain * body_eat_damage * (1 / 2 + larticle_win.body.health / (2 * body_health_bar))
        h = larticle_lose.body.health
        if h > c:
            larticle_win.body.health += c
        else:
            larticle_win.body.health += body_eat_health_gain * h
        larticle_lose.body.health -= c
        if larticle_lose.body.health <= 0:
            larticle_win.body.kills += 1
            larticle_win.body.killer = 1


def Body_attack(larticle_attacking, larticle_attacked):
    if not larticle_attacked.body.wall:
        larticle_attacked.body.health -= body_attack_damage * (
            1 / 2 + larticle_attacking.body.health / (2 * body_health_bar))

    if larticle_attacked.body.health <= 0:
        larticle_attacking.body.kills += 1
        larticle_attacking.body.killer = 1


def Body_freeze(larticle_frozen):
    larticle_frozen.body.freeztime = body_freeztime


def Body_give(larticle_give, larticle_gain):
    if larticle_give.body.health > abs(body_eat_damage):
        larticle_give.body.health -= body_eat_damage
        larticle_gain.body.health += body_eat_damage


def Body_speak(larticle_speaker, larticle_listener):
    scale = 1
    front = False
    if int(larticle_speaker.body.x + larticle_speaker.body.direction[0]) == larticle_listener.body.x:
        if int(larticle_speaker.body.y + larticle_speaker.body.direction[1]) == larticle_listener.body.y:
            front = True
    if not front:
        d = ((larticle_speaker.body.x - larticle_listener.body.x) ** 2 + (
            larticle_speaker.body.y - larticle_listener.body.y) ** 2) ** (1 / 2)
        scale = float(1 / (d + 1))
    larticle_listener.body.sound_1 += larticle_speaker.body.voice_1 * scale
    larticle_listener.body.sound_2 += larticle_speaker.body.voice_2 * scale

def Body_place_left(larticle_lose,larticle_win):
    d = Body_rotate_left(larticle_win.body.direction)
    x0,y0 = larticle_lose.body.x,larticle_lose.body.y
    x1 = larticle_win.body.x + d[0]
    y1 = larticle_win.body.y + d[1]
    x1,y1 = recalc_grid(x1,y1)
    larticle_lose.body.x = x1
    larticle_lose.body.y = y1
    larticle_win.body.place_counter = body_place_counter
    return str(x0) + '_' + str(y0),str(x1) + '_' + str(y1)
def Body_place_right(larticle_lose,larticle_win):
    d = Body_rotate_right(larticle_win.body.direction)
    x0,y0 = larticle_lose.body.x,larticle_lose.body.y
    x1 = larticle_win.body.x + d[0]
    y1 = larticle_win.body.y + d[1]
    x1,y1 = recalc_grid(x1,y1)
    larticle_lose.body.x = x1
    larticle_lose.body.y = y1
    larticle_win.body.place_counter = body_place_counter
    return str(x0) + '_' + str(y0),str(x1) + '_' + str(y1)

def Body_command(larticle, commands, surounding):
    result = []
    body = larticle.body
    body.body_drain = 0
    body.regen = 0
    r2 = surounding['north']
    body.colour = body_colour_inactive

    body.voice_1 = commands['command_voice_1_value']
    body.voice_2 = commands['command_voice_2_value']

    happy = body.health - body.previous_health
    if happy > 0:
        body.happy = 1
    else:
        body.happy = 0

    body.reflect_1 = commands['command_reflect_1']

    if commands['command_memory_1_set'] > 0.5:
        body.memory_1 = commands['command_memory_1_value']
    if commands['command_memory_1_erase']:
        body.memory_1 = 0

    if commands['command_set_state'] > 0.5:
        body.state = commands['command_state_value']
    if commands['command_erase_state'] > 0.5:
        body.state = 0

    if commands['command_voice_speak'] > 0.5:
        body.talking = True
        for pos in surounding:
            if surounding[pos] != None:
                Body_speak(larticle, surounding[pos])
    else:
        body.talking = False

    if commands['command_wall_1'] > 0.5 and commands['command_wall_2'] > 0.5:
        body.wall = True
        body.health -= body_wall_drain
    else:
        body.wall = False

    if commands['command_regenerate'] > 0.5 and not body.wall:
        result.append('regenerate')
        body.regenerating = True
        body.colour = body_colour_regenerating
        body.regen = Body_regenerate(larticle, surounding)
    else:
        body.regenerating = False

    if commands['command_eat'] > 0.5 and not body.wall:
        if not body.regenerating:
            body.eating = True
            body.colour = body_colour_eating
            if r2 != None:
                Body_eat(larticle, r2)
        else:
            body.eating = False
    else:
        body.eating = False

    if commands['command_attack'] > 0.5 and not body.wall:
        body.attacking = True
        if body.regenerating:
            body.colour = body_colour_attacking_regenerating
        else:
            if body.colour == body_colour_inactive:
                body.colour = body_colour_attacking_else
            else:
                body.colour = body_colour_attacking_eating
        if r2 != None:
            Body_attack(larticle, r2)
    else:
        body.attacking = False

    if commands['command_freeze'] > 0.5 and not body.frozen and not body.wall:
        if body.freezedelay == 0:
            body.freezedelay = body_freeze_delay
            body.freezing = True
            if r2 != None:
                Body_freeze(r2)
    else:
        body.freezing = False

    if commands['command_give'] > 0.5 and not body.wall:
        body.give_health = True
        if r2 != None:
            Body_give(larticle, r2)
        else:
            result.append('move')
    else:
        body.give_health = False

    if body.freezing:
        if body.regenerating:
            body.colour = [0.4, body.colour[1], body.colour[2]]
        elif body.eating:
            body.colour = [body.colour[0], body.colour[1], 0.4]
        else:
            body.colour = [1 / 2, 1, 1 / 2]

    if body.wall:
        body.colour = body_colour_wall


    if commands['command_split'] > 0.5 and not body.wall:
        if body.regenerating:
            if r2 == None:
                minh = body_health_bar + body_health_bar / 10
                if body.health > minh:
                    body.health -= body_health_bar
                    result.append('split')



        else:
            rs2 = surounding['south']
            if rs2 == None:
                minh = body_splitrate_red * (body_health_bar + body_health_bar / 10)
                if body.health > minh:
                    body.health -= body_splitrate_red * body_health_bar
                    result.append('split')

    larticle.body.clock_timer += 1
    larticle.body.clock = 0
    if larticle.body.clock_timer >= body_clock_interval:
        larticle.body.clock = 1
        larticle.body.clock_timer = 0

    if body.freezedelay > 0:
        body.freezedelay -= 1

    if body.place_counter > 0:
        body.place_counter -= 1

    if body.freeztime > 0:
        body.frozen = True
        body.freeztime -= 1
    else:
        body.frozen = False


    t = body_suffer
    if body.colour == body_colour_inactive:
        t /= 3
    if body.regenerating:
        t = 0
    body.body_drain = abs(t)
    body.health += t

    if body.attacking and body.regenerating:
        if body.health > 2 * body_max_health:
            body.health = 2 * body_max_health
    else:
        if body.health > body_max_health:
            body.health = body_max_health

    return result


def Body_pos_to_sense(x, y):
    sx = 1 / 2 * math.sin(2 * x / (constant_grid_size) * 2 * math.pi) + 0.5
    sy = 1 / 2 * math.sin(2 * y / (constant_grid_size) * 2 * math.pi) + 0.5
    return sx, sy


def Body_to_brain(larticle, surounding):
    see = Body_see(larticle, surounding)
    sense = Body_sense(surounding)

    sx, sy = Body_pos_to_sense(larticle.body.x, larticle.body.y)

    frozen = 0
    if larticle.body.frozen:
        frozen = 1

    sound = voice_scale([larticle.body.sound_1, larticle.body.sound_2])
    others = {'sense_health': larticle.body.health / body_health_bar, 'sense_happy': larticle.body.happy,
              'sense_alive_0': 1, 'sense_alive_1': larticle.body.clock_timer % 2,
              'sense_memory_1': larticle.body.memory_1,
              'sense_sound_1': sound[0], 'sense_sound_2': sound[1],
              'sense_killed': larticle.body.killer, 'sense_frozen': frozen,
              'sense_pos_x': sx,
              'sense_pos_y': sy,
              'sense_reflect_1': larticle.body.reflect_1}
    result = {}
    for i in see:
        result[i] = see[i]
    for i in sense:
        result[i] = sense[i]
    for i in others:
        result[i] = others[i]
    larticle.body.sound_1 = 0
    larticle.body.sound_2 = 0
    larticle.body.killer = 0
    return result


class Brain():
    def __init__(self, dna=None):
        self.neurons = {}
        for i in brain_all_neuron_names:
            self.neurons[i] = Neuron(i)
        if dna == None:
            self.dna = Brain_create_random_dna()
        else:
            self.dna = copy.deepcopy(dna)
        Brain_set_dna(self, self.dna)


def Brain_create_random_dna():
    p = list(itertools.permutations(brain_all_neuron_names, 2))
    length = random.randrange(brain_min_dna_length, brain_max_dna_length)
    dna = []

    for i in range(length):
        t = True
        while t:

            n1, n2 = random.choice(p)
            if n1 != n2 and n1 not in body_perception:
                r2 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
                if r2 == 0:
                    r2 = random.choice([-1,1])
                dna.append([n1, n2, r2])
                t = False
    return dna


def Brain_set_dna(brain, dna):
    for neuron1, neuron2, weight in dna:
        if neuron1 not in brain.neurons:
            brain.neurons[neuron1] = Neuron(neuron1)
        if neuron2 not in brain.neurons:
            brain.neurons[neuron2] = Neuron(neuron2)
        Neuron_connect(brain.neurons[neuron1], brain.neurons[neuron2], weight)


def Brain_get_dna(larticle):
    dna = []
    for name in brain_all_neuron_names:
        dna += Neuron_get_connections(larticle.brain.neurons[name])
    larticle.brain.dna = dna
    return dna


def Brain_mutate(larticle):
    r1 = random.randrange(0, 100)
    if 0 <= r1 < 33:
        if len(larticle.brain.dna) != 0:
            r2 = random.randrange(0, len(larticle.brain.dna))
            Neuron_disconnect(larticle.brain.neurons[larticle.brain.dna[r2][0]], larticle.brain.dna[r2][1])
            larticle.brain.dna.pop(r2)

    elif 33 <= r1 < 66:
        n1 = random.choice(list(brain_all_neuron_names))
        n2 = random.choice(list(brain_all_neuron_names))
        if n1 != n2 and n1 not in body_perception:
            r2 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
            if n1 not in larticle.brain.neurons:
                larticle.brain.neurons[n1] = Neuron(n1)
            if n2 not in larticle.brain.neurons:
                larticle.brain.neurons[n2] = Neuron(n2)
            tt = Neuron_connect(larticle.brain.neurons[n1], larticle.brain.neurons[n2], r2)
            if tt:
                larticle.brain.dna.append([n1, n2, r2])

    else:
        if len(larticle.brain.dna) != 0:
            r2 = random.randrange(0, len(larticle.brain.dna))
            r3 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
            larticle.brain.dna[r2][-1] = r3
            Neuron_connect(larticle.brain.neurons[larticle.brain.dna[r2][0]],
                           larticle.brain.neurons[larticle.brain.dna[r2][0]], r3)



def Brain_to_body(larticle, inputs):
    result = {}
    for name in inputs:
        Neuron_set_potential(larticle.brain.neurons[name], inputs[name])
    for name in body_commands:
        result[name] = Neuron_calculate(larticle.brain.neurons[name])
    return result



class Larticle():
    def __init__(self, name, dna=None):
        self.name = name
        self.body = Body()
        self.brain = Brain(dna)
        self.time_alive = 0
        self.brain_drain = (len(self.brain.dna)) / brain_drain_scale
        self.splits = 0
        self.generation = 0


def Larticle_simulate(larticle, surounding):
    larticle.time_alive += 1
    forbrain = Body_to_brain(larticle, surounding)
    forbody = Brain_to_body(larticle, forbrain)
    return forbody


def Larticle_doe(larticle, forbody, surounding):
    r = Body_command(larticle, forbody, surounding)
    larticle.body.health -= larticle.brain_drain
    return r


def Larticle_mutate(larticle):
    Brain_mutate(larticle)
    Brain_mutate(larticle)


def Larticle_score(larticle):
    score = int(larticle.time_alive * larticle.body.health * (larticle.splits + 1) * (larticle.body.kills / 10 + 1))
    return score


class Handler():
    def __init__(self):
        print(' ')
        print(' ')
        print('Initializing Handler Constants.')
        print(' ')
        print(' ')
        self.count = 0
        self.died = 0
        self.solardeaths = 0
        self.epoch = 0
        self.splits = 0
        self.larticles = {}
        self.random_larticles = []
        self.previous_amount_kills = 0

        self.eaters = 0
        self.stupids = 0
        self.regenerators = 0
        self.newbies = 0
        self.attacking = 0
        self.walls = 0

        self.suns = []
        self.positions = {}

        self.visual = False

        self.selected_larticle = None
        self.selected_neuron = None
        self.selected_forbody = None
        self.selected_forbrain = None

        self.frames = []

        print(' ')
        print(' ')
        print('Initializing Handler.')
        print(' ')
        print(' ')

        Handler_initialize(self)


def Handler_create_random_larticles(n):
    random_larticles = []
    for i in range(int(n)):
        l = Larticle('Random' + str(i))
        random_larticles.append(l)
    return random_larticles


def Handler_initialize(handler):
    print(' ')
    print('Placing Larticles.')
    print(' ')
    s1 = "In this world"
    s2 = "is the destiny of mankind controlled"
    s3 = "by some transcendental entity "
    s3b = "or law...?"
    s3bb = ''
    s4 = "Is it like the hand of God "
    s4b = "hovering above?"
    s4bb = ''
    s5 = "At least it is true "
    s5b = "that man has no control"
    s6 = "even over his own will."
    ls = [s1, s2, s3, s3b, s3bb, s4, s4b, s4bb, s5, s5b, s6]
    t = [200, 200, 300, 100]
    b = [800, 200, 200, 200]
    handler.epoch = 0
    tt = 0
    if screen.display != None:
        textsurface = myfont30.render(ls[0], False, [250, 250, 250])
        screen.display.blit(textsurface, [200, 500, 100, 100])
        textsurface = myfont75.render('LOADING', False, [250, 250, 250])
        screen.display.blit(textsurface, t)
        textsurface = myfont75.render(str(0) + ' %', False, [250, 250, 250])
        screen.display.blit(textsurface, b)
        pygame.display.update()
        if not testing:
            pygame.time.wait(500)

    p = -1
    for i in range(handler_amount_larticles):
        larticle = Larticle('Big Bang Larticle: ' + str(i))
        #larticle.body.health = body_max_health
        Handler_place_larticle(handler, larticle)
        if i % int(handler_amount_larticles / 10) == 0:
            p += 1
            perc = p * 10
            print(str(perc), '%')
            if screen.display != None:
                screen.display.fill([0, 0, 0])
                if tt < len(ls):
                    textsurface = myfont30.render(ls[tt], False, [250, 250, 250])
                    screen.display.blit(textsurface, [200, 500, 100, 100])
                textsurface = myfont75.render(str(perc) + ' %', False, [250, 250, 250])
                screen.display.blit(textsurface, b)
                textsurface = myfont75.render('LOADING', False, [250, 250, 250])
                screen.display.blit(textsurface, t)
                pygame.display.update()
                if not testing:
                    pygame.time.wait(1000)
                tt += 1
    if screen.display != None:
        screen.display.fill([0, 0, 0])
        textsurface = myfont30.render(ls[-1], False, [250, 250, 250])
        screen.display.blit(textsurface, [200, 500, 100, 100])
        textsurface = myfont75.render(str(100) + ' %', False, [250, 250, 250])
        screen.display.blit(textsurface, b)
        textsurface = myfont75.render('LOADING', False, [250, 250, 250])
        screen.display.blit(textsurface, t)
        pygame.display.update()
        if not testing:
            pygame.time.wait(2000)
        tt += 1

    Handler_get_all_positions(handler)
    print(' ')
    print('Placing Larticles Done.')
    print(' ')

    if screen.display != None:
        screen.display.fill([0, 0, 0])

        t = [200, 200, 300, 100]
        textsurface = myfont50.render('Appending Random Brains..', False, [250, 250, 250])
        screen.display.blit(textsurface, t)
        pygame.display.update()


    print(' ')
    print(' ')
    print('Creating random Larticles')
    print(' ')
    print(' ')

    handler.random_larticles += Handler_create_random_larticles(1000)

    print(' ')
    print(' ')
    print('Creating random Larticles done.')
    print(' ')
    print(' ')

    Handler_remove_larticles(handler)

    print(' ')
    print('Handler Initializing Succesfull.')
    print(' ')

def Handler_remove_larticles(handler):
    print(' ')
    print('Removing Larticles.')
    print(' ')
    Handler_run(handler)
    excessives = []
    for name in handler.larticles:
        if handler.larticles[name].body.colour == body_colour_wall and False:
            excessives.append(name)
        elif handler.larticles[name].body.colour == body_colour_inactive and False:
            excessives.append(name)
    for name in excessives:
        handler.larticles.pop(name)
    Handler_get_all_positions(handler)
    print(' ')
    print('Removing Larticles Done.')
    print(' ')

def Handler_get_all_positions(handler):
    pos = {}
    doubles = []
    for name in handler.larticles:
        x, y = int(handler.larticles[name].body.x), int(handler.larticles[name].body.y)
        x, y = recalc_grid(x, y)
        s = str(x) + '_' + str(y)

        if s not in pos:
            pos[s] = name
        else:
            print('Double: ', name)
            doubles.append(name)
    for name in doubles:
        if name in handler.larticles:
            handler.larticles.pop(name)
    handler.positions = pos
    return pos


def Handler_get_surrounding_positions(handler, larticle):
    positions = Body_get_surounding_pos(larticle.body.x, larticle.body.y, larticle.body.direction)
    ss = {}
    for position in positions:
        sx, sy = recalc_grid(positions[position][0], positions[position][1])
        s1 = str(sx) + '_' + str(sy)
        ss[position] = s1
    l = {}
    for position in ss:
        if ss[position] in handler.positions:
            if handler.positions[ss[position]] in handler.larticles:
                l[position] = handler.larticles[handler.positions[ss[position]]]
            else:
                l[position] = None
        else:
            l[position] = None
    return l


def Handler_check_pos(handler, x, y):
    s = str(int(x)) + '_' + str(int(y))
    if s in handler.positions:
        return False
    return True


def Handler_check_around(handler, x, y):
    p1x, p1y = x + 1, y
    p2x, p2y = x - 1, y
    p3x, p3y = x, y + 1
    p4x, p4y = x, y - 1
    r = [[int(x), int(y)], [int(p1x), int(p1y)], [int(p2x), int(p2y)], [int(p3x), int(p3y)], [int(p4x), int(p4y)]]
    for pos in r:
        s = str(int(pos[0])) + '_' + str(int(pos[1]))
        if s in handler.positions:
            return False
    return True


def Handler_place_larticle(handler, larticle):
    t = True
    tt = 0
    ranx = None
    rany = None
    while t:
        tt += 1
        ranx = random.randrange(0, int(constant_grid_size))
        rany = random.randrange(0, int(constant_grid_size))
        r1 = Handler_check_around(handler, ranx, rany)
        if r1:
            handler.count += 1
            larticle.body.x = int(ranx)
            larticle.body.y = int(rany)
            rs = str(ranx) + '_' + str(rany)
            handler.positions[rs] = larticle.name
            handler.larticles[larticle.name] = larticle
            t = False
        if tt > 50:
            print('larticle handler place larticle while break')
            break
    return ranx, rany


def Handler_run(handler, autoselect=False):
    print('Epoch: ', handler.epoch)
    handler.eaters = 0
    handler.stupids = 0
    handler.regenerators = 0
    handler.newbies = 0
    handler.walls = 0
    handler.attacking = 0
    handler.epoch += 1
    died = []

    handler.suns = []
    for i in range(constant_suns):
        handler.suns.append([random.randrange(0, constant_grid_size), random.randrange(0, constant_grid_size)])

    for name in list(handler.larticles.keys()):

        larticle = handler.larticles[name]

        body = larticle.body
        x0 = int(body.x)
        y0 = int(body.y)
        s0 = str(x0) + '_' + str(y0)
        handler.positions.pop(s0)

        if [x0, y0] not in handler.suns:

            if body.health > 0:

                surounding = Handler_get_surrounding_positions(handler, larticle)
                forbody = Larticle_simulate(larticle, surounding)

                move = False
                rotate = False

                if forbody['command_rotate_right'] > 0.5 and not body.wall and not forbody[
                    'command_rotate_left'] > 0.5:
                    rotate = 'right'
                    body.direction = Body_rotate_right(body.direction)

                elif forbody['command_rotate_left'] > 0.5 and not body.wall and not forbody[
                    'command_rotate_right'] > 0.5:
                    rotate = 'left'
                    body.direction = Body_rotate_left(body.direction)

                if forbody['command_move'] > 0.5 and not body.frozen and not body.wall and not forbody[
                    'command_regenerate'] > 0.5:
                    sx, sy = int(body.x + body.direction[0]), int(body.y + body.direction[1])
                    sx, sy = recalc_grid(sx, sy)
                    ss = str(sx) + '_' + str(sy)
                    if ss not in handler.positions:
                        move = True
                        Body_move(larticle)

                x = int(body.x)
                y = int(body.y)
                direction = body.direction
                s = str(x) + '_' + str(y)
                handler.positions[s] = larticle.name

                sur = {}
                if rotate != False and not move:
                    if rotate == 'right':
                        sur['north'] = surounding['west']
                        sur['west'] = surounding['south']
                        sur['south'] = surounding['east']
                        sur['east'] = surounding['north']
                    if rotate == 'left':
                        sur['north'] = surounding['east']
                        sur['east'] = surounding['south']
                        sur['south'] = surounding['west']
                        sur['west'] = surounding['north']
                elif move and rotate == False:
                    sur['north'] = surounding['northnorth']
                    sur['south'] = None
                    sur['west'] = surounding['northwest']
                    sur['east'] = surounding['northeast']
                elif move and rotate != False:
                    if rotate == 'right':
                        sur['north'] = surounding['westwest']
                        sur['west'] = surounding['southwest']
                        sur['south'] = None
                        sur['east'] = surounding['northwest']
                    if rotate == 'left':
                        sur['north'] = surounding['easteast']
                        sur['west'] = surounding['northeast']
                        sur['south'] = None
                        sur['east'] = surounding['southeast']
                else:
                    sur = surounding

                surounding = sur

                result = Larticle_doe(larticle, forbody, surounding)

                if not body.regenerating:
                    body.health -= larticle.brain_drain


                if 'split' in result:

                    if body.regenerating:
                        if not body.attacking:
                            t = surounding['north']
                            dx, dy = int(x + direction[0]), int(y + direction[1])
                            ldir = []
                            for i in body_directions:
                                if i != (-direction[0], -direction[1]):
                                    ldir.append(i)
                        else:
                            t = surounding['south']
                            dx, dy = int(x - direction[0]), int(y - direction[1])
                            ldir = []
                            for i in body_directions:
                                if i != direction:
                                    ldir.append(i)
                    else:
                        t = surounding['south']
                        dx, dy = int(x - direction[0]), int(y - direction[1])
                        ldir = []
                        for i in body_directions:
                            if i != direction:
                                ldir.append(i)

                    dx, dy = recalc_grid(dx, dy)

                    if t == None:
                        handler.count += 1
                        handler.splits += 1
                        larticle.splits += 1
                        name = str(larticle.name.split('_')[0]) + '_' + str(handler.epoch) + '_' + str(
                            handler.splits)

                        r = random.randrange(0, 100)
                        if r <= handler_mutationrate:
                            r2 = random.randrange(0, 100)
                            if r2 >= handler_random_mutationrate:
                                l = Larticle(name,larticle.brain.dna)
                                Larticle_mutate(l)

                            else:
                                l = handler.random_larticles[0]
                                handler.random_larticles.pop(0)
                        else:
                            l = Larticle(name, larticle.brain.dna)
                        l.body.x = dx
                        l.body.y = dy
                        l.body.direction = random.choice(ldir)
                        l.generation = larticle.generation + 1
                        if l.name not in handler.larticles:
                            handler.larticles[l.name] = l
                            handler.positions[str(dx) + '_' + str(dy)] = l.name
                        else:
                            print('Double split name!')

            else:
                died.append(name)
        else:
            died.append(name)
            handler.solardeaths += 1


    for name in died:
        handler.died += 1
        handler.larticles.pop(name)


def Handler_set_visual(handler):
    handler.visual = not handler.visual


def Handler_reset_selected(handler):
    handler.selected_larticle = None
    handler.selected_neuron = None
    handler.selected_forbody = None
    handler.selected_forbrain = None


def Handler_kill_selected(handler):
    if handler.selected_larticle.name in handler.larticles:
        handler.larticles.pop(handler.selected_larticle.name)
        Handler_reset_selected(handler)


def map_color(color):
    r = color[0] * 250 + 50
    g = color[1] * 250 + 50
    b = color[2] * 250 + 50
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return [r, g, b]


def state_color(larticle):
    c = larticle.body.state * 150
    colour = list(larticle.body.colour)
    colour = map_color(colour)
    colour[0] += c - 50
    colour[1] += c - 50
    colour[2] += c - 50
    if colour[0] > 255:
        colour[0] = 255
    if colour[1] > 255:
        colour[1] = 255
    if colour[2] > 255:
        colour[2] = 255
    return colour


def Handler_get_larticle_properties(larticle):
    properties = Body_get_properties(larticle.body)
    properties['age'] = larticle.time_alive
    properties['name'] = larticle.name
    properties['brain drain'] = larticle.brain_drain
    properties['splits'] = larticle.splits
    properties['neuron amount'] = len(larticle.brain.neurons)
    properties['score'] = Larticle_score(larticle)
    properties['generation'] = larticle.generation
    return properties


def Handler_blits_frame(handler, scale, x, y, gx, gy, mx=None, my=None):

    if handler.visual:
        for i in range(constant_grid_size):
            pygame.draw.line(screen.display, grijsdonker, [x, i * scale + scale / 2 + y],
                             [x + constant_grid_size * scale, i * scale + scale / 2 + y])
            pygame.draw.line(screen.display, grijsdonker, [i * scale + scale / 2 + x, y],
                             [i * scale + scale / 2 + x, y + constant_grid_size * scale])

    pygame.draw.rect(screen.display, [0, 0, 0],
                     [screen.y, 0, screen.x, screen.x])
    d = screen.y + 10
    dy = 10
    textsurface = myfont12.render('Epoch: ' + str(handler.epoch), False, (250, 250, 250))
    screen.display.blit(textsurface, (d + 10, 0 + dy))

    textsurface = myfont12.render('Larticles: ' + str(len(handler.larticles)), False, (250, 250, 250))
    screen.display.blit(textsurface, (d + 10, 15 + dy))

    textsurface = myfont12.render('Died: ' + str(handler.died), False, (250, 250, 250))
    screen.display.blit(textsurface, (d + 10, 30 + dy))

    textsurface = myfont12.render('Solar Deaths: ' + str(handler.solardeaths), False, (255, 227, 15))
    screen.display.blit(textsurface, (d + 10, 45 + dy))

    textsurface = myfont12.render('Splits: ' + str(handler.splits), False, (250, 250, 250))
    screen.display.blit(textsurface, (d + 10, 60 + dy))


    dd = int((screen.x - screen.y)*2/5)

    textsurface = myfont12.render('Deaths: ' + str(handler.died - handler.previous_amount_kills), False,
                                  (255, 255, 255))
    screen.display.blit(textsurface, (dd + screen.y, 0 + dy))
    handler.previous_amount_kills = handler.died

    textsurface = myfont12.render('Newborns: ' + str(handler.newbies), False, (250, 250, 250))
    screen.display.blit(textsurface, (dd + screen.y, 15 + dy))

    textsurface = myfont12.render('Eaters: ' + str(handler.eaters), False, (250, 100, 100))
    screen.display.blit(textsurface, (dd + screen.y, 30 + dy))

    textsurface = myfont12.render('Conservatives: ' + str(handler.stupids), False, (100, 250, 100))
    screen.display.blit(textsurface, (dd + screen.y, 45 + dy))

    textsurface = myfont12.render('Regenerators: ' + str(handler.regenerators), False, (100, 100, 250))
    screen.display.blit(textsurface, (dd + screen.y, 60 + dy))

    textsurface = myfont12.render('Walls: ' + str(handler.walls), False, (125, 125, 125))
    screen.display.blit(textsurface, (dd + screen.y, 75 + dy))

    textsurface = myfont12.render('Attackers: ' + str(handler.attacking), False, (250, 150, 100))
    screen.display.blit(textsurface, (dd + screen.y, 90 + dy))



def Handler_blits_map(handler, scale, x, y, gx, gy, mx=None, my=None, map_only=False):

    pos = {}
    doubles = []
    map_x = 0
    map_y = 0
    if map_only:
        if screen.x > screen.y:
            map_x = int((screen.x - screen.y)/2)
        else:
            map_y = int((screen.y - screen.x)/2)
    d = 1
    pygame.draw.rect(screen.display, [150, 150, 150],
                     [x + map_x, y + map_y, int((constant_grid_size + 1) * scale + d),
                      int((constant_grid_size + 1) * scale + d)],
                     d)



    for name in handler.larticles:
        larticle = handler.larticles[name]
        lx = int(larticle.body.x)
        ly = int(larticle.body.y)
        ls = str(lx) + '_' + str(ly)

        lx, ly = recalc_blit(lx, ly, gx, gy)

        if ls not in pos:
            pos[ls] = name
        else:
            doubles.append(name)

        if mx != None and my != None and not map_only:
            if mx < screen.y:
                if abs(lx * scale - handler_click_error * scale) <= mx - x <= abs(
                                        lx * scale + handler_click_error * scale) and abs(
                                    ly * scale - handler_click_error * scale) <= my - y <= abs(
                                    ly * scale + handler_click_error * scale):
                    handler.selected_larticle = larticle
        if not handler.visual:
            k = map_color(larticle.body.colour)
        else:
            k = state_color(larticle)
        pygame.draw.circle(screen.display, k,
                            [int(lx * scale + x + map_x), int(ly * scale + y + map_y)],
                            int(scale / 2))

        if handler.visual:
            if larticle.body.talking:
                kleur = [250, 100, 250]
            else:
                kleur = [0, 0, 0]


            if larticle.body.frozen:
                pygame.draw.circle(screen.display, [250, 250, 250],
                                    [int(lx * scale + x + map_x), int(ly * scale + y + map_y)],
                                    int(scale / 2 + 1), 2)

            if larticle.body.give_health:
                direction = Body_rotate_right(larticle.body.direction)
                pygame.draw.circle(screen.display, [255, 227, 15],
                                    [int((lx - direction[0] / 8) * scale + x + map_x),
                                    int((ly - direction[1] / 8) * scale + y + map_y)], int(scale / 10))
            pygame.draw.line(screen.display, kleur,
                                [int((lx + larticle.body.direction[0] / 2) * scale + x + map_x),
                                int((ly + larticle.body.direction[1] / 2) * scale + y + map_y)],
                                [int(lx * scale + x + map_x), int(ly * scale + y + map_y)], int(scale / 5))




        else:
            pygame.draw.line(screen.display, [0, 0, 0],
                                [int((lx + larticle.body.direction[0] / 2) * scale + x + map_x),
                                int((ly + larticle.body.direction[1] / 2) * scale + y + map_y)],
                                [int(lx * scale + x + map_x), int(ly * scale + y + map_y)], int(scale / 5))



    for sun in handler.suns:
        sx, sy = recalc_blit(sun[0],sun[1],gx,gy)
        pygame.draw.circle(screen.display, [255, 227, 15],
                            [int(sx * scale + x + map_x), int(sy * scale + y + map_y)],
                            int(scale), int(scale / 3))

    if map_only:
        pygame.draw.rect(screen.display,zwart,[0,0,map_x,screen.y])
        pygame.draw.rect(screen.display,zwart,[screen.x - map_x,0,map_x,screen.y])
        pygame.draw.rect(screen.display,zwart,[0,0,screen.x,map_y])
        pygame.draw.rect(screen.display,zwart,[0,screen.y - map_y,screen.x,map_y])
        pygame.draw.rect(screen.display,grijs,[map_x,map_y,screen.x - 2*map_x,screen.y - 2*map_y],1)

    for name in doubles:
        print('Double: ', name)
        if name in handler.larticles:
            x, y = handler.larticles[name].body.x, handler.larticles[name].body.y
            s = str(x) + '_' + str(y)
            print('Pos: ', x, y)
            print('Age: ', handler.larticles[name].time_alive)
            print('Commands', handler.larticles[name].previous_memory)
            if pos[s] in handler.larticles:
                l = handler.larticles[pos[s]]
                print('  Larticle now at pos: ', l.name)
                print('  pos', l.body.x, l.body.y)
                print('  age', l.time_alive)
                print('  Commands', l.previous_memory)
            else:
                print('  Larticle at pos not found')
            print('Deleted.')
            handler.larticles.pop(name)
            handler.died += 1
        else:
            print('Not found.')

    handler.positions = pos


def voice_scale(s):
    m = max([s[0], s[1]])
    s1, s2 = s
    if m != 0:
        c1 = float(s1 / m)
        c2 = float(s2 / m)
        c3 = 0
    else:
        c1, c2, c3 = 0, 0, 0
    return c1, c2, c3


def Handler_show_selected_larticle(handler, scale, x, y, gx, gy, mx=None, my=None):
    dyy = 150
    pygame.draw.rect(screen.display,grijsdonker,[screen.y,dyy,screen.y,screen.y])
    selected = handler.selected_larticle
    body = selected.body
    brain = selected.brain
    neuronradius = 5
    circleradius = int((screen.y) / 4)
    circleposition = [int(screen.y + circleradius + 3 * neuronradius),int(screen.y - (circleradius + 3 * neuronradius))]

    xs = 10
    xi = 70
    dy = 15
    ty = 15
    textsurface = myfont12.render('Name: ', False, wit)
    screen.display.blit(textsurface, (screen.y + xs,dy + dyy))
    textsurface = myfont12.render(str(handler.selected_larticle.name), False, wit)
    screen.display.blit(textsurface, (screen.y + xi, dy + dyy))
    dy += ty
    textsurface = myfont12.render('Age: ', False, wit)
    screen.display.blit(textsurface, (screen.y + xs,dy + dyy))
    textsurface = myfont12.render(str(handler.selected_larticle.time_alive), False, wit)
    screen.display.blit(textsurface, (screen.y + xi,dy + dyy))
    dy += ty
    textsurface = myfont12.render('Children: ', False, wit)
    screen.display.blit(textsurface, (screen.y + xs,dy + dyy))
    textsurface = myfont12.render(str(handler.selected_larticle.splits), False, wit)
    screen.display.blit(textsurface, (screen.y + xi,dy + dyy))
    dy += ty
    textsurface = myfont12.render('Kills: ', False, wit)
    screen.display.blit(textsurface, (screen.y + xs,dy + dyy))
    textsurface = myfont12.render(str(handler.selected_larticle.body.kills), False, wit)
    screen.display.blit(textsurface, (screen.y + xi,dy + dyy))
    dy += ty



    lx, ly = recalc_blit(body.x, body.y, gx, gy)
    if 0 <= int(lx * scale + x) <= screen.y:
        pygame.draw.circle(screen.display, paars, [int(lx * scale + x),
                                                            int(ly * scale + y)],
                           int(scale * 3), int(scale))

    neuronpositions = {}
    fullcircle = len(brain.neurons)
    count = 0
    for neuronname in sorted(brain.neurons.keys()):
        neuronpositions[neuronname] = [int(circleradius * math.cos(2 * math.pi * count / fullcircle) + circleposition[0]),
                       int(circleradius * math.sin(2 * math.pi * count / fullcircle) + circleposition[1])]
        count += 1

    for name1,name2,weight in brain.dna:
        if weight < 0:
            kleur = rood
        else:
            kleur = groen
        pygame.draw.line(screen.display,kleur,neuronpositions[name1],neuronpositions[name2],int(abs(weight) +1))

    for name in neuronpositions:
        if mx != None:
            if neuronpositions[name][0] - neuronradius < mx < neuronpositions[name][0] + neuronradius:
                if neuronpositions[name][1] - neuronradius < my < neuronpositions[name][1] + neuronradius:
                    handler.selected_neuron = brain.neurons[name]

        if name in body_commands:
            kleur = rood
        elif name in body_perception:
            kleur = groen
        else:
            kleur = blauw
        pygame.draw.circle(screen.display,kleur,neuronpositions[name],neuronradius)
        pygame.draw.circle(screen.display,wit,neuronpositions[name],neuronradius,1)

    if handler.selected_neuron != None:
        pygame.draw.circle(screen.display,paars,neuronpositions[handler.selected_neuron.name],neuronradius * 2, neuronradius)
        textsurface = myfont12.render(str(handler.selected_neuron.name), False, wit)
        screen.display.blit(textsurface, (screen.x - int((screen.x - screen.y)/2),screen.y - 20 ))

        connections = []
        connectionstemp = []
        connectionstemp += Neuron_get_connections(handler.selected_neuron)
        while connectionstemp != []:
            c = list(connectionstemp)
            connectionstemp = []
            for name1,name2,weight in c:
                connections.append([name1,name2])
                connectionstemp += Neuron_get_connections(brain.neurons[name2])

        for name1,name2 in connections:
            pygame.draw.line(screen.display,paars,neuronpositions[name1],neuronpositions[name2],neuronradius)
            textsurface = myfont15.render(str(' '.join(name1.split('_')[1:])), False, wit)
            screen.display.blit(textsurface, (neuronpositions[name1], neuronpositions[name1]))
            textsurface = myfont15.render(str(' '.join(name2.split('_')[1:])), False, wit)
            screen.display.blit(textsurface, (neuronpositions[name2], neuronpositions[name2]))














def Handler_blits_selected_larticle(display, handler, scale, x, y, gx, gy, mx=None, my=None):


    selected = handler.selected_larticle

    dy = 120
    if selected != None:
        body = selected.body
        brain = selected.brain
        Brain_get_dna(selected)
        lx, ly = recalc_blit(body.x, body.y, gx, gy)
        if 0 <= int(lx * scale + x) <= screen.y:
            pygame.draw.circle(screen.display, [211, 14, 237], [int(lx * scale + x),
                                                                int(ly * scale + y)],
                               int(scale * 3), int(scale))
        properties = Handler_get_larticle_properties(selected)
        i = 0
        for prop in list(sorted(properties.keys())):
            i += 1
            textsurface = myfont12.render(str(prop) + ': ' + str(properties[prop]), False, (250, 250, 250))
            screen.display.blit(textsurface, (screen.y + 20, dy + (i + 1) * 15))

        r = int(screen.y / 4)
        t = len(brain.neurons)
        tt = 0
        tttt = 0
        tttttt = 0
        pos = {}
        dx = 250
        for neuron in sorted(brain.neurons.keys()):

            pos[neuron] = [r * math.cos(2 * math.pi * tt / t) + screen.y - r - 150,
                           r * math.sin(2 * math.pi * tt / t) + screen.y - r - 50]
            tt += 1
            n = brain.neurons[neuron].name
            if n.split('_')[0] != 'hidden':
                p = brain.neurons[neuron].potential
                if n != 'command_split' and n != 'command_eat':
                    if p > 0.5:
                        kleur = [100, 250, 100]
                    else:
                        kleur = [250, 100, 100]
                else:
                    if p >= 0.5:
                        kleur = [100, 250, 100]
                    else:
                        kleur = [250, 100, 100]
                textsurface = myfont12.render(
                    n + ' = ' + str(p)[0:6],
                    False,
                    kleur)
                if n in body_perception:
                    screen.display.blit(textsurface, (screen.y + dx, dy + 12 * tttt))
                    tttt += 1
                elif n in body_commands:
                    screen.display.blit(textsurface, (screen.y + 2 * dx - 20, dy + 12 * tttttt))
                    tttttt += 1

        for name1, name2, weight in brain.dna:
            kleur = [0, 250, 0]
            if weight < 0:
                kleur = [250, 0, 0]
            if name1 in pos and name2 in pos:
                pygame.draw.line(screen.display, kleur, pos[name1], pos[name2], int(abs(weight) + 1))
            else:
                print(name1, name2, weight)

        size = 5
        for name in pos:
            if mx != None and my != None:
                if pos[name][0] - size < mx < pos[name][0] + size and pos[name][1] - size < my < pos[name][
                    1] + size:
                    handler.selected_neuron = brain.neurons[name]
            kleur = [250, 100, 100]
            if name != 'command_eat' or name != 'command_split':
                if brain.neurons[name].potential > 0.5:
                    kleur = [100, 250, 100]
            else:
                if brain.neurons[name].potential >= 0.5:
                    kleur = [100, 250, 100]
            pygame.draw.circle(screen.display, kleur,
                               [int(pos[name][0]), int(pos[name][1])],
                               int(size))

        if handler.selected_neuron != None:

            if handler.selected_neuron.name in body_perception:
                kleur = [100, 250, 100]
            elif handler.selected_neuron.name in body_commands:
                kleur = [250, 100, 100]
            else:
                kleur = [100, 100, 250]
            textsurface = myfont12.render(str(handler.selected_neuron.name) + ': ' + str(
                brain.neurons[handler.selected_neuron.name].potential), False,
                                          kleur)
            screen.display.blit(textsurface, (screen.y + 10, screen.y - 30))

            if handler.selected_neuron.name in pos:
                pygame.draw.circle(screen.display, [250, 250, 250],
                                   [int(pos[handler.selected_neuron.name][0]),
                                    int(pos[handler.selected_neuron.name][1])],
                                   int(size * 3), 4)
            connections = Neuron_get_connections(brain.neurons[handler.selected_neuron.name])
            names = []
            for name1, name2, weight in connections:
                names.append(name2)
                pygame.draw.line(screen.display, [250, 0, 250], pos[name1], pos[name2], 3)
            names2 = []
            for name in names:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    names2.append(name2)
                    pygame.draw.line(screen.display, [250, 0, 250], pos[name1], pos[name2], 3)
            names3 = []
            for name in names2:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    names3.append(name2)
                    pygame.draw.line(screen.display, [250, 0, 250], pos[name1], pos[name2], 3)
            for name in names3:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    pygame.draw.line(screen.display, [250, 0, 250], pos[name1], pos[name2], 3)


class Simulation():
    def __init__(self):
        self.initialized = False
        print('')
        print('Initializing Simulation.')
        print('')

        self.set_scale()
        self.handler = Handler()
        self.saved_larticles = {}
        self.time0 = time.time()
        self.running = True
        self.blits = True
        self.memory = []
        self.autoselect = False
        self.previous_handler = None
        self.starts = 0
        self.map_only = False
        print('')
        print('Initializing Simulation Succes.')
        print('')

    def set_scale(self):
        if screen.x > screen.y:
            self.beginscale = float(screen.y / (constant_grid_size + 1))
        else:
            self.beginscale = float(screen.x / (constant_grid_size + 1))
        self.scale = float(self.beginscale)
    def Simulation_reset(self):
        self.handler = Handler()
        self.set_scale()

    def onresize(self,w,h):
        screen.x,screen.y = w,h
        self.set_scale()

    def Simulation_run(self):
        self.initialized = True
        x = 0
        y = 0
        gx = 0
        gy = 0

        dxr = 0
        dxl = 0
        dyu = 0
        dyd = 0
        dgxr = 0
        dgxl = 0
        dgyu = 0
        dgyd = 0

        speed = 4 * self.scale
        speed2 = 1
        scrollspeed = 0.5
        stop = False
        checking = False

        while not stop:

            if len(self.handler.larticles) <= 0:
                print('No more larticles.')
                self.handler = Handler()
                self.starts += 1

            if len(self.handler.random_larticles) <= handler_random_larticles_amount and not checking:
                checking = True
                print('Appending buffer.')
                p = subprocess.Popen('python create_random_larticles.py', creationflags=0x08000000)

            if checking:
                r = p.poll()
                if r != None:
                    file = open('Random_larticles.pickle', 'rb')
                    l = pickle.load(file)
                    self.handler.random_larticles += l
                    file.close()
                    checking = False
                    p.kill()
                    print('Buffer appended.')

            time0 = time.time()

            mx = None
            my = None

            gx, gy = recalc_grid(gx, gy)

            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()

                elif event.type == pygame.VIDEORESIZE:
                    self.onresize(event.w,event.h)

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_HOME:
                        self.Simulation_reset()
                    elif event.key == pygame.K_RETURN:
                        stop = True
                    elif event.key == pygame.K_F1:
                        self.map_only = not self.map_only
                    elif event.key == pygame.K_k:
                        Handler_kill_selected(self.handler)
                    elif event.key == pygame.K_s:
                        dgyd = speed2
                    elif event.key == pygame.K_w:
                        dgyu = -speed2
                    elif event.key == pygame.K_a:
                        dgxl = -speed2
                    elif event.key == pygame.K_d:
                        dgxr = speed2
                    elif event.key == pygame.K_c:
                        Handler_run(self.handler)
                    elif event.key == pygame.K_r:
                        gx, gy = 0, 0
                    elif event.key == pygame.K_y:
                        self.autoselect = not self.autoselect

                    elif event.key == pygame.K_END:
                        self.scale = self.beginscale
                        x = 0
                        y = 0

                    elif event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_INSERT:
                        self.running = not self.running

                    elif event.key == pygame.K_PAGEUP:
                        self.blits = not self.blits

                    elif event.key == pygame.K_PAGEDOWN:
                        Handler_set_visual(self.handler)

                    elif event.key == pygame.K_KP_ENTER:
                        stop = True
                        break

                    elif event.key == pygame.K_DOWN:
                        dyd = speed
                    elif event.key == pygame.K_UP:
                        dyu = -speed
                    elif event.key == pygame.K_LEFT:
                        dxl = -speed
                    elif event.key == pygame.K_RIGHT:
                        dxr = speed

                    elif event.key == pygame.K_f:
                        screen.toggle_fullscreen()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dyd = 0
                    elif event.key == pygame.K_UP:
                        dyu = -0
                    elif event.key == pygame.K_LEFT:
                        dxl = -0
                    elif event.key == pygame.K_RIGHT:
                        dxr = 0
                    elif event.key == pygame.K_s:
                        dgyd = 0
                    elif event.key == pygame.K_w:
                        dgyu = 0
                    elif event.key == pygame.K_a:
                        dgxl = 0
                    elif event.key == pygame.K_d:
                        dgxr = 0


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                    elif event.button == 3:
                        Handler_reset_selected(self.handler)
                    elif event.button == 4 and self.scale <= 50:
                        self.scale += scrollspeed
                    elif event.button == 5 and self.scale > 1 + scrollspeed:
                        self.scale -= scrollspeed

            x -= dxl + dxr
            y -= dyd + dyu
            gx -= dgxl + dgxr
            gy -= dgyd + dgyu


            screen.display.fill(zwart)

            if not self.map_only:
                pygame.draw.line(screen.display, [150, 150, 150], [screen.y, 0],
                                 [screen.y, screen.y], 3)

            if self.running:
                Handler_run(self.handler, self.autoselect)
            Handler_blits_map(self.handler, self.scale, x, y, gx, gy, mx, my,self.map_only)

            if screen.x - screen.y > 200 and not self.map_only:
                Handler_blits_frame(self.handler, self.scale, x, y, gx, gy, mx, my)
            if self.handler.selected_larticle != None and not self.map_only:
                Handler_show_selected_larticle(self.handler, self.scale, x, y, gx, gy, mx, my)

            time1 = time.time()
            tijd = time1 - time0

            d = int((screen.x - screen.y)*3/4)
            dy = 10
            if screen.x - screen.y > 300 and not self.map_only:
                textsurface = myfont12.render('Runtime: ' + str(tijd), False, (250, 250, 250))
                screen.display.blit(textsurface, (screen.y + d, 0 + dy))
                textsurface = myfont12.render('Elapsed: ' + str((time.time() - self.time0)), False, (250, 250, 250))
                screen.display.blit(textsurface, (screen.y + d, 15 + dy))
                textsurface = myfont12.render('Starts: ' + str(self.starts), False, (250, 250, 250))
                screen.display.blit(textsurface, (screen.y + d, 30 + dy))
                textsurface = myfont12.render('Random Brains: ' + str(len(self.handler.random_larticles)), False,
                                              (250, 250, 250))
                screen.display.blit(textsurface, (screen.y + d, 45 + dy))


            mainrect = [screen.x - 50, screen.y - 20, 50, 20]

            pygame.draw.rect(screen.display, rood, mainrect)
            textsurface = myfont12.render('Main', False, (0, 0, 0))
            screen.display.blit(textsurface, (mainrect))

            if mx != None and my != None:
                if mainrect[0] < mx < mainrect[0] + mainrect[2]:
                    if mainrect[1] < my < mainrect[1] + mainrect[3]:
                        stop = True

            pygame.display.update()
            if self.running:
                screen.clock.tick()
            else:
                screen.clock.tick(30)

