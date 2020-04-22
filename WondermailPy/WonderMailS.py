// Wonder Mail S Structure data
var WMSStruct = [
	{"name": "nullBits", "note": "Null bits", "size": 8},
	{"name": "specialFloor", "note": "Special floor marker", "size": 8},
	{"name": "floor", "note": "Floor", "size": 8},
	{"name": "dungeon", "note": "Dungeon", "size": 8},
	{"name": "flavorText", "note": "Modifies the flavor text", "size": 24},
	{"name": "restriction", "note": "Restriction data", "size": 11},
	{"name": "restrictionType", "note": "Restriction type; mon = 1, type = 0", "size": 1},
	{"name": "reward", "note": "Reward", "size": 11},
	{"name": "rewardType", "note": "Reward type", "size": 4},
	{"name": "targetItem", "note": "Target item", "size": 10},
	{"name": "target2", "note": "Additional target Poke for certain mission types", "size": 11},
	{"name": "target", "note": "Target Poke", "size": 11},
	{"name": "client", "note": "Client Poke", "size": 11},
	{"name": "missionSpecial", "note": "Mission special texts", "size": 4},
	{"name": "missionType", "note": "Mission type", "size": 4},
	{"name": "mailType", "note": "Mail type marker (must be 0100 = 4)", "size": 4},
	{"name": "checksum", "note": "checksum", "size": 32, "noinclude": true}
];