def donne_des_sous(a:int,b:int) -> int:
    if a > 10:
        return a + b + 2
    return a+b

compte_en_banque = donne_des_sous(10,2)
print(compte_en_banque)