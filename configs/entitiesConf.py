GENERIC_CONFIG = {
    "speed": 5,
    "health": 100,
}

PLAYER_CONFIG = {
    "speed": 30,
    "health": 100,
    "damage": 10,
    "iframes": 240,
    "level": 1,
}

SIMPLE_ENEMY_CONFIG = {
    "speed": 5,
    "health": 100,
    "damage": 10,
    "exp": 2,
    "points": 10,
}

MISC = {

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
            "exp": 1.5,
            "points": 1,

        },

    ],
    "spawns":
        [
            (1000, 100),
            (200, 200),
            (300, 1000),
            (130, 900),
            (50, 2000),
            (600, 1200)
        ]
}
