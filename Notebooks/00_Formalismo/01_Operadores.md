---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
title: Operadores
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
    '\i': '{i}'
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
    '\V': '{V}'
---
$\newcommand{\V}{{V}}$
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
$\newcommand{\i}{{i}}$

+++

```{figure} ../thumbnails/myThumbnail.png
:align: center
```

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
import sys
sys.path.append('../')
import macro_tQ as tQ

import numpy as np
import scipy.linalg as la
from IPython.display import display,Markdown,Latex
import matplotlib.pyplot as plt
from qiskit.tools.visualization import array_to_latex
```

+++ {"slideshow": {"slide_type": "skip"}}

## Operadores y Matrices

+++ {"slideshow": {"slide_type": "skip"}}

En un espacio vectorial, además de los **vectores**, será esencial entender las **transformaciones** de estos elementos entre sí. 

+++ {"slideshow": {"slide_type": "slide"}}

:::{card}
**Definición**: *operador lineal*

^^^

Un <i>operador lineal</i>  transforma <u>todo vector en otro</u> 

$$
A: \ket{u} ~~\to ~~ \ket{v}   
$$
:::

+++ {"slideshow": {"slide_type": "fragment"}}

El apelativo lineal es una condición extremadamente útil, que indica cómo se transforma un vector que es combinación lineal de otros dos

$$
A: \big(\alpha\ket{u} + \beta\ket{w}\big)~~\to ~~ \ket{v} =\alpha A\ket{u} + \beta A\ket{w}
$$ 

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Notación
:class: note

Escribimos también $\ket{v} = A\ket{u} \equiv \ket{Au}$ $~~$ donde $Au=v$ deben entenderse como la etiqueta sinónimas del vector imagen

:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejemplo
:class: tip

Un <i>operador</i>  fácil de visualizar es el operador de <i>rotación en un plano</i>. Dado un ángulo $\theta \in (0,2\pi)$ el operador $A = R(\theta)$ gira cualquier vector un ángulo $\theta$ en el sentido antihorario

Un vector en  ${\bf u} =  (u_1,u_2)\in {\mathbb R}^2$  es equivalente al número complejo $u = u_1 + i u_2 \in {\mathbb C}$.

    
Escrito en polares, $u=|u|e^{i\phi}$, y sabemos que una rotación de ángulo $\theta$ es equivalente a añadirle dicho  ángulo a la fase 

$$
 v = R(\theta) u = |u| e^{i(\phi + \theta)} =  |u| e^{i\phi } e^{i\theta} = u\cdot e^{i\theta} 
$$
    
Por tanto, rotar un número complejo un ángulo $\theta$ se corresponde con la acción el operador $R(\theta)$
que multiplica cualquier número complejo por la fase $e^{i\theta}$.

    
    
La propiedad fundamental de una rotación es la de mantener invariante el módulo  $|v| = |u|$.    

:::

+++ {"slideshow": {"slide_type": "skip"}}

::::{admonition} Ejercicio
:class: tip

Usando el ejemplo anterior, define una función $R$ en python, que recibe un vector en el plano $(u_1,u_2)$ y devuelve el vector $(v_1,v_2)$ de componentes rotadas un ángulo $\theta$.


:::{dropdown} Solución

```{code-block} python
def R(u1,u2,theta):
   u = u1 + u2*1j
   v = u*np.exp(1j*theta) # u rotado un angulo theta
   return v.real,v.imag
```
:::
::::
 

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
'''ángulo que queremos rotar'''
theta=0.6 

'''vector a rotar'''
u1=2.
u2=2.

#'''v1 y v2 a partir de u1, u2 y theta'''
#def R(u1,u2,theta):
#        u = u1 + u2*1j
#        v = u*np.exp(1j*theta) # u rotado un angulo theta
#        return v.real,v.imag
    
v1,v2 =  R(u1,u2,theta)

''' Representación en el plano complejo '''
v = v1**2+v2**2
tQ.plot_2D_plane(left=-int(abs(v1))-2,right=int(abs(v1))+2,up=int(abs(v2))+1,down=-int(abs(v2))-1)
tQ.draw_vector(u1,u1,vcolor='b')
tQ.draw_vector(v1,v2,vcolor='r')
```

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Matriz de un operador
<a id='matriz_op'></a>

*Dada una base* $\ket{i}$ sabemos que:

$\Rightarrow $  un vector queda especificado por una *columna de números* 

$$
\ket{v} \sim \begin{pmatrix} v_1 \\ v_2\\ \vdots \\ v_N\end{pmatrix}
$$

+++ {"slideshow": {"slide_type": "fragment"}}

$\Rightarrow $  un operador queda definido por una *matriz de números*. 

$$
A \sim \begin{pmatrix} 
A_{11} & A_{12} & \cdots & A_{1N} \\
A_{21} & A_{22} & \cdots & A_{2N} \\
\vdots & \vdots &  \ddots      & \vdots \\
A_{N1} & A_{N2} &    \cdots    & A_{NN}
\end{pmatrix}
$$

+++

En ambos casos, los números son las **componentes** en una base. 

+++ {"slideshow": {"slide_type": "skip"}}

Efectivamente, en una base, la relación $\ket{v} = A\ket{u}$ equivale a una ecuación que relacione las componentes de ambos vectores
$$
v_i = \sum_{j=1}^N A_{ij} u_j  \, .
$$

+++ {"slideshow": {"slide_type": "skip"}}

Esta operación se corresponde con la siguiente *multiplicación de matrices*

$$
\begin{pmatrix}
v_1 \\ v_2 \\ \vdots \\ v_N \end{pmatrix} =  \begin{pmatrix} 
A_{11} & A_{12} & \cdots & A_{1N} \\
A_{21} & A_{22} & \cdots & A_{2N} \\
\vdots & \vdots &  \ddots      & \vdots \\
A_{N1} & A_{N2} &    \cdots    & A_{NN}
\end{pmatrix}
 \begin{pmatrix} 
u_1 \\ u_2 \\ \vdots \\ u_N\end{pmatrix} 
$$

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejemplo
:class: tip

Continuando con el ejemplo del operador de rotación en un plano, hemos visto que las componentes de $u = u_1 + i u_2$ y las de $R(\theta)u = v = v_1 + i v_2$ se obtienen mediante la multiplicación por una fase pura 

\begin{eqnarray}
v&=& u e^{i\theta} \\
\end{eqnarray}
    
Vamos a desarrollar cada miembro en cartesianas, separando las partes real e imaginaria
    
\begin{eqnarray}
v_1 + i v_2 &=& (u_1 + iu_2) (\cos \theta + i \sin \theta)  \\
    \rule{0mm}{6mm}
    &=& (\cos\theta \, u_1 - \sin \theta\,  u_2) + i(\sin\theta\,  u_1 + \cos \theta\,  u_2)
\end{eqnarray}
   
es decir las coordenadas del vector origen y el vector rotado imagen se relacionan en la  forma 
\begin{eqnarray}
v_1 = \cos\theta \, u_1 - \sin \theta\,  u_2 ~~~~~~~,~~~~~~~~
v_2 = \sin\theta \, u_1 + \cos \theta\,  u_2     
\end{eqnarray}
que podemos expresar en forma matricial
    
$$
\begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta &\cos\theta\end{pmatrix} \begin{pmatrix} u_1 \\ u_2 \end{pmatrix}
$$    
:::

+++ {"slideshow": {"slide_type": "slide"}}

##   El Espacio Vectorial  $\Lin(\Hil)$ 

+++ {"slideshow": {"slide_type": "-"}}

El <i>conjunto</i> de **todos** <i>los operadores lineales</i> sobre un espacio vectorial $\Hil$ tiene, de forma natural, una estructura de espacio vectorial que denominamos $\Lin(\Hil)$

+++ {"slideshow": {"slide_type": "fragment"}}

En efecto, dados dos operadores,  $A$ y $B$ tanto la suma $C = A+B$ como la multiplicación por un número complejo $D=\lambda A$ son *nuevos operadores* definidos por su acción sobre un vector cualquiera $\ket{v}\in \Hil$

$$
C\ket{v} ~=~ (A + B) \ket{v} = A\ket{v} + B\ket{v}
$$

$$
D\ket{v} ~=~ (\lambda A) \ket{v} = \lambda (A\ket{v})
$$

+++

El elemento neutro es el operador que aniquila cualquier vector

$$
(A + 0)\ket{u} = A\ket{u} + 0\ket{u} = A\ket{u} + 0 = \ket{v}
$$

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Producto externo

+++

$\Lin(\Hil)$ es por tanto, un espacio vectorial cuyos vectores son los operadore lineales sobre $\Hil$. Como para cualquier espacio vectorial, para describir los operadores $A$,  necesitamos una base. 

Resulta que, como vamos a ver, una base $\{ \ket{i}\}$ para describir los vectores  de $\ket{v}\in \Hil$ nos permite definir una base para los operadores $A \in \Lin(\Hil)$ de forma natural. 

Para verlo vamos a definir dos formas de componer dos vectores de $\ket{u},\ket{v} \in \Hil$: el producto interno, y el producto externos. 

+++ {"slideshow": {"slide_type": "skip"}}



- El **producto interno**, o *producto escalar* es un *número complejo*

$$
 a = \braket{u}{v} = \braket{v}{u}^* 
$$

- El **producto externo**  es un *operador*

$$
A = \ketbra{v}{u}
$$

+++ {"slideshow": {"slide_type": "skip"}}

Para comprender <u>por qué el producto externo es un operador</u>, observamos que dicha expresión aplicada a un vector $\ket{w}$ da otro, <br>

$$
A : \ket{w} ~\to ~ A\ket{w} =  \ket{v}\braket{u}{w}=\ket{v} b  = b \ket{v} 
$$ 

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

- El *orden* en que escribimos las cosas es *muy* relevante.
    - $\braket{u}{v}$ y $\ket{v}\!\bra{u}$ son objetos <i> radicalmente distintos</i>: el primero es un número y el segundo es un operador. 

    - En cambio $\ket{v} b  = b \ket{v}$, así como $\bra{u}b = b\bra{u}$, es decir,  los números complejos  pueden escribirse en cualquier posición (decimos que <i>conmutan con todo</i>).

- La acción del operador  $A = \ket{v}\bra{u}$ es muy fácil de *expresar con palabras*: 
<br>  
    - el operador $A$ toma <i>cualquier vector</i> $\ket{w}$ y lo convierte en un vector <i>paralelo</i> a $\ket{v}$ proporcionalmente a su proyección $b=\braket{u}{w}$. 
<br>    
    - si la proyección es nula $a=0$, el operador <i>aniquila</i>, es decir, da el elemento neutro.
:::

+++ {"slideshow": {"slide_type": "skip"}}

**En componentes**

La diferencia entre el *producto interno* $a=\braket{u}{v}$ y el *externo* $A=\ketbra{u}{v}$ tiene su reflejo en una base expresando ambos vectores, $\ket{u} = \sum_i u_i\ket{i}$ y $\ket{v} = \sum_j v_j \ket{j}$,  en componentes en una base ortonormal

-  el *número complejo* $a$  es el *producto escalar*
  
$$
 a = \braket{u}{v}  = \begin{pmatrix} u_1^*,...,u_N^*\end{pmatrix}
\begin{pmatrix} v_1 \\ \vdots \\ v_N\end{pmatrix}\, =  \sum_i u_i^*v_i
$$

+++ {"slideshow": {"slide_type": "skip"}}

-  la matriz $A_{ij}$    *representa* el operador $A$ en la base $\{\ket{i}\}$

$$
A = \ketbra{v}{u} ~\sim ~\begin{pmatrix} v_1 \\ \vdots \\ v_N\end{pmatrix}
\begin{pmatrix} u_1^*,...,u_N^*\end{pmatrix} ~=~ 
\begin{pmatrix} v_1 u_1^* & v_1u_2^* & ... & v_1 u_N^* \\
v_2 u_1^* & v_2 u_1^*& ... & v_2 u_N^* \\ \vdots & \vdots  & \ddots & \vdots \\
v_N u_1^* & & ... & v_N u_N^* \end{pmatrix} ~ = ~A_{ij}
$$

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Base canónica de operadores
<a id='base_canonica'></a>

Consideremos el *producto externo* de dos elementos de la base ortonormal
$\ketbra{i}{j}$

- La acción de $\ketbra{i}{j}$ sobre otro vector, $\ket{k}$,  de la base es sencilla 

$$
 \ket{i}\braket{j}{k} = \ket{i} \delta_{jk} = \left\{ \begin{array}{rl}
0 & {\rm si} ~~k\neq j \\ \ket{i} & {\rm si} ~~ k=j \end{array} \right.
$$

+++ {"slideshow": {"slide_type": "skip"}}

- La matriz asociada al operador  tiene sólo un 1 en el elemento $(ij)$ y cero en todos los demás. Por ejemplo, supongamos que 
$N=4$ 

<br>

$$
\ketbra{2}{3} ~\to ~~
 \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}\begin{pmatrix} 0 & 0 & 1 & 0 \end{pmatrix} = 
\begin{pmatrix}
0 &  0 & 0 &  0 \\  0 &  0 & 1&  0 \\ 0 &  0 & 0 &  0 \\ 0 &  0 & 0 &  0
\end{pmatrix} ~~\Rightarrow ~~ A_{ij} = \delta_{i2}\delta_{j3}
$$

<br>

+++ {"slideshow": {"slide_type": "slide"}}


Los <i>elementos de matriz</i> $A_{ij}$ expresan las <i>componentes de un operador</i> en la <b>base de operadores</b> $\ketbra{i}{j}$

+++ {"slideshow": {"slide_type": "-"}}

$$
A ~=~ \sum_{i,j=1}^N A_{ij} \ketbra{i}{j} 
$$

+++

:::{dropdown} Consistencia
Verifiquemos que actúa de la forma correcta

$$
\begin{array}{rcl}
A |u\rangle &=&  \sum_{i,j} A_{ij} \ketbra{i}{j}  \left(\sum_k u_k |k\rangle \right) \\
&\stackrel{\rm linealidad}{=} \rule{0mm}{6mm}& \sum_{i,j} \sum_k A_{ij} | i\rangle  \,   u_k \langle j| k\rangle \nonumber\\
&\stackrel{\rm ortonormalidad}{=}\rule{0mm}{6mm}& \sum_{i,j,k} A_{ij} | i\rangle  \,   u_k \delta_{jk}\\
&=\rule{0mm}{6mm}&\sum_{ij} A_{ij}\,|i\rangle \, u_j= \sum_i \left(\sum_{j} A_{ij}\, u_j\right)  |i\rangle    \\
&=\rule{0mm}{6mm}&\sum_i v_i \ket{i} \nonumber\\
&=\rule{0mm}{6mm}&   | v\rangle
\end{array}
$$
:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Elementos de matriz

De la misma manera que obteníamos las componentes de un vector proyectando sobre un elemento de la base

$$
v_i = \braket{i}{v}
$$

ahora podemos obtener los *elementos de matriz* de un operador $A$ en la forma

$$  A_{ij} = \bra{i} A \ket{j} $$

+++ {"slideshow": {"slide_type": "fragment"}}

:::{admonition} Ejercicio
:class: tip

Comprueba la consistencia de las expresiones $~A = \sum_{i,j=1}^N A_{ij} \ketbra{i}{j} $ y $~A_{ij} = \bra{i} A \ket{j}$
<details>
    <summary><p style="text-align:left"> >> <i>Solución:</i> </p></summary>

aquí tu solución
:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} En resumen
:class: attention

En una base $\{\ket{i}\}$ podemos siempre relacionar una matriz con un operador. La relación concreta es de matriz a  operador: $A_{ij} \to ~ A = \sum_{ij} A_{ij}\ketbra{i}{j}$ de operador a  matriz: $A \to ~ A_{ij} = \bra{i}A\ket{j}$
:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Cambio de base 

Dos bases ortonormales $\ket{e_i}$ y $\ket{\tilde e_i}$ se relacionadas linealmente mediante una matriz

$$ \ket{e_j} \to \ket{\tilde e_j} = \sum_{ij}U_{ij} \ket{e_i}$$


Tomar la conjugación *adjunta* de esta expresión es muy sencillo usando las reglas

$$ \bra{e_j} \to \bra{\tilde e_j} = \sum_{ij}U^*_{ij} \bra{e_i}$$


+++ {"slideshow": {"slide_type": "skip"}}


En cada base, un operador $A$ *se representa* mediante elementos de matriz distintos

$$
 A_{ij} = \bra{e_i} A \ket{e_j} ~~~~,~~~~~ \tilde A_{ij} = \bra{\tilde e_i} A \ket{\tilde e_j} \, .
$$


+++ {"slideshow": {"slide_type": "skip"}}

Podemos encontrar la relación sustituyendo el cambio de base

\begin{eqnarray}
\tilde A_{ij} &=& \bra{\tilde e_i} A \ket{\tilde e_j} \\ \rule{0mm}{8mm}
&=& \sum_{k}U^*_{ki}\bra{e_k} ~A~ \sum_l U_{lj}\ket{e_l} \\ 
&=&  \sum_{k,l} U^\dagger_{ik}\bra{e_k} A  \ket{e_l}U_{lj}   = \sum_{k,l} U^\dagger_{ik}A_{kl} U_{lj} \, .
\end{eqnarray}

+++ {"slideshow": {"slide_type": "skip"}}

:::{card} 
**Lema**

^^^

Bajo un cambio de bases ortonormales $ \ket{e_j} \to \ket{\tilde e_j} = \sum_{i}U_{ij} \ket{e_i}$ las componentes de un vector $\ket{v}$ y de  un operador $A$ cambian siguiendo la regla:
<br>      
\begin{eqnarray}
\tilde v_i &=& (U^\dagger \cdot v)_i \\ 
\tilde A_{ij} &=& (U^\dagger \cdot A \cdot U)_{ij}
\end{eqnarray}
:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

La regla *memotécnica* es que las columnas se multiplican por $U^\dagger\cdot$ y las filas por $\cdot\, U$

$$
\begin{pmatrix} \tilde v_1 \\ \vdots \\ \tilde v_N \end{pmatrix} = 
U^\dagger \cdot \begin{pmatrix} v_1 \\ \vdots \\  v_N \end{pmatrix} ~~~~
~~~~~~~;~~~~~~~~
\begin{pmatrix} 
\tilde A_{11} & \cdots & \tilde A_{1N} \\
\tilde \vdots & \ddots & \vdots  \\
\tilde A_{N1} & \cdots & \tilde A_{NN} 
\end{pmatrix} 
 =  U^\dagger\cdot
 \overbrace{\begin{pmatrix} 
 A_{11} & \cdots &  A_{1N} \\
\tilde \vdots & \ddots & \vdots  \\
 A_{N1} & \cdots &  A_{NN} 
\end{pmatrix} }^{\large \cdot ~ U}
$$
:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} **Ejercicio** (*explícaselo a tu ordenador*)
:class: tip

Escribe una función en python, $basis\_change$, que reciba una matriz $U_{ij}$ de cambio de base $\ket{\tilde e_j} = \sum_i{U_{ij}}\ket{e_i}$, la componentes $v_i$ de un vector, ó $A_{ij}$ de un operador, y devuelva las componentes $\tilde v_i~$ ó $~\tilde A_{ij}$ en la nueva base. 
:::    

+++

:::{admonition} **Ejercicio** 
:class: tip
La matriz $\begin{pmatrix} 0 & -i \\ i & 0\end{pmatrix}$ representa un operador $\sigma_y$ en la base $\{ \ket{0},\ket{1}\}$. Utilizando la función *basis\_change*, escribe $\sigma_y$ en la nueva base $\{\ket{\!+\!i}= \frac{1}{\sqrt{2}}(\ket{0}+i \ket{1})~,~\ket{\!-\!i}= \frac{1}{\sqrt{2}}(\ket{0}-i \ket{1})\}$
:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Relación de completitud    
    
La acción del operador identidad es 

$$
I\ket{v} = \ket{v}
$$

En particular sobre todo elemento de la base $I\ket{i} = \ket{i}$. En otras palabras,
el operador identidad $I$ tiene por matriz $I_{ij}=\delta_{ij}={\rm diagonal}\, (1,1,...,1)$ con lo que
<br>

$$
I = \sum_{i}  \ketbra{i}{i}= \sum_{ij} \delta_{ij}\ketbra{i}{j} 
$$

Esta expresión se conoce también como <b>relación de completitud</b> o, también, <b>relación de cierre</b> y se utiliza muy frecuentemente.

+++ {"slideshow": {"slide_type": "skip"}}

La relación de completitud es una propiedad de <b> cualquier base</b>. Dicho de otro modo, si $\{\ket{e_i}\}$ y $\{\ket{\tilde e_i}\}$ son, ambas, bases entonces $I\ket{e_i} = \ket{e_ i}$ y $I\ket{\tilde e_j} = \ket{\tilde e_j}$.
Esto quiere decir que, en cualquier base, la matriz que representa la identidad es la matriz diagonal $\delta_{ij}$
<br>

$$
I =  \sum_{i}  \ketbra{e_i}{e_i} =  \sum_{j}  \ketbra{\tilde e_j}{ \tilde e_j}\, .
$$

+++ {"slideshow": {"slide_type": "skip"}}

La relación de cierre, o completitud,  siempre **se puede insertar** en cualquier momento del cálculo. Se utiliza con frecuencia para efectuar cambios de base.

+++ {"slideshow": {"slide_type": "skip"}}

Por ejemplo, 

\begin{eqnarray}
\ket{\tilde e_j} ~&=&~ \left(\sum_i \ketbra{e_i}{e_i}\right) \ket{\tilde e_j} \nonumber\\
&=&\sum_i \braket{e_i}{\tilde e_j} \ket{e_i} \nonumber\\
&=&\sum_i U_{ij}\ket{e_i}
\end{eqnarray}

Donde la matriz de cambio de base es
$$
U_{ij} = \braket{e_i}{\tilde e_j}
$$

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Operador Adjunto
<a id='opadj'></a>

    
La *conjugación adjunta* definida sobre $\Hil$ puede extenderse a $\Lin(\Hil)$
<br><br>

$$
\dagger ~\to ~
\left\{
\begin{matrix}
z & \leftrightarrow  &  z^* \\
|u\rangle & \leftrightarrow &   \langle u | \\
A & \leftrightarrow & A^{\dagger}
\end{matrix}
\right. \hspace{5cm}
$$
<br>

+++ {"slideshow": {"slide_type": "skip"}}

y hay <b>dos reglas más</b> que permiten aplicar $\dagger$ a sumas y productos de <i> objetos </i> $a \in\{z,\ket{u},A\}$
<br>

- *linealidad* $( a + b)^\dagger = a^\dagger + b^\dagger $
<br>

- *trasposición* $(ab)^\dagger = b^\dagger a^\dagger$ (sólo relevante cuando $a$ y $b$ no sean C-números que conmutan)
<br>

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} **Ejemplos**
:class: tip


1. $\ket{v} = A\ket{u} ~~~~\Leftrightarrow ~~~~\bra{v} = \bra{u}A^\dagger
~~$ donde el operador en la derecha actúa sobre el *bra* a su izquierda.
Notar que, como $\ket{v}^\dagger=\ket{Au}^\dagger = \bra{Au}$ la ecuación anterior implica

$$
\bra{Au} = \bra{u} A^\dagger
$$

2. $\bra{w}A\ket{u}^* = \big(\bra{w}A\ket{u}\big)^\dagger = \bra{u}A^\dagger\ket{w}$
:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Matriz adjunta

Estas reglas nos permiten obtener el adjunto de un operador


<br>


$$
A^\dagger = \sum_{ij}\left( A_{ij}\ketbra{i}{j}\right)^\dagger = \sum_{ij} \, \ketbra{j}{i}A_{ij}^* =  \sum_{ji} \, A_{ji}^*\ketbra{i}{j}
$$

donde en la última ecuación hemos hecho un simple intercambio de etiquetas $i\leftrightarrow j$
<br>
<br>

+++ {"slideshow": {"slide_type": "skip"}}

Vemos que la matriz que representa $A^\dagger$ es la *matriz adjunta* de $A_{ij}$, es decir, la traspuesta y conjugada
<br>


$$
(A^\dagger)_{ij} = A^*_{ji} = (A^{*}_{ij})^t \equiv (A_{ij})^\dagger
$$

donde $^\dagger$ significa el adjunto de un operador a la izquierda, y de una matriz a la derecha.

```{code-cell} ipython3
A = np.array([[1,1+2j],[2+3j,3-1j]])
display(array_to_latex(A))

Aadj = A.T.conj()
display(array_to_latex(Aadj))
```

+++ {"slideshow": {"slide_type": "skip"}}

Si $\Hil$ tiene dimensión $N$, un *operador general* $A\in \Lin(\Hil)$ se especifica mediante una matriz de $N^2$ números complejos $\Rightarrow A = A_{ij}\ket{e_i}\bra{e_j}$. 

$N^2$ números complejos equivalen a $2N^2$ números reales. 

+++ {"slideshow": {"slide_type": "skip"}}

En otras palabras: $A$  tiene $N^2$ grados de libertad complejos y, por tanto, ésta es la dimension del espacio ${\rm L}(\Hil)$ es  
<br>

$$ {\rm dim}_{\bf C}(\Lin(\Hil)) = N^2 ~~~ \Longleftrightarrow ~~~ {\rm dim}_{\bf R}(\Lin(\Hil)) =  2N^2
$$
<br>

+++

## Clases de Operadores
<a id='classop'></a>

+++ {"slideshow": {"slide_type": "-"}}

Vamos a considerar **clases de operadores** que satisfagan algún tipo de *condición* o *restricción*

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Operador Unitario

+++

:::{card} 
**Definción**: *operador unitario*

^^^

Un <i>operador unitario</i> $U$ es tal que su <i>adjunto</i> es igual a su <i>inverso</i>


$$
U^\dagger = U^{-1}  \, 
$$
:::

+++ {"slideshow": {"slide_type": "fragment"}}

Naturalmente, esta ecuación se traduce en la misma ecuación para las matrices asociadas en *cualquier base*
<br>
<br>
$$
(U_{ij})^\dagger = U_{ji}^* = U^{-1}_{ij}
$$
<br>
Veamos ahora por qué hemos definido esta clase de operadores.

+++ {"slideshow": {"slide_type": "slide"}}

::::{card} 

**Teorema**

^^^

La acción de un operador unitario <i>preserva </i> el producto escalar de dos vectores cualesquiera. 

:::{dropdown} Demostración

Sea $U$ un operador unitario, y $\ket{\varphi'}=U\ket{\varphi}$ y $\ket{\psi'} = U\ket{\psi}$
dos vectores transformados por $U$, entonces

$$
\braket{\varphi'}{\psi'} = \left(\bra{\varphi}U^\dagger\right)U\ket{\psi} = \bra{\varphi} U^\dagger U \ket{\psi} = 
\braket{\varphi}{\psi}
$$

particularizando para $\ket{\varphi} = \ket{\psi}$ tenemos que un operador unitario *conserva la norma*.

$$
\|U \ket{\varphi}\| = \|\ket{\varphi}\|
$$
:::

+++ {"slideshow": {"slide_type": "skip"}}


- En particular, preserva  la <i>norma</i> de cualquier vector. 
<br>
Por tanto, conserva la <i>distancia</i> entre dos vectores $ d (\ket{v},\ket{w})= \| (\ket{v}-\ket{w}) \| $.<br>
En un lenguaje más formal, se dice que un operador unitario es una *isometría* 

+++ {"slideshow": {"slide_type": "fragment"}}

- La <i>combinación lineal</i> de operadores unitarios **no es** unitaria
<br>
<br>
$$
 (a U+ bV)^\dagger = a^* V^\dagger+ b^* U^\dagger = a^* V^{-1}+ b^* U^{-1} \neq  (a U+ b V)^{-1}
$$
<br>
Matemáticamente esto quiere decir que los operadores unitarios no forman un subespacio vectorial de $\Lin(\Hil)$

+++ {"slideshow": {"slide_type": "slide"}}

- La *composición* de  operadores unitarios  **sí es** unitaria
<br>
<br>
$$
(UV)^\dagger = V^\dagger U^\dagger = V^{-1}U^{-1} = (UV)^{-1} 
$$
<br>
Matemáticamente esto quiere decir que los operadores unitarios forman un <i>grupo</i>: el <i>grupo unitario</i> $U(d)$ actúa sobre $\Hil$ de dimensión $d$. 
    

+++ {"slideshow": {"slide_type": "skip"}}

- Aun así, forman una *variedad*: un conjunto continuo  que se puede parametrizar mediante una colección de parámetros, la *dimensión de la variedad*.
<br>
Como hay una relación 1 a 1 entre un operador una matriz (en una base), esa dimensión será igual a la *dimensión del conjunto de matrices unitarias* 


+++ {"slideshow": {"slide_type": "fragment"}}

:::{admonition} **Ejercicio** *(explícaselo a tu cuaderno)*
:class: tip
   
Resta de  ${\rm dim}_{\bf R}({\rm L}(\Hil)) =  2N^2$ el número de ecuaciones que restringen la matriz de un operador 
unitario y halla así la  dimensión (real) del grupo $U(N)$ de <i> operadores unitarios</i> de dimensión $N$.
:::

+++ {"slideshow": {"slide_type": "skip"}}

**Bases ortonormales**

- Como caso particular, aplicando un operador unitario $U$ a una base ortonormal $\{\ket{e_i}\}$ obtenemos otra base ortonormal $\{\ket{\tilde e_i}\}$
<br>

$$
\left. \begin{array}{c}\ket{\tilde e_i} = U\ket{e_i}\\ U^{-1} =  U^\dagger \end{array} \right\}
~~~~ \Longleftrightarrow ~~~~\braket{\tilde e_i}{\tilde e_j} = \bra{\tilde e_i}U^\dagger U\ket{\tilde e_j} = \braket{e_i}{e_j} = \delta_{ij}
$$

<br>

+++ {"slideshow": {"slide_type": "skip"}}

- Inversamente, dadas dos bases ortonormales, $\{\ket{e_i}\}$ y $\{\ket{\tilde e_i}\}$, el operador que las relaciona es un operador unitario
    
$$ 
 \begin{array}{rcl} 
U = \sum_i \ketbra{\tilde e_i}{e_i} & \Rightarrow &  U\ket{e_j} = \ket{\tilde e_j} 
 \\ \rule{0mm}{10mm}
U^\dagger = \sum_i \ketbra{e_i}{\tilde e_i}  & \Rightarrow &    U^\dagger\ket{\tilde e_j} = \ket{e_j} ~~~\Rightarrow ~~~U^\dagger = U^{-1}
 \end{array}
$$

+++ {"slideshow": {"slide_type": "skip"}}

- Un  <i>operador ortogonal</i> es un caso particular de operador  unitario con *elementos de matriz reales*. El operador de rotación $R(\theta)$ que hemos estudiado al comienzo de este tema es un operador ortogonal.
Efectivamente, dado
$$
R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}
$$
es inmediato comprobar que 

$$ R(\theta)^\dagger =R(\theta)^t = R(-\theta) = R(\theta)^{-1}$$
    

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
U=np.matrix([[1,1J],[1J, + 1]])/np.sqrt(2)
array_to_latex(U)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
Uadj=U.getH() # getH es un método de la clase matrix que devuelve la matriz conjugada hermítica
array_to_latex(Uadj)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
print('comprobamos que U es unitaria')

array_to_latex(np.dot(Uadj,U))
```

:::{card}
**Definición** *(operador normal)*

^^^

Un operador $N$  es <i>normal</i> si conmuta con su adjunto
   
$$
NN^\dagger = N^\dagger N
$$   
:::

+++

Los operadores normales tienen una propiedad extremadamente importante

:::{card}
**Teorema** 

^^^

Un operador $N\in \Lin(\Hil)$ es normal sí y sólo si, existe una base $\{\ket{i}\}\in \Hil$ en la cual la matriz $N_{ij}$ que representa dicho operador es diagonal

$$
N_{ij} = \bra{i}N\ket{j} =  \lambda_i \delta_{ij} = \begin{pmatrix} \lambda_1 & & & \\
& \lambda_2 & & \\ & & \ddots& \\ & & & \lambda_{N} \end{pmatrix}
$$

donde los números $\lambda_i$ son, en general, complejos.

:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Operador Hermítico

:::{card}

**Definción** (operador hermítico)

^^^

Un operador  $H$ es <i>Hermítico</i> (o <i>autoadjunto</i>)  si  verifica la siguiente ecuación 
  
$$
H = H^\dagger 
$$
:::

+++ {"slideshow": {"slide_type": "skip"}}


- Evidentemente, un *operador hermítico* $~\Rightarrow ~$ es un *operador normal*, pero a la inversa no tiene por qué ser verdad.

+++ {"slideshow": {"slide_type": "slide"}}

- La *combinación lineal* de operadores *hermíticos*  con coeficientes *reales* **es**  *hermítica*
<br>
<br>
$$
C^\dagger = (a A + b B)^\dagger = a^* A^\dagger + b^* B^\dagger = aA + b B = C
$$
<br>
Matemáticamente: los operadores autoadjuntos forman un subespacio vectorial real $\hbox{Her}(\Hil) \subset \Lin(\Hil)$.

+++ {"slideshow": {"slide_type": "fragment"}}

- La composición de operadores hermíticos, en general **no es** hermítica
<br>
<br>
$$
(A B)^\dagger = B^\dagger A^\dagger = BA \neq AB
$$
<br>
Matemáticamente, esto implica que <i>no forman grupo</i> salvo que $A$ y $B$ conmuten entre sí, en cuyo caso forman un <i>grupo Abeliano</i>

+++ {"slideshow": {"slide_type": "skip"}}

- La matriz asociada a un operador hermítico también se llama hermítica, y coincide con su traspuesta y conjugada
<br>

$$
A_{ij} = A^\dagger_{ij} \equiv  A^{*t}_{ij} = A^*_{ji}   \hspace{4cm}
$$


+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

A partir de cualquier operador $C\neq C^\dagger $ siempre podemos construir un operador hermítico $H=H^\dagger$ mediante la combinación lineal  

$$
H = C + C^\dagger
$$

donde $a$ es un número real. Esto se extiende trivialmente a las matrices que los representan en cualquier base
    

$$
H_{ij} = C_{ij} + C_{ji}^*
$$ 
:::

+++ {"slideshow": {"slide_type": "fragment"}}

:::{card}

**Ejercicio**

^^^

Resta de  ${\rm dim}_{\bf R}({\rm L}(\Hil)) =  2N^2$ el número de ecuaciones que restringen la matriz de un operador hermítico y halla así la dimensión (real) de la  <i>subespacio vectorial de operadores hermíticos</i>. 
:::

+++ {"slideshow": {"slide_type": "skip"}}

Si has hecho los dos últimos ejercicios  habrás encontrado la misma respuesta en ambos. Eso quiere decir que podría haber una relación entre matrices hermíticas y unitarias. Veremos que es así cuando estudiemos funciones de operadores

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

<a id='opproyec'></a>
### Proyectores


El operador $P = \ketbra{u}{u}$ *proyecta* cualquier vector en la dirección de $\ket{u}$

$$
P \ket{w} = \ket{u}\braket{u}{w} = a \ket{u}
$$

donde el número $a = \braket{u}{w}$ es la *proyección* 

+++ {"slideshow": {"slide_type": "skip"}}

De su forma se siguen dos propiedades que caracterizan un operador de proyección 

- es hermítico 

$$
P^\dagger = (\ketbra{u}{u})^\dagger = \ketbra{u}{u} = P
$$

- es idempotente

$$
P^2 = \ket{u}\braket{u}{u}\bra{u} = \ketbra{u}{u} = P
$$

+++ {"slideshow": {"slide_type": "slide"}}

:::{card}

**Definition** *(operador hermítico)*

^^^

Un <i>proyector</i> es un operador hermítico que verifica la ecuación

$$
P^2 = P
$$
:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

El proyector es un operador <b>no-unitario</b>: la proyección <i>reduce</i> la norma.
Efectivamente,supongamos que $\ket{u}$ y $\ket{w}$ son vectores unitarios y distintos

$$
\| P\ket{w}\|^2 = \bra{w}P^\dagger P\ket{w} = \bra{w} P\ket{w}= \braket{w}{u}\braket{u}{w} = |\braket{u}{w}|^2 < \|\ket{u}\|\|\ket{w}\| = 1  
$$

donde hemos aplicado la <i>desigualdad de Cauchy Schwarz</i> estricta, al suponer que $\ket{u}\neq\ket{w}$.
:::

+++ {"slideshow": {"slide_type": "skip"}}

**Matriz asociada a un proyector**


- Si $\ket{u} = \ket{e_1}$ el operador $P_1 = \ket{e_1}\bra{e_1}$ proyecta cualquier vector a lo largo de $\ket{e_1}$. En forma matricial
\begin{equation}
 \ket{e_1}\bra{e_1} = \begin{pmatrix} 1 & 0 & ...& 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \\ \vdots\\ 0 \end{pmatrix} =
 \begin{pmatrix} 1 & 0 &  \cdots & 0 \\ 0 & 0  & \cdots & 0 \\ 
 \vdots & \vdots &\vdots & \vdots  \\
 0  & 0 & \cdots & 0\end{pmatrix}
\end{equation}
de modo que
\begin{equation}
\ket{e_1}\braket{e_1}{u} ~= ~\begin{pmatrix} 1 & 0 &  \cdots & 0 \\ 0 & 0  & \cdots & 0 \\ 
 \vdots & \vdots &\vdots & \vdots  \\
0  & 0 & \cdots & 0\end{pmatrix} \begin{pmatrix} u_1 \\ u_2 \\ \vdots \\ u_N \end{pmatrix}
 = \begin{pmatrix} u^1 \\ 0 \\ \vdots \\ 0 \end{pmatrix} = u^1 \ket{e_1}
\end{equation}
    

+++ {"slideshow": {"slide_type": "skip"}}

- Si $\ket{u} = \sum_i u^i\ket{e_i}$ es un vector unitario  $\|\ket{u}\|=1$, entonces el proyector a lo largo de $\ket{u}$ viene dado por

$$
P(u) = \ketbra{u}{u} = \sum_{i,j} u_i u^*_j \ketbra{e_i}{e_j}
$$

Es decir, le está asociada una matriz dada por $P_{ij}=u_iu^*_j$. Es trivial verificar que 

$$
P^2_{ik} = \sum_j P_{ij}P_{jk} = \sum_j u_i u^*_j u_j u^*_k = u_i\left(\sum_j u^*_j u_j\right) u_k = u_i u_k^* = P_{ik}
$$

como corresponde a un proyector.
    

+++ {"slideshow": {"slide_type": "slide"}}

**Proyector ortogonal**

+++ {"slideshow": {"slide_type": "-"}}


Sea $P = \ket{u}\bra{u}$ un proyector a lo largo de un vector $\ket{u}.~$
Entonces el operador $\Rightarrow  P_\perp = I - P$ verifica que

- es proyector 

$$~~ P_\perp^2 = P_\perp $$

- es perpendicular a $P$ 

\begin{eqnarray}
P_\perp P &=& (I - P) P = P - P^2 = P - P =  0 
\end{eqnarray} 
 
<br>


+++ {"slideshow": {"slide_type": "slide"}}

**En resumen:** 

- dado un vector $\ket{u}$, podemos descomponer cualquier  otro vector $\ket{\psi}$ en sus proyecciones paralela y perpendicular
<br>
$$
\ket{\psi} = ( P + P_\perp) \ket{\psi} = a \ket{u} + b \ket{u_\perp} 
$$
<br>
donde $a = \braket{u}{\psi}$ y  $b = \braket{u_\perp}{\psi}$
<br>
<br>

- $\ket{u_\perp}$ y  $\ket{u}$ son perpendiculares
<br>

- $\ket{u}$, $\ket{u_\perp}$  y $\ket{\psi}$, están en un mismo plano (ver figura)

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
d = 3

' generamos un vector aleatorio'
u = tQ.random_ket(d)
display(array_to_latex(u))

' obtenemos los proyectores paralelo y perpendicular'
P_par = tQ.ket_bra(u,u);
P_perp = np.identity(d) - P_par

display(array_to_latex(P_par))
display(array_to_latex(P_perp))
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---

' check properties P^2 = P, and orthogonality '
A = P_par@P_par - P_par
B = P_perp@P_perp - P_perp
C = P_par@P_perp

display(array_to_latex(A))


' obtain parallel and perpendicular components of another vector'
psi = tQ.random_ket(d)

psi_par = np.dot(P_par,psi)
psi_perp = np.dot(P_perp,psi)


print(np.round(tQ.braket(psi_par,psi_perp),4))
```

+++ {"slideshow": {"slide_type": "slide"}}

:::{admonition} **Ejercicio** (*reflector*)
:class: tip 

Dado un vector unitario $\ket{u}$, escribe el operador $R_u^{\perp}$ que <i>refleja la componente perpendicular</i> a $\ket{u}$ de cualquier  vector $\ket{\psi}$ el operador $R_{u}^{\|}$ que <i>refleja la componente paralela</i> a $\ket{u}$ de cualquier  vector $\ket{\psi}$ 
:::

+++ {"slideshow": {"slide_type": "skip"}}

**Proyectores sobre un subespacio**

Consideremos una base ortonormal $\{\ket{e_i}\}~,i=1,...,N $  de $\Hil$ y dividámosla en dos subconjuntos

$$
\{\ket{e_i}\},~ i=1,...,N_1 ~~~~~~~,~~~~~~~~\{\ket{e_{j+N_1}},~j=1,...,N_2   
$$

Cualquier vector admite una descomposición ortogonal 

\begin{eqnarray}
\ket{\psi} &~=~& \sum_{i=1}^N a_i \ket{e_i}   ~= ~ \sum_{i=1}^N a_i \ket{e_i} + \sum_{i=1}^{N_2} a_{i+N_1} \ket{e_{i+N_1}} ~\equiv ~ \ket{\psi_1} + \ket{\psi_2}\rule{0mm}{5mm}
\end{eqnarray}

con $\braket{\psi_1}{\psi_2} = 0$. 

+++ {"slideshow": {"slide_type": "skip"}}

Decimos que el espacio $\Hil$ se descompone en la *suma directa de subespacios ortogonales*

$$
\Hil = \Hil_1 \oplus \Hil_2 
$$

de dimensiones $N_1 + N_2 = N$,

+++ {"slideshow": {"slide_type": "skip"}}

Los operadores 

$$
P_1 = \sum_{i=1}^{N_1} \ket{e_i}\bra{e_i} ~~~~~~~,~~~~~~~~ P_2 = \sum_{i=1}^{N_2} \ket{e_{i+N_1}}\bra{e_{i+N_1}}
= I - P_1
$$

Verifican la ecuación que define un proyector

$$
P_1^2 = P_1~~~~~,~~~~P_2^2 = P_2
$$

+++ {"slideshow": {"slide_type": "skip"}}

Su acción extrae de un vector su componente en el subespacio asociado

$$
P_1 \ket{\psi} ~=~ \sum_{i=1}^{N_1} \ket{e_i}\bra{e_i} \left(\sum_{k=1}^N a_k \ket{u_k} \right) ~=~
\sum_{i=1}^{N_1} a_i \ket{e_i} ~=~ \ket{\psi_1}\in Hil_1
$$

$$
P_2 \ket{\psi} ~=~ \sum_{i=1}^{N_2} \ket{e_{i+N_1}}\bra{e_{i+N_1}} \left(\sum_{k=1}^N a_k \ket{u_k} \right) ~=~
\sum_{i=1}^{N_1} a_{i+N_1} \ket{e_{i+N_1}} ~=~ \ket{\psi_2}\in Hil_2
$$

+++ {"slideshow": {"slide_type": "skip"}}

Claramente verifican

$$
(P_1 + P_2)\ket{\psi} = \ket{\psi}
$$

En resumen, vemos que satisfacen 

$$
P_1 P_2 = P_2 P_1  = 0 ~~~,~~~~P_1 + P_2 = I
$$

+++ {"slideshow": {"slide_type": "skip"}}

**Notar**: que $P_1 \neq P_v = \ketbra{v}{v}$ donde $\ket{v} = \sum_i \ket{i}$. Este operador proyectaría cualquier vector *siempre* en la dirección de $\ket{v}$.

+++ {"slideshow": {"slide_type": "skip"}}

## Autovalores y autovectores
       

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Valores y vectores propios

:::{card}

**Definición** (*autovalores y autovectores*)

^^^

Existen vectores, $\ket{\lambda}$ para los cuales la <i>la acción de un operador</i> $A$ devuelve un vector <i>paralelo</i> al original

$$
A\ket{\lambda} = \lambda \ket{\lambda}\, 
$$
    
Decimos que $\ket{\lambda}$ es un vector propio (o autovector) de $A$ con valor propio (o autovalor) asociado $\lambda\in {\mathbb C}$ 
:::

+++ {"slideshow": {"slide_type": "skip"}}

Supongamos que $A$ tiene $d$ vectores propios con los que podemos formar un *base ortonormal* $\{\ket{\lambda_i}\}$
tal que

$$
\ket{\lambda_j} = \sum_i U_{ij}\ket{e_i}, 
$$
Claramente $U_{ij}$ es la matriz unitaria formada por las componentes de los vectores propios (apilados por columnas)

::::{card}
**Lema**

^^^

La matriz $U$ es la matriz que diagonaliza $A$

$$
A_{diag} = \begin{pmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_d \end{pmatrix} = U^\dagger A U
$$

:::{dropdown} Demostración
\begin{eqnarray}
(A_{diag})_{ij} &\equiv& \bra{\lambda_i}A\ket{\lambda_j} \\
&=& \big(\sum_k\bra{e_k}U_{ki}^*\big)  A \sum_l\big( U_{lj}\ket{e_l}) \\
&=& \sum_{k,l} U_{ki}^* \bra{e_k} A\ket{e_l}    U_{lj}\\
&=& \sum_{k,l} U^\dagger_{ik} A_{kl} U_{lj} \\
&=& (U^\dagger A U)_{ij}
\end{eqnarray}
:::
::::

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
A = np.matrix([[1, -1], [1, 1]])

' hallamos los autovalores y autovectores'
eigvals, eigvecs = np.linalg.eig(A)
print('valprop =',eigvals)
#print('vecprop =',eigvecs)
array_to_latex(eigvecs)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
'verificamos que los autovectores son las columnas de v'

#m=0
m=1
array_to_latex(np.dot(A, eigvecs[:, m]) - eigvals[m] * eigvecs[:, m],prefix=r'A|\lambda_m \rangle -\lambda_m |\lambda_m\rangle =  ')
```

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
' diagonalizamos A '
U = np.matrix(eigvecs);

array_to_latex(np.dot(U.getH(),np.dot(A,U)),prefix='A_{diag} = U^\dagger A U = ')
```

+++ {"slideshow": {"slide_type": "skip"}}

### Autovalores degenerados: subespacios propios 

+++ {"slideshow": {"slide_type": "skip"}}

:::{card} 

**Definición:**

^^^

Decimos que un autovalor $\lambda$ es $d$ <i>veces degenerado</i> si existen $d$ autovectores linealmente independientes,  $\ket{\lambda^{a}}$ con $a=1,...,d$ asociados al **mismo** autovalor, es decir:

$$
A\ket{\lambda^a} = \lambda \ket{\lambda^a}
$$ 

:::

+++ {"slideshow": {"slide_type": "skip"}}

Sea $\ket{u} = \sum_{a=1}^{d} c_a\ket{\lambda^a} $ una combinación de dichos vectores propios, entonces
<br>
<br>
\begin{eqnarray}
A \ket{u} 
=  \sum_{a=1}^{d} c_a A\ket{\lambda^a}  =  \sum_{a=1}^{d} c_a \lambda\ket{\lambda^a}  =   \lambda \sum_{a=1}^{d} c_a \ket{\lambda^a}  =\lambda\ket{u}
\end{eqnarray}
<br>
Por tanto $\ket{u}$ es también vector propio con idéntico autovalor. Matemáticamente esto quiere decir que los autovectores asociados a un autovalor $d$ veces degenerado generan un <i>subespacio vectorial propio</i> $\Hil_\lambda\subset \Hil$. 


+++ {"slideshow": {"slide_type": "skip"}}

- El teorema de Gramm-Schmidt garantiza que podemos elegir (mediante un cambio adecuado) el conjunto $\{\ket{\lambda^a}\}\in (\lambda), a=1,...,d$ de forma que que sea una  <i>base ortonormal</i> 

$$\braket{\lambda^a}{\lambda^b}=\delta_{ab}$$

+++ {"slideshow": {"slide_type": "skip"}}

- El **proyector ortogonal** sobre el subespacio propio $\Hil_\lambda$ será la suma de proyectores sobre cada autovector propio

$$
P = \sum_{a=1}^{d} \ketbra{\lambda^a}{\lambda^a}
$$

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejemplo
:class: tip

Llamemos $R_z(\theta)$ el operador que efectúa una rotación  en el plano  $(x,y)$ de ángulo $\theta$. Cuando $\theta = \pi$ encontramos las siguiente acción sobre los tres elementos $\{\hat{\bf x},\hat{\bf y},\hat{\bf z}\}$
de la base cartesiana

\begin{eqnarray}
R_z(\pi)\hat{\bf x} &=&-\hat{\bf x}  \\ \rule{0mm}{6mm}
R_z(\pi)\hat{\bf y} &=& -\hat{\bf y}  \\ \rule{0mm}{6mm}
R_z(\pi)\hat{\bf z} &=& + \hat{\bf z}  
\end{eqnarray}    
 
Vemos que hay un autovector $\hat{\bf z}$ con autovalor $+1$ y dos autovectores $\hat{\bf x} $ y $\hat{\bf y} $
con autovalor $-1$. 

El espacio ${\mathbb R}^3$ se divide en dos subespacios propios de $R_z(\pi)$, uno de dimensión 1 (a lo largo del eje $\hat{\bf z}$) y otro de dimensión 2 (en el plano $(\hat{\bf x},\hat{\bf y})$).

Los proyectores asociados serán
   
$$
P_{\hat{\bf z}}= \ket{\hat{\bf z}}\bra{\hat{\bf z}}=\begin{bmatrix} 0 & & \\ & 0 & \\ & & 1 \end{bmatrix}~~~,~~~
P_{\hat{\bf x}\hat{\bf y}}= \ket{\hat{\bf x}}\bra{\hat{\bf x}}+\ket{\hat{\bf y}}\bra{\hat{\bf y}}=\begin{bmatrix} 1 & & \\ & 1 & \\ & & 0 \end{bmatrix}~~~,~~~
$$

:::

+++ {"slideshow": {"slide_type": "skip"}}

### Espectro de Operadores Normales


+++ {"slideshow": {"slide_type": "skip"}}

Recordemos la definición de un operador normal. $N$ será un operador normal si conmuta con su adjunto

$$
NN^\dagger = N^\dagger N
$$

La importancia de los operadores normales radica en el siguiente lema     

+++ {"slideshow": {"slide_type": "skip"}}

::::{card} 

**Teorema**

^^^

Un operador es normal si y sólo si es diagonalizable

Dos autovectores de un operador normal asociados a dos autovalores <i>distintos</i>  son <i>ortogonales</i>

$$
\lambda_i\neq \lambda_j~~~~\Longleftrightarrow ~~~~ \braket{\lambda_i}{\lambda_j} = 0
$$

:::{dropdown} Desmostración

De la ecuación de autovalores $N\ket{\lambda_j} =  \lambda_j \ket{\lambda_j}$, y de $NN^\dagger = N^\dagger N$, se sigue que

$$
\bra{\lambda_j}(N^\dagger - \lambda_j^*)(N - \lambda_j) \ket{\lambda_j} = \bra{\lambda_j}(N - \lambda_j)(N^\dagger - \lambda_j^*) \ket{\lambda_j}  = 0\,
$$

de donde obtenemos $(N^\dagger - \lambda_j^*) \ket{\lambda_j} = 0 \Rightarrow \bra{\lambda_j} N = \bra{\lambda_j}\lambda_j$. Entonces

$$
\bra{\lambda_j}N\ket{\lambda_i} = \lambda_j \braket{\lambda_j}{\lambda_i} = \lambda_i \braket{\lambda_j}{\lambda_i} \, ,
$$

de donde se sigue que, para $\lambda_i \neq \lambda_j \Rightarrow \braket{\lambda_i}{\lambda_j} = 0$. 

:::
::::

+++ {"slideshow": {"slide_type": "skip"}}

En general, cada autovalor $\lambda_k$ será $d_k \geq 1$ veces degenerado. 

En ese caso hay  $\{\ket{\lambda^a_k}\}, a=1,...,d_k$ autovectores que generan el subespacio propio, $\Hil_{\lambda_k}\subset \Hil $, de dimensión $d_k$. 

Subespacios $\Hil_{\lambda_k}\perp \Hil_{\lambda_j}$ son ortogonales para $k\neq j$ según el teorema. 
<br>


+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Resumen
:class: attention

Siempre podemos encontrar una base  ortonormal de $\Hil$, formada por autovectores de un operador normal $N$

$$
I = \sum_k\sum_{a=1}^{d_k} \ket{\lambda^a_k}\bra{\lambda^a_k} ~~~~~~~~~~~;~~~~~~~~~ \braket{\lambda^a_j}{\lambda^b_k} = \delta_{ab}\delta_{jk}
$$

El proyector sobre el subespacio propio $\Hil_{\lambda_k}$ será

$$
P_k = \sum_{a=1}^{d_k} \ketbra{\lambda^a_k}{\lambda^a_k}
$$
:::

+++ {"slideshow": {"slide_type": "slide"}}

### Descomposición  espectral

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Teorema Espectral**

^^^
    
Para todo operador normal $N$, existe una base de  autovectores ortonormales,  $\{\ket{\lambda^a_k}\}$,  tales que 
$A$ admite la siguiente <b> descomposición espectral </b>

$$
N = \sum_{k=1}^d \lambda_k   P_k
$$
     
donde $d=  {\rm dim}(\Hil)$ y $P_k = \sum_{a=1}^{g_k} \ketbra{\lambda^a_k}{\lambda^a_k}$ es el proyector sobre el subespacio propio $\Hil_{\lambda_k}$ si $\lambda_k$ es $g_k$ veces degenerado.

:::

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
A = np.array([[1, 1], [-1, 1]])
array_to_latex(A)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
' Realizamos la descomposición espectral'
eigvals, eigvecs = np.linalg.eig(A)

eigvec0 = eigvecs[:,0]
P0 = tQ.ket_bra(eigvec0,eigvec0)
display(array_to_latex(P0,prefix='P_0='))

eigvec1 = eigvecs[:,1]
P1 = tQ.ket_bra(eigvec1,eigvec1)
display(array_to_latex(P1,prefix='P_1='))

'verificamos completitud'
array_to_latex(P0+P1,prefix='P_0 + P_1=')
```

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
' verificamos el teorema de descomposición espectral '
A_descomp_espect = eigvals[0]*P0+eigvals[1]*P1

array_to_latex(A_descomp_espect)
```

+++ {"slideshow": {"slide_type": "slide"}}

La matriz $A_{ij}$ que expresa $A$ en la base $\ket{\lambda_i}$ es diagonal 

$$
A_{ij} = \bra{\lambda^a_i} A\ket{\lambda^b_j} =  \lambda_k \delta_{kj} \delta_{ab} =\begin{bmatrix} \lambda_1 &  &  &  &  \\ & \ddots & & & \\ & & \lambda_2 & &  \\&  & & \ddots & \\  & & & &  \lambda_N \end{bmatrix}
$$
<br>
donde $\lambda_k$ aparecerá $d_k$ veces repetido.

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

El operador identidad tiene a cualquier vector por autovector $ I\ket{v} = \ket{v}$, con autovalores $\lambda_ i = 1$. Por tanto, en <b>cualquier base</b>, la matriz asociada a $I$ tiene la forma diagonal

$$
I_{ij} = \delta_{ij} = \begin{pmatrix} 1 &  &  &  \\ & 1 & &  \\ & & \ddots & \\ & & &  1 \end{pmatrix}
$$


- La descomposición espectral de $I$ no es otra que la <b>relación de completitud</b>, que es cierta *para cualquier base*, ya que todas las bases son bases de autoestados de $I$

$$
I ~=~ \sum_{i=1}^N \ketbra{\lambda_i}{\lambda_i} ~=~ \sum_{i=1}^N \ketbra{e_i}{e_i}
$$

:::

+++

:::{admonition} Ejercicio *(explícaselo a tu ordenador)*
:class: tip

Escribe una función en python, $spectral\_decomp$, que verifique si un operador $A$ es normal y, en caso afirmativo, devuelva las dos listas $\lambda_i$ y $P_i$ asociadas a la decomposición espectral  $A = \sum_i \lambda_i P_i$.   
:::

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Espectro de Operadores Hermíticos, Unitarios y Proyectores

Los operadores hermíticos, unitarios y proyectores, son casos particulares de operadores  normales. Por tanto son diagonalizables y sus autovectores, asociados a autovalores distintos, generan subespacios mútuamente ortogonales. 


Vamos a ver cómo los requisitos adicionales que definend operadores hermíticos, unitarios y proyectores, se traducen en propiedades particulares para sus espectros. 


+++


- **Espectro de Operadores Hermíticos**
<br>

>**Teorema**:  los autovalores de un operador hermíticos son reales $\lambda_i \in {\mathbb R}$.
<br>

<details>
<summary>
<p style="text-align:left"> >> <i>Prueba:</i></p>
</summary>
<br>
Tomemos un autovector normalizado de $A$, $\ket{\lambda}$ de autovalor $\lambda$.
<br>
<br>
$$
\lambda = \bra{\lambda}A\ket{\lambda} =  (\bra{\lambda}A^\dagger\ket{\lambda})^* = (\bra{\lambda}A\ket{\lambda})^*= \lambda^* .~~~
$$   
}

+++ {"slideshow": {"slide_type": "skip"}}

><b>Ejercicio:</b> *(explícaselo a tu ordenador)*
<br>
Escribe una función en python, $random\_hermitian$, que reciba un número entero $d$ y genere una matriz hermítica de esa dimensión. <br>    
Comprueba en distintos casos que el espectro es real. 
 

+++ {"slideshow": {"slide_type": "slide"}}

- **Espectro de Operadores Unitarios**


>**Teorema**: los autovalores de un operador unitario son fases puras
<br><br>
$$
U^\dagger = U^{-1} ~~~\Longleftrightarrow ~~~\lambda_i = e^{i\phi_i}
$$ 
</div>

<details>
<summary><p style="color:grey;text-align:left"> >> <i>Prueba</i> </p></summary>

aquí tu prueba
    
</details>


+++ {"slideshow": {"slide_type": "slide"}}

- **Espectro de Proyectores**

><b> Teorema: </b>
los autovalores de un proyector sólo pueden ser $~0~$ ó $~1~$
<br><br>
$$
P^2= P ~~~\Longleftrightarrow ~~~\lambda_i \in \{0,1\}
$$ 


<details>
<summary><p style="color:grey;text-align:left"> >> <i>Prueba</i> </p></summary>
La ecuación 
    
$$ P^2 = P ~~~~~\Rightarrow ~~~~~~~~ P^2 \ket{u} = P\ket{u} $$

sólo tiene dos soluciones consistentes 
    
$$
P\ket{u} = \ket{u}~~~~~~~\hbox{y} ~~~~~~~~~~P\ket{u} = 0
$$
</details>


+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Operadores que conmutan

Cuando dos operadores conmutan se dan ciertas propiedades algebraicas que son muy ventajosas. En cierto modo se parecen más a c-números. Veamos la primera.
 
::::{card}

**Teorema**

^^^

Dados dos operadores $A$ y $B$ que conmutan, [A,B] = 0, existe una base $\{\ket{\lambda_i}\}$ de autovalores simultáneos de ambos operadores, es decir 

$$
A = \lambda_i^A\ketbra{\lambda_i}{\lambda_i} ~~~~,~~~~~ B= \lambda_i^B\ketbra{\lambda_i}{\lambda_i} 
$$

:::{dropdown} Demostración

Supongamos que $A$ y $B$ conmutan. Entonces la acción de $A$ <i>estabiliza</i> los subespacios propios de $B$. 

Es decir, si $\ket{\lambda}$ es autoestado de $B$, entonces $B\ket{\lambda} = \ket{\mu}$ también es autoestado con idéntico autovalor. Se comprueba fácilmente

$$
A(B\ket{\lambda} ) = B(A\ket{\lambda}) = B(\lambda\ket{\lambda}) = \lambda (B\ket{\lambda})
$$

Por tanto $\ket{\lambda}$ y $B\ket{\lambda}$ pertenecen al <i>mismo subespacio propio</i>. Esto es lo que se entiende por <i>estabilizar el subespacio</i>. 


Si $\lambda$ es degenerado esto sólo asegura que $B\ket{\lambda} = \ket{\lambda'}$ pertenece al subespacio propio del mismo autovalor $\lambda$. 

Esto quiere decir que, dento de cada subespacio propio de $B$, podemos escoger la base que queramos. En particular podemos escoger una base que diagonalice $A$ dentro de dicho subespacio.     

:::
::::

+++ {"slideshow": {"slide_type": "skip"}}

En otras palabras, dos operadores que conmutan, son diagonalizables simultáneamente. 

Eso no implica que sus autovalores sean iguales. La matriz de cada uno en la base que diagonaliza ambos $\{\ket{\lambda_i}\}$ es
<br>

$$
A = \begin{bmatrix} \lambda^A_1 & & &  \\ & \lambda^A_2 & &   \\ & & \ddots &  \\ & & & \lambda^A_n 
\end{bmatrix}~~~~~~~,~~~~~~~~
B = \begin{bmatrix} \lambda^B_1 & & &  \\ & \lambda^B_2 & &   \\ & & \ddots &  \\ & & & \lambda^B_n 
\end{bmatrix}\, .
$$

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Descomposición Polar (DP)

:::{card}

**Teorema**

^^^

Todo operador $A\in \Lin(\Hil)$ admite la descomposición polar $A = UR$ donde $U$ es un operador unitario, y $R$ es un operador semi-definido positivo (sólo tiene autovalores positivos o cero) 
:::

+++ {"slideshow": {"slide_type": "skip"}}

- La descomposición polar es *única* y generaliza la representación polar de *números complejos* $z = r e^{i\phi}$ a *operadores*  $A = UR$
<br>

- El hecho de que $r\geq 0$ es la contrapartida a que $R$ sea semi-definida positiva. 
<br>

- El factor $e^{i\phi}$ es análogo al hecho de que un operador unitario, como veremos, sólo tiene autovalores que son fases puras. 

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
'''Método para construir una matriz unitaria arbitraria usando la descomposición polar'''
d = 3
A = np.matrix(np.random.rand(d,d)+ np.random.rand(d,d) * 1j)

#u, s, vh = linalg.svd(A, full_matrices=False)
u,r = la.polar(A)
    
R = np.matrix(r) 
' verificamos que R sólo tiene autovalores no-negativos '
Reigval, Reigvec = la.eig(R)
print(np.round(Reigval,3))

U=np.matrix(u) 
display(array_to_latex(U,prefix='U='))

''' Verifiquemos unitariedad '''
display(array_to_latex(np.dot(U.getH(),U),prefix='U^\dagger U='))

''' verificamos que los autovalores de U tienen norma unidad'''
np.round([la.norm(la.eig(U)[0][i]) for i in range(d)],5)
```

+++ {"slideshow": {"slide_type": "slide"}}

### Descomposición en Valores Singulares (SVD)

+++ {"slideshow": {"slide_type": "skip"}}

Vamos a enunciar este teorema para matrices. Concretamente el teorema habla de una matriz $m\times n$. Este tipo de matrices se corresponden con operadores $O \in \Lin(\Hil_A,\Hil_B)$ entre espacios de dimensiones $m$ y $n$.

+++

Sea $A\in \Lin(\Hil)$ un operador arbitrario. Podemos formar otro operador $A^\dagger A$ 

::::{card}

**Lema**

^^^


Los autovalores de $A^\dagger A$ son realess, $\lambda_i\in {\mathbb R}$,  y no-negativos $\lambda_i\geq 0$

:::{dropdown} Desmostración

Claramente $A^\dagger A$ es un operador hermítico $(A^\dagger A)^\dagger = A^\dagger A$, así que sus autovalores son reales $\lambda_i \in {\mathbb R}$. 

Además es definido semi-positivo. Es decir, para todo $\ket{v}\in \Hil$

$$
\bra{v}(A^\dagger A) \ket{v} = \| A\ket{v}\|^2 \geq 0 
$$

donde la desigualdad de satura si y sólo si $A\ket{v} = 0$. Por tanto todos los autovalores deben ser positivos o cero $\lambda_i \geq 0$
    
:::
::::

+++

Al ser no-negativos, los autovalores $\lambda_i$ admiten una raíz cuadrada. Los que no son nulos tienen una importancia especial, y por eso se merecen un nombre 

>**Definición**: los números $\sigma_i = \sqrt{\lambda_i} > 0$ se denominan <b>valores singulares</b> de $A$, donde $\lambda_i>0$ son los autovalores no-nulos de $A^\dagger A$.

+++ {"slideshow": {"slide_type": "-"}}

><b> Teorema:</b>$~$
Sea $A$ una matriz compleja $m\times n$. Entonces  admite la siguiente <b>descomposición en valores singulares</b>
<br>
<br>
$$
A = U\,\Sigma\, V^{\dagger} \, ,
$$
<br>
donde $U\in U(m)$, $V\in U(n)$ son matrices unitarias cuadradas y $\,\Sigma \,$ es una matriz rectangular $m\times n$ con $\sigma_1, ...,\sigma_r$ <i>valores singulares</i> reales y positivos   en la diagonal, donde $r\leq {\rm min}(m,n)$. 
    

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
A = np.random.randn(3,2)+ 1j*np.random.randn(3,2)
display(array_to_latex(A,prefix='A='))
print( 'the shape of A is :', A.shape)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
U, sig, Vadj = la.svd(A, full_matrices=True)
m = U.shape[0]
n = Vadj.shape[0]

V = Vadj.T.conj()
Sigma = np.zeros([m,n])
for i in range(min(m,n)):
    Sigma[i,i]=s[i]

    
display(array_to_latex(U,prefix='U='))
display(array_to_latex(Sigma,prefix='\Sigma='))
display(array_to_latex(V,prefix='V='))

'''Verifiquemos unitariedad'''
display(array_to_latex(np.dot(U.T.conj(),U),prefix='U^{\dagger}U ='))
display(array_to_latex(np.dot(V.T.conj(),V),prefix='V^{\dagger}V ='))

```

```{code-cell} ipython3
(sig1, V) = la.eigh(np.dot(A.T.conj(),A))

print(sig1)
array_to_latex(V, prefix='H=')
```

```{code-cell} ipython3
(sig2, U) = la.eigh(np.dot(A,A.T.conj()))

print(sig2)
array_to_latex(U, prefix='U=')
```

No acaba de salir $U$

+++ {"slideshow": {"slide_type": "skip"}}

## Traza de un operador

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "slide"}}

### Definición de traza de un operador

><b> Definición:</b> la traza de un operador $A$ se define como la suma de elementos diagonales de su matriz
<br>
<br>    
$$
\tr A = \sum_ i \bra{e_i} A\ket{e_i} =  \sum_{i} A_{ii} 
$$
<br>
de sus elementos de matriz diagonales <u> en cualquier base </u>        


+++ {"slideshow": {"slide_type": "slide"}}

Para ser consistente esta definición es necesario probar que se puede calcular en cualquier base

><b> Lema:</b> la traza de un operador es <i>independiente de la base</i> en la que se calcule
</div>  

<details>
<summary> >> <i>Prueba</i> </summary>
\begin{eqnarray} Sean $\{\ket{i}\}$ y $\{\ket{\tilde i}\}$ dos bases cualesquiera. Entonces
{\rm tr} A  &=&\sum_i A_{ii} =\sum_{i} \bra{i}A\ket{i} =\sum_{i} \bra{i}A\left( \sum_j\ketbra{\tilde j}{\tilde j}\right)\ket{i}
\nonumber\\
&=& \sum_{ij}\bra{i}A\ket{\tilde j} \braket{\tilde j}{i} = \sum_{ij}\braket{\tilde j}{i}\bra{i}A\ket{\tilde j}  \nonumber\\
&=& \sum_{j} \bra{\tilde j}\left(\sum_i\ketbra{i}{i}\right) A \ket{\tilde j}= \sum_{j} \bra{\tilde j}A\ket{\tilde j}\nonumber\\
&=& \sum_j \tilde A_{jj}
\end{eqnarray}
</details>

+++ {"slideshow": {"slide_type": "slide"}}

- Si $A$ es diagonalizable, la traza es la suma de sus autovalores. En efecto, si $\ket{\lambda_i}$ es la base de autoestados 
<br>
<br>
$$
A\ket{\lambda_j} = \lambda_i \ket{\lambda_i}
$$ 
<br>
entonces
<br>
$$
{\rm tr} A = \sum_i \bra{\lambda_i}A\ket{\lambda_i} = \sum_i \lambda_i
$$

+++ {"slideshow": {"slide_type": "skip"}}

- La traza es una operación *lineal*
<br>
<br>
$$
{\rm tr} (A + B ) = {\rm tr}A + {\rm tr}B
$$

+++ {"slideshow": {"slide_type": "slide"}}

- La traza de un producto de operadores tiene la propiedad de *cíclicidad*: es invariante bajo permutaciones  cíclicas de los operadores en su argumento. Por ejemplo, para tres operadores $A, B$ y $C$
<br>
$$
{\rm tr}(ABC)= {\rm tr}(BCA) 
$$

<details>
<summary> >> <i>Prueba</i> </summary>
\begin{eqnarray} 
    {\rm tr}(ABC)&=&\sum_i (ABC)_{ii} =  \sum_{ijk} A_{ij}B_{jk}C_{ki}\\
    &=& \sum_{ijk} B_{jk}C_{ki}A_{ij} = \sum_j (BCA)_{jj}\\
    &=&  {\rm tr}(BCA)
\end{eqnarray}
</details>

Para un producto de dos operadores, el anterior resultado implica que la *traza de un conmutador es cero*. Dicho de otra forma

$$
{\rm tr}(AB) = {\rm tr}(BA) ~~~\Rightarrow ~~~~{\rm tr}([A,B]) = 0 \, .
$$

+++ {"slideshow": {"slide_type": "fragment"}}

- Sea el operador *producto externo* de dos vectores $A = \ketbra{u}{v}$. Entonces 

$$
\tr \left(\rule{0mm}{5mm}\ketbra{u}{v}\right)  = \braket{v}{u}
$$


<details>
<summary> >> <i>Prueba</i> </summary>
$$ \tr \left(\rule{0mm}{5mm}\ketbra{u}{v}\right) = \sum_i \braket{e_i}{u}\braket{v}{e_i} = \bra{v}\left(\sum_i \ketbra{e_i}{e_i}\right) \ket{u} = \braket{v}{u}
$$
</details>   

+++ {"slideshow": {"slide_type": "slide"}}

### $\Lin(\Hil)$ como un espacio de Hilbert

+++ {"slideshow": {"slide_type": "-"}}

Para transformar $\Lin(\Hil)$ en un espacio de Hilbert sólo es necesario definir un *producto escalar hermítico* entre dos elementos 

><b> Definición: </b> <i> (producto escalar) </i> 
<br>     
dados dos operadores lineales,  $A, B \in \Lin(\Hil)$  definimos su <i> producto escalar </i>  $( A, B)\in {\mathbb C}$
<br> 
<br>
$$
( A, B) \equiv {\rm tr}\left( A^\dagger B \right) 
$$

+++ {"slideshow": {"slide_type": "skip"}}

En una base tenemos que

$$
(A,B) = \sum_{ij} A^\dagger_{ij} B_{ji} = \sum_{ij} A^*_{ji} B_{ji}
$$

mientras que 

$$
(B,A) = \sum_{ij} B^\dagger_{ij} A_{ji} = \sum_{ij} B^*_{ji} A_{ji}
$$

Se sigue que  $(B,A) = (A,B)^*$. Además es trivial comprobar que  $(A,B+C) = (A,B) + (A,C)$, por lo que se trata de un *producto escalar hermítico*

+++ {"slideshow": {"slide_type": "slide"}}

### $\Lin(\Hil)$ como un espacio normado

+++

Una **norma** definida sobre $\Lin(\Hil)  $es un una función real $ A\to  \| A\| \in {\mathbb R}$ con las propiedades 
que se han definido en una [sección anterior](../00_Formalismo/01_Vectores.ipynb#norm)

+++

><b> Definición: </b> <i> ($p$-norma Shatten) </i> : dado un operador $A\in \Lin(\Hil)$ la función  
<br> 
$$
\| A \|_p =  \left({\rm tr} \left(A^\dagger A\right)^{p/2} \right)^{1/p}
$$
define una norma, denominada <b>$p$-norma de Shatten</b>.


+++ {"slideshow": {"slide_type": "skip"}}

 Ya hemos mencionado que el operador $A^\dagger A$ es un operador con propiedades importantes cuyos autovalores son los cuadrados de los valores principales $\lambda_i = \sigma_i^2$. Es decir, en la base diagonal
 $$
 A^\dagger A = \begin{pmatrix} \sigma_1^2 & & & & &  \\ & \ddots & & & \\ & & \sigma_r^2 & & & \\ & & & 0 & &\\ & & & & \ddots & \\ & & & & & 0 \end{pmatrix}
 $$

+++ {"slideshow": {"slide_type": "-"}}

Los tres casos más frecuentes son

- $p=1$ **norma de la traza** $~\Rightarrow ~  \| A \|_1 =  {\rm tr} \sqrt{A^\dagger A}$
<br>


Esta norma es igual a la suma de los valores singulares de $A ~\Rightarrow ~\| A \|_1  = \sum_i^r \sigma_i$

+++


- $p=2$ **norma de Frobenius** $~\Rightarrow ~ \| A \|_2 =  \sqrt{{ \rm tr} A^\dagger A }$
<br>

La norma de Frobenius es la que se obtiene a partir  del producto escalar $\|A\|_2 = (A,A)$

+++


- $p=\infty$ **norma espectral** $~\Rightarrow ~  \| A \|_\infty = \lim_{p\to \infty} \| A \|_p$

Puede demostrarse que la norma espectral es equivalente a la siguiente definición

$$
\|A\|_\infty = \hbox{max}_{\ket{u}\in \Hil}\{ \|A\ket{u}\| ~~\hbox{con} ~ \|\ket{u}\| = 1\}
$$

+++

><b>Ejercicio:</b>$~$*(explícaselo a tu ordenador)*
<br>
Escribe una función en python, $trace\_norm(A_{ij})$, que calcule la norma de la traza de un operador $A$ dado por una matriz $A_{ij}$.
</div>

+++ {"slideshow": {"slide_type": "slide"}}

### Distancia de traza

+++ {"slideshow": {"slide_type": "skip"}}

Cualquier norma permite definir una noción de *distancia* o *diferencia* entre dos operadores. 

+++ {"slideshow": {"slide_type": "-"}}

><b> Definición: </b> <i> (Distancia de traza) </i> 
<br>     
Se define la  <b> distancia de traza</b> entre dos operadores $A$ y $B$ como la <i>norma del operador diferencia</i>
<br> 
<br>
$$
d(A,B) = \| A - B \|_1 
$$
</div>

+++ {"slideshow": {"slide_type": "skip"}}

## Funciones de Operadores

+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### Funciones analíticas de operadores

Estamos acostumbrados a escribir funciones *de una variable real o compleja*. Por ejemplo $f(x)= x^2$, ó, $ f(z) = e^z$. 

Querríamos dar sentido a una función *de un operador* 
$
A \to f(A)
$

+++ {"slideshow": {"slide_type": "skip"}}

En el caso de que $f(z)$ sea una función analítica expresable como una serie de Taylor en torno a $x=0$ 

$$
f(z) = \sum_{n=0}^\infty \frac{1}{n!} f^{(n)}(0)\,  z^n
$$

tomaremos como **definición** la *misma serie* cambiando el argumento $x\to A$

$$
f(A) = \sum_{n=0}^\infty \frac{1}{n!} f^{(n)}(0)\,  A^n
$$


+++ {"slideshow": {"slide_type": "skip"}}

<b>Notar:</b> 
 $~$ de la misma forma que, para funciones analíticas $f(z)^* = f(z^*)$, también la definición anterior asegura que 
$f(A)^\dagger = f(A^\dagger)$



+++ {"jp-MarkdownHeadingCollapsed": true, "slideshow": {"slide_type": "skip"}}

### La exponenciación de un operador 

Sea $A\in \Lin(\Hil)$, definimos la exponencial $e^A$ mediante la serie de Taylor usual

$$
\exp(A) = e^A \equiv  I + A + \frac{1}{2} A^2 + \frac{1}{3!} A^3 + ...
$$

```{code-cell} ipython3
' para exponenciar matrices es recomendable la función expm de la libreria scipy.linalg'

from scipy.linalg import expm
from numpy.linalg import matrix_power
import math

A = 0.1*np.matrix([[2,3+1j],[2j,-1-2j]])

display(array_to_latex(np.around(expm(A),5)))

' podemos comparar con la serie de Taylor a tercer orden'
array_to_latex(np.round(matrix_power(A,0)  + matrix_power(A,1)  + 1./2.*matrix_power(A,2)  + 1./math.factorial(3)*matrix_power(A,3),5))
```

+++ {"slideshow": {"slide_type": "skip"}}

Una propiedad importante de la función exponencial es  $e^xe^y = e^{x+y}$. La propiedad análoga para operadores *sólo es cierta cuando conmutan entre sí*.  Para el caso genérico tenemos dos opciones

+++ {"slideshow": {"slide_type": "skip"}}

**Teorema de Baker-Campbel-Haussdorf**

><b> Teorema: </b> 
<br>
Sean $A,B\subset{\rm L}(\Hil)$ dos operadores lineales genéricos. Entonces
<br>
<br>
$$
e^A e^B = e^{\left({A+B + \frac{1}{2}[A,B] + \frac{1}{12}[A,[A,B]]+ \frac{1}{12}[B,[B,A]] + ...}\right)}
$$

+++ {"slideshow": {"slide_type": "skip"}}

Vemos que

-  Si $A$ y $B$ conmutan, 

$$[A,B]=0 ~\Leftrightarrow ~e^A e^B = e^{A+B}$$

+++ {"slideshow": {"slide_type": "skip"}}


-  Si el conmutador de $A$ y $B$  es un c-número 

$$[A,B]= c I  ~\Leftrightarrow ~  e^A e^B = e^{A+B + \frac{c}{2}}$$


+++ {"slideshow": {"slide_type": "skip"}}


-  El inverso de $e^A$ es $e^{-A}$.$~$ Efectivamente, como 

$$[A,A]=0 \Rightarrow e^A e^{-A} = e^{A-A} = e^0 = I$$

+++ {"slideshow": {"slide_type": "skip"}}

**Teorema de Lie-Suzuki-Trotter**

><b> Teorema: </b> 
<br>
Sean $A,B\subset{\rm L}(\Hil)$ dos operadores lineales genéricos. Entonces
<br>
<br>
$$
e^{A+B} = \lim_{n\to\infty} \left(e^{{A/n}} e^{B/n}\right)^n
$$

Esta segunda opción es de uso muy frecuente en el contexto de la *simulación cuántica*. 

+++ {"slideshow": {"slide_type": "skip"}}

**Relación entre operadores hermíticos y unitarios**

>**Teorema:** todo operador unitario $U$ se puede expresar como la exponencial imaginaria de un operador hermítico $H$
<br>
<br>
$$
U = e^{i H}
$$

Efectivamente, 

$$U^\dagger = \left(e^{i H}\right)^\dagger = e^{-i H^\dagger} = e^{-i H}=U^{-1}$$ 

por tanto, $U$ es unitario si y sólo si $H$ es hermítico.
<br>
<br>
<details>
<summary><p > >>$~$ <i>Detalles:</i> </p></summary>
\begin{eqnarray}
U^\dagger &=& \left( e^{iH}\right)^\dagger = \left( 1+ iH + \frac{1}{2}(i H)^2 + ...\right)^\dagger \\
&=& 1 - iH^\dagger  + \frac{1}{2}(-i)^2 (H^2)^\dagger + ... \\
&=& 1 - iH +\frac{1}{2} H^2 - ... \\
&=& e^{-iH}\\ \rule{0mm}{6mm}
&=& U^{-1}
\end{eqnarray}
</details>

+++ {"slideshow": {"slide_type": "slide"}}

### Funciones  generales 

+++ {"slideshow": {"slide_type": "skip"}}

No siempre $f(z)$ admite una expansión en serie de Taylor. Por ejemplo $f(z) = \exp(1/z)$ en torno a $z=0$ no es analítica.

En estos casos, el operador $f(A)$ existe, pero para construirlo es necesario recurrir a la *forma diagonalizada*

+++ {"slideshow": {"slide_type": "-"}}


><b> Teorema: </b> $~$   Sea $A$ un operador diagonalizable, y sea $A= \sum_i \lambda_i \ket{\lambda_i}\bra{\lambda_i}$ su representación espectral. 
<br>
Entonces el operador $f(A)$ tiene la representación espectral siguiente
<br>    
$$
f(A) = \sum_i f(\lambda_i) \ket{\lambda_i}\bra{\lambda_i}
$$

En particular, la matriz asociada a $f(A)$ en la base $\{\ket{\lambda_i}\}$ que diagonaliza $A^{(D)}_{ij}$ 
es la diagonal de los elementos $f(\lambda_i)$ de los autovalores

$$
f(A^{(D)}_{ij}) = \begin{bmatrix} f(\lambda_1)& &  & \\ & f(\lambda_2) & &  \\ & & \ddots & \\ & & & f(\lambda_n)
\end{bmatrix}
$$

+++ {"slideshow": {"slide_type": "slide"}}

><b>Ejemplo 1:</b>    
$$f(A) = e^{1/A} = \sum_i e^{1/\lambda_i} \ket{\lambda_i}\bra{\lambda_i}$$


+++ {"slideshow": {"slide_type": "slide"}}

><b>Ejemplo 2:</b>    
\begin{eqnarray}
f(A) = {\rm tr}(A \log A) &=& {\rm tr}\left[\left(\sum_j \lambda_j \ket{\lambda_j}\bra{\lambda_j}\right)\left(\sum_k\log \lambda_k \ket{\lambda_k}\bra{\lambda_k}\right)\right] ~=~  {\rm tr}\left[\sum_k \lambda_k \log\lambda_k \ket{\lambda_k}\bra{\lambda_k} \right] \\ \rule{0mm}{20mm}
&=& {\rm tr} \begin{bmatrix} \lambda_1 \log \lambda_1& &  & \\ &\lambda_2 \log \lambda_2 & &  \\ & & \ddots & \\ & & & \lambda_n \log \lambda_n
\end{bmatrix}
 ~= ~ \sum_k \lambda_k \log \lambda_k \rule{0mm}{8mm}
\end{eqnarray}

+++ {"slideshow": {"slide_type": "slide"}}

## Matrices de Pauli


+++ {"slideshow": {"slide_type": "-"}}

><b> Definición: </b>  $~$ se definen las matrices de Pauli 
<br>
<br>
$$
\sigma_x = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}~~~~~,~~~~~~~~~
\sigma_y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}~~~~~,~~~~~~~~~
\sigma_z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \, .
$$

+++ {"slideshow": {"slide_type": "fragment"}}

- También se usan los subíndices enteros $\sigma_1=\sigma_x, ~
\sigma_2=\sigma_y$  y  $\sigma_3=\sigma_z$. 
<br>
<br>
- Una propiedad importantísima de las matrices de Pauli  es que son, a la vez,  <u>*hermíticas* y *unitarias*</u>.


+++ {"slideshow": {"slide_type": "slide"}}

**Composición de matrices de Pauli**

+++ {"slideshow": {"slide_type": "fragment"}}

Es inmediato verificar que se cumplen las siguientes relaciones


- si multiplicamos dos matrices de Pauli **iguales**

$$
\sigma_1\sigma_1 = \sigma_2\sigma_2 = \sigma_3\sigma_3 =   I
$$

- si multiplicamos dos matrices de Pauli **diferentes**

\begin{eqnarray}
\sigma_1\sigma_2 &=&  - \sigma_2\sigma_1 = i \sigma_3   \\
\sigma_2\sigma_3 &=&  -\sigma_3\sigma_2  = -i \sigma_1  \\
\sigma_3\sigma_1 &=& -\sigma_2\sigma_3 = -i \sigma_2   \\
\end{eqnarray}

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
I = np.eye(2)
s1 = np.matrix([[0,1],[1,0]])
s2 = np.matrix([[0,-1j],[1j,0]])
s3 = np.matrix([[1,0],[0,-1]])

'verifica todas las opciones'
print(s1*s1==I)
print(s1*s2==1j*s3)
print(s2*s1==-1j*s3)
'etc'
```

Todas estas *relaciones de composición* se pueden condensar en la siguiente ecuación algebráica
<br>

$$
\fbox{$\sigma_i \sigma_j = \delta_{ij}I + i\epsilon_{ijk}  \sigma_k$}
$$

donde hemos hecho uso del *símbolo antisimétrico*
$$\epsilon_{123} = \epsilon_{231}=\epsilon_{312}=1~~~~,~~~~\epsilon_{213} = \epsilon_{132}=\epsilon_{321}=-1$$

+++ {"slideshow": {"slide_type": "skip"}}

A partir de estas relaciones es inmediado ver que las matrices de Pauli verifican relaciones de conmutación 

    
$$
[\sigma_i,\sigma_j] ~=~ \sigma_i\sigma_j - \sigma_j\sigma_i ~=~ 2i\epsilon_{ijk}\sigma_k
$$

y de anticonmutación 

$$
\{\sigma_i,\sigma_j \} ~=~ \sigma_i\sigma_j + \sigma_j\sigma_i =  2\delta_{ij} ~~~~~
$$

+++ {"slideshow": {"slide_type": "skip"}}

Las matrices de Pauli tienen traza nula

$$
{\rm tr} \, \sigma_i = 0
$$

+++ {"slideshow": {"slide_type": "skip"}}

Tomando la traza de la relación de composición obtenemos que las matrices de Pauli <u>*son ortogonales*</u> 
en el sentido del producto escalar definido sobre $\Lin(\Hil)$
<br>

$$
(\sigma_i, \sigma_j) \equiv {\rm tr}(\sigma_i\sigma_j) = {\rm tr}(\delta_{ij}I + i\epsilon_{ijk}  \sigma_k) = 2\delta_{ij}
$$

+++ {"slideshow": {"slide_type": "slide"}}

Las matrices hermíticas de dimensión 2$\times$2 tienen cuatro grados de libertad reales. 

Si añadimos la matriz identidad $~I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}~
$  el conjunto $\{I,\sigma_x,\sigma_y,\sigma_z\}$ forma una *base* para el espacio de *matrices hermíticas* $2\times 2$.  

\begin{eqnarray}
A &=& a_0 I + {\bf a} \cdot \boldsymbol{\sigma} \\  \rule{0mm}{10mm} &=&  a_0 I + a_1 \sigma_1 + a_2 \sigma_2 + a_3 \sigma_3 \\ \rule{0mm}{10mm}&=& 
\begin{bmatrix}
a_0 + a_3 & a_1 - i a_2 \\ a_1 + i a_2 & a_0 - a_3
\end{bmatrix} = A^\dagger
\end{eqnarray}
con $a_i\in {\mathbb R}$ cuatro números reales.

+++ {"slideshow": {"slide_type": "slide"}}

Separemos el vector ${\bf a}$ en su módulo $a$, y su dirección unitaria $\hat{\bf n}$

$${\bf a} = (a_1,a_2,a_3) =a \left( \frac{a_1}{a},\frac{a_2}{a},\frac{a_3}{a}\right) =  a\, \hat{\bf n}$$ 

donde $a=|{\bf a}|=\sqrt{a_1^2+a_2^3+a_3^2}~$  y $\hat{\bf n}$ es unitario

+++ {"slideshow": {"slide_type": "fragment"}}


Entonces
<br>
$$
 {\bf a} \cdot \boldsymbol{\sigma} =  a\, \hat{\bf n} \cdot \boldsymbol{\sigma}
$$

es una matriz *hermítica*, que podemos exponenciar para formar una matriz *unitaria*. La sorpresa ahora, es que el resultado, vuelve a ser expresable en términos de las propias matrices de Pauli!

+++ {"slideshow": {"slide_type": "fragment"}}

><b> Teorema: </b>  $~$ 
$$
\fbox{$\exp \left( \rule{0mm}{4mm} i\,   {\bf a} \cdot \boldsymbol{\sigma}  \right) = (\cos a)\, I + i (\sin a)\,\hat{\bf n} \cdot  \boldsymbol{\sigma} $}
$$
<br>

+++ {"slideshow": {"slide_type": "skip"}}

Esta expresión, extremadamente útil,  generaliza la *fórmula de Euler*  para una fase compleja 

$$ \exp(i\alpha) =  \cos\alpha + i \sin\alpha $$
<br>

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
'verificamos la ecuación anterio numéricamente'
from scipy.linalg import expm

'generamos un vector aleatorio'
avec = np.random.rand(3)
a = np.linalg.norm(avec)
nvec = avec/a
print('a=',a)
display(array_to_latex(nvec))

sigvec = np.array([s1,s2,s3])

adots= sum(list(avec[i]*sigvec[i] for i in range(3)))

'exponentiating'
e1 = expm(1j*adots)

'using the Euler-like formula'
ndots= sum(list(nvec[i]*sigvec[i] for i in range(3)))
e2 = np.cos(a)*s0 + 1j*np.sin(a)*(nvec[0]*sigvec[0]+nvec[1]*sigvec[1]+nvec[2]*sigvec[2])

'verify'
display(array_to_latex(np.round(e1,4),prefix='e1='))
display(array_to_latex(np.round(e2,4),prefix='e1='))
```

+++ {"slideshow": {"slide_type": "skip"}}

><b> Ejercicio: </b> <br> 
Obtén la descomposición espectral de las tres matrices de Pauli, $\sigma_x, \sigma_y $ y $\sigma_z$. Utiliza esta descomposición para demostrar la expresión
<br>
<br>
$$
e^{i \alpha\,  \hat{\bf n}\cdot\boldsymbol{\sigma}} = \cos \alpha \, I + i \sin \alpha \, \hat{\bf n}\cdot\boldsymbol{\sigma}
$$
donde $\hat{\bf n} = (n_x, n_y,n_z)$ es un vector unitario.
</div>
