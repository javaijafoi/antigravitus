from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Status(str, Enum):
    DONE = 'done'
    PAUSED = 'paused'
    REJECTED = 'rejected'
    FLED = 'fled'
    CAMPED = 'camped'
    DISCONNECTED = 'disconnected'


@dataclass
class Result:
    status: Status
    reason: str
    data: dict = field(default_factory=dict)

    @property
    def ok(self):
        return self.status in (Status.DONE, Status.CAMPED)


@dataclass
class Vitals:
    hp: Optional[int] = None
    mana: Optional[int] = None
    mv: Optional[int] = None
    max_hp: Optional[int] = None
    max_mana: Optional[int] = None
    max_mv: Optional[int] = None
    observed_at: float = -1

    def known(self):
        return all(value is not None for value in (self.hp, self.mana, self.mv, self.max_hp, self.max_mana, self.max_mv))

    def fresh(self, now, ttl=15):
        return self.known() and 0 <= now-self.observed_at <= ttl


@dataclass
class Entity:
    description: str
    target: str = ''
    kind: str = 'unknown'  # hostile, friendly, player, unknown
    verified: bool = False


@dataclass
class Item:
    target: str
    name: str
    quantity: int = 1
    weight: Optional[float] = None
    sale_value: Optional[int] = None  # A shop quotation, not the identify "Valor" field.
    verified: bool = False
    category: str = 'unknown'
    disposable: bool = False
    quest: bool = False
    rare: bool = False
    upgrade: bool = False
    contents_known: bool = True
    carried: bool = False


@dataclass
class Room:
    title: str
    fingerprint: str
    exits: dict
    entities: list = field(default_factory=list)
    ground: list = field(default_factory=list)
    raw: str = ''
    node_id: str = ''
    hint_id: str = ''
    city: Optional[bool] = None
    known_shelter: bool = False
    clean_checks: int = 0
    damage_seen: bool = False

    def quiet(self):
        return not self.damage_seen and all(e.kind == 'friendly' and e.verified for e in self.entities)

    def suitable_camp(self):
        return self.quiet() and self.clean_checks >= 3 and (self.known_shelter or len(self.exits) <= 1)


@dataclass
class Supplies:
    food: int = 0
    water: Optional[float] = None  # fraction observed in a container; None is unknown
    hungry: Optional[bool] = None
    thirsty: Optional[bool] = None
    gold: Optional[int] = None
    count: Optional[int] = None
    max_count: Optional[int] = None
    weight: Optional[float] = None
    max_weight: Optional[float] = None


@dataclass(frozen=True)
class Profile:
    name: str
    combat: str
    hp_fraction: float
    damage_turns: float
    mana_reserve: int = 12
    escape_mv: int = 12
    loot: bool = True


PROFILES = {
    'dungeon_corajoso': Profile('dungeon_corajoso', 'corajosa', .30, 2.0),
    'exploracao': Profile('exploracao', 'cautelosa', .45, 3.0),
    'batedor': Profile('batedor', 'evitar', .60, 3.0),
}


@dataclass
class Config:
    mode: str = 'dungeon_corajoso'
    destination_id: Optional[str] = None
    food_target: int = 4
    food_price_ceiling: int = 10
    min_loot_value_per_weight: float = 10
    spare_weapons: int = 1
    max_commands: int = 400
    max_seconds: int = 1800
    recovery_seconds: int = 45
    max_no_progress: int = 3
    max_combat_rounds: int = 16
    max_room_encounters: int = 8
    first_cast_budget: int = 25
    max_step_cost: int = 3
    spare_slots: int = 2
    burn_verified_trash: bool = True
    allow_verified_melee: bool = False
    melee_max_enemy_hits: Optional[int] = None
    known_entities: list = field(default_factory=list)
    item_catalog: list = field(default_factory=list)
    verified_shelters: list = field(default_factory=list)
    outside_rooms: list = field(default_factory=list)

    def validate(self):
        if self.mode not in PROFILES:
            raise ValueError('Modo desconhecido.')
        for name in ('food_target', 'max_commands', 'max_seconds', 'recovery_seconds', 'max_no_progress', 'max_combat_rounds', 'max_room_encounters', 'max_step_cost'):
            if not isinstance(getattr(self, name), int) or getattr(self, name) <= 0:
                raise ValueError('Limite deve ser positivo: '+name)
        if self.food_price_ceiling < 0 or self.first_cast_budget < 1 or self.spare_slots < 0:
            raise ValueError('Orçamento ou capacidade inválidos.')
        return self
