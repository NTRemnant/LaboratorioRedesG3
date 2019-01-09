def modulacion_digital_qask(senal, fc, Tb, fs):

    resultado = []
    t = np.linspace(0, Tb, fs * Tb)

    C_0000 =  100 * cos(2 * pi * fc * t)
    C_0001 =  500 * cos(2 * pi * fc * t)
    C_0010 = 1000 * cos(2 * pi * fc * t)
    C_0011 = 1500 * cos(2 * pi * fc * t)
    C_0100 = 2000 * cos(2 * pi * fc * t)
    C_0101 = 2500 * cos(2 * pi * fc * t)
    C_0110 = 3000 * cos(2 * pi * fc * t)
    C_0111 = 3500 * cos(2 * pi * fc * t)
    C_1000 = 4000 * cos(2 * pi * fc * t)
    C_1001 = 4500 * cos(2 * pi * fc * t)
    C_1010 = 5000 * cos(2 * pi * fc * t)
    C_1011 = 5500 * cos(2 * pi * fc * t)
    C_1100 = 6000 * cos(2 * pi * fc * t)
    C_1101 = 6500 * cos(2 * pi * fc * t)
    C_1110 = 7000 * cos(2 * pi * fc * t)
    C_1111 = 7500 * cos(2 * pi * fc * t)


    for b in range(0, len(senal)-3, 4):
        print(b)
        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_0000)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_0001)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_0010)

        if senal[b] == 0 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_0011)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_0100)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_0101)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_0110)

        if senal[b] == 0 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_0111)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_1000)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_1001)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_1010)

        if senal[b] == 1 and senal[b+1] == 0 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_1011)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 0:
            resultado.extend(C_1100)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 0 and senal[b+3] == 1:
            resultado.extend(C_1101)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 0:
            resultado.extend(C_1110)

        if senal[b] == 1 and senal[b+1] == 1 and senal[b+2] == 1 and senal[b+3] == 1:
            resultado.extend(C_1111)



    tiempo = np.linspace(0, Tb * len(senal), len(resultado))
    return tiempo, resultado