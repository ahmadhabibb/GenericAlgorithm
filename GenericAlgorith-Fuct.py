import random
import numpy as np
import math

def createIndividu(x):
    individu = []
    for i in range(x):
        individu.append(random.randint(0, 9))
    return individu
    
def createPopulasi(x):
    populasi = []
    populasi.append(createIndividu(x))
    return populasi

def countX(rMin_1, rMax_1, rMin_2, rMax_2, panjangIndividu, check, loop):
    a = panjangIndividu // 2
    g = 0
    inisial = 1
    hasil = 0
    hasil2 = 0
    for i in range(a):
        g = g + (10**-inisial)
        inisial = inisial + 1
    
    inisial = 1
    for j in range(a):
        hitung = check[j] * 10**-inisial
        inisial = inisial + 1
        hasil = hasil + hitung

    inisial = 1
    for k in range(a):
        hitung2 = check[k+a] * 10**-inisial
        inisial = inisial + 1
        hasil2 = hasil2 + hitung2
        
    x = rMin_1 + ((rMax_1 - rMin_1) / (9 * g) * hasil)
    y = rMin_2 + ((rMax_2 - rMin_2) / (9 * g) * hasil2)
    return (x,y)

def hitungProbabilitas(x, y):
    prob = 0
    prob = x / y
    return prob

def nilaiMinimum(x, y):
    hitung = (4 - 2*1*x**2 + (x**4 / 3)) * x**2 + x*y + (-4 + 4*y**2)*y**2
    return hitung

def pilihOrtu(panjangPopulasi, arr_prob, pop):
    kandidatOT = []
    pilihOT = []
    ortuFix = []
    loopX = 1
    i = 0

    for i in range(panjangPopulasi):
        x = math.ceil(arr_prob[i]*10)
        for j in range(x):
            kandidatOT.append(loopX)
        loopX = loopX + 1

    for k in range(panjangPopulasi):
        rand = random.randint(0, len(kandidatOT)-1)
        pilihOT.append(kandidatOT[rand])

    for ab in range(panjangPopulasi):
        ortuFix.append(pop[pilihOT[ab]-1][0])

    return pilihOT, ortuFix

def crossOver(ortuFix):
    anak = []
    individuBaru = []

    for a in range(len(ortuFix) // 2):
        panjang = len(ortuFix[a])
        splitPoint = random.randint(1, panjang-1)
        for b in range(len(ortuFix[a])):
            if (b < splitPoint):
                individuBaru.append(ortuFix[a*2][b])
            else:
                individuBaru.append(ortuFix[(a*2) + 1][b])
        anak.append(individuBaru)
        individuBaru = []
        for c in range(len(ortuFix[a])):
            if (c < splitPoint):
                individuBaru.append(ortuFix[(a*2) + 1][c])
            else:
                individuBaru.append(ortuFix[a*2][c])
        anak.append(individuBaru)
        individuBaru = []
    
    return anak

def swapPosition(anak, panjangIndividu, iterasi):
    # Swap Position
    rnd1 = random.randint(1, panjangIndividu)
    rnd2 = random.randint(1, panjangIndividu)
    temp = anak[iterasi][rnd1-1]
    anak[iterasi][rnd1-1] = anak[iterasi][rnd2-1]
    anak[iterasi][rnd2-1] = temp 
    return anak

def compareFitness(fitness_1, fitness_2, ortu, anak, loop):
    kromosomFix = []
    fitnessFix = []

    if (fitness_1[loop] > fitness_2[loop]):
        kromosomFix.append(ortu[loop])
        fitnessFix.append(fitness_1[loop])
    else:
        kromosomFix.append(anak[loop])
        fitnessFix.append(fitness_2[loop])
    return (kromosomFix, fitnessFix)

def main():
    jumlahGenerasi = 1000
    rMin_x1 = -3
    rMax_x1 = 3
    rMin_x2 = -2
    rMax_x2 = 2
    panjangIndividu = 10
    panjangPopulasi = 10
    posisiX2 = panjangIndividu // 2
    nilai_x1 = 0
    nilai_x2 = 0

    pop = []
    bestOfTheBest_fitness = []
    for loopGen in range(jumlahGenerasi):
        countFitness = 0
        array_fitness = []
        array_prob = []
        array_nilaiMin = []
        array_nilaiMin_anak = []
        array_fitness_anak = []
        bestKromosom = []
        bestFitness = []

        if (len(pop) == 0):
            for abc in range(panjangPopulasi):
                pop.append(createPopulasi(panjangIndividu))

        for i in range(panjangPopulasi):
            a,b = countX(rMin_x1, rMax_x1, rMin_x2, rMax_x2, panjangIndividu, pop[i][0], i)
            hitungMin = nilaiMinimum(a, b)
            array_nilaiMin.append(hitungMin)
            array_fitness.append(1 / (hitungMin + 0.0001))
            countFitness = countFitness + array_fitness[i]

        # Hitung Probabilitas
        for m in range(panjangPopulasi):
            probabilitas = hitungProbabilitas(array_fitness[m], countFitness)
            pemb = round(probabilitas,1)
            array_prob.append(pemb)

        nomorOT,isiOT = pilihOrtu(panjangPopulasi, array_prob, pop)
        anak = crossOver(isiOT)

        # Swap Position
        for p in range(len(anak)):
            anak = swapPosition(anak, panjangIndividu, p)

        array_fitness_ortu = []
        for q in range(panjangPopulasi):
            checkFitness = nomorOT[q]
            array_fitness_ortu.append(array_fitness[checkFitness-1])
        
        for s in range(len(anak)):
            c,d = countX(rMin_x1, rMax_x1, rMin_x2, rMax_x2, panjangIndividu, anak[s], s)

            hitungMin_anak = nilaiMinimum(c, d)
            array_nilaiMin_anak.append(hitungMin_anak)
            array_fitness_anak.append((1 / hitungMin_anak) + 0.0001)

        pop = []
        for t in range(panjangPopulasi):
            temp1, temp2 = compareFitness(array_fitness_ortu, array_fitness_anak, isiOT, anak, t)
            pop.append(temp1)
            bestFitness.append(temp2)

        bestOfTheBest_fitness.append(bestFitness)

    panjangBest = len(bestFitness) - 1
    isiKromosom = 0
    
    checkTerbaik = 0
    for abcd in range(panjangBest):
        if (checkTerbaik < bestFitness[abcd][0]):
            checkTerbaik = bestFitness[abcd][0]
    

    for check in range(len(bestFitness)-1):
        if (checkTerbaik == bestFitness[check][0]):
            isiKromosom = check
            break
    
    print("Fitness Maximum Terbaik  =", checkTerbaik)
    print("Isi Kromosom             =",pop[isiKromosom])

    x1,x2 = countX(rMin_x1, rMax_x1, rMin_x2, rMax_x2, panjangIndividu, pop[0][0], isiKromosom)
    print("X1                       =",x1)
    print("X2                       =",x2)

    nilaiMinFix = nilaiMinimum(x1,x2)
    print("Nilai Minimum            =",nilaiMinFix)

        

if __name__ == "__main__":
    main()