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

+++

```{figure} ../thumbnails/myThumbnail.png
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

# Tensores

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
%run ../macro_tQ.py

import sys
sys.path.append('../')
import macro_tQ as tQ

import numpy as np
import scipy.linalg as la
from IPython.display import display,Markdown,Latex
import matplotlib.pyplot as plt
from qiskit.tools.visualization import array_to_latex
```

+++ {"slideshow": {"slide_type": "slide"}}

## Producto Tensorial

+++ {"slideshow": {"slide_type": "skip"}}

En física clásica a cada *grado de libertad* se le asocia una variable real o compleja. En Mecánica Cuántica, se le asocia un vector en un espacio de Hilbert. 

Los sistemas físicos, en general, tienen más de un grado de libertad. En física clásica les asociamos funciones multi-variable. En Mecánica Cuántica la estructura matemática adecuada es el **producto tensorial** de espacios vectoriales.

+++ {"slideshow": {"slide_type": "skip"}}

:::{card}

**Definición**

^^^

Sean $\Hil_1$ y $\Hil_2$ dos espacios de Hilbert.  Dados dos vectores $\ket{u}_1\in \Hil_1$ y  $\ket{v}_2\in \Hil_2$, denominamos <i>producto tensorial</i> al par ordenado

$$
\ket{uv} ~\equiv \ket{u}_1\otimes \ket{v}_2
$$

:::

+++ {"slideshow": {"slide_type": "skip"}}

Como si se tratara de un producto ordinario, el producto tensorial satisface la **propiedad distributiva**
<br>
<br>
\begin{eqnarray}
\big(\ket{u}+\ket{v}\big)\otimes \big(\ket{y}+\ket{z}\big) ~&= ~~
\ket{u}\otimes\ket{y} ~+~ \ket{u}\otimes\ket{z} ~+~ \ket{v}\otimes\ket{y} ~+~~
 \ket{v}\otimes\ket{z} \\
 \rule{0mm}{8mm}
 &= ~~ \ket{uy} + \ket{uz} + \ket{vy} + \ket{vz}
\end{eqnarray}

+++

Este cálculo tan inocente esconde un hecho crucial: los elementos $\big(\ket{u}+\ket{v}\big)\otimes \big(\ket{y}+\ket{z}\big)$ y $\big(\ket{u}\otimes\ket{y}+ \ket{u}\otimes\ket{z}\big)$ son <u>diferentes</u>. 

 Es por esto que, para dotar de estructura de espacio vectorial al conjunto de productos tensoriales <u>de forma consistente con la distributividad</u>,  debamos incluir todas las posibles combinaciones como elementos independientes

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Definición**

^^^

Sean $V_1$ y $V_2$ dos espacios vectorieles. El  <b>espacio producto tensorial</b>  $V = V_1 \otimes V_2$ está formado por  <u>todas las combinaciones lineales</u> posibles de   <u>pares ordenados</u> 

$$
\ket{s}= a\ket{u}_1\otimes\ket{u}_2 ~+~ b \ket{v}_1\otimes\ket{v}_2 ~+ ~...
$$
  
donde  $\ket{u}_1,\ket{v}_1,...\in V_1\, ~$ y $~\, \ket{u}_2,\ket{v}_2,...\in V_2~$,
    y $~a,b,... \in {\mathbb C}$ son coeficientes complejos.

:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note
    
- Prescindiremos del subíndice $\ket{u}_1\otimes \ket{y}_2=\ket{u}\otimes \ket{y} \equiv \ket{uy}$ que estará implícito en el orden. 
<br>       
- Para computación cuántica con <i>cúbits (cúdits)</i>, el valor relevante es $d=2\,(d\geq 3)$. 
<br>
- En adelante supondremos que los espacios vectoriales $V_{1,2} = \Hil_{1,2}$ son espacios de Hilbert

:::

+++ {"slideshow": {"slide_type": "slide"}}

### Base y Dimensión

+++ {"slideshow": {"slide_type": "-"}}

- Sea $\ket{i_1}$ una base de $\Hil_1$ y $\ket{i_2}$ una base de $\Hil_2$. Entonces, una base de $\Hil_1\otimes \Hil_2$ se obtiene
a partir de *todos* los emparejamientos 
<br>
<br>
$$
\ket{i_1 i_2} = \ket{i_1}\otimes \ket{i_2}~~~~~~~~~~~~~~~~~~ 
$$
<br>
con
$
i_1=0....d_1-1$ y $i_2=0,...,d_2-1
$

+++ {"slideshow": {"slide_type": "-"}}

-  El número parejas posibles es $d_1d_2$, que coincide con la **dimensión** de $\Hil_1\otimes \Hil_2$.

+++ {"slideshow": {"slide_type": "slide"}}

- Vemos que las etiquetas de los vectores de la base forman un *bi-índice* $\to i_1 i_2$ que asume $d_1 d_2$ parejas de valores distintos  

+++ {"slideshow": {"slide_type": "-"}}

- Un *vector* se escribirá igualmente usando $d_1 d_2$ <i>componentes</i> complejas $w_{i_1 i_2}$, etiquetadas mediante un bi-índice en lugar de un índice
<br>
<br>
\begin{eqnarray}
\ket{\omega} & ~= ~& 
w_{00}\ket{00} + w_{01}\ket{01} + ... + w_{10}\ket{10} + ...\ldots + w_{d_1 d_2}\ket{d_1 d_2} \nonumber\\
\rule{0mm}{10mm}
&~=~& \sum_{i_1=0}^{d_1-1}\sum_{i_2=0}^{d_2-1} w_{i_1i_2} \ket{i_1 i_2} 
\end{eqnarray}

+++ {"slideshow": {"slide_type": "slide"}}

### Indexación equivalente

Podemos etiquetar las componentes (o los elementos de la base) con índices, en lugar de bi-índices

Para ello basta con definir un mapa  entre dos bi-índices $i_1,i_2$ y un índice $a$ 

$$
\ket{w} ~= ~ \sum_{i_1=0}^{d_1-1}\sum_{i_2=0}^{d_2-1} w_{i_1 i_2} \ket{i_1 i_2} ~=~ \sum_{a=0}^{d_1d_2-1} w_{a} \ket{a}
$$
<br>
donde hemos querido resaltar que las componente y  los vectores son los mismos, etiquetados de forma diferente.

+++ {"slideshow": {"slide_type": "fragment"}}

 En el caso genera el mapa es 
<br>

$$
i_1 i_2 ~~\to ~~ a = d_2*i_1 + i_2  
$$
<br>
Claramente $a = 0,...,d_1d_2-1$

+++ {"slideshow": {"slide_type": "slide"}}

### Producto de Kronecker

+++ {"slideshow": {"slide_type": "-"}}

Como sabemos, cualquier vector admite, en una base, una representación como un vector columna con sus coeficientes como entradas. 

<br>
<br>
$$
\ket{w} ~= ~ \sum_{i,j=1}^2 w_{ij} \ket{e_{ij}}\sim~ \begin{pmatrix}w_{11}\\ w_{12}\\ w_{21} \\ w_{22}  \end{pmatrix}  ~  
$$

+++ {"slideshow": {"slide_type": "skip"}}

La matriz columna asociada $\ket{uv}= \ket{u}\otimes \ket{v}$ se forma a partir de las matrices columna de $\ket{u}$ y $\ket{v}$ mediante el denominado *producto de Kronecker* o, también *producto tensorial*. 
<br>
<br>

$$
 \ket{uv} = \ket{u}\otimes \ket{v} ~\sim~ 
\begin{pmatrix}u_1\\ u_2 \end{pmatrix}\otimes \begin{pmatrix}v_1\\ v_2 \end{pmatrix} ~\equiv ~
\begin{pmatrix}u_1 \begin{pmatrix}v_1\\ v_2 \end{pmatrix} \\ u_2 \begin{pmatrix}v_1\\ v_2 \end{pmatrix}  \end{pmatrix}
~=~\begin{pmatrix}u_1v_1\\ u_1v_2 \\ u_2 v_1 \\ u_2 v_2  \end{pmatrix}
$$

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

Con dos vectores $\ket{u} = \sum_i u_i \ket{e_i}$ y $\ket{v} = \sum_i v_i \ket{e_i} \in \Hil$, hay dos objetos muy parecidos que podemos formar

1. un operador $\Omega = \ketbra{u}{v} = \sum_{ij}u_i v^*_j\ketbra{e_i}{e_j} \in \Lin(\Hil)$.  
<br>
    
2. un vector $\ket{\omega} = \ket{u}\otimes \ket{v} = \sum_{ij} u_i v_j \ket{e_i} \ket{e_j} \in \Hil\otimes \Hil$. 
    
Nota la conjugación compleja relativa entre las dos matrices de componentes $\Omega_{ij} = u^*_i v_j$ y $\omega_{ij} =  u_i v_j$.

:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejercicio
:class: tip

Escribe una función  <i>kronecker(u,v)</i> que tome dos kets (como vectores columna)  y devuelva su producto de Kronecker. Verifica el resultado con la funcion $kron$ de numpy.

:::

+++ {"slideshow": {"slide_type": "slide"}}

## Factorización y Entrelazamiento

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Definición** *(Vector entrelazado)*

^^^

Decimos que, un vector $\ket{w}\in \Hil\otimes\Hil$ es <b>factorizable</b> cuando es posible encontrar vectores $\ket{u},\ket{v}\in \Hil$ tales que $ \ket{w} = \ket{u}\otimes\ket{v}$.

Cuando esto no sea posible, decimos que  $\ket{w}$ es un vector <b>entrelazado</b>.
:::

+++ {"slideshow": {"slide_type": "skip"}}

Ya hemos visto que, dada una base $\ket{e_i}$ de $\Hil$, el vector más general que pertenece al espacio producto admite una descomposición 

$$
\ket{w} = \sum_{i,j=1}^d w_{ij}\ket{e_{i}}\otimes \ket{e_j} = w_{11}\ket{e_1}\otimes\ket{e_1} + w_{12}\ket{e_1}\otimes\ket{e_2} + ...\, .
$$

+++ {"slideshow": {"slide_type": "skip"}}

Podría ocurrir que en otra base $\ket{w} = \tilde w_{11} \ket{f_1}\otimes\ket{f_1}$ sólo tuviese un término y fuese factorizable.

+++ {"slideshow": {"slide_type": "skip"}}


Discernir si un vector es factorizable o entrelazado no es algo que se pueda hacer a primera vista. 

+++ {"slideshow": {"slide_type": "slide"}}

### Criterio de factorizabilidad


:::{card}

Criterio de factorización

^^^

El estado es $\ket{w}$ es factorizable si y sólo si las componentes $w_{ij}$ son factorizables en la forma $w_{ij} = u_i v_j~$ con $i=1,...,d_1$ y $j = 1,...,d_2$. 

:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{dropdown} Demostración

$$
\ket{w}= \sum_{i,j=1}^d w_{ij} \ket{e_{ij}}  = \sum_{i,j} u_{i}v_j \ket{e_i}\otimes \ket{e_j}= \sum_{i,j} u_{i} \ket{e_i}\otimes v_j\ket{e_j}  ~ =~ \sum_i u_i\ket{e_i} \otimes \sum_j v_j\ket{e_j} ~=~   \ket{u}\otimes \ket{v}
$$

identidad que se puede leer en ambos sentidos

:::

+++ {"slideshow": {"slide_type": "fragment"}}

- El carácter entrelazado de un vector es <i>genérico</i>, mientras que el carácter factorizable es <i>accidental</i>.
<br>

- Esto se sigue de un sencillo contaje: 

    - como función de $d$,  $\{w_{ij}\}$ forma un conjunto de $d_1d_2$ parámetros complejos (grados de libertad). 

    - Sin embargo en $\{u_i v_j\}$ sólo hay $d_1 + d_2$ números independientes. Es evidente que $d_1 d_2 \gg d_1 + d_2$.

+++ {"slideshow": {"slide_type": "slide"}}



-  En el caso  $d_1 = d_2 =2$  la condición de *factorizabilidad* $~\Rightarrow ~w_{ij} = u_i v_j$ es <i>equivalente</i> a verificar
    la anulación del  determinante de la matriz $2\times 2$ formada por las componentes
<br>
    
$$\det w_{ij} =  w_{11}w_{22}- w_{12}w_{21} = u_1v_1u_2v_2-u_1v_2u_2v_1=0$$  

<br>

- En el caso general $d_1, d_2 \geq 2$ la busqueda de un criterio para detectar si $w_{ij}$ es factorizable o entrelazado pasa por la descomposición de Schmidt. 

+++ {"slideshow": {"slide_type": "slide"}}

### Descomposición de Schmidt

+++ {"slideshow": {"slide_type": "-"}}

Supongamos que, en sendas bases arbitrarias $\{\ket{e_{1,i}},~ i=1,...,d_1\}$  de $\Hil_1$ y  $\{\ket{e_{2,a}},~a=1,...,d_2\}$  de $\Hil_2$ nuestro vector se escribe

$$
\ket{w} = \sum_{i=1}^{d_1}\sum_{a=1}^{d_2} w_{ia} \ket{e_{1,i}}\otimes \ket{e_{2,a}}
$$

+++ {"slideshow": {"slide_type": "skip"}}

Los valores de las *componentes* $w_{ia}$ **dependen de las bases escogida**. En *otras* base $\ket{ \tilde e_{1,i}}\otimes\ket{\tilde e_{2,a}}$ encontraremos *otras* componentes $\tilde w_{ia}$ para el *mismo* vector 
<br> 

+++ {"slideshow": {"slide_type": "skip"}}

Si existe una base en la que $\tilde w_{ia}=0$ para todos los $i,a$ menos para uno (por ejemplo $\tilde w_{11}\neq 0$), entonces 
<br>
<br>
$$\ket{w}= \tilde w_{11}\ket{\tilde e_{1,1}}\otimes \ket{\tilde e_{2,1}}$$ 
<br>
y, secretamente, el vector $\ket{w}$ era factorizable. 

+++ {"slideshow": {"slide_type": "skip"}}

El siguiente teorema nos permite averiguar **cuánto nos podemos acercar a esta situación**

+++ {"slideshow": {"slide_type": "slide"}}

:::{card}

**Teorema** *(de Schmidt)*

^^^

Para cada vector $\ket{w}\in \Hil_1\otimes \Hil_2$, existen sendas  bases  $\ket{f_{1,i}}$  de $\Hil_1$ y  $\ket{f_{2,a}}$  de $\Hil_2$, tales que, podemos expresar 

$$
\ket{w} = \sum_{i=1}^r s_i \ket{f_{1,i}}\otimes\ket{f_{2,i}} \, ,
$$
    
donde $s_i>0$, y la suma   involucra el <i>mínimo número</i>, $r$, de términos.

:::

+++ {"slideshow": {"slide_type": "slide"}}

El número $1\leq r\leq {\rm min}(d_1,d_2)$ se denomina <b>rango</b> de $w$ y  es la información relevante  porque 

-  cuando $r=1$ el estado $\ket{w}$ será *factorizable*. 
<br>
<br>
-  si $r\geq 2$ el estado será *entrelazado*.


+++ {"slideshow": {"slide_type": "slide"}}

La *demostración del Teorema de Schmidt* es interesante porque nos da un **método constructivo** para encontrar la descomposición. 

Supongamos que nuestro vector se escribe

$$
\ket{w} = \sum_{i=1}^{d_2}\sum_{a=1}^{d_2} w_{ia} \ket{e_{1,i}}\otimes \ket{e_{2,a}}
$$

La matriz de coeficientes $w_{ia}$ tiene  dimension $d_1\times d_2$. 
Asumiremos $d_1 \geq d_2$ sin pérdida de generalidad

+++ {"slideshow": {"slide_type": "slide"}}

 El **teorema SVD** de descomposición en valores singulares, nos garantiza que podemos expresar dicha matriz en la forma siguiente
<br>

$$
w = U\Sigma V^\dagger ~~~\Rightarrow ~~~~w_{ia} = \sum_{j=1}^{d_1}\sum_{b=1}^{d_2} U_{ij}\Sigma_{jb}V_{ab}^*
$$

donde $U$ y $V$ son unitarias $(d_1\times d_1)$ y $(d_2\times d_2)$ respectivamente, mientras que $\Sigma$ es diagonal


+++ {"slideshow": {"slide_type": "slide"}}

$$
\Sigma_{jb} = 
\overbrace{\left.
\begin{bmatrix}
s_1 &\cdots  &    &  & & &  0  \\  \vdots & \ddots & & & & & \vdots  \\  & & s_r & & & &  \\
   & &  & 0  & &  &    \\ & & & & & \ddots &  \\  0 & &\cdots  & & & & 0  \\ \vdots & &&&& & \vdots \\ 0 & & \cdots & & & & 0
\end{bmatrix}   \right\}  }^{\displaystyle d_2} \, d_1 ~~~~~~\Rightarrow ~~~~~ \Sigma_{jb} = s_j\delta_{jb}
$$

- Los números $s_1,...,s_r >0$ son los autovalores de la matriz $w^\dagger w$  y se denominan <i>valores principales </i>  de la matriz $w_{ij}$ 

+++ {"slideshow": {"slide_type": "slide"}}


Esto quiere decir que podemos escribir

\begin{eqnarray}
\ket{w} &=& \sum_{i=1}^{d_1}\sum_{a=1}^{d_2}\left( \sum_{j=1}^{d_1}\sum_{b=1}^{d_2} U_{ij}\Sigma_{jb}V_{ab}^* \right)\ket{e_{1,i}}\otimes \ket{e_{2,a}}
\\  \rule{0mm}{10mm}
&=& \sum_{j=1}^{d_1}\sum_{b=1}^{d_2}\Sigma_{jb}\left( \sum_{i=1}^{d_1} U_{ij}\ket{e_{1,i}} \right)\otimes  \left( \sum_{a=1}^{d_2} V_{ab}^* \ket{e_{2,a}}\right)
\\   \rule{0mm}{10mm}
&=& \sum_{j=1}^{d_1}\sum_{b=1}^{d_2}s_j\delta_{jb} \ket{f_{1,j}}\otimes \ket{f_{2,b}}\\   \rule{0mm}{10mm}
&=& \sum_{j=1}^r s_j \ket{f_{1,j}}\otimes \ket{f_{2,j}}
\end{eqnarray}

+++ {"slideshow": {"slide_type": "fragment"}}

Por tanto, podemos saber si un *estado bipartito* es entrelazado calculando la descomposición en valores singulares de su matriz de coeficientes en cualquier base. 

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# Veamos el caso genérico 

d1=4 # Dimensión de H1
d2=3 # Dimensión de H2

' generate a random complex matrix '
w = np.random.randn(d1,d2)+ np.random.randn(d1,d2) * 1j  # coeficientes w_{ia} de un estado genérico
display(array_to_latex(w))

' perform the SVD decomposition'
u, s, vh = np.linalg.svd(w, full_matrices=True)

np.round(s,3)

print('principal values s_i = ',np.round(s,3))
print('The Schmidt number is r =', np.count_nonzero(s))
```

+++ {"slideshow": {"slide_type": "fragment"}}

Corre la celda anterior muchas veces y mira si consigues encontrar algún caso en que $r<{\rm min}(d_1,d_2)$

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# Veamos ahora el caso particular de un estado factorizable

d1=5
d2=3

' create two random vectors '
u = tQ.random_ket(d1)
v = tQ.random_ket(d2)

w = np.outer(u,v)
display(array_to_latex(w))

' SVG decomposition '
u, s, vh = np.linalg.svd(w, full_matrices=True)

print('principal values s_i = ',np.round(s,3))
print('The Schmidt number is p =', np.count_nonzero(np.round(s,3)))
```

+++ {"slideshow": {"slide_type": "fragment"}}

Podemos correr la celda anterior varias veces comprobar que nunca obtendremos $r>1$

+++ {"slideshow": {"slide_type": "slide"}}

## Producto Tensorial Múltiple

+++ {"slideshow": {"slide_type": "skip"}}

- El producto tensorial se puede generalizar a más de un factor. 


+++ {"slideshow": {"slide_type": "-"}}


- El espacio $ \Hil_1\otimes \Hil_2 ... \otimes \Hil_n$ formado por todas las *n-tuplas* ordenadas de vectores 
<br>
<br>
$$\ket{u} = \ket{u_1u_2...u_n} \equiv\ket{u_1}\otimes\ket{u_2}\otimes ...\otimes \ket{u_n}$$ 
<br>
donde $\ket{u_i}\in 
\Hil_i$ y sus combinaciones lineales $\{ a\ket{u}+ b\ket{v} + ...\}$.

<br>
<br>

- Salvo mención expresa, asumiremos que todos los $\Hil_j=\Hil$ son iguales y de dimension $d$. En el contexto de la computación cuántica usual con cúbits $\Rightarrow \, d=2$ 

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejercicio
:class: tip

Escribe una función  <i>kronecker($u_1,u_2,...,u_n$)</i> que tome n kets (como vectores columna)  y devuelva su producto de Kronecker múltiple.  

:::

+++ {"slideshow": {"slide_type": "slide"}}

### Base de $\Hil^{\otimes n}$

Una base de $\Hil^{\otimes n}$ se obtiene a partir de cadenas 

$$
\ket{i_1 i_2.... i_n} = 
\ket{i_1}\ket{i_2}  ... \ket{i_n}
$$ 

donde $i_1,..,i_n=0,...,d-1$. 

+++ {"slideshow": {"slide_type": "fragment"}}

El número de posibles cadenas es $d^n$ que  es la dimensión de $\Hil^{\otimes n}$.

$$
{\rm dim}_{\mathbb C} \Hil^{\otimes n} = d^n
$$

+++ {"slideshow": {"slide_type": "slide"}}

Podemos cambiar de etiqueta 

$$
\ket{i_1...i_n} \to \ket{a}
$$ 

con

$$
a = i_n + d i_{n-1} + d^2 i_{n-2} \, +...+ \,  d^{n-1} i_1
$$

Claramente $a ~\in ~(0,d^n-1)$.

+++ {"slideshow": {"slide_type": "fragment"}}

Si cada base $\{\ket{i}\}$ es ortonormal, tendremos que la *base producto* también lo será
<br>

$$
\braket{i_1 i_2... i_n}{j_1j_2...j_n} = \delta_{i_1j_1}\delta_{i_2j_2}...\delta_{i_nj_n} ~~~~\leftrightarrow ~~~~
\braket{a}{b} = \delta_{ab}
$$

+++ {"slideshow": {"slide_type": "slide"}}



### Estado entrelazado general


Un *vector general* admitirá una expansión en esta base mediante $d^n$ *componentes complejas*
$u_{i_1 i_2...i_n}$ en la forma

$$
\ket{u} ~~=~ \sum_{i_1,...,i_n=0}^{d-1} u_{i_1i_2...i_n} \ket{i_1i_2...i_n} ~~=~
 \sum_{a=0}^{d^n-1} u_a\ket{a}\, .
$$

+++ {"slideshow": {"slide_type": "fragment"}}


Podemos obtener cualquier componente compleja proyectando sobre el elemento correspondiente de la base

$$
u_{i_1i_2...i_n} = \braket{i_1 i_2... i_n}{u}~~~~~~\leftrightarrow~~~~~~~~u_a = \braket{a}{u}
$$

+++ {"slideshow": {"slide_type": "skip"}}

Decimos que $u_{i_1i_2...i_n}$ forman las componentes de un *tensor de rango* $n$
<br>
<br>
Un estado genérico depende de un conjunto de $d*d...*d = d^n$ componentes independiente $u_{i_1i_2...i_n}$.

Ya hemos visto los casos de rango $n=1$ <i>(vector)</i> y $n=2$ <i>(operador)</i>

+++ {"slideshow": {"slide_type": "slide"}}

### Estado factorizable

Al igual que antes, *sólo en casos muy particulares*, un vector de $\Hil^{\otimes n}$ se podrá escribir en forma factorizada
<br>
<br>
$$
\ket{w} = \ket{v_1}\ket{v_2}\ldots\ket{v_n} \equiv \ket{v_1 v_2 \ldots v_n}
$$

+++ {"slideshow": {"slide_type": "fragment"}}

Escribiendo $\ket{v_k} = \sum_{i_k=1}^d v_{i_k}\ket{i_k}$ vemos que un *vector factorizable* admite una expansión general en la que los coeficientes son factorizables

$$
v_{i_1i_2...i_n}  = v_{i_1} v_{i_2}.... v_{i_n}
$$

El conjunto de coefficientes
está parametrizado por $d +d + ...d = nd$ cantidades $v_{i_k}, \, i_k=1,...,d, \, k=1,...,n$.

+++ {"slideshow": {"slide_type": "skip"}}

### Estados producto de matrices *(MPS)*

En medio de los dos casos extremos anteriores encontramos la posibilidad de que las componentes del tensor se puedan escribir como productos de matrices. 


+++

:::{card}

**Definición**

^^^

Un estado $\ket{v}$ es un <b>MPS</b> <i>(estado producto de matrices)</i> si sus componentes en cualquier base pueden escribirse como la traza total de un producto de matrices

$$
v_{i_1 i_2 i_3... i_n} =\tr ( A^{(1)}_{i_1}\cdot A^{(2)}_{i_2}\cdot A^{(3)}_{i_3} \cdots A^{(n)}_{i_n} )
$$

:::

+++ {"slideshow": {"slide_type": "skip"}}

- Si $A^{(a)}_i$ con $a=1,...,n$ y $i=1,...,d$ es un conjunto  de $nd$ matrices de dimensión $D\times D$, con $D$ la  *(dimensión local de enlace)*, el número de parámetros independientes es $ndD^2$. 
<br>
<br>
Los MPS tienen entrelazamiento no nulo, que crece con $D$. 

+++ {"slideshow": {"slide_type": "skip"}}

-  Si $A^{(a)}_i = A_i$ para todo $a=1,..,n$ decimos que el MPS formado es *invariante traslacional*

Por ejemplo, con $n=4$, $\ket{v} =  v_{i_1i_2i_3i_4} \ket{e_{i_1i_2i_3i_4} }$

$$
v_{i_1i_2i_3i_4} =  \sum_{\alpha\beta\gamma\mu = 1}^DA_{i_1}^{\mu \alpha}A_{i_2}^{\alpha\beta}A_{i_3}^{\beta\gamma}A_{i_4}^{\gamma\mu}
$$

```{figure} figuras/XTN4.png
:scale: 50 %
:alt: map to buried treasure
:align: center
```

+++ {"slideshow": {"slide_type": "skip"}}

### Redes de tensores 

Si queremos aumentar el entrelazamiento del estado podemos, además de aumentar $D$, recurrir a contracciones de índices de tensores de mayor rango

$$
v_{i_1i_2i_3i_4} = \sum_{\alpha\beta\gamma\mu\delta = 1}^D A_{i_1}^{\mu \alpha\delta}A_{i_2}^{\alpha\beta}A_{i_3}^{\beta\delta\gamma}A_{i_4}^{\gamma\mu}
$$

```{figure} figuras/XTensNet.png
:scale: 40 %
:alt: map to buried treasure
:align: center
```

+++ {"slideshow": {"slide_type": "skip"}}

Los estados MPS, y los estados TN  para una dimensión de enlace local $D$ finita, no son suficientemente expresivos para capturar el máximo entrelazamiento posible en un estado.

```{figure} figuras/XTN_complete.png
:scale: 50 %
:alt: map to buried treasure
:align: center
```

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

- $nd \ll d^n$. El crecimiento exponencial del número de estados entrelazados es el ingrediente crucial para la computación cuántica. Observar que $d^n$ es el <i>número de enteros</i> alcanzables por $n$ bits. Pero en computación cuántica es el <i>número de dimensiones</i> en la que podemos poner $d^n$ amplitudes complejas.  
<br>

- No existe un criterio general para saber si un estado es, a priori, factorizable o entrelazado. 
<br>

- Además, hay formas de caracterizar matemáticamente el nivel de entrelazamiento (*entanglement witnesses, entanglement monotones* etc.) desde nulo (estado factorizable) hasta maximal.

:::

+++ {"slideshow": {"slide_type": "skip"}}

## Operadores sobre  $\Hil^{\otimes n}$

+++ {"slideshow": {"slide_type": "skip"}}



El espacio $\Hil^{\otimes n}$ admite, como cualquier espacio vectorial, la acción de *operadores lineales* $A: \Hil^{\otimes n} \to \Hil^{\otimes n}$ donde

$$
A:\ket{u} \to \ket{v} \equiv A\ket{u}
$$    

El conjunto de todos los operadores lineales forman el espacio vectorial $\Lin(\Hil^{\otimes n})$.

+++ {"slideshow": {"slide_type": "skip"}}

### Matrices

- A cada operador, $A$, le podemos asociadar una *matriz*, una vez elijamos nuestra base  $\{ \ket{i_1 i_2... i_n}\}$ donde, $i_k = 1,...,d$. 
<br> 
<br>
 
 
- Los *elementos de matriz* ahora vendrán etiquetados por dos *multi-índices*

$$
A_{i_1...i_n, \, j_1...j_n} = \bra{i_1...i_n}A\ket{j_1...j_n}  ~~~~~\leftrightarrow ~~~~~~ A_{ab}= \bra{a}A\ket{b}
$$



+++ {"slideshow": {"slide_type": "skip"}}

-  Con la matriz, el operador se reconstruye en la base canónica de productos externos

\begin{eqnarray} 
 A &~~=~& 
 \sum_{i_1,...,i_n,\, j_1,...,j_n=0}^{d-1} A_{i_1...i_n, \, j_1...j_n} \ket{i_1...i_n}\bra{j_1...j_n}
 ~~~~=~~~~
  \sum_{a,b=a}^{d^{N}-1} A_{ab} \ket{a}\bra{b}
\end{eqnarray}

+++ {"slideshow": {"slide_type": "skip"}}

- En $A_{i_1...i_n,\,j_1...j_n} = A_{ab}$ hay $d^n\times d^n = d^{2n}$ grados de libertad. Esta sería la dimensión del espacio  $\Lin(\Hil^{\otimes n})$.
<br>

+++ {"slideshow": {"slide_type": "skip"}}

### Producto tensorial de operadores

+++ {"slideshow": {"slide_type": "skip"}}

En $\Lin(\Hil^{\otimes n})$ hay un análogo de los vectores factorizables de $\Hil^{\otimes n}$: los *operadores factorizables*.

Supongamos que existen $n$ operadores lineales $A^{(a)}\, ,\, a=1,...,n$ definidos sobre cada espacio factor $\Hil$.

+++ {"slideshow": {"slide_type": "skip"}}

:::{card}

**Definición**

^^^

La acción del producto tensorial de operadores  $A = A^{(1)}\otimes A^{(2)} \otimes ...A^{(n)}$ sobre un vector $\ket{v} = \ket{v}_1\otimes ...\otimes \ket{v_n}\in \Hil~$   factoriza 

$$
A\ket{v} = A^{(1)}\ket{v_1}\otimes ... \otimes A^{(n)} \ket{v_n}\, .
$$

:::

+++ {"slideshow": {"slide_type": "skip"}}


La acción sobre vectores generales se sigue imponiento linealidad

$$
A(\ket{v} + \ket{w}) = A\ket{v} + A\ket{w}\, .
$$

+++ {"slideshow": {"slide_type": "skip"}}

-  El adjunto de un producto tensorial de operadores es el producto de los adjuntos (no se permuta el orden)

$$
A^\dagger = A^{(1)\dagger} \otimes ... \otimes A^{(n)\dagger}
$$

+++ {"slideshow": {"slide_type": "skip"}}

-  El producto tensorial de operadores hermíticos es hermítico

$$ A^{(a)\dagger} = A^{(a)} ~~\Longrightarrow A^{\dagger} = A $$

+++ {"slideshow": {"slide_type": "skip"}}

- El producto tensorial de operadores unitarios, es unitario

$$ A^{(a)\dagger} = A^{(a)\, -1} \,  ~~\Longrightarrow ~~A^{\dagger} = A^{-1} $$

+++ {"slideshow": {"slide_type": "skip"}}

### Producto de Kronecker de matrices

+++ {"slideshow": {"slide_type": "skip"}}

¿Cómo será la matriz $A_{i_1...i_n, \, j_1...j_n}$ de un operador factorizable, $ A = A^{(1)}\otimes A^{(2)} \otimes ...A^{(n)}$, en términos de las matrices  $ A^{(a)}_{ij}$ de sus factores?

+++ {"slideshow": {"slide_type": "skip"}}

Vamos a tomar  $n=2$ por simplicidad
\begin{eqnarray}
A = A^{(1)}\otimes  A^{(2)} &=&\left( \sum_{i_1i_2}A^{(1)}_{i_1 j_1} \ket{i_1}\bra{j_1}\right)\left( \sum_{i_2j_2}A^{(2)}_{i_2 j_2} \ket{i_2}\bra{j_2}\right)\\
&=& \sum_{i_1 i_2 , j_1 j_2} A^{(1)}_{i_1 j_1}A^{(2)}_{i_2 j_2}\ket{i_1 i_2}\bra{j_1j_2} \\
&=& \sum_{i_1 i_2 , j_1 j_2} A_{i_1i_2,\, j_1j_2}\ket{i_1 i_2}\bra{j_1j_2}
\end{eqnarray}

+++ {"slideshow": {"slide_type": "skip"}}

Vemos que la matriz asociada a $A$ se obtiene  a partir de las matrices de $A^{(a)}$ mediante el  *producto exterior de las matrices*, o *producto de Kronecker*.


$$
  A_{i_1i_2,\,j_1j_2} = A^{(1)}_{i_1j_1}A^{(2)}_{i_2 j_2} 
$$

+++ {"slideshow": {"slide_type": "skip"}}

- El método para de **representar** matricialmente el producto de Kronecker de dos matrices $A\otimes B$ es sencillo. Supongamos que $d=2$ y tenemos un operador producto $A\otimes B$. Entonces su matriz 

<br>

$$
(A\otimes B)_{ab} = \begin{pmatrix} A_{00}B & A_{01}B \\ A_{10}B & A_{11}B \end{pmatrix} = \begin{pmatrix} A_{00}B_{00} & A_{00}B_{01} & A_{01}B_{00} & A_{01}B_{01} \\
                A_{00}B_{10} & A_{00}B_{11} & A_{01}B_{10} & A_{01}B_{11} \\
                A_{10}B_{00} & A_{10}B_{01} & A_{11}B_{00} & A_{11}B_{01} \\
                A_{10}B_{10} & A_{10}B_{11} & A_{11}B_{10} & A_{11}B_{11} \end{pmatrix}.
$$

+++ {"slideshow": {"slide_type": "skip"}}

- El producto de Kronecker verifica las siguientes propiedades para dos matrices $A$  y $B$ de dimensiones $d_A$ y $d_B$. 
<br>
<br>

\begin{eqnarray}
(A\otimes B)(C\otimes D) &=& (AC)\otimes (BD) \nonumber\\ \rule{0mm}{6mm}
\tr(A\otimes B) &=& (\tr A)(\tr B) \nonumber\\ \rule{0mm}{6mm}
A\otimes(B+D) &=& A\otimes B + A\otimes D \nonumber\\ \rule{0mm}{6mm}
(A\otimes B)^\dagger &=& A^\dagger\otimes B^\dagger \nonumber\\ \rule{0mm}{6mm}
(A\otimes B)^{-1} &=& A^{-1} \otimes B^{-1} \nonumber\\ \rule{0mm}{6mm}
\det (A\otimes B) &=& (\det A)^{d_B}(\det B)^{d_A}
\end{eqnarray}


donde $AC$ significa el producto de matrices $A$ y $C$

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejercicio
:class: tip

1. Demuestra estos resultados
    
2. Rescribe la función $kronecker$  para que acepte  dos matrices $A$  y $B$ de dimensiones $d_A$ y $d_B$ y devuelva su producto de Kronecker $A\otimes B$. Verifica el resultado con la funcion kron de numpy.   Verifica las propiedades anteriores.   
    
:::

+++ {"slideshow": {"slide_type": "skip"}}

La generalización a todo $n$ es obvia. El producto de Kronecker de $n$ matrices $ A^{(a)}_{i_aj_a}$ asociadas a operadores $A^{(a)}$ es

$$
 A_{i_1...i_n,\,j_1...j_n} = A^{(1)}_{i_1j_1}...A^{(n)}_{i_n j_n} 
$$

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejercicio
:class: tip

Calcula $\sigma_1\otimes \sigma_2\otimes \sigma_3$

:::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Nota
:class: note

Observar que en un operador general, la matriz $ A_{i_1...i_n,\,j_1...j_n}$ tiene $d^n\times d^n = d^{2n}$ entradas independientes. 

Sin embargo 
en un producto de Kronecker $A^{(1)}_{i_1j_1}...A^{(n)}_{i_n j_n}$ sólo hay $nd^2$. 
    
Por tanto, los *operadores factorizables* forman un subconjunto muy pequeño dentro del conjunto de los operadores generales.

:::

+++ {"slideshow": {"slide_type": "skip"}}

### Generación de entrelazamiento

Supongamos que $\ket{u} = \ket{u_1}\otimes\ket{u_2}$ es factorizable. 

* Si $A=A_1\otimes A_2$ es un operador factorizable entonces

$$
\ket{v} = A\ket{u} = A_1\ket{u_1}\otimes A_2\ket{u_2} = \ket{v_1}\otimes \ket{v_2}
$$

también es factorizable.

* Inversamente, la *acción de un operador no factorizable* $A\neq A_1\otimes A_2$ genera estados entrelazados

$$
\ket{v} = A\ket{u}  \neq \ket{v_1}\otimes \ket{v_2}
$$
