# Laboratorio: Transmisión de datos entre computadoras (variación transmisión de imagen vía cable de audio).

Proyecto semestral de laboratorio para la asignatura de Redes de Computadores 2°Semestre del 2018. Grupo N°3.

## Integrantes
- Carlos Alvarez
- Sebastián Pasutti
- Alberto Pizarro

## Indice

- [Etapa 1: Análisis  de señales](#etapa-1-an%C3%A1lisis--de-se%C3%B1ales)
  - [Objetivos](#objetivos)
  - [Caracteristicas de la entrega](#caracteristicas-de-la-entrega)
  - [Análisis de resultados](#an%C3%A1lisis-de-resultados)
- [Tecnología utilizada](#tecnolog%C3%ADa-utilizada)
- [Modo de uso](#modo-de-uso) 

## Etapa 1: Análisis  de señales

### Objetivos
El objetivo que nos fue entrega corresponde a crear un programa en el lenguaje de programación Python, que sea capaz de analizar y procesar señales en el dominio del tiempo y en el de la frecuencia.

Específicamente, se nos pide crear:
>1.-Módulos para leer y grabar archivos.
>2.-Módulos para graficar transformadas de fourier y espectrogramas.
>3.-Módulos para aplicar filtros digitales a señales de audio.
>4.-Documentación de experimentos realizados y sus resultados.

Como material para probar nuestros programas, se nos proveyó de archivos de audio de comunicaciones reales y otros simulados que debieron ser analizados para eliminar el ruido y aquellas bandas inaudibles.

### Caracteristicas de la entrega 
  - Carac 2
  
### Análisis de resultados

![Gráfico Amplitud vs. Tiempo](/Images/Etapa1/Prueba_A_1.jpg.jpg)

![Diagrama de clases](/Images/Etapa1/Prueba_A_2.jpg.jpg)

![Diagrama de clases](/Images/Etapa1/Prueba_A_3.jpg.jpg)

## Tecnología utilizada
Se utilizaron las siguientes tecnologías y librerías para construir el proyecto:

* [PyCharm](https://www.jetbrains.com/pycharm/download/#section=linux) - IDE especializado en proyectos de python
* [Python 3.0](https://www.python.org/download/releases/3.0/)  - Lenguaje de programación
* [NumPy](http://www.numpy.org/)   - Librería Python para calculo matricial y analisis cientifico
* [SciPy](https://www.scipy.org/) - Librería Python para computación cientifica y tecnica
* [PIL](https://pypi.org/project/PIL/) - Librería python para manejo especializado de imagenes
* [Matplotlib](https://matplotlib.org/) - Librería Python para Generación de Gráficas

## Modo de uso
La interacción con el programa se realiza durante su ejecución, siendo el ususario el que ingresa por consola el nombre del archivo .wav a modificar y los parámetros de filtrado según corresponda.