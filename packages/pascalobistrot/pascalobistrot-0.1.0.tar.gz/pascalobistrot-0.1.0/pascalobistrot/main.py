def donne_a_boire(a:int, b:int) -> int:
    if a > 10:
        return a + b +2
    return a + b

coup_a_boire = donne_a_boire(8, 10)
print(coup_a_boire)
