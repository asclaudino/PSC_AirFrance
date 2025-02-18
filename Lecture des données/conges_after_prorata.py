def number_of_conges_after_proata(prorata_days: int):
    mapping = {
        0: (5, 6),
        1: (5, 6),
        2: (5, 6),
        3: (5, 5),
        4: (5, 5),
        5: (5, 4),
        6: (5, 4),
        7: (5, 4),
        8: (4, 4),
        9: (4, 4),
        10: (4, 3),
        11: (4, 3),
        12: (4, 3),
        13: (3, 3),
        14: (3, 3),
        15: (3, 2),
        16: (3, 2),
        17: (3, 2),
        18: (2, 2),
        19: (2, 2),
        20: (2, 1),
        21: (2, 1),
        22: (2, 1),
        23: (2,0),
        24: (2,0),
        25: (1,0),
        26: (1,0),
        27: (1,0),
    }
        
    if prorata_days < 0: return (5,6)
    if prorata_days > 27: return (0,0)
    
    result = mapping.get(prorata_days)
    if result is None:
        raise ValueError(f"Invalid prorata_days value: {prorata_days}")
    return result
