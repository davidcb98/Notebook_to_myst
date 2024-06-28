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

+++

# Operadores II

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

## Autovalores y autovectores
       

+++ {"slideshow": {"slide_type": "slide"}}

### Valores y vectores propios

+++

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

\begin{eqnarray}
A \ket{u} 
=  \sum_{a=1}^{d} c_a A\ket{\lambda^a}  =  \sum_{a=1}^{d} c_a \lambda\ket{\lambda^a}  =   \lambda \sum_{a=1}^{d} c_a \ket{\lambda^a}  =\lambda\ket{u}
\end{eqnarray}

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

Escribe una función en python, `spectral_decomp`, que verifique si un operador $A$ es normal y, en caso afirmativo, devuelva las dos listas $\lambda_i$ y $P_i$ asociadas a la decomposición espectral  $A = \sum_i \lambda_i P_i$.   
:::

+++ {"slideshow": {"slide_type": "slide"}}

### Espectro de Operadores Hermíticos, Unitarios y Proyectores

+++

Los operadores hermíticos, unitarios y proyectores, son casos particulares de operadores  normales. Por tanto son diagonalizables y sus autovectores, asociados a autovalores distintos, generan subespacios mútuamente ortogonales. 


Vamos a ver cómo los requisitos adicionales que definend operadores hermíticos, unitarios y proyectores, se traducen en propiedades particulares para sus espectros. 

+++


- **Espectro de Operadores Hermíticos**

::::{card}

**Teorema**

^^^


Los autovalores de un operador hermíticos son reales $\lambda_i \in {\mathbb R}$.

:::{dropdown} Demostración

Tomemos un autovector normalizado de $A$, $\ket{\lambda}$ de autovalor $\lambda$.

$$
\lambda = \bra{\lambda}A\ket{\lambda} =  (\bra{\lambda}A^\dagger\ket{\lambda})^* = (\bra{\lambda}A\ket{\lambda})^*= \lambda^* .~~~
$$   

:::
::::

+++ {"slideshow": {"slide_type": "skip"}}

:::{admonition} Ejericio *(explícaselo a tu ordenador)*
:class: tip

Escribe una función en python, `random_hermitian`, que reciba un número entero $d$ y genere una matriz hermítica de esa dimensión. <br>    
Comprueba en distintos casos que el espectro es real. 

:::
 

+++ {"slideshow": {"slide_type": "slide"}}

- **Espectro de Operadores Unitarios**

::::{card}

**Teorema**

^^^

Los autovalores de un operador unitario son fases puras

$$
U^\dagger = U^{-1} ~~~\Longleftrightarrow ~~~\lambda_i = e^{i\phi_i}
$$ 

:::{dropdown} Demostración

Aquí tu prueba
    
:::
::::

+++ {"slideshow": {"slide_type": "slide"}}

- **Espectro de Proyectores**

::::{card}

**Teorema**

^^^

Los autovalores de un proyector sólo pueden ser $~0~$ ó $~1~$

$$
P^2= P ~~~\Longleftrightarrow ~~~\lambda_i \in \{0,1\}
$$ 

:::{dropdown} Demostración

La ecuación 
    
$$ P^2 = P ~~~~~\Rightarrow ~~~~~~~~ P^2 \ket{u} = P\ket{u} $$

sólo tiene dos soluciones consistentes 
    
$$
P\ket{u} = \ket{u}~~~~~~~\hbox{y} ~~~~~~~~~~P\ket{u} = 0
$$

:::
::::

+++ {"slideshow": {"slide_type": "skip"}}

### Operadores que conmutan

+++

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

+++ {"slideshow": {"slide_type": "skip"}}

### Descomposición Polar (DP)

+++

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

:::{card}

**Definición**

^^^

Los números $\sigma_i = \sqrt{\lambda_i} > 0$ se denominan <b>valores singulares</b> de $A$, donde $\lambda_i>0$ son los autovalores no-nulos de $A^\dagger A$.

:::

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Teorema**

^^^

Sea $A$ una matriz compleja $m\times n$. Entonces  admite la siguiente <b>descomposición en valores singulares</b>

$$
A = U\,\Sigma\, V^{\dagger} \, ,
$$

donde $U\in U(m)$, $V\in U(n)$ son matrices unitarias cuadradas y $\,\Sigma \,$ es una matriz rectangular $m\times n$ con $\sigma_1, ...,\sigma_r$ <i>valores singulares</i> reales y positivos   en la diagonal, donde $r\leq {\rm min}(m,n)$. 
:::    

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

+++ {"slideshow": {"slide_type": "slide"}}

### Definición de traza de un operador

:::{card}

**Definción**

^^^

La traza de un operador $A$ se define como la suma de elementos diagonales de su matriz
   
$$
\tr A = \sum_ i \bra{e_i} A\ket{e_i} =  \sum_{i} A_{ii} 
$$

de sus elementos de matriz diagonales <u> en cualquier base </u>        
:::

+++ {"slideshow": {"slide_type": "slide"}}

Para ser consistente esta definición es necesario probar que se puede calcular en cualquier base

::::{card} 

**Lema**

^^^

La traza de un operador es <i>independiente de la base</i> en la que se calcule

:::{dropdown} Demostración

\begin{eqnarray} Sean $\{\ket{i}\}$ y $\{\ket{\tilde i}\}$ dos bases cualesquiera. Entonces
{\rm tr} A  &=&\sum_i A_{ii} =\sum_{i} \bra{i}A\ket{i} =\sum_{i} \bra{i}A\left( \sum_j\ketbra{\tilde j}{\tilde j}\right)\ket{i}
\nonumber\\
&=& \sum_{ij}\bra{i}A\ket{\tilde j} \braket{\tilde j}{i} = \sum_{ij}\braket{\tilde j}{i}\bra{i}A\ket{\tilde j}  \nonumber\\
&=& \sum_{j} \bra{\tilde j}\left(\sum_i\ketbra{i}{i}\right) A \ket{\tilde j}= \sum_{j} \bra{\tilde j}A\ket{\tilde j}\nonumber\\
&=& \sum_j \tilde A_{jj}
\end{eqnarray}


:::
::::

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

$$
{\rm tr}(ABC)= {\rm tr}(BCA) 
$$

:::{dropdown} Prueba

\begin{eqnarray} 
    {\rm tr}(ABC)&=&\sum_i (ABC)_{ii} =  \sum_{ijk} A_{ij}B_{jk}C_{ki}\\
    &=& \sum_{ijk} B_{jk}C_{ki}A_{ij} = \sum_j (BCA)_{jj}\\
    &=&  {\rm tr}(BCA)
\end{eqnarray}
:::

Para un producto de dos operadores, el anterior resultado implica que la *traza de un conmutador es cero*. Dicho de otra forma

$$
{\rm tr}(AB) = {\rm tr}(BA) ~~~\Rightarrow ~~~~{\rm tr}([A,B]) = 0 \, .
$$

+++ {"slideshow": {"slide_type": "fragment"}}

- Sea el operador *producto externo* de dos vectores $A = \ketbra{u}{v}$. Entonces 

$$
\tr \left(\rule{0mm}{5mm}\ketbra{u}{v}\right)  = \braket{v}{u}
$$

:::{dropdown} Prueba

$$ 
\tr \left(\rule{0mm}{5mm}\ketbra{u}{v}\right) = \sum_i \braket{e_i}{u}\braket{v}{e_i} = \bra{v}\left(\sum_i \ketbra{e_i}{e_i}\right) \ket{u} = \braket{v}{u}
$$

::: 

+++ {"slideshow": {"slide_type": "slide"}}

### $\Lin(\Hil)$ como un espacio de Hilbert

+++ {"slideshow": {"slide_type": "-"}}

Para transformar $\Lin(\Hil)$ en un espacio de Hilbert sólo es necesario definir un *producto escalar hermítico* entre dos elementos 

:::{card}

**Definición**

^^^

Dados dos operadores lineales,  $A, B \in \Lin(\Hil)$  definimos su <i> producto escalar </i>  $( A, B)\in {\mathbb C}$

$$
( A, B) \equiv {\rm tr}\left( A^\dagger B \right) 
$$

:::

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

:::{card}

**Definción** *(norma Shatten)*

^^^

Dado un operador $A\in \Lin(\Hil)$ la función  

$$
\| A \|_p =  \left({\rm tr} \left(A^\dagger A\right)^{p/2} \right)^{1/p}
$$

define una norma, denominada <b>$p$-norma de Shatten</b>.

:::

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

:::{admonition} Ejercicio (explícaselo a tu ordenador)
:class: tip

Escribe una función en python, `trace_norm(A_{ij})`, que calcule la norma de la traza de un operador $A$ dado por una matriz $A_{ij}$.
:::

+++ {"slideshow": {"slide_type": "slide"}}

### Distancia de traza

+++ {"slideshow": {"slide_type": "skip"}}

Cualquier norma permite definir una noción de *distancia* o *diferencia* entre dos operadores. 

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Definción** 

^^^

Se define la  <b> distancia de traza</b> entre dos operadores $A$ y $B$ como la <i>norma del operador diferencia</i>

$$
d(A,B) = \| A - B \|_1 
$$

:::

+++ {"slideshow": {"slide_type": "skip"}}

## Funciones de Operadores

+++ {"slideshow": {"slide_type": "skip"}}

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

:::{admonition} Nota
:class: note

De la misma forma que, para funciones analíticas $f(z)^* = f(z^*)$, también la definición anterior asegura que 
$f(A)^\dagger = f(A^\dagger)$
:::



+++ {"slideshow": {"slide_type": "skip"}}

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

:::{card}

**Teorema** *(de Baker-Campbel-Haussdorf)*

^^^

Sean $A,B\subset{\rm L}(\Hil)$ dos operadores lineales genéricos. Entonces

$$
e^A e^B = e^{\left({A+B + \frac{1}{2}[A,B] + \frac{1}{12}[A,[A,B]]+ \frac{1}{12}[B,[B,A]] + ...}\right)}
$$

:::

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

:::{card}

**Teorema** *(de Lie-Suzuki-Trotter)*

^^^

Sean $A,B\subset{\rm L}(\Hil)$ dos operadores lineales genéricos. Entonces

$$
e^{A+B} = \lim_{n\to\infty} \left(e^{{A/n}} e^{B/n}\right)^n
$$

Esta segunda opción es de uso muy frecuente en el contexto de la *simulación cuántica*. 
:::

+++ {"slideshow": {"slide_type": "skip"}}

**Relación entre operadores hermíticos y unitarios**

:::{card}

**Teorema** 

^^^

Todo operador unitario $U$ se puede expresar como la exponencial imaginaria de un operador hermítico $H$

$$
U = e^{i H}
$$
:::

Efectivamente, 

$$U^\dagger = \left(e^{i H}\right)^\dagger = e^{-i H^\dagger} = e^{-i H}=U^{-1}$$ 

por tanto, $U$ es unitario si y sólo si $H$ es hermítico.

:::{dropdown} Detalles

\begin{eqnarray}
U^\dagger &=& \left( e^{iH}\right)^\dagger = \left( 1+ iH + \frac{1}{2}(i H)^2 + ...\right)^\dagger \\
&=& 1 - iH^\dagger  + \frac{1}{2}(-i)^2 (H^2)^\dagger + ... \\
&=& 1 - iH +\frac{1}{2} H^2 - ... \\
&=& e^{-iH}\\ \rule{0mm}{6mm}
&=& U^{-1}
\end{eqnarray}
:::

+++ {"slideshow": {"slide_type": "slide"}}

### Funciones  generales 

+++ {"slideshow": {"slide_type": "skip"}}

No siempre $f(z)$ admite una expansión en serie de Taylor. Por ejemplo $f(z) = \exp(1/z)$ en torno a $z=0$ no es analítica.

En estos casos, el operador $f(A)$ existe, pero para construirlo es necesario recurrir a la *forma diagonalizada*

+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Teorema**

^^^

Sea $A$ un operador diagonalizable, y sea $A= \sum_i \lambda_i \ket{\lambda_i}\bra{\lambda_i}$ su representación espectral. 
Entonces el operador $f(A)$ tiene la representación espectral siguiente
    
$$
f(A) = \sum_i f(\lambda_i) \ket{\lambda_i}\bra{\lambda_i}
$$
:::

En particular, la matriz asociada a $f(A)$ en la base $\{\ket{\lambda_i}\}$ que diagonaliza $A^{(D)}_{ij}$ 
es la diagonal de los elementos $f(\lambda_i)$ de los autovalores

$$
f(A^{(D)}_{ij}) = \begin{bmatrix} f(\lambda_1)& &  & \\ & f(\lambda_2) & &  \\ & & \ddots & \\ & & & f(\lambda_n)
\end{bmatrix}
$$

+++ {"slideshow": {"slide_type": "slide"}}

:::{admonition} Ejemplo
:class: tip

$$
f(A) = e^{1/A} = \sum_i e^{1/\lambda_i} \ket{\lambda_i}\bra{\lambda_i}
$$

:::

+++ {"slideshow": {"slide_type": "slide"}}

:::{admonition} Ejemplo
:class: tip

\begin{eqnarray}
f(A) = {\rm tr}(A \log A) &=& {\rm tr}\left[\left(\sum_j \lambda_j \ket{\lambda_j}\bra{\lambda_j}\right)\left(\sum_k\log \lambda_k \ket{\lambda_k}\bra{\lambda_k}\right)\right] ~=~  {\rm tr}\left[\sum_k \lambda_k \log\lambda_k \ket{\lambda_k}\bra{\lambda_k} \right] \\ \rule{0mm}{20mm}
&=& {\rm tr} \begin{bmatrix} \lambda_1 \log \lambda_1& &  & \\ &\lambda_2 \log \lambda_2 & &  \\ & & \ddots & \\ & & & \lambda_n \log \lambda_n
\end{bmatrix}
 ~= ~ \sum_k \lambda_k \log \lambda_k \rule{0mm}{8mm}
\end{eqnarray}

:::

+++ {"slideshow": {"slide_type": "slide"}}

## Matrices de Pauli


+++ {"slideshow": {"slide_type": "-"}}

:::{card}

**Definición**

^^^

$$
\sigma_x = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}~~~~~,~~~~~~~~~
\sigma_y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}~~~~~,~~~~~~~~~
\sigma_z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \, .
$$

:::

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

:::{card}

**Teorema**

^^^

$$
\exp \left( i\,   {\bf a} \cdot \boldsymbol{\sigma}  \right) = (\cos a)\, I + i (\sin a)\,\hat{\bf n} \cdot  \boldsymbol{\sigma} 
$$

:::

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

:::{card}

**Ejericios**

^^^

Obtén la descomposición espectral de las tres matrices de Pauli, $\sigma_x, \sigma_y $ y $\sigma_z$. Utiliza esta descomposición para demostrar la expresión

$$
e^{i \alpha\,  \hat{\bf n}\cdot\boldsymbol{\sigma}} = \cos \alpha \, I + i \sin \alpha \, \hat{\bf n}\cdot\boldsymbol{\sigma}
$$

donde $\hat{\bf n} = (n_x, n_y,n_z)$ es un vector unitario.

:::
