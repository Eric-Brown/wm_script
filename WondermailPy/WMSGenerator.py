# The Wonder Mail S Generator backend code

# This file is placed in the public domain and may be freely used, reproduced, modified, sold or whatever you want.
# However, it may or may not work; use at your own risk.

#  Data for the Wonder Mail S generator.

class WMSGenerator:
    # Mission type format:

    # name: name of type
    # mainType: struct.mainType field
    # specialType: struct.missionSpecial field
    # clientIsTarget: boolean that sets the target to the client
    # useTargetItem: boolean that enables the targetItem box if set and True; will be disabled if not set or false
    # useTarget2: boolean that enables the secondary target box if set and True; will be disabled if not set or false
    # forceClient: if set and non-zero, sets the client to this number and disables the client box
    # forceTarget: if set and non-zero, sets the target to this number and disables the target box
    # specialFloor: special floor to include in code
    # specialFloorFromList: take a random entry from the named staticList
    # noReward: disable reward boxes

    # Every mission type can have a "subTypes" array which overrides all settings for the parent.
    missionTypes = [
        {"name": "Rescue client", "mainType": 0,
            "specialType": 0, "clientIsTarget": True},
        {"name": "Rescue target", "mainType": 1, "specialType": 0},
        {"name": "Escort to target", "mainType": 2, "specialType": 0},

        {"name": "Explore with client", "mainType": 3, "clientIsTarget": True, "subTypes": [
            {"name": "Normal", "specialType": 0},
            {"name": "Sealed Chamber", "specialType": 1, "specialFloor": 165},
            {"name": "Golden Chamber", "specialType": 2, "specialFloor": 111},
            {"name": "New Dungeon (broken?)",
             "specialType": 3, "advancedOnly": True}
        ]},

        {"name": "Prospect with client", "mainType": 4, "specialType": 0,
            "useTargetItem": True, "clientIsTarget": True},
        {"name": "Guide client", "mainType": 5,
            "specialType": 0, "clientIsTarget": True},
        {"name": "Find target item", "mainType": 6, "specialType": 0,
            "useTargetItem": True, "clientIsTarget": True},
        {"name": "Deliver target item", "mainType": 7, "specialType": 0,
            "useTargetItem": True, "clientIsTarget": True},
        {"name": "Search for client", "mainType": 8, "specialType": 0},

        {"name": "Steal from target", "mainType": 9, "useTargetItem": True, "subTypes": [
            {"name": "Normal", "specialType": 0},
            {"name": "Target hidden", "specialType": 1},
            {"name": "Target runs", "specialType": 2}
        ]},

        {"name": "Arrest client (Magnemite)", "advancedOnly": True, "mainType": 10, "forceClient": 81, "subTypes": [
            {"name": "Normal", "specialType": 0},
            {"name": "Escort", "specialType": 4},
            {"name": "Special Floor (broken)", "specialType": 6,
             "useTarget2": True, "specialFloorFromList": "thievesden"},
            {"name": "Monster House", "specialType": 7}
        ]},

        # This is the same list as above, just with Magnezone.
        {"name": "Arrest client (Magnezone)", "advancedOnly": True, "mainType": 10, "forceClient": 504, "subTypes": [
            {"name": "Normal", "specialType": 0},
            {"name": "Escort", "specialType": 4},
            {"name": "Special Floor (broken)", "specialType": 6,
             "useTarget2": True, "specialFloorFromList": "thievesden"},
            {"name": "Monster House", "specialType": 7}
        ]},

        {"name": "Challenge Request", "mainType": 11, "subTypes": [
            {"name": "Normal (broken)", "specialType": 0, "useTarget2": True,
             "advancedOnly": True, "specialFloorFromList": "challengerequest"},
            {"name": "Mewtwo", "specialType": 1, "forceClient": 150,
                "forceTarget": 150, "specialFloor": 145},
            {"name": "Entei", "specialType": 2, "forceClient": 271,
                "forceTarget": 271, "specialFloor": 146},
            {"name": "Raikou", "specialType": 3, "forceClient": 270,
                "forceTarget": 270, "specialFloor": 147},
            {"name": "Suicine", "specialType": 4, "forceClient": 272,
                "forceTarget": 272, "specialFloor": 148},
            {"name": "Jirachi", "specialType": 5, "forceClient": 417,
                "forceTarget": 417, "specialFloor": 149}
        ]},

        # You can use any client/target but the game prefers them to be the same.
        {"name": "Treasure hunt", "mainType": 12, "specialType": 0, "forceClient": 422,
            "forceTarget": 422, "specialFloorFromList": "treasurehunt", "noReward": True}
    ]

    validDungeons = [
        0x01, 0x03, 0x04, 0x06, 0x07, 0x08, 0x0A, 0x0C, 0x0E, 0x11, 0x14, 0x15, 0x18,
        0x19, 0x22, 0x23, 0x2C, 0x2E, 0x2F, 0x32, 0x33, 0x3E, 0x40, 0x43, 0x46, 0x48,
        0x49, 0x4B, 0x4D, 0x4F, 0x51, 0x53, 0x55, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C,
        0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x6B, 0x6C,
        0x6D, 0x6E
    ]

    validClients = [
        # Game extracted data
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19,
        20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37,
        38, 39, 41, 42, 43, 44, 45, 46, 48, 49, 52, 53, 54, 55, 56, 57,
        58, 59, 60, 61, 62, 64, 65, 66, 68, 69, 70, 72, 73, 74, 75, 76,
        77, 78, 79, 80, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,
        95, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
        112, 114, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129,
        132, 133, 134, 135, 136, 138, 139, 140, 141, 142, 143, 147, 148, 149, 152, 153,
        154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170,
        171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 184, 185, 186, 187, 188,
        189, 190, 193, 194, 195, 196, 198, 199, 200, 230, 231, 232, 233, 234, 235, 236,
        237, 238, 240, 245, 246, 247, 248, 249, 250, 252, 253, 254, 255, 256, 257, 258,
        259, 261, 262, 263, 265, 266, 267, 268, 269, 273, 274, 275, 283, 284, 287, 288,
        289, 290, 292, 293, 295, 297, 298, 299, 300, 301, 302, 303, 305, 306, 307, 308,
        309, 311, 312, 313, 315, 316, 317, 318, 319, 320, 321, 323, 327, 328, 332, 333,
        334, 335, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 350, 351,
        352, 353, 354, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368,
        370, 371, 372, 373, 374, 375, 377, 385, 386, 387, 388, 389, 391, 393, 394, 395,
        396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 422, 423, 424,
        426, 427, 428, 429, 430, 431, 432, 433, 435, 436, 437, 439, 441, 443, 444, 445,
        446, 447, 448, 450, 451, 452, 453, 454, 455, 457, 458, 459, 460, 462, 463, 464,
        465, 466, 467, 468, 469, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481,
        482, 484, 485, 486, 487, 488, 489, 491, 492, 493, 494, 496, 497, 498, 499, 500,
        501, 502, 503, 505, 507, 508, 509, 511, 512, 513, 514, 515, 518, 521
    ]

    # Items that are not valid for use as target item (should be whitelist?)
    badTargetItems = [0, 1, 2, 3, 4, 9]
    # http://bulbapedia.bulbagarden.net/wiki/Category:Male-only_Pok%C3%A9mon
    maleOnly = [0x205, 0x6A, 0x6B, 0x108, 0x19D,
                0x1C5, 0x22, 0x21, 0x80, 0x107, 0x155]
    # http://bulbapedia.bulbagarden.net/wiki/Category:Female-only_Pok%C3%A9mon
    femaleOnly = [
        0x10D, 0x71, 0x212, 0x208, 0x1E2, 0x156, 0x7C, 0x73, 0x19C, 0x10C, 0x01F,
        0x01E, 0x109, 0x1C7, 0x1C2, 0x1C3, 0x1C4
    ]

    # Very special case... only Female is included in the list now.
    NIDORAN_FEMALE: 0x18
    NIDORAN_MALE: 0x20

    staticLists = {
        # Valid floors for treasure hunts.
        "treasurehunt": [
            114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
            130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144
        ],

        # Valid floors for challenge requests.
        # This is from memory, it might be wrong.
        "challengerequest": [
            145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160
        ],

        # Valid floors for Thieves Den missions.
        # This is from memory, it might be wrong.
        "thievesden": [
            161, 162, 163, 164, 165
        ]
    }

    # TODO: list of dungeon floor count
