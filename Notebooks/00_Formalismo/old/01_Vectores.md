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
github: https://github.com/executablebooks/mystmd
subject: Curso
venue: Quantum Spain
math:   
    '\i': '{\color{blue}{i}}'
    '\bes': '\begin{equation*}'
    '\ees': '\end{equation*}'
    '\O': '{\mathcal O}'
    '\Lin': '\hbox{Lin}'
    '\Hil': '{\mathcal H}'
    '\bra[1]': '{\langle #1|}'
    '\ket[1]': '{|#1\rangle}'
    '\braket[2]': '{\langle #1|#2\rangle}'
    '\R': '{\mathbb R}' 
    '\C': '{\mathbb C}'
    '\V': '{V}'
abbreviations:
    MyST: Markedly Structured Text
    TLA: Three Letter Acronym
---


+++

```{figure} ../thumbnails/myThumbnail.png
:align: center
```

+++

# Vectores

+++

```{contents}
:local:
:depth: 2
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
import copy 
```

+++ {"slideshow": {"slide_type": "skip"}}

## Espacio Vectorial 

+++

Comenzaremos definiendo los vectores de una forma operativa, y después haremos hincapié en su carácter abstracto.

+++ {"slideshow": {"slide_type": "skip"}}

::::{prf:definition} *Vector*
La forma operacional de definir  un *vector de dimensión* $N$ consiste en lista (columna) de $N$ números complejos 
<br>
<br>
$$
|u\rangle = \begin{pmatrix} {u_1}\\ {u_2}\\ \vdots \\ {u_N} 
\end{pmatrix}
$$
::::

+++ {"slideshow": {"slide_type": "skip"}}

- El símbolo $\ket{u}$  *representa* al vector y se denomina **ket** en la *notación de Dirac*. Se trata simplemente de una notación alternativa a la usual, donde un vector se representa en la forma ${\bf u}$ o también $\vec u$ 



- Los números complejos $u_i \in {\mathbb C}$ con $\, i=1,...,N$ se denominan **componentes** del vector $\ket{u}$

+++ {"slideshow": {"slide_type": "skip"}}

:::{prf:definition}(*Espacio Vectorial*)   
    La colección de <i>todos los posibles vectores</i> de $N$ componentes,  con las  propiedades de suma y multiplicación forman un <b>espacio vectorial</b>, $\V$ de dimension compleja $N$
:::

+++ {"slideshow": {"slide_type": "skip"}}

es decir,  en un espacio vectorial  tenemos dos operaciones posibles: 

- sumar dos vectores
    
$$
 |u\rangle + \ket{v}~ =~\, 
\begin{pmatrix} {u_1}+v_1\\ {u_2}+v_2\\ \vdots \\ {u_N}+v_n \end{pmatrix} ~= ~\ket{w}
$$

- multiplicar un vector por número complejo $\lambda\in {\mathbb C}$
<br>

$$
 \lambda|u\rangle ~ =~   \begin{pmatrix} {\lambda u_1}\\ {\lambda u_2}\\ \vdots \\ {\lambda u_N} \end{pmatrix} ~\equiv~\ket{\lambda u}
$$

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
' qiskit tiene un visualizador de matrices bastante nítido'
from qiskit.tools.visualization import array_to_latex

uket=np.array([[1 + 1.j],[2-3*1.j]])
 
display(array_to_latex(uket))
```

+++ {"slideshow": {"slide_type": "skip"}}

- todo vector de $V$ se denota mediante el símbolo $\ket{v}$ menos uno, el **elemento neutro** que se escribe como $0$.
<br>
<br>
- La existencia de un **elemento opuesto** y de un elemento neutro son dos propiedades importantes en un espacio vectorial

\begin{eqnarray}
\ket{v} + 0 &=& \ket{v} \nonumber\\
\ket{v} + \ket{\hbox{-}v} &=& \ket{v}-\ket{v} = 0 \nonumber\\
\end{eqnarray}

+++ {"slideshow": {"slide_type": "skip"}}

```{admonition} Notar
:class: note  

La <b>dimensión</b> es igual al número de cantidades (<i>grados de libertad</i>) que debemos fijar para especificar un vector. 
Pero $N$ números complejos equivalen a $2N$ números reales. 

   
Entonces, podemos decir que:  la <i>dimensión compleja</i> de un espacio vectorial complejo  $\V$ es $N$, o que su <i>dimensión real</i> es $2N$ 
<br>
<br>
$$
{\rm dim}_{\mathbb C} \V = N ~~~~\Longleftrightarrow ~~~   {\rm dim}_{\mathbb R} \V = 2N 
$$
```

+++ {"slideshow": {"slide_type": "slide"}}

### Base 

+++ {"slideshow": {"slide_type": "skip"}}

Es evidente que el vector $\ket{v}$ definido anteriormente se puede expandir de la siguiente manera
<br>


<br>

$$
\ket{u} ~=~ \begin{pmatrix} {u_1} \\ {u_2} \\{u_3}\\ \vdots 
\\ \,{u_{N-1}}\, \\ {u_{N}} \end{pmatrix}~= =~ {u_1} \begin{pmatrix} 1 \\ 0 \\ 0\\ \vdots 
\\ 0 \\ 0 \end{pmatrix} \,+\,{u_2} \begin{pmatrix} 0 \\ 1 \\ 0\\ \vdots \\ 0 \\ 0 \end{pmatrix}~+~ ... ~+ ~
{u_{N-1}} \begin{pmatrix} 0 \\ 0 \\ 0\\\vdots 
\\ 1 \\ 0 \end{pmatrix}+ 
\,{u_N}\,  \begin{pmatrix} 0 \\ 0 \\0\\ \vdots 
\\ 0 \\ 1 \end{pmatrix}
$$

<br>

+++ {"slideshow": {"slide_type": "skip"}}

Esta notación se vuelve inmanejable cuando $N$ se hace muy grande. Sin embargo, la notación de Dirac equivalente es muy concisa. Definamos la siguiente colección  $\{ e_i\}$ de vectores 

<br>

$$
|1\rangle \sim \begin{pmatrix} 1 \\ 0 \\ 0\\ \vdots 
\\ 0 \\ 0 \end{pmatrix}~~~~
~~~|2\rangle \sim \begin{pmatrix} 0 \\ 1 \\ 0\\ \vdots 
\\ 0 \\ 0 \end{pmatrix}~~~~~~~~~
\cdots ~~~~~~~~
~~|{N-1}\rangle \sim \begin{pmatrix} 0 \\ 0 \\ 0\\\vdots 
\\ 1 \\ 0 \end{pmatrix}~~~~
~~|N\rangle \sim \begin{pmatrix} 0 \\ 0 \\0\\ \vdots 
\\ 0 \\ 1 \end{pmatrix}
$$


+++

Entonces simplemente

$$
\ket{u} ~=~ {u_1} |1 \rangle + {u_2} | 2\rangle +... + {u_{ N}}|{ N}\rangle~=~ \sum_{i=1}^N {u_ i} |i\rangle 
$$

+++

Lo único que hemos hecho es representar el vector $\ket{u}$ en una base. Vamos a formalizar esto.

+++ {"slideshow": {"slide_type": "-"}}

```{prf:definition} Base

En un espacio vectorial $V$ de dimensión $N$ una <b>base</b> es una colección $\{\ket{e_1},...,\ket{e_N}\}$ de $N$ vectores  <i>linealmente independientes</i>

```

+++

 Cualquier vector $\ket{v}\in V$ que no sea el elemento neutro $\ket{v}\neq 0$,  se puede expresar como una <i>combinación lineal</i> de  los vectores de una base

$$
\ket{v} = \sum_{i=1}^N v_i \ket{e_i} ~=~ v_1\ket{e_1} \,+\, v_2\ket{e_2}\, +\, ...\, +\, v_N \ket{e_N}
$$  

Los coeficientes $v_i$ son las **componentes** de $\ket{v}$ **en la base dada** $ \{ \ket{e_i} \}$.

+++

```{admonition} Nota
:class: note  

Los símbolos $e_i$ son *cualquier coleccón de etiquetan* que sirva para distinguir entre los $N$ estados de la base. En el ejemplo anterior hemos tomado $e_i  = i \in (1,...,N)$.

Por ejemplo, con $N=4$ podríamos usar también notación binaria

$$
\ket{e_0} = \ket{0} = \ket{00}~~~~~~,~~~~~~\ket{e_1} = \ket{1} = \ket{01}~~~~~~,~~~~~~\ket{e_2} = \ket{2} = \ket{10}~~~~~~,~~~~~~\ket{e_3} = \ket{3} = \ket{11}
$$

```

+++ {"slideshow": {"slide_type": "skip"}}

Podemos usar la clase **Statevector** de *qiskit* para tener una expansión en la base $\{\ket{e_i}=\ket{b(i)}\}$, donde $b(i)$ es la representación binaria del índice $i$. Por ejemplo $b(3) = 11$.

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
from qiskit.quantum_info import Statevector
uket=np.array([[ 1.+1.j], [ 2.-3.j],[ 2.+2.j],[-1.-1.j]])
display(array_to_latex(uket))

Statevector(uket).draw('latex')
```

### Vectores: definición intrínseca

La definición de vector que hemos introducido antes está asociada a una base concreta, en la cuál, los números $v_i$ representan *las componentes* de dicho vector en esa base.

Sin embargo un vector es un objeto abstracto, que admite <u>una representación distinta en cada base</u>. Para ellos debemos comenzar por hablar de las distintas bases. 

+++ {"slideshow": {"slide_type": "slide"}}

**Cambio de base**

En un espacio vectorial de dimensión finita $N$, existen *infinitas* bases  .
Todas ellas sirven para representar un vector arbitrario.

+++

Consideremos dos bases 
$\{\ket{e_i}\}$ y $\{\ket{\tilde e_j}\}$ donde $ i,j = 1,...,N$.
Por ser bases, <u>un vector cualquier admitirá una representación</u> en cada una de ellas
<br>
<br>
$$~~\ket{v}  = \sum_{i} \color{blue}{v_i} \color{blue}{\ket{e_i}} = \sum_j \color{red}{\tilde v_j} \color{magenta}{\ket{\tilde e_j}}$$

```{figure} figuras/Descomp_ortogonal.png
:scale: 70 %
:alt: map to buried treasure
:name: fig-target
:align: center
This is the caption of the figure (a simple paragraph).
```

+++

Las listas de componentes  $v_i$ y $\tilde v_i$ contienen *la misma información*, puesto que representan al mismo vector $\ket{v}$, cada una en una base

Por tanto: debe ser posible entonces encontrar la *traducción* de una lista de valores a la otra.

Es evidente que este traductor debe *depender* de la relación que guardan ambas bases $\{\ket{e_i}\}$ y $\{\ket{\tilde e_i}\}$  entre sí

+++ {"slideshow": {"slide_type": "fragment"}}

Por ser bases, cualquier *elemento* (vector) <u>de una</u> se puede expresar como una *combinación lineal de elementos*  <u>de la otra</u>. Por ejemplo 

$$
\ket{\tilde e_j} = \sum_{i=1}^N C_{ i j} \ket{e_i} ~~~~~~~j=1,..., N
$$

Los coefficientes  $C_{ i j}\in {\mathbb C}$ constituyen la **matriz de cambio de base**


+++

Notar que de los subíndices de $C_{ij}$

- el índice $i$ está sumado con los elementos de la base

- el índice $j$ es una etiqueta que recuerda que estamos expandiendo el vector $\ket{\tilde e_j}$

+++ {"slideshow": {"slide_type": "skip"}}

<b>Ejemplo</b>: Sea la matriz de coeficientes es 

$$
C_{ij} = \begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix} =  \begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix}\, ,
$$

Entonces la expresión $\ket{\tilde e_j} = \sum_{i=1}^N C_{ i j} \ket{e_i}$ en este caso relaciona las dos bases en la forma siguiente 

\begin{eqnarray}
\ket{\tilde e_1} &=& C_{11}\ket{e_1}  + C_{21}\ket{e_2}  =  \ket{e_1} + i\ket{e_2}\nonumber\\ \rule{0mm}{8mm}
\ket{\tilde e_2} &=& C_{12}\ket{e_1}  + C_{22}\ket{e_2}=\ket{e_1} - i\ket{e_2} \nonumber
\end{eqnarray}


El cambio de base, se puede escribir como una multiplicación de matrices colocando los vectores en una fila

$$
\big(\ket{\tilde e_1},\ket{\tilde e_2}\big) = \big(\ket{e_1},\ket{e_2}\big) \, \begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix} = \big(\ket{e_1} + i\ket{e_2}, \ket{e_1}-i\ket{e_2} \big)
$$

+++ {"slideshow": {"slide_type": "skip"}}

```{admonition} Nota
:class: note

La forma en que están sumados los índices 

$$
\ket{\tilde e_j} = \sum_{\color{blue}{i=1}}^{\color{blue}{N}} C_{ \color{blue}{i} j} \ket{e_{\color{blue}{i}}}
$$

Esto hace que, si queremos escribir esta ecuación en notación matricial,  debamos poner los vectores en una fila
    
$$
\begin{pmatrix} \ket{\tilde e_1} & \cdots & \ket{\tilde e_N} \end{pmatrix} = 
\begin{pmatrix} \ket{ e_{\color{blue}{1}}} & \cdots & \ket{e_ {\color{blue}{N}}}\end{pmatrix}
\begin{pmatrix} C_{\color{blue}{1}1} & \cdots & C_{\color{blue}{1}N} \\ \vdots & \ddots & \vdots \\ C_{\color{blue}{N}1} & \cdots & C_{\color{blue}{N}N} \end{pmatrix}
$$

```

+++ {"slideshow": {"slide_type": "slide"}}

Ahora podemos obtener el *diccionario* entre componentes $v_i$ y $\tilde v_i$, a partir de la  matriz de cambio de base


\begin{eqnarray}
\ket{v}  ~= ~ \sum_{i} v_i \ket{e_i} &~=~ \sum_j \tilde v_j \ket{\tilde e_j} \nonumber\\
&~=~  \sum_j \tilde v_j \left( \sum_{i} C_{ij} \ket{e_i}\right) \nonumber \\
&~=~  \sum_{j}\sum_{i} \tilde v_j   C_{ij} \ket{e_i} \nonumber \\
&~=~ \sum_i \left( \sum_j C_{ij} \tilde v_j \right) \ket{e_i}  \nonumber \\
\end{eqnarray}

+++ {"slideshow": {"slide_type": "slide"}}

Comparando obtenemos la relación de coeficientes 

$$
v_i = \sum_{j} C_{i\color{black}{j}} \tilde v_{\color{black}{j}}
$$

Esta expresión devuelve las componentes  $v_i$ de un vector $\ket{v}$ en la base $\{ \ket{e_i}\}$ suponiendo que son conocidas las $\tilde v_i$ en la base $\{ \ket{\tilde e_i} \}$

+++ {"slideshow": {"slide_type": "skip"}}

```{admonition} Nota:
:class: note
    
1. La forma en que están sumados los índices hace que, en notación matricial esta operación se represente como sigue

$$
\begin{pmatrix} v_1\\ \vdots \\ v_n\end{pmatrix} = 
\begin{pmatrix} C_{11} & \cdots & C_{1n} \\ \vdots & \ddots & \vdots \\ C_{n1} & \cdots & C_{nn} \end{pmatrix}
\begin{pmatrix} \tilde v_1\\ \vdots \\ \tilde v_n\end{pmatrix}
$$
   
<br>    
    
2.  La misma matriz $C$, que lleva $\ket{e_i} \to \ket{\tilde e_i}$, lleva $\tilde v_j \to v_j$

```

+++

Un vector es un objeto abstracto, un elemento de un espacio vectorial. La definición que dimos al principio es fácil de entender, pero conlleva la elección implícita de una base. En cada base un vector se representa con un conjunto de componentes diferentes

+++

```{prf:example} 

Vamos a hacer un test de consistencia con vectores que conocemos en ambas bases. 
Escojamos por ejemplo $\ket{v} = \ket{\tilde e_1}$. Las componentes $\tilde v_i$ de este vector en la base $\{\ket{\tilde e_i}\}$ son claramente $\tilde v_i = \begin{pmatrix}1\\0\end{pmatrix}$. Entonces podemos obtener las componentes $v_i$ en la base $\{\ket{e_i}\}$ siguiendo la regla encontrada

$$
\ket{\tilde e_1} \sim  \begin{pmatrix} \tilde v_1\\ \tilde v_2\end{pmatrix} = \begin{pmatrix} 1\\ 0 \end{pmatrix} ~\hbox{en la base} \{\ket{\tilde e_i}\}~~~~\Longrightarrow ~~~~\ket{\tilde e_1} \sim  \begin{pmatrix} v_1\\v_2\end{pmatrix} = \begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix}\begin{pmatrix} 1\\ 0 \end{pmatrix} = \begin{pmatrix} 1\\ i \end{pmatrix}~\hbox{en la base} \{\ket{e_i}\}
$$

y, análogamente, escogiendo $\ket{v} = \ket{\tilde e_2}$

$$
\ket{\tilde e_2} \sim  \begin{pmatrix} \tilde v_1\\ \tilde v_2\end{pmatrix} = \begin{pmatrix} 0\\ 1 \end{pmatrix} ~\hbox{en la base} \{\ket{\tilde e_i}\}~~~~\Longrightarrow ~~~~ \ket{\tilde e_2} \sim \begin{pmatrix} v_1\\v_2\end{pmatrix} = \begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix}\begin{pmatrix} 0\\ 1 \end{pmatrix} = \begin{pmatrix} 1\\ -i \end{pmatrix} ~\hbox{en la base} \{\ket{e_i}\}
$$

```

+++

Si queremos obtener las componentes $\tilde v_i$ a partir de las $v_i$, tenemos que invertir la matriz

$$
\tilde v_i = \sum_{j} C^{-1}_{i\color{black}{j}} v_{\color{black}{j}}
$$

+++ {"slideshow": {"slide_type": "skip"}}

```{prf:example} continuación


Continuando con el ejemplo anterior, invertir la matriz da
$$
C^{-1}_{ij} = \frac{1}{2}\begin{pmatrix} 1 &- i\\  1 & i \end{pmatrix}
$$

lo cual nos permite encontrar las componentes de $\ket{e_1}$ en la base $\ket{\tilde e_i}$

$$
\ket{e_1} = \ket{v} = \begin{pmatrix} \tilde v_1\\\tilde v_2\end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1 &- i\\  1 & i \end{pmatrix}\begin{pmatrix} 1\\ 0 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1\\ 1 \end{pmatrix}~~~~\hbox{en la base} \{\ket{\tilde e_i}\}
$$

y también

$$
\ket{e_2} = \ket{v} = \begin{pmatrix} \tilde v_1\\\tilde v_2\end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1 &- i\\  1 & i \end{pmatrix}\begin{pmatrix} 0\\ 1 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} -i\\ i \end{pmatrix}~~~~\hbox{en la base} \{\ket{\tilde e_i}\}
$$

```

+++ {"slideshow": {"slide_type": "skip"}}

```{exercise}
Considera las bases ortonormales $\{\ket{e_i}\} = \{\ket{0},\ket{1}\}$ y $\{\ket{\tilde e_i}\} =\{\ket{+},\ket{-}\}$ donde $\ket{\pm} = \frac{1}{\sqrt{2}}(\ket{0} \pm \ket{1})$. 

Las componentes del vector $\ket{u} \sim \begin{pmatrix}3\\1\end{pmatrix}$ están escritas en la primera base. 

Halla las componentes de $\ket{u}$ en la segunda.
```

+++

###  Subespacios Vectoriales

+++

Seal $B = \{\ket{e_i}\}_{i=1,...,N}$ la base  de un espacio vectorial $V$. Cualquier subconjunto de elementos de dicha base, $\bar B\subset B$, genera un *subespacio vectorial* $\bar V \subset V$


+++

**Suma Directa**

Por ejemplo, podemos dividir $B$ en dos subconjuntos complementarios

$$B_1 =  \{\ket{e_i}\}_{i=1,...,N_1}~~~~~~~,~~~~~~~~~  B_2 =  \{\ket{e_i}\}_{i={N_1}+1,...,N}$$

de forma que $B = B_1 \cup B_2$

+++

Cada subconjunto será base de un subespacio vectorial $B_1 \to V_1$ y $B_2\to V_2$ de forma que el espacio original será la **suma directa** de ambos

$$
V  = V_1  + V_2
$$


+++

Cualquier vector $\ket{u}\in V$ se escribirá en la forma $\ket{v} = \ket{v_1} + \ket{v_2}$ de vectores pertenecientes a cada subespacio.

+++

Por construcción, la dimensión de una suma directa es la suma de las dimensiones $\hbox{dim}\, V = \hbox{dim}\, V_1 + \hbox{dim}\, V_2$

+++ {"slideshow": {"slide_type": "slide"}}

## Espacios de Hilbert

+++ {"slideshow": {"slide_type": "skip"}}

###  Conjugación adjunta

La operación *conjugación adjunta*,  $\dagger$, es una *extensión* de la *conjugación compleja* de ${\mathbb C}$ a todos los elementos  de $\Hil$

+++ {"slideshow": {"slide_type": "skip"}}

Asociado a cada *ket* $\ket{u}$, definimos un vector **adjunto**, o *bra* $\bra{u}\equiv\left(\ket{u}\right)^\dagger$,  que representamos mediante un vector fila con las componentes conjugadas complejas.  
<br>
<br>
$$
\dagger \,: \quad\,|u\rangle = \begin{pmatrix} {u_1}\\ {u_2}\\ \vdots \\ {u_N} 
\end{pmatrix} ~~~~~{\rightarrow}~~~~~~ \left(\ket{u}\right)^\dagger \equiv \bra{u} =\begin{pmatrix} {u_1^*} & {u_2^*} & \cdots & {u_N^*}
\end{pmatrix}
$$

<hr />

+++ {"slideshow": {"slide_type": "skip"}}

Consistentemente encontramos para el producto de un vector por un número complejo $\lambda$

$$
\dagger \,:\quad\,  \lambda\ket{u}=\ket{\lambda u} ~~~~~{\rightarrow}~~~~~~ \left(\lambda\ket{u}\right)^\dagger=\lambda^*\bra{u} = \bra{u}\lambda^* = \bra{\lambda u}
$$

ya que el producto de un vector por un número es conmutativo.

+++ {"slideshow": {"slide_type": "skip"}}

Al igual que la conjugación compleja, la conjugación adjunta es una *involución*: su aplicación sucesiva devuelve el vector original

$$
(\ket{u}^\dagger)^\dagger =\bra{u}^\dagger =  \ket{u}
$$

es decir, $\dagger^2 = I$, el operador identidad.

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---
'definamos un array'
u = np.array([1+1j,2-3*1j])

'ket es un vector columna'
uket=u.reshape(len(u),1)
display(array_to_latex(uket))

'el bra asociado será una fila formada por las componentes conjugadas complejas'
ubra=uket.conj().T
ubra = u.reshape(1,len(u)).conj()
display(array_to_latex(ubra))
```

+++ {"slideshow": {"slide_type": "fragment"}}

```{prf:definition} Espacio de Hilbert
Un <i> espacio de Hilbert</i>,  ${\Hil}$, es un espacio vectorial
dotado de una operación interna   denominada <i>producto escalar</i>.
```

+++ {"slideshow": {"slide_type": "slide"}}

### Producto Escalar

+++

```{prf:definition} Producto escalar

El producto escalar de dos vectores $\ket{u}$ y $\ket{v}$ es un <i>número complejo</i> 
$a\in{\mathbb C}$ que denotamos <i>braket</i>

$$
a \equiv \braket{u}{v} 
$$ 

si verifica las propiedades siguientes linealidad: $\to \bra{u}\big(\ket{v}+\ket{w}\big) = \braket{u}{v} + \braket{u}{w}$ hermiticidad: $\to \braket{v}{u} = \braket{u}{v}^*$ positividad: $\braket{u}{u} >0$ para todo ket $\ket{u}\neq 0$ no-degeneración: $~$ si  $\braket{u}{v} = 0$ para todo $\bra{u}$, entonces necesariamente $\ket{v}=0$

```

+++ {"slideshow": {"slide_type": "slide"}}

Combinando ambas propiedades, el producto escalar también es lineal en el primer argumento

$$(\bra{u}+\bra{w})\ket{v} = \braket{u}{v} + \braket{w}{v}$$

+++ {"slideshow": {"slide_type": "skip"}}

Notar que la propiedad de hermiticidad es precisamente la extensión de la conjugación compleja de la que hablábamos al definir la aplicación *adjunta*

$$
\braket{u}{v}^* = \braket{u}{v}^\dagger  = \braket{v}{u}
$$

Hemos usado que $\bra{u}^\dagger = \ket{u}$ y  $\ket{v}^\dagger = \bra{v}$ pero le hemos añadido una regla más: 
<u>*al tomar el mapa adjunto es necesario invertir el orden de los elementos*</u>
 
 De no haber seguido esta regla, habríamos obtenido un resultado **erróneo**
 
 $$
\braket{u}{v}^\dagger \to \ket{u}\bra{v} 
 $$
 
que no es ni siguiera un número complejo. 

+++ {"slideshow": {"slide_type": "slide"}}

### Norma

Una **norma** es un una función real $\|\cdot\| : \Lin(\Hil) \to {\mathbb R}$ con las siguientes propiedades 


- ser definida positiva $\|A\|\geq 0$ con $\| A\| = 0 \Leftrightarrow A= 0$
<br>

- homogeneidad $\|\lambda A\| = |\lambda| \|A\|$ 
<br>

- triangle inequality. $\|A+B\| \leq \| A\| + \|B\|$

+++ {"slideshow": {"slide_type": "slide"}}

Un espacio de Hilbert es, automáticamente un espacio normado. 
La positividad  del producto escalar de un vector por sí mismo  permite definir su *norma*.

$$
\|\ket{v}\| = \sqrt{\braket{v}{v}} 
$$

+++ {"slideshow": {"slide_type": "skip"}}

```{admonition} Nota
:class: note

- En contraste con la definición de producto escalar en espacios vectoriales reales, en el caso complejo se hace necesario conjugar el <i>bra</i>, para  que la <i>norma</i> de un vector sea siempre real y positiva. Esta es la idea detrás de la definición de la <i>conjugación adjunta</i>.


- El único vector que tiene norma nula en un espacio de Hilbert es el elemento neutro

$$
\braket{v}{v} = 0 ~~~ \Leftrightarrow ~~~\ket{v} = 0
$$
  
```

+++ {"slideshow": {"slide_type": "fragment"}}

### Distancia

+++ {"slideshow": {"slide_type": "-"}}

Dados dos elementos $\ket{u}$ y $\ket{v}$ de $\Hil$, podemos definir la *distancia* entre ellos como la *norma de su diferencia* 
<br>

$$
d(\rule{0mm}{5mm}\ket{v},\ket{w}) = \| \ket{v}-\ket{w}\|
$$

+++ {"slideshow": {"slide_type": "skip"}}

En particular 

-  $d(\ket{v}, \ket{w}) = d(\ket{w}, \ket{v})$ 

<br>

- $d(\ket{v}, \ket{v}) = 0$

+++ {"slideshow": {"slide_type": "slide"}}

## Bases ortonormales

+++ {"slideshow": {"slide_type": "skip"}}

Hasta ahora, a los vectores de una base $\{\ket{e_i}\}$ sólo se les ha pedido que sean $N$ vectores *linealmente independientes*, donde $N$ es la dimensión del espacio vectorial $\V$:

En un espacio de Hilbert $\Hil$ tiene sentido calcular el producto escalar de dos elementos de una base. 

+++

```{prf:definition} Base ortonormal

Una base ortornormal se caracteriza por la siguiente lista de productos escalares

$$
\braket{e_i}{e_j} = \delta_{ij}
$$

```

+++ {"slideshow": {"slide_type": "skip"}}



- Por un lado, dos elementos distintos de la base son ortogonales $\braket{e_1}{e_2} = 0$. 
<br>



- Por otro, todos están normalizados  $ \| e_i \| = \sqrt{\braket{e_1}{e_1}} = \sqrt{1} = 1$. 

+++

```{prf:theorem} Teorema de Gram-Schmidt

Dada una base general $\{\braket{f_i}{f_j}\neq \delta_{ij}\}$ de vectores no ortonormales, existe una procedimiento iterativo (de <a href="https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process">Gram-Schmidt</a> ) para construir, a partir de ella, una nueva base ortonormal $\{\braket{e_i}{e_j}\}=\delta_{ij}$
```

+++ {"slideshow": {"slide_type": "fragment"}}


 Dado un vector  $\ket{v} = \sum_{i=1}^N v_i \ket{e_i}$ escrito en una base ortonormal, la *componente* $v_i$ se extrae mediante la *proyección ortogonal*
<br>
<br>
$$
v_i =\braket{e_i}{v}
$$

+++

````{exercise}
Verifica esta expresión

```{dropdown} Desmostración
\begin{eqnarray}
\braket{e_k}{v} &=&  \bra{e_k}\left(\sum_{j=1}^N v_j\ket{e_j}\right) \nonumber\\
                &=&  \sum_{j=1}^N  v_j\braket{e_k}{e_j}  \nonumber\\
                &=&  \sum_{j=1}^N  v_j\delta_{kj} = v_k
\end{eqnarray}
```
````

+++ {"slideshow": {"slide_type": "slide"}}

En una base
ortonormal, calcular el valor de un *producto escalar* $a=\braket{u}{v}$ es muy simple 

+++ {"slideshow": {"slide_type": "fragment"}}

\begin{eqnarray}
a = 
\braket{u}{v}&=& \left(\sum_{i}u_i^*\bra{e_i}\right)\left(\sum_{j}v_j\ket{e_j} \right) = 
\sum_{ij} u_i^* v_j  \braket{e_i}{e_j}
=
\sum_{ij} u_i^* v_j \delta_{ij} 
\\
&=&\sum_{i} u_i^* v_i =
  \begin{pmatrix}
{u_1^*} & {u_2^*} & \cdots & {u_N^*}
\end{pmatrix}\begin{pmatrix} {v_1}\\ {v_2}\\ \vdots \\ {v_N} 
\end{pmatrix}
\end{eqnarray}

<br>

+++ {"slideshow": {"slide_type": "skip"}}

```{admonition} Nota
:class: note 
<br>
la expresión de la izquierda  $a = \braket{u}{v}$ <b>no hace referencia a ninguna base</b>. Por tanto, el resultado $\sum_{i=1}^n{ u_i^* v_i} $ debe ser independiente de la base que utilizamos para representar estos vectores mediante sus componentes $u_i$ y $v_i$. 
    
Subrayamos la importancia de esto: $\braket{u}{v}$ puede ser calculado en la base más conveniente.

```

+++

```{exercise}
- Escribe una función <i>braket</i>$(u,v)$ que calcule y devuelva la el producto escalar $\braket{u}{v}$, y, con ella, una función $norm(u)$ que calcule la norma $\| \ket{u}\|$.
Verifica que $\| \ket{u}\| = \sqrt{\braket{u}{u}}$ coincide con el resultado que da la función `np.linalg.norm`.

- Escribe una función <i>random$\_$ket</i>$(d)$ que genere un vector normalizado  $\ket{v}\in\Hil$ de dimensión $d$.
```

```{code-cell} ipython3
def braket(u,v):
    return np.sum([u[i].conjugate()*v[i] for i in range(len(u))])
```
