DUNGEON = {
    "width": 54,
    "height": 23,
    "tile": 32,
}
GENERIC_CONFIG = {
    "speed": 5,
    "health": 10,
    "iframes": 90,
}

PLAYER_CONFIG = {
    "speed": 5,
    "health": 100,
    "level_up_heal": 0.15,
    "iframes": 240,
    "level": 1,
    "aoe_radius": 100,
    "aoe_attack_speed": 5,
    "aoe_damage": 10,
    "line_length": 110,
    "wave_frequency": 0.5
}

ENEMY_CONFIG = {
    "speed": 5,
    "health": 20,
    "damage": 10,
    "exp": 10,
    "points": 10,

}

MISC = {
    "base_exp": 12,
    "difficulty_multipliers": [
        {  # Easy
            "speed": 0.9,
            "health": 0.8,
            "damage": 0.85,
            "exp": 1.5,
            "points": 1.1,
        }, {  # Normal
            "speed": 1,
            "health": 1,
            "damage": 1,
            "exp": 1,
            "points": 1,

        }, {  # Hard
            "speed": 1.3,
            "health": 1.2,
            "damage": 1.1,
            "exp": 1.1,
            "points": 1.2,

        }, {  # Nighmare
            "speed": 2,
            "health": 1.5,
            "damage": 1.5,
            "exp": 1.5,
            "points": 1.5,

        }, {  # Unfair / Unalive
            "speed": 3,
            "health": 2.5,
            "damage": 3,
            "exp": 2.5,
            "points": 1,

        },

    ],
    "spawns":
        [
            # TODO When making the better spawn locations, remove magic numbers and make it relative
            (1000, 100),
            (200, 200),
            (300, 1000),
            (130, 900),
            (50, 2000),
            (600, 1200)
        ]
}

SPAWN_PATTERNS = [
    {
        "time_limit": 30,
        "possible_spawns": [
            {"type": "generic", "quantity": 2}
        ]
    },
    {
        "time_limit": 90,
        "possible_spawns": [
            {"type": "generic", "quantity": 3},
            {"type": "fast", "chance": 0.3},
            {"type": "tank", "chance": 0.05}
        ]
    },
    {
        "time_limit": 120,
        "possible_spawns": [
            {"type": "strong", "quantity": 2},
            {"type": "tank", "chance": 0.3}
        ]
    },
    {
        "time_limit": 180,
        "possible_spawns": [
            {"type": "strong", "quantity": 3},
            {"type": "fast", "chance": 0.5},
            {"type": "tank", "chance": 0.3}
        ]
    }
]

BOSS_SPAWN_CONDITIONS = [
    {"kill_threshold": 50, "boss_stage": 0, "boss_type": "first_boss"},
    {"kill_threshold": 500, "boss_stage": 1, "boss_type": "second_boss"}
]
