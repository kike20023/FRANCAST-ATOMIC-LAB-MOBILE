# /// script
# dependencies = ["pygame-ce"]
# ///
import os
import sys
import asyncio
import math
import random
import unicodedata
import pygame

# ============================================================
# FRANCAST ATOMIC LAB — MOBILE
# Versión vertical/táctil para Android y prueba en PC.
# Desarrollado por Jorge Enrique Castellanos Franco
# ============================================================

pygame.init()

# Resolución lógica vertical. Pygame SCALED adapta la vista a la pantalla real.
ANCHO, ALTO = 720, 1280
FPS = 60
IS_ANDROID = "ANDROID_ARGUMENT" in os.environ or "ANDROID_PRIVATE" in os.environ
flags = pygame.SCALED | (pygame.FULLSCREEN if IS_ANDROID else pygame.RESIZABLE)
pantalla = pygame.display.set_mode((ANCHO, ALTO), flags)
pygame.display.set_caption("FRANCAST ATOMIC LAB // MOBILE")
reloj = pygame.time.Clock()

# Tipografía: se usan fuentes del sistema para no depender de archivos externos.
def sysfont(size, bold=False):
    return pygame.font.SysFont("segoeui", size, bold=bold)

FONT_XS = sysfont(16)
FONT_S = sysfont(20)
FONT_M = sysfont(25)
FONT_L = sysfont(33, True)
FONT_XL = sysfont(66, True)
FONT_SYMBOL = sysfont(30, True)
FONT_CONFIG = sysfont(25, True)

BG_TOP = (3, 9, 18)
BG_BOTTOM = (8, 28, 40)
PANEL = (7, 22, 33)
PANEL_2 = (11, 35, 47)
WHITE = (226, 244, 248)
GRAY = (105, 143, 153)
CYAN = (0, 235, 255)
GREEN = (65, 255, 155)
YELLOW = (255, 211, 80)
RED = (255, 82, 100)
DARK = (4, 16, 24)

COLORS = {
    "Metal alcalino": (255, 92, 104),
    "Metal alcalinotérreo": (255, 157, 72),
    "Metal de transición": (62, 159, 243),
    "Metal postransición": (62, 194, 205),
    "Metaloide": (79, 204, 134),
    "No metal": (94, 224, 102),
    "Halógeno": (211, 221, 70),
    "Gas noble": (180, 101, 244),
    "Lantánido": (239, 99, 175),
    "Actínido": (215, 80, 126),
}

DESCRIPTIONS = {
    "Metal alcalino": "Metal blando y muy reactivo del grupo 1. Tiende a perder un electrón.",
    "Metal alcalinotérreo": "Metal reactivo del grupo 2 con dos electrones de valencia.",
    "Metal de transición": "Buen conductor, resistente y con estados de oxidación variables.",
    "Metal postransición": "Metal relativamente blando, situado después del bloque de transición.",
    "Metaloide": "Presenta propiedades intermedias; varios son semiconductores importantes.",
    "No metal": "Conduce poco el calor y participa en numerosos compuestos esenciales.",
    "Halógeno": "No metal muy reactivo del grupo 17 que suele formar sales.",
    "Gas noble": "Elemento del grupo 18 con una capa exterior especialmente estable.",
    "Lantánido": "Metal de tierras raras del bloque f, usado en óptica e imanes.",
    "Actínido": "Elemento pesado del bloque f; todos sus integrantes son radiactivos.",
}

RAW_DATA = """
H|Hidrógeno|1.008
He|Helio|4.0026
Li|Litio|6.94
Be|Berilio|9.0122
B|Boro|10.81
C|Carbono|12.011
N|Nitrógeno|14.007
O|Oxígeno|15.999
F|Flúor|18.998
Ne|Neón|20.180
Na|Sodio|22.990
Mg|Magnesio|24.305
Al|Aluminio|26.982
Si|Silicio|28.085
P|Fósforo|30.974
S|Azufre|32.06
Cl|Cloro|35.45
Ar|Argón|39.948
K|Potasio|39.098
Ca|Calcio|40.078
Sc|Escandio|44.956
Ti|Titanio|47.867
V|Vanadio|50.942
Cr|Cromo|51.996
Mn|Manganeso|54.938
Fe|Hierro|55.845
Co|Cobalto|58.933
Ni|Níquel|58.693
Cu|Cobre|63.546
Zn|Zinc|65.38
Ga|Galio|69.723
Ge|Germanio|72.630
As|Arsénico|74.922
Se|Selenio|78.971
Br|Bromo|79.904
Kr|Kriptón|83.798
Rb|Rubidio|85.468
Sr|Estroncio|87.62
Y|Itrio|88.906
Zr|Circonio|91.224
Nb|Niobio|92.906
Mo|Molibdeno|95.95
Tc|Tecnecio|98
Ru|Rutenio|101.07
Rh|Rodio|102.91
Pd|Paladio|106.42
Ag|Plata|107.87
Cd|Cadmio|112.41
In|Indio|114.82
Sn|Estaño|118.71
Sb|Antimonio|121.76
Te|Telurio|127.60
I|Yodo|126.90
Xe|Xenón|131.29
Cs|Cesio|132.91
Ba|Bario|137.33
La|Lantano|138.91
Ce|Cerio|140.12
Pr|Praseodimio|140.91
Nd|Neodimio|144.24
Pm|Prometio|145
Sm|Samario|150.36
Eu|Europio|151.96
Gd|Gadolinio|157.25
Tb|Terbio|158.93
Dy|Disprosio|162.50
Ho|Holmio|164.93
Er|Erbio|167.26
Tm|Tulio|168.93
Yb|Iterbio|173.05
Lu|Lutecio|174.97
Hf|Hafnio|178.49
Ta|Tantalio|180.95
W|Wolframio|183.84
Re|Renio|186.21
Os|Osmio|190.23
Ir|Iridio|192.22
Pt|Platino|195.08
Au|Oro|196.97
Hg|Mercurio|200.59
Tl|Talio|204.38
Pb|Plomo|207.2
Bi|Bismuto|208.98
Po|Polonio|209
At|Astato|210
Rn|Radón|222
Fr|Francio|223
Ra|Radio|226
Ac|Actinio|227
Th|Torio|232.04
Pa|Protactinio|231.04
U|Uranio|238.03
Np|Neptunio|237
Pu|Plutonio|244
Am|Americio|243
Cm|Curio|247
Bk|Berkelio|247
Cf|Californio|251
Es|Einstenio|252
Fm|Fermio|257
Md|Mendelevio|258
No|Nobelio|259
Lr|Lawrencio|266
Rf|Rutherfordio|267
Db|Dubnio|268
Sg|Seaborgio|269
Bh|Bohrio|270
Hs|Hassio|269
Mt|Meitnerio|278
Ds|Darmstadtio|281
Rg|Roentgenio|282
Cn|Copernicio|285
Nh|Nihonio|286
Fl|Flerovio|289
Mc|Moscovio|290
Lv|Livermorio|293
Ts|Teneso|294
Og|Oganesón|294
""".strip().splitlines()

ALKALI = {3, 11, 19, 37, 55, 87}
ALKALINE = {4, 12, 20, 38, 56, 88}
HALOGENS = {9, 17, 35, 53, 85, 117}
NOBLE = {2, 10, 18, 36, 54, 86, 118}
METALLOIDS = {5, 14, 32, 33, 51, 52}
NONMETALS = {1, 6, 7, 8, 15, 16, 34}
POST = {13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116}
GASES = {1, 2, 7, 8, 9, 10, 17, 18, 36, 54, 86}
LIQUIDS = {35, 80}
SYNTHETIC = {43, 61} | set(range(93, 119))
RADIOACTIVE = {43, 61} | set(range(84, 119))


def category(z):
    if z in ALKALI: return "Metal alcalino"
    if z in ALKALINE: return "Metal alcalinotérreo"
    if z in HALOGENS: return "Halógeno"
    if z in NOBLE: return "Gas noble"
    if z in METALLOIDS: return "Metaloide"
    if z in NONMETALS: return "No metal"
    if z in POST: return "Metal postransición"
    if 57 <= z <= 71: return "Lantánido"
    if 89 <= z <= 103: return "Actínido"
    return "Metal de transición"


def state(z):
    if z in GASES: return "Gas"
    if z in LIQUIDS: return "Líquido"
    if z >= 104: return "Estimado / desconocido"
    return "Sólido"


ORBITALS = [
    (1, "s", 2), (2, "s", 2), (2, "p", 6), (3, "s", 2),
    (3, "p", 6), (4, "s", 2), (3, "d", 10), (4, "p", 6),
    (5, "s", 2), (4, "d", 10), (5, "p", 6), (6, "s", 2),
    (4, "f", 14), (5, "d", 10), (6, "p", 6), (7, "s", 2),
    (5, "f", 14), (6, "d", 10), (7, "p", 6),
]
SHELL_EXCEPTIONS = {
    24: [2, 8, 13, 1], 29: [2, 8, 18, 1],
    41: [2, 8, 18, 12, 1], 42: [2, 8, 18, 13, 1],
    44: [2, 8, 18, 15, 1], 45: [2, 8, 18, 16, 1],
    46: [2, 8, 18, 18], 47: [2, 8, 18, 18, 1],
    78: [2, 8, 18, 32, 17, 1], 79: [2, 8, 18, 32, 18, 1],
}


def electron_data(z):
    remaining = z
    occupations, shells = [], [0] * 7
    for n, sub, capacity in ORBITALS:
        if remaining <= 0: break
        used = min(remaining, capacity)
        occupations.append(f"{n}{sub}{used}")
        shells[n - 1] += used
        remaining -= used
    while shells and shells[-1] == 0: shells.pop()
    if z in SHELL_EXCEPTIONS: shells = SHELL_EXCEPTIONS[z]
    return shells, " ".join(occupations)


def group_period(z):
    # Datos suficientes para la ficha móvil. Los lantánidos/actínidos usan 3*.
    periods = [2, 10, 18, 36, 54, 86, 118]
    period = next(i + 1 for i, n in enumerate(periods) if z <= n)
    if z == 1: return 1, 1
    if z == 2: return 18, 1
    rows = {
        2: (3, 10), 3: (11, 18), 4: (19, 36), 5: (37, 54),
        6: (55, 86), 7: (87, 118)
    }
    start, end = rows[period]
    if period in (2, 3):
        offset = z - start
        group = offset + 1 if offset < 2 else offset + 11
    elif period in (4, 5): group = z - start + 1
    elif period == 6:
        if z <= 56: group = z - 54
        elif 57 <= z <= 71: group = "3*"
        else: group = z - 68
    else:
        if z <= 88: group = z - 86
        elif 89 <= z <= 103: group = "3*"
        else: group = z - 100
    return group, period


def block_for(group, z):
    if 57 <= z <= 71 or 89 <= z <= 103: return "f"
    if group in (1, 2) or z == 2: return "s"
    if isinstance(group, int) and group >= 13: return "p"
    return "d"


elements = []
for z, line in enumerate(RAW_DATA, 1):
    symbol, name, mass = line.split("|")
    group, period = group_period(z)
    shells, configuration = electron_data(z)
    elements.append({
        "z": z, "symbol": symbol, "name": name, "mass": float(mass),
        "group": group, "period": period, "category": category(z),
        "state": state(z), "shells": shells, "configuration": configuration,
        "block": block_for(group, z), "origin": "Sintético" if z in SYNTHETIC else "Natural",
        "radioactive": "Sí" if z in RADIOACTIVE else "No",
    })


def text(value, x, y, color=WHITE, font=FONT_M, center=False, surface=None):
    target = surface or pantalla
    img = font.render(str(value), True, color)
    rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
    target.blit(img, rect)
    return rect


def normalized(value):
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(c for c in value if unicodedata.category(c) != "Mn")


def wrap(value, font, width):
    lines, current = [], ""
    for word in str(value).split():
        attempt = (current + " " + word).strip()
        if font.size(attempt)[0] <= width:
            current = attempt
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines


SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def pretty_configuration(configuration):
    parts = []
    for orbital in configuration.split():
        parts.append(orbital[:2] + orbital[2:].translate(SUPERSCRIPT))
    return "  ".join(parts)


class Particle:
    def __init__(self):
        self.x = random.randrange(ANCHO); self.y = random.randrange(ALTO)
        self.speed = random.uniform(.2, .8); self.r = random.choice((1, 1, 2))
    def update_draw(self):
        self.y += self.speed
        if self.y > ALTO: self.y = 0; self.x = random.randrange(ANCHO)
        pygame.draw.circle(pantalla, (0, 96, 112), (int(self.x), int(self.y)), self.r)

particles = [Particle() for _ in range(55)]


def draw_background():
    # Degradado económico en móvil: bandas de 8 px.
    for y in range(0, ALTO, 8):
        p = y / ALTO
        c = tuple(int(BG_TOP[i] * (1-p) + BG_BOTTOM[i] * p) for i in range(3))
        pygame.draw.rect(pantalla, c, (0, y, ANCHO, 8))
    for x in range(0, ANCHO, 45): pygame.draw.line(pantalla, (6, 29, 39), (x, 0), (x, ALTO))
    for y in range(0, ALTO, 45): pygame.draw.line(pantalla, (6, 29, 39), (0, y), (ANCHO, y))
    for p in particles: p.update_draw()


# ---------------------- ÁTOMO 3D ----------------------
atom_rot_x = -0.35
atom_rot_y = 0.45
atom_dragging = False
atom_box_rect = pygame.Rect(0, 0, 0, 0)
last_pointer = (0, 0)


def rotate_point_3d(x, y, z, rx, ry):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    y, z = y * cx - z * sx, y * sx + z * cx
    x, z = x * cy + z * sy, -x * sy + z * cy
    return x, y, z


def project_point_3d(x, y, z, cx, cy, camera=470.0):
    denom = max(140.0, camera - z)
    scale = camera / denom
    return cx + x * scale, cy + y * scale, scale, z


def orbital_point(radius, angle, tilt_x, tilt_z):
    x, y, z = radius * math.cos(angle), radius * math.sin(angle), 0.0
    cx, sx = math.cos(tilt_x), math.sin(tilt_x)
    y, z = y * cx - z * sx, y * sx + z * cx
    cz, sz = math.cos(tilt_z), math.sin(tilt_z)
    x, y = x * cz - y * sz, x * sz + y * cz
    return x, y, z


def draw_atom_3d(e, rect, elapsed):
    global atom_rot_y
    c = COLORS[e["category"]]
    cx, cy = rect.centerx, rect.centery + 8
    shell_count = max(1, len(e["shells"]))
    max_r = min(rect.w * .39, rect.h * .37)
    step = max_r / shell_count
    if not atom_dragging: atom_rot_y += 0.004
    tilts = [(0.25,0.0),(0.75,.45),(-.55,.9),(1.05,-.55),(-.9,-.25),(.45,1.15),(-.3,-1.0)]

    for shell_index in range(1, shell_count + 1):
        radius = step * shell_index
        tx, tz = tilts[(shell_index - 1) % len(tilts)]
        pts = []
        for j in range(64):
            a = math.tau * j / 64
            x,y,z = orbital_point(radius,a,tx,tz)
            x,y,z = rotate_point_3d(x,y,z,atom_rot_x,atom_rot_y)
            px,py,_,_ = project_point_3d(x,y,z,cx,cy)
            pts.append((int(px),int(py)))
        pygame.draw.aalines(pantalla, (45,104,118), True, pts)

    dots = []
    for shell_index, count in enumerate(e["shells"],1):
        radius = step * shell_index
        tx,tz = tilts[(shell_index-1)%len(tilts)]
        direction = -1 if shell_index % 2 else 1
        speed = .35 + shell_index*.05
        for i in range(count):
            a = elapsed*speed*direction + math.tau*i/max(1,count)
            x,y,z = orbital_point(radius,a,tx,tz)
            x,y,z = rotate_point_3d(x,y,z,atom_rot_x,atom_rot_y)
            px,py,scale,depth = project_point_3d(x,y,z,cx,cy)
            dots.append((depth,px,py,scale))
    for depth,px,py,scale in sorted(dots):
        rr = max(2,int(4*scale))
        pygame.draw.circle(pantalla, WHITE, (int(px),int(py)), rr)
        pygame.draw.circle(pantalla, c, (int(px),int(py)), max(1,rr//2))

    halo = pygame.Surface((110,110), pygame.SRCALPHA)
    pygame.draw.circle(halo, (*c,35), (55,55), 52)
    pygame.draw.circle(halo, (*c,75), (55,55), 37)
    pantalla.blit(halo,(cx-55,cy-55))
    pygame.draw.circle(pantalla,c,(cx,cy),24)
    pygame.draw.circle(pantalla,WHITE,(cx,cy),9)
    text(e["symbol"],cx,cy,(5,16,22),FONT_XS,True)


# ---------------------- ESTADO APP ----------------------
mode = "Tabla"
selected = elements[25]  # Hierro
compare_a = None
compare_b = None
compare_target = None
show_picker = False
picker_scroll = 0.0
table_scroll = 0.0
scroll_dragging = False
scroll_last_y = 0
search = ""
search_active = False

quiz_question = None
quiz_options = []
quiz_correct = None
quiz_score = 0
quiz_total = 0
quiz_feedback = ""
quiz_feedback_color = WHITE
quiz_next_at = 0
quiz_rects = []

NAV_H = 88
HEADER_H = 92
SEARCH_H = 58
CONTENT_TOP = HEADER_H + SEARCH_H + 12
CONTENT_BOTTOM = ALTO - NAV_H - 10
NAVS = [("Tabla","TABLA"),("Config","CONFIG."),("Comparar","COMPARAR"),("Quiz","QUIZ")]
nav_rects = {}
search_rect = pygame.Rect(20, HEADER_H + 4, ANCHO - 40, 48)


def current_filtered():
    q = normalized(search.strip())
    if not q: return elements
    return [e for e in elements if q in normalized(f"{e['z']} {e['symbol']} {e['name']}")]


def panel(rect, color=CYAN, width=1, fill=PANEL):
    pygame.draw.rect(pantalla, fill, rect, border_radius=14)
    pygame.draw.rect(pantalla, color, rect, width, border_radius=14)


def draw_header():
    pygame.draw.rect(pantalla, PANEL, (14, 12, ANCHO-28, 76), border_radius=14)
    pygame.draw.rect(pantalla, CYAN, (14,12,ANCHO-28,76), 2, border_radius=14)
    text("FRANCAST ATOMIC LAB", 32, 25, CYAN, FONT_L)
    text("Conocimiento en tus manos • MOBILE", 34, 62, GREEN, FONT_XS)

    pygame.draw.rect(pantalla, DARK, search_rect, border_radius=11)
    pygame.draw.rect(pantalla, CYAN if search_active else GRAY, search_rect, 2 if search_active else 1, border_radius=11)
    shown = search if search else "Buscar elemento..."
    text("⌕", search_rect.x+14, search_rect.y+9, CYAN, FONT_M)
    text(shown, search_rect.x+48, search_rect.y+12, WHITE if search else GRAY, FONT_S)


def draw_nav():
    y = ALTO - NAV_H
    pygame.draw.rect(pantalla, PANEL, (0,y,ANCHO,NAV_H))
    pygame.draw.line(pantalla, (31,89,102), (0,y),(ANCHO,y),2)
    w = ANCHO // 4
    nav_rects.clear()
    for i,(key,label) in enumerate(NAVS):
        r = pygame.Rect(i*w,y,w,NAV_H)
        nav_rects[key] = r
        active = mode == key
        if active: pygame.draw.rect(pantalla, PANEL_2, r)
        text(label,r.centerx,r.y+34,CYAN if active else GRAY,FONT_XS,True)
        if active: pygame.draw.rect(pantalla,CYAN,(r.x+32,r.bottom-8,r.w-64,3),border_radius=2)


def draw_selected_card(y=CONTENT_TOP):
    e=selected; c=COLORS[e["category"]]
    r=pygame.Rect(18,y,ANCHO-36,150); panel(r,c,2)
    pygame.draw.rect(pantalla,c,(r.x+15,r.y+18,82,82),border_radius=12)
    text(e["z"],r.x+22,r.y+23,(5,16,22),FONT_XS)
    text(e["symbol"],r.x+56,r.y+61,(5,16,22),FONT_L,True)
    text(e["name"],r.x+120,r.y+24,WHITE,FONT_L)
    text(f"{e['category']} • {e['state']}",r.x+122,r.y+67,c,FONT_S)
    text(f"Masa {e['mass']} u   •   Grupo {e['group']}   •   Periodo {e['period']}",r.x+122,r.y+101,GRAY,FONT_XS)
    text("Toca otro elemento para analizarlo",r.x+18,r.bottom-27,GRAY,FONT_XS)
    return r


def element_grid_layout(items, top, scroll, cols=4, cell_h=92, gap=10):
    margin=18; cell_w=(ANCHO-2*margin-(cols-1)*gap)//cols
    rects=[]
    for i,e in enumerate(items):
        row,col=divmod(i,cols)
        x=margin+col*(cell_w+gap)
        y=top+row*(cell_h+gap)-int(scroll)
        rects.append((e,pygame.Rect(x,y,cell_w,cell_h)))
    total_rows=(len(items)+cols-1)//cols
    total_h=max(0,total_rows*(cell_h+gap)-gap)
    return rects,total_h


def draw_element_tile(e,r):
    if r.bottom < CONTENT_TOP or r.top > CONTENT_BOTTOM: return
    c=COLORS[e["category"]]; active=e is selected
    pygame.draw.rect(pantalla, tuple(int(v*.62) for v in c) if not active else c, r, border_radius=10)
    pygame.draw.rect(pantalla, WHITE if active else c, r, 2 if active else 1, border_radius=10)
    text(e["z"],r.x+8,r.y+7,(4,15,21),FONT_XS)
    text(e["symbol"],r.centerx,r.y+43,(4,15,21),FONT_SYMBOL,True)
    text(e["name"][:11],r.centerx,r.bottom-15,(4,15,21),sysfont(13),True)


def draw_table():
    global table_max_scroll
    card=draw_selected_card()
    top=card.bottom+16
    items=current_filtered()
    rects,total_h=element_grid_layout(items,top,table_scroll)
    clip=pygame.Rect(0,top,ANCHO,CONTENT_BOTTOM-top)
    old=pantalla.get_clip(); pantalla.set_clip(clip)
    for e,r in rects: draw_element_tile(e,r)
    pantalla.set_clip(old)
    table_rect_cache[:] = rects
    table_max_scroll=max(0,total_h-clip.h)
    if not items: text("No se encontraron elementos",ANCHO//2,top+80,YELLOW,FONT_M,True)


def draw_config():
    global atom_box_rect
    e=selected;c=COLORS[e["category"]]
    y=CONTENT_TOP
    # Identidad + cambiar elemento
    r=pygame.Rect(18,y,ANCHO-36,112); panel(r,c,2)
    text(e["symbol"],r.x+23,r.y+19,c,FONT_XL)
    text(e["name"],r.x+130,r.y+20,WHITE,FONT_L)
    text(f"Elemento #{e['z']} • bloque {e['block']}",r.x+132,r.y+62,GRAY,FONT_XS)
    change=pygame.Rect(r.right-190,r.y+62,165,36)
    pygame.draw.rect(pantalla,PANEL_2,change,border_radius=8); pygame.draw.rect(pantalla,CYAN,change,1,border_radius=8)
    text("CAMBIAR",change.centerx,change.centery,CYAN,FONT_XS,True)
    config_buttons["change"] = change

    atom_box_rect=pygame.Rect(18,r.bottom+14,ANCHO-36,470)
    panel(atom_box_rect,c,1,DARK)
    text("ÁTOMO 3D INTERACTIVO",atom_box_rect.centerx,atom_box_rect.y+29,c,FONT_S,True)
    text("ARRASTRA CON EL DEDO PARA GIRAR",atom_box_rect.centerx,atom_box_rect.y+60,GRAY,FONT_XS,True)
    draw_atom_3d(e,atom_box_rect,pygame.time.get_ticks()/1000)

    box=pygame.Rect(18,atom_box_rect.bottom+14,ANCHO-36,230)
    panel(box,c,2,DARK)
    text("CONFIGURACIÓN ELECTRÓNICA",box.x+18,box.y+16,GRAY,FONT_XS)
    lines=wrap(pretty_configuration(e["configuration"]),FONT_CONFIG,box.w-36)
    for i,line in enumerate(lines[:5]): text(line,box.x+18,box.y+51+i*31,WHITE,FONT_CONFIG)
    text("CAPAS",box.x+18,box.bottom-53,GRAY,FONT_XS)
    text(" – ".join(map(str,e["shells"])),box.x+91,box.bottom-57,CYAN,FONT_S)

    info=pygame.Rect(18,box.bottom+14,ANCHO-36,110)
    panel(info,c,1)
    for i,line in enumerate(wrap(DESCRIPTIONS[e["category"]],FONT_XS,info.w-32)[:3]):
        text(line,info.x+16,info.y+15+i*24,WHITE,FONT_XS)


def compare_card(e, r, title):
    c=COLORS[e["category"]] if e else GRAY; panel(r,c,2)
    text(title,r.x+16,r.y+14,c,FONT_XS)
    if not e:
        text("TOCA PARA ELEGIR",r.centerx,r.centery+8,GRAY,FONT_S,True); return
    text(e["symbol"],r.x+18,r.y+43,c,FONT_XL)
    text(e["name"],r.x+122,r.y+48,WHITE,FONT_M)
    text(f"#{e['z']} • {e['mass']} u",r.x+124,r.y+82,GRAY,FONT_XS)
    text(e["category"],r.x+18,r.bottom-35,c,FONT_XS)


def draw_compare():
    y=CONTENT_TOP
    text("COMPARAR ELEMENTOS",22,y,CYAN,FONT_L)
    text("Toca cada tarjeta para elegir un elemento",22,y+43,GRAY,FONT_XS)
    a=pygame.Rect(18,y+80,ANCHO-36,166); b=pygame.Rect(18,a.bottom+14,ANCHO-36,166)
    compare_card(compare_a,a,"ELEMENTO A"); compare_card(compare_b,b,"ELEMENTO B")
    compare_buttons["A"]=a;compare_buttons["B"]=b
    if compare_a and compare_b:
        box=pygame.Rect(18,b.bottom+18,ANCHO-36,360); panel(box,CYAN,1,DARK)
        text("RESULTADO",box.x+18,box.y+16,CYAN,FONT_S)
        mass_sign = ">" if compare_a["mass"]>compare_b["mass"] else "<" if compare_a["mass"]<compare_b["mass"] else "="
        z_sign = ">" if compare_a["z"]>compare_b["z"] else "<" if compare_a["z"]<compare_b["z"] else "="
        text(f"MASA:  {compare_a['symbol']}  {mass_sign}  {compare_b['symbol']}",box.x+22,box.y+66,YELLOW,FONT_M)
        text(f"NÚMERO ATÓMICO:  {compare_a['symbol']}  {z_sign}  {compare_b['symbol']}",box.x+22,box.y+112,CYAN,FONT_M)
        text("CAPAS",box.x+22,box.y+170,GRAY,FONT_XS)
        text(f"{compare_a['symbol']}: " + " – ".join(map(str,compare_a["shells"])),box.x+22,box.y+201,WHITE,FONT_S)
        text(f"{compare_b['symbol']}: " + " – ".join(map(str,compare_b["shells"])),box.x+22,box.y+235,WHITE,FONT_S)
        text("CONFIGURACIÓN",box.x+22,box.y+282,GRAY,FONT_XS)
        text(pretty_configuration(compare_a["configuration"])[:42],box.x+22,box.y+310,WHITE,FONT_XS)
        text(pretty_configuration(compare_b["configuration"])[:42],box.x+22,box.y+336,WHITE,FONT_XS)


def new_question():
    global quiz_question, quiz_options, quiz_correct, quiz_feedback, quiz_rects
    target=random.choice(elements); kind=random.choice(("symbol","number","name","config"))
    if kind=="symbol":
        quiz_question=f"¿Cuál es el símbolo de {target['name']}?"; quiz_correct=target["symbol"]
        pool=[e["symbol"] for e in elements if e is not target]
    elif kind=="number":
        quiz_question=f"¿Cuál es el número atómico de {target['name']}?"; quiz_correct=str(target["z"])
        pool=[str(e["z"]) for e in elements if e is not target]
    elif kind=="name":
        quiz_question=f"¿Qué elemento usa el símbolo {target['symbol']}?"; quiz_correct=target["name"]
        pool=[e["name"] for e in elements if e is not target]
    else:
        quiz_question=f"¿Qué configuración corresponde a {target['symbol']}?"
        quiz_correct=pretty_configuration(target["configuration"])
        candidates=random.sample([e for e in elements if e is not target],3)
        pool=[pretty_configuration(e["configuration"]) for e in candidates]
        quiz_options=pool+[quiz_correct];random.shuffle(quiz_options);quiz_feedback="";quiz_rects=[];return
    quiz_options=random.sample(pool,3)+[quiz_correct];random.shuffle(quiz_options);quiz_feedback="";quiz_rects=[]


def choose_quiz(i):
    global quiz_score,quiz_total,quiz_feedback,quiz_feedback_color,quiz_next_at
    if quiz_feedback or not(0<=i<len(quiz_options)): return
    quiz_total+=1
    if quiz_options[i]==quiz_correct:
        quiz_score+=1;quiz_feedback="¡CORRECTO!";quiz_feedback_color=GREEN
    else:
        quiz_feedback="Respuesta correcta: " + str(quiz_correct);quiz_feedback_color=RED
    quiz_next_at=pygame.time.get_ticks()+1600


def draw_quiz():
    global quiz_rects
    y=CONTENT_TOP
    card=pygame.Rect(18,y,ANCHO-36,CONTENT_BOTTOM-y-12); panel(card,CYAN,2)
    text("FRANCAST KNOWLEDGE CORE",card.centerx,card.y+42,CYAN,FONT_L,True)
    text(f"PUNTUACIÓN {quiz_score} / {quiz_total}",card.centerx,card.y+87,GREEN,FONT_S,True)
    qlines=wrap(quiz_question,FONT_M,card.w-52)
    for i,line in enumerate(qlines[:3]): text(line,card.centerx,card.y+150+i*35,WHITE,FONT_M,True)
    quiz_rects=[];start=card.y+285
    for i,opt in enumerate(quiz_options):
        r=pygame.Rect(card.x+25,start+i*112,card.w-50,86);quiz_rects.append(r)
        pygame.draw.rect(pantalla,DARK,r,border_radius=13);pygame.draw.rect(pantalla,GRAY,r,2,border_radius=13)
        lines=wrap(opt,FONT_XS,r.w-30)
        for j,line in enumerate(lines[:2]): text(line,r.centerx,r.centery-11+j*24,WHITE,FONT_XS,True)
    if quiz_feedback:
        for i,line in enumerate(wrap(quiz_feedback,FONT_S,card.w-50)[:2]):
            text(line,card.centerx,card.bottom-95+i*27,quiz_feedback_color,FONT_S,True)
    text("Toca una respuesta",card.centerx,card.bottom-36,GRAY,FONT_XS,True)


# ---------------------- SELECTOR MODAL ----------------------
picker_cache=[]; table_rect_cache=[]
table_max_scroll=0; picker_max_scroll=0
config_buttons={}; compare_buttons={}

def draw_picker():
    global picker_max_scroll
    overlay=pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA);overlay.fill((1,5,10,225));pantalla.blit(overlay,(0,0))
    r=pygame.Rect(14,86,ANCHO-28,ALTO-175);panel(r,CYAN,2,(5,18,28))
    text("SELECCIONA UN ELEMENTO",r.x+20,r.y+18,CYAN,FONT_L)
    close=pygame.Rect(r.right-70,r.y+17,50,50);pygame.draw.rect(pantalla,PANEL_2,close,border_radius=10);pygame.draw.rect(pantalla,GRAY,close,1,border_radius=10)
    text("×",close.centerx,close.centery,WHITE,FONT_L,True);picker_buttons["close"]=close
    items=current_filtered();top=r.y+90
    rects,total_h=element_grid_layout(items,top,picker_scroll,cols=4,cell_h=88,gap=9)
    clip=pygame.Rect(r.x+4,top,r.w-8,r.bottom-top-10);old=pantalla.get_clip();pantalla.set_clip(clip)
    for e,rr in rects: draw_element_tile(e,rr)
    pantalla.set_clip(old);picker_cache[:]=rects;picker_max_scroll=max(0,total_h-clip.h)

picker_buttons={}


def set_mode(new_mode):
    global mode, show_picker, search_active
    mode=new_mode;show_picker=False;search_active=False
    pygame.key.stop_text_input()
    if mode=="Quiz" and quiz_question is None: new_question()


def open_picker(target=None):
    global show_picker,compare_target,picker_scroll
    show_picker=True;compare_target=target;picker_scroll=0


def pointer_down(pos):
    global selected,atom_dragging,last_pointer,scroll_dragging,scroll_last_y,search_active,compare_a,compare_b,show_picker,compare_target
    # Modal primero
    if show_picker:
        if picker_buttons.get("close") and picker_buttons["close"].collidepoint(pos):
            show_picker=False;return
        for e,r in picker_cache:
            if r.collidepoint(pos):
                if compare_target=="A": compare_a=e
                elif compare_target=="B": compare_b=e
                else: selected=e
                show_picker=False;compare_target=None;return
        scroll_dragging=True;scroll_last_y=pos[1];return

    # Navegación
    for key,r in nav_rects.items():
        if r.collidepoint(pos): set_mode(key);return
    if search_rect.collidepoint(pos):
        search_active=True;pygame.key.start_text_input();return
    else:
        search_active=False;pygame.key.stop_text_input()

    if mode=="Tabla":
        for e,r in table_rect_cache:
            if r.collidepoint(pos): selected=e;return
        if pos[1] >= CONTENT_TOP+166 and pos[1] < CONTENT_BOTTOM:
            scroll_dragging=True;scroll_last_y=pos[1]
    elif mode=="Config":
        if config_buttons.get("change") and config_buttons["change"].collidepoint(pos): open_picker(None);return
        if atom_box_rect.collidepoint(pos): atom_dragging=True;last_pointer=pos;return
    elif mode=="Comparar":
        if compare_buttons.get("A") and compare_buttons["A"].collidepoint(pos): open_picker("A");return
        if compare_buttons.get("B") and compare_buttons["B"].collidepoint(pos): open_picker("B");return
    elif mode=="Quiz":
        for i,r in enumerate(quiz_rects):
            if r.collidepoint(pos): choose_quiz(i);return


def pointer_move(pos, rel):
    global atom_rot_x,atom_rot_y,last_pointer,table_scroll,picker_scroll,scroll_last_y
    if atom_dragging and mode=="Config" and not show_picker:
        dx,dy=rel;atom_rot_y+=dx*.012;atom_rot_x+=dy*.012;atom_rot_x=max(-1.45,min(1.45,atom_rot_x));last_pointer=pos
    elif scroll_dragging:
        dy=pos[1]-scroll_last_y;scroll_last_y=pos[1]
        if show_picker: picker_scroll=max(0,min(picker_max_scroll,picker_scroll-dy))
        elif mode=="Tabla": table_scroll=max(0,min(table_max_scroll,table_scroll-dy))


def pointer_up():
    global atom_dragging,scroll_dragging
    atom_dragging=False;scroll_dragging=False


def finger_pos(event):
    return int(event.x*ANCHO), int(event.y*ALTO)


def finger_rel(event):
    return int(event.dx*ANCHO), int(event.dy*ALTO)


# ---------------------- LOOP PRINCIPAL ----------------------
async def main():
    new_question()
    running=True
    frame_count=0
    test_frames=int(os.environ.get("FRANCAST_TEST_FRAMES","0") or 0)
    while running:
        dt=reloj.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if show_picker: show_picker=False
                    elif search_active: search_active=False;pygame.key.stop_text_input()
                    elif mode!="Tabla": set_mode("Tabla")
                    else: running=False
                elif search_active:
                    if event.key==pygame.K_BACKSPACE: search=search[:-1]
                    elif event.key==pygame.K_RETURN: search_active=False;pygame.key.stop_text_input()
                    elif event.unicode and event.unicode.isprintable() and len(search)<24: search+=event.unicode
            elif event.type==pygame.TEXTINPUT and search_active:
                if len(search)<24: search=(search+event.text)[:24]
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and not getattr(event, "touch", False):
                pointer_down(event.pos)
            elif event.type==pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not getattr(event, "touch", False):
                pointer_move(event.pos,event.rel)
            elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and not getattr(event, "touch", False):
                pointer_up()
            elif event.type==pygame.MOUSEWHEEL:
                if show_picker: picker_scroll=max(0,min(picker_max_scroll,picker_scroll-event.y*70))
                elif mode=="Tabla": table_scroll=max(0,min(table_max_scroll,table_scroll-event.y*70))
            elif event.type==pygame.FINGERDOWN:
                pointer_down(finger_pos(event))
            elif event.type==pygame.FINGERMOTION:
                pointer_move(finger_pos(event),finger_rel(event))
            elif event.type==pygame.FINGERUP:
                pointer_up()

        if quiz_feedback and pygame.time.get_ticks()>=quiz_next_at: new_question()

        draw_background();draw_header()
        if mode=="Tabla": draw_table()
        elif mode=="Config": draw_config()
        elif mode=="Comparar": draw_compare()
        else: draw_quiz()
        draw_nav()
        if show_picker: draw_picker()
        pygame.display.flip()
        await asyncio.sleep(0)

        frame_count += 1
        if test_frames and frame_count >= test_frames: running=False

    pygame.quit()


asyncio.run(main())
