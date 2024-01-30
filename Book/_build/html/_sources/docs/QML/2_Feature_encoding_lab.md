---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
license: CC-BY-4.0
github: https://github.com/jamasole/Curso-TalentQ-Jupyterlab
subject: Curso
venue: Quantum Spain
authors:
  - name: Javier Mas
    email: javier.mas@usc.es
    corresponding: true
    orcid: 0000-0001-7008-2126
    affiliations:
      - IGFAE-USC
  - name: David Castaño
    email: david.castano@uma.es
    corresponding: true
    orcid: 0000-0001-7008-2126
    affiliations:
      - UMA
math:   
    '\i': '{\color{blue} i}'
    '\bes': '\begin{equation*}'
    '\ees': '\end{equation*}'
    '\O': '{\mathcal O}'
    '\Lin': '\rm L'
    '\Hil': '{\mathcal H}'
    '\braa': '{\langle #1|}'
    '\ket': '{|#1\rangle}'
    '\braket': '{\langle #1|#2\rangle}'
    '\ketbra': '{|#1\rangle\langle #2|}'
    '\tr': '{\rm tr}'
    '\R': '{\mathbb R}' 
    '\C': '{\mathbb C}'
    '\V': '{\cal V}'
---
$\newcommand{\V}{{\cal V}}$
$\newcommand{\C}{{\mathbb C}}$
$\newcommand{\R}{{\mathbb R}}$
$\newcommand{\tr}{{\rm tr}}$
$\newcommand{\ketbra}[2]{{|#1\rangle\langle #2|}}$
$\newcommand{\braket}[2]{{\langle #1|#2\rangle}}$
$\newcommand{\ket}[1]{{|#1\rangle}}$
$\newcommand{\braa}[1]{{\langle #1|}}$
$\newcommand{\Hil}{{\mathcal H}}$
$\newcommand{\Lin}{\rm L}$
$\newcommand{\O}{{\mathcal O}}$
$\newcommand{\ees}{\end{equation*}}$
$\newcommand{\bes}{\begin{equation*}}$
$\newcommand{\i}{{\color{blue} i}}$

+++

```{figure} ../thumbnails/myThumbnail.png
:align: center
```

+++

# QML (Quantum Machine Learning)


+++

Consulta la notación que se ha utilizado durante todo el documento en el siguiente [enlace](#notacion).

```{code-cell} ipython3
import numpy as np
import qibo
import matplotlib.pyplot as plt
from qibo import callbacks, gates, hamiltonians, models
from qibo.symbols import Y, Z, I
from sklearn.datasets import make_moons
from qibo.models import Circuit

import tensorflow as tf
qibo.set_backend("tensorflow")
```

# 2. Feature encoding

+++

<a id='IntroFeatureEncoding'></a>
## 2.1. Introducción

+++

El proceso de ***feature encoding*** se encarga de codificar datos clásicos en estados cuánticos. El problema de codificar datos clásicos en estados cuánticos es esencial en todas las disciplinas que estudian sacar ventaja de las propiedades cuánticas para problemas clásicos, como la comunicación, criptografía o la computación cuántica. Este notebook se centra en las técnicas de *feature encoding* básicas para QML. Se empieza con un conjunto de datos $\mathbf{x}$ Conjunto que se quiere codificar en un estado $\ket{\psi_x}$ con el que trabajar, para ello se construye un circuito parametrizado que generará una unitaria $\mathcal{U}(\mathbf{x})$ tal que $\ket{\psi_x}=\mathcal{U}(\mathbf{x})\ket{0}$. Dependiendo del tipo de *feature encoding* que se utilice, la unitaria $\mathcal{U}(x)$ tendrá diferentes características. Se trata de un proceso crucial para el diseño y aplicación de los algoritmos, ya que influye en su capacidad computacional y en su eficiencia [[1]](#referencias)[[2]](#referencias)[[3]](#referencias)[[4]](#referencias).

Se define un conjunto de datos de entrada $D$ de dimensión $M$ x $N$, es decir, se cuenta con un dataset con M instancias y N variables. Este *dataset* se puede expresar como $D = \{\mathbf{x}_{(1)}, ..., \mathbf{x}_{(m)}, ..., \mathbf{x}_{(M)}\}$ donde cada $\mathbf{x}_{(m)}$ es un vector de dimensión N.


Hay multiples técnicas de ***feature encoding***, algunas se detallan a continuación. Como ejemplo intentaremos codificar el vector $x=(0,1,2,3)$ de diferentes maneras en nuestro circuito.

+++

<a id='TiposFeatureEncoding'></a>
## 2.2. Tipos de feature encoding

+++

<a id='BasisEncoding'></a>
### 2.2.1. Basis encoding

+++

La técnica *Basis encoding*, también conocida como *Basis Embedding*, asocia un *input* (entrada) a un estado de la base computacional de un sistema de qubits. Es por eso que los datos clásicos deben estar, o poder ser representados, por una cadena de bits, es decir, mediante este método de codificación se trabajará con cadenas binarias. Este método representa el dato clásico $x=1101$ como el estado $\ket{1101}$, por ejemplo.

Se considera el conjunto de datos $D$, definido anteriormente. En el caso de *basis encoding*, las N características de cada ejemplo deben estar representadas por cadenas binarias, es decir, $\mathbf{x}_{m} = (b_1,...,b_N)$ con $b_i\in \{ 0,1\}$ para $i=1,...,N$. Asumiendo que todas las variables (características?) del *dataset* se representan mediante un único bit, cada *input* (entrada) $\mathbf{x}_{m}$ puede representarse como $\ket{\mathbf{x}_{m}}$. Extendiendo la expresión anterior a todo el *dataset*, obtenemos la representación del conjunto de datos al completo, ésta corresponde a la siguiente expresión:

$$\ket{D} = \frac{1}{\sqrt M} \sum^M_{m=1} \ket{\mathbf{x}_{m}}$$

+++

Por ejemplo, si consideramos que el *dataset* x los datos en binario correspondria a ejemplos $x = 1111011$, la representación de los mismos se corresponde con $\ket{1111011}$. En este caso, el estado corresponde a:

$$\ket D = \ket{1111011}$$


```{code-cell} ipython3
num_q=7
```

```{code-cell} ipython3
def Basis_encoding(x, nqubits= 2):
    c= Circuit(nqubits=nqubits)
    
    for i in range(nqubits):
        if x[i]==1:
            c.add(gates.X(q=i))
    return c
```

```{code-cell} ipython3
x = np.array([1,1,1,1,0,1,1])
c_b=Basis_encoding(x,num_q)


print("x               : ", x)
print("amplitude vector: ", np.array(c_b.execute().state()))
print(c_b.draw())
```

<a id='AmplitudeEncoding'></a>
### 2.2.2. Amplitude encoding

+++

La técnica *Amplitude encoding* o *amplitude embedding*, codifica los datos clásicos como las amplitudes de un estado cuántico. En este caso, una instancia del *dataset* que clásicamente se representa mediante un vector normalizado (denominado $x$) de dimensión N , aplicando esta técnica de codificación, dicho vector corresponde a las amplitudes del estado cuántico de n-qubits. La expresión es la siguiente:

$$ \ket{\psi_x} = \sum^N_{i=1} x_i\ket i$$   


Donde $N=2^n$, $x_i$ es el i-ésimo elemento del vector $\mathbf{x}$ y $\ket i$ es el i-ésimo estado de la base computacional. A diferencia de la técnica, *basis encoding*, $x_i$ puede tomar valores de distintos tipos, como *integer* (valores enteros) o *float* (valores de coma flotante). 

+++

Como ejemplo, si tratamos de codificar la instancia correspondiente al vector 
utilizando esta técnica obtendremos:

$$\ket{\psi_x} = \frac{1}{4} [\ket{01}+2\ket{10}+3\ket{11}]$$

+++

Nota: Todos los vectores cuánticos deben estar normalizados, $\bra{\psi_x}\ket{\psi_x} = 1$

```{code-cell} ipython3
num_q=2
```

```{code-cell} ipython3
def Normalize(x):
    N=np.linalg.norm(x)
    return 1/N*x
```

```{code-cell} ipython3
x = np.array([0,1,2,3])
#We normalize x
x_norm=Normalize(x)
c_a = Circuit(num_q)

print("x               : ", x)
print("amplitude vector: ", np.array(c_a(x_norm,nshots=10000).state()))
print(c_a.draw())
```

La función de pennylane *Amplitude Embedding* utiliza el método desarollado en [[4]](#referencias) para codificar un vector arbitrario en las amplitudes de un estado cuántico con el mínimo número de *gates* (puertas cuánticas). Para una documentación más extensa de cómo aplicar este método se puede consultar [[5]](#referencias).

+++

<a id='angleEncoding'></a>
### 2.2.3. Angle encoding

+++

*Angle encoding* es una técnica de codificación básica, las N características de las instancias del *dataset* se codifican como ángulos de rotación de N cúbits. Esta metodología codifica N características en los ángulos de rotación de N qubits. Dichas rotaciones pueden llevarse a cabo en cualquier eje, tanto en el X, como en el Y o en el Z.

En general, para codificar una instancia $\mathbf{x}=(x_1,...,x_N)$ se utiliza la siguiente expresión: 

$$
\ket {\mathbf{x}} = \bigotimes^N_{i=1} \cos(x_i)\ket 0 + \sin(x_i)\ket 1
$$

Este método es diferente a los dos métodos anteriores, ya que únicamente codifica una instancia cada vez en lugar de trabajar con todo el *dataset*. No obstante, utiliza N qubits y la profundidad del circuito es constante, por lo que resulta compatible con el hardware cuántico.

Esta técnica se puede representar mediante una matriz unitaria:

$$
S_{\mathbf{x}_j} = \bigotimes^N_{i=1} U(\mathbf{x}_{j_i})
$$

donde:

$$
U(\mathbf{x}_{j_i}) = \begin{bmatrix} \cos(\mathbf{x}_{j_i}) & -\sin (\mathbf{x}_{j_i}) \\ \sin (\mathbf{x}_{j_i}) & \cos (\mathbf{x}_{j_i}) \end{bmatrix}
$$

+++

Por ejemplo, si se trata de codificar el vector$\mathbf{x}=(0,1,2,3)$  con este tipo de *encoding* se necesitarán cuatro cúbits y quedará como sigue: 
$$
\ket {\mathbf{x}} = (\cos(0)\ket 0 + \sin(0)\ket 1 ) \otimes (\cos(1)\ket 0 + \sin(1)\ket 1) \otimes (\cos(2)\ket 0 + \sin(2)\ket 1) \otimes (\cos(3)\ket 0 + \sin(3)\ket 1 )
$$

```{code-cell} ipython3
num_q=4
```

```{code-cell} ipython3
def Angle(x,nqubits):
    c= Circuit(nqubits=nqubits)
    
    for i in range(nqubits):
        c.add(gates.RX(q=i,theta=x[i]))
    return c
```

```{code-cell} ipython3
x = np.array([0,1,2,3])

c_an=Angle(x,num_q)

print("x               : ", x)
print("amplitude vector: ", np.array(c_an.execute().state()))
print(c_an.draw())
```

<a id='DenseAngleEncoding'></a>
### 2.2.4. Dense angle encoding

+++

Esta técnica es una generalización de la codificación anterior, es capaz de codificar dos características por cada *qubit*, haciendo uso de fases relativas. En este caso, la instancia $x=(x_1,...,x_N)$ se codifica como sigue:

$$
\ket x = \bigotimes^{N/2}_{i=1} \cos(x_{2i-1})\ket 0 + e^{ix_{2i}}\sin(x_{2i-1})\ket 1
$$

Aunque *dense angle encoding* y *angle encoding* utilizan funciones sinusoidales y exponenciales se pueden sustituir por funciones unitarias arbitrarias para generar otras técnicas de *feature encoding*.

+++

Por ejemplo, si se trata de codificar el vector$\mathbf{x}=(0,1,2,3)$  con este tipo de *encoding* se necesitarán dos cúbits y quedará como sigue: 
$$
\ket {\mathbf{x}} = (\cos(0)\ket 0 + e^{i1}\sin(0)\ket 1 ) \otimes (\cos(2)\ket 0 + e^{i3}\sin(2)\ket 1)
$$

```{code-cell} ipython3
num_q=2
```

```{code-cell} ipython3
def denseAngle(x,nqubits):
    c= Circuit(nqubits=nqubits)
    
    for i in range(nqubits):
        c.add(gates.RX(q=i,theta=x[i]))
        c.add(gates.RZ(q=i,theta=x[i+1]))
    return c
```

```{code-cell} ipython3
x = np.array([0,1,2,3])

c_dan=denseAngle(x,num_q)

print("x               : ", x)
print("amplitude vector: ", np.array(c_dan.execute().state()))
print(c_dan.draw())
```

En este apartado se muestran algunas de las técnicas de codificación, no obstante existen otras como *Displacement Embedding*, *IQP Embedding*, *QAOA Embedding*...

+++

<a id='EleccionFeatureEncoding'></a>
## 2.3. Cómo escoger Feature Encoding

+++

Cuando se trata con circuitos variacionales la decisión de qué *feature encoding* utilizar es crucial. Los diferentes *feature encoding* presentan diferentes ventajas e inconvenientes dependiendo del problema que queramos resolver. Las técnicas mencionadas en este notebook se pueden separar en dos tipos:
- *basis encoding* donde se trabaja con los elementos de la base computacional como *inputs* (entradas)
- el resto de codificadores que trabajan con las amplitudes del vector cuántico.

+++

La técnica de *basis encoding* presenta la capacidad de calcular operaciones no lineales de forma natural, a cambio es el codificador que presenta mayor número de problemas: 
- Es el más susceptible a errores.
- Escala muy mal con el número de cúbits, ya que de esto depende la precisión de los *feature* que se quiere codificar.
- Es el método que presenta mayor dificultad a la hora de entrenar la red neuronal y tiene tendencias a presentar barren plateaus (gradientes que tienden a cero).

+++

El resto de métodos basados en codificar en las amplitudes del vector cuántico no presentan los inconvenientes enumerados anteriormente y son los métodos preferidos para desarollar algoritmos en la era del NISQ (*Noisy intermediate-scale quantum*). Aún así, presentan el inconveniente que hay que escoger sabiamente cómo introducir la no-linealidad necesaria para cada problema. La forma más genérica es utilizar *Amplitude encoding* y aplicar una función $f(x)$ a tus datos para obtener correlaciones entre ellos y así poder resolver problemas no-lineales. Este método, que es a primera vista sencillo, presenta el problema que la amplitud del circuito puede ser muy grande dependiendo de $f(x)$ y además, escoger $f(x)$ puede ser un proceso muy arbitrario. Por otra parte, otros métodos de codificación más sencillos pueden proporcionar directamente los elementos de no linealidad necesarios para resolver el problema.

+++

Escoger el método de *feature encoding* es un proceso crucial para un VQC (*Variational Quantum Circuit*) pero, como se ha visto, no es una ciéncia exacta, por lo que se deben probar distintas técnicas y escoger la que mejor se ajusta al problema en particular. Para finalizar, existen otras técnicas más sofisticadas para introducir datos clásicos en un circuito variacional, una de ellas es conocido como *data re-uploading* [[7]](#referencias).

+++

<a id='notacion'></a>
::::{admonition} ANEXO NOTACIÓN
:class: note


Para que la comprensión de los notebooks sea mejor se ha unificado la notación utilizada en los mismos. Para diferenciar un vector de un valor único se hará uso de la negrita. De manera que $\mathbf{x}$ corresponde a un vector y $z$ será una variable de una única componente. 

    
Si se quiere hacer referencia a dos vectores distintos pero que pertenecen al mismo *dataset* se utilizará un subíndice, es decir, $\mathbf{x_i}$ hará referencia al i-ésimo vector del dataset. Si se quiere referenciar una característica concreta del vector $\mathbf{x_i}$ se añadirá un nuevo subíndice, de manera que $\mathbf{x_{i_j}}$ hará referencia a la j-ésima variable del i-ésimo vector.

::::

+++

---------------------------
## Referencias
<a id='referencias'></a>
[1]. https://learn.qiskit.org/course/machine-learning/data-encoding/
[2]. https://pennylane.ai/qml/glossary/quantum_embedding.html/
[3]. https://arxiv.org/abs/1804.11326/
[4]. https://arxiv.org/abs/2003.01695/
[5]. https://docs.pennylane.ai/en/stable/code/api/pennylane.MottonenStatePreparation.html/
[6]. http://arxiv.org/abs/quant-ph/0407010/
[7]. https://arxiv.org/abs/1907.02085/

+++

This work has been financially supported by the Ministry of Economic Affairs and Digital Transformation of the Spanish Government through the QUANTUM ENIA project call - Quantum Spain project, and by the European Union through the Recovery, Transformation and Resilience Plan - NextGenerationEU within the framework of the Digital Spain 2025 Agenda.


<img align="left" src="https://quantumspain-project.es/wp-content/uploads/2022/11/LOGOS-GOB_QS.png" width="1000px" />
