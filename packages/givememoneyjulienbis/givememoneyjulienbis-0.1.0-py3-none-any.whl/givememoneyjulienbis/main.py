def give_me_money_julien_bis(a: int, b: int) -> int:
    if a > 10:
        return a + b + 2
    return a + b

compte_en_banque = give_me_money_julien_bis(8, 10)
print(compte_en_banque)