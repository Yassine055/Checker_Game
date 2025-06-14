# logique.py
def case_est_noire(ligne, colonne):
    return (ligne + colonne) % 2 == 1

def pion_adverse(pion, autre_pion):
    if pion is None or autre_pion is None:
        return False
    couleur = pion.replace('_dame', '')
    autre_couleur = autre_pion.replace('_dame', '')
    return couleur != autre_couleur

def mouvements_possibles(plateau, ligne, colonne):
    deplacements = []
    pion = plateau[ligne][colonne]
    if pion is None:
        return deplacements

    est_dame = '_dame' in pion
    couleur = pion.replace('_dame', '')

    if est_dame:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in directions:
            for distance in range(1, 10):
                l2 = ligne + dl * distance
                c2 = colonne + dc * distance
                if not (0 <= l2 < 10 and 0 <= c2 < 10):
                    break
                if not case_est_noire(l2, c2):
                    break
                if plateau[l2][c2] is None:
                    deplacements.append((l2, c2))
                elif pion_adverse(pion, plateau[l2][c2]):
                    for distance_apres in range(distance + 1, 10):
                        l3 = ligne + dl * distance_apres
                        c3 = colonne + dc * distance_apres
                        if not (0 <= l3 < 10 and 0 <= c3 < 10):
                            break
                        if not case_est_noire(l3, c3):
                            break
                        if plateau[l3][c3] is None:
                            deplacements.append((l3, c3))
                    break
    else:
        if couleur == 'blanc':
            directions_avancer = [(-1, -1), (-1, 1)]
            directions_prises = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions_avancer = [(1, -1), (1, 1)]
            directions_prises = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dl, dc in directions_avancer:
            l2 = ligne + dl
            c2 = colonne + dc
            if 0 <= l2 < 10 and 0 <= c2 < 10 and plateau[l2][c2] is None and case_est_noire(l2, c2):
                deplacements.append((l2, c2))

        for dl, dc in directions_prises:
            l2 = ligne + dl
            c2 = colonne + dc
            l3 = ligne + 2 * dl
            c3 = colonne + 2 * dc
            if 0 <= l3 < 10 and 0 <= c3 < 10 and plateau[l3][c3] is None and case_est_noire(l3, c3):
                if plateau[l2][c2] is not None and pion_adverse(pion, plateau[l2][c2]):
                    deplacements.append((l3, c3))

    return deplacements
