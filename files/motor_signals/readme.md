# Nomeclatura dos arquivos:

`F -> Falha`

`C -> Carga`

`rpm -> rotações por minuto`

Exemplo:

```F0-C0-1797rpm.txt```

0 Falhas, Carga 0 e 1797 rotações por minuto.

# Aquisição

Os arquivos possuem dados de vibração, coletados através de um acelerômetro de três eixos, modelo MPU-6050.
Foram coletadas 200 mil leituras para cada cenário, exceto o cenário com carga 20 (C20), para esse arquivo, foram obtidas apenas 50 mil leituras.

Assumimos como uma leitura o valor do eixo X, eixo Y, eixo Z e timestamp. Sendo os quatro valores posicionados em uma mesma linha do arquivo. Como separador foi utilizado o ';'. 

O timestamp foi capturado usando a função time() do Python 3: https://docs.python.org/3/library/time.html#time.time.


Abaixo está um exemplo de uma leitura:

`-1376;-3520;15744;1686751994.5462475`