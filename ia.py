# ia.py
from copy import deepcopy
from logique import mouvements_possibles, pion_adverse


def evaluer_plateau(p):
    score = 0
    for ligne in p:
        for piece in ligne:
            if piece:
                if piece == 'noir':
                    score -= 1
                elif piece == 'noir_dame':
                    score -= 2
                elif piece == 'blanc':
                    score += 1
                elif piece == 'blanc_dame':
                    score += 2
    return score


def simuler_deplacement(p, dep, arr):
    l1, c1 = dep
    l2, c2 = arr
    p[l2][c2] = p[l1][c1]
    p[l1][c1] = None
    if abs(l2 - l1) == 2:
        p[(l1 + l2) // 2][(c1 + c2) // 2] = None


def minmax(plateau_actuel, profondeur, est_ia, alpha=float('-inf'), beta=float('inf')):
    if profondeur == 0:
        return evaluer_plateau(plateau_actuel), None

    couleur = "blanc" if est_ia else "noir"
    meilleur_coup = None
    coups = []

    for l in range(10):
        for c in range(10):
            pion = plateau_actuel[l][c]
            if pion and couleur in pion:
                for dest in mouvements_possibles(plateau_actuel, l, c):
                    if plateau_actuel[dest[0]][dest[1]] is None:
                        coups.append(((l, c), dest))

    if est_ia:
        max_eval = float('-inf')
        for dep, arr in coups:
            copie = deepcopy(plateau_actuel)
            simuler_deplacement(copie, dep, arr)
            eval_, _ = minmax(copie, profondeur - 1, False, alpha, beta)
            if eval_ > max_eval:
                max_eval = eval_
                meilleur_coup = (dep, arr)
            alpha = max(alpha, eval_)
            if beta <= alpha:
                break
        return max_eval, meilleur_coup
    else:
        min_eval = float('inf')
        for dep, arr in coups:
            copie = deepcopy(plateau_actuel)
            simuler_deplacement(copie, dep, arr)
            eval_, _ = minmax(copie, profondeur - 1, True, alpha, beta)
            if eval_ < min_eval:
                min_eval = eval_
                meilleur_coup = (dep, arr)
            beta = min(beta, eval_)
            if beta <= alpha:
                break
        return min_eval, meilleur_coup
