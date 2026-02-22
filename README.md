# Geographic-Centre
The Centre of N Points was my A-Level Computer Science coursework project, a weave of Mathematics and Computing to explore a problem that fascinated me. Given $n$ points in some space $S$, what is the point in $S$ that is equidistant from from all those points. Right now that seems vague and poorly defined, and thats because it is ! The original problem was spurred on from an issue me and my family were having: we are scattered across the UK, where would be a location to meet such that each party would have to travel an equal distance to travel to arrive at that location. Furthermore, what would be a location that would be an equal distance to travel whilst also minimizing the total distance that all parties have to travel. At the time, I was learning Djikstra's algorithm and A*; as well as learning the basics of 3D geometry and calculus. Thus, I pursued this problem for my A-Level project.<br>

This involved a deep exploration into mathematics and optimisation. The original project was created with PyQt5 for the interface; but later I engineered this to work on my website in Python (for a Flask server backend) and then in raw JavaScript. These are all included, with the original in the PyQT directory, the flask implementation in the Flask directory and the JavaScript implementation in the JS directory. You will see a general improvement in understanding and programming, as PyQT was done as an A-Level Student, Flask was done as a 2nd Year Graduate, and JS was done post graduation (currently incomplete). While the PyQT and Flask implementations likely won't fully work, lacking a server or API keys, the JavaScript implementation is fully complete and should be able to be run locally without issue. You can run this like so:<br>
1. Clone the project 
```
git clone https://github.com/Illuminarchie66/Geographic-Centre.git
```
2. Navigate into the correct folder and run a local server: 
```
cd JS
python -m http.server
```
3. Then go and visit the associated page: `http://localhost:8000/`

You can read more about the design and implementation below - or read it here on my website: [Geographic Centre](https://www.archie-harrodine.com/projects/project.html?key=geographic-centre)

# Introduction
The Centre of N Points was my A-Level Computer Science coursework project, a weave of Mathematics and Computing to explore a problem that fascinated me. Given $n$ points in some space $S$, what is the point in $S$ that is equidistant from from all those points. Right now that seems vague and poorly defined, and thats because it is ! The original problem was spurred on from an issue me and my family were having: we are scattered across the UK, where would be a location to meet such that each party would have to travel an equal distance to travel to arrive at that location. Furthermore, what would be a location that would be an equal distance to travel whilst also minimizing the total distance that all parties have to travel. At the time, I was learning Djikstra's algorithm and A*; as well as learning the basics of 3D geometry and calculus. Thus, I pursued this problem for my A-Level project.<br><br>

This involved a deep exploration into mathematics and optimisation. The original project was created with PyQt5 for the interface; but later I engineered this to work on my website in Python (for a Flask server backend) and then in raw JavaScript. This achieved an A* for my A-Level coursework, and you can download the original word document I wrote [here](https://archie-harrodine.com/projects/geographic-centre/CentreOfNPoints.pdf). 

# Design
## Problem Breakdown
The original problem of finding a location of equal distance to travel to in our world was too defined and bounded by the complexities of real world travel. Thus, we abstracted away the information to reduce it to a more mathematical formulation. Given $n$ points ($\text{s.t.} n > 0$), we shall call vertices $\{\mathbf{v}_1, \mathbf{v}_2, \ldots \mathbf{v}_n\}$, in some space $S$, we want to find $\mathbf{c} \in S$, such that distance $\ell: S^2 \rightarrow \mathbb{R}$ between $\mathbf{v}_i$ and $\mathbf{c} = k \in \mathbb{R} \forall i$. When we refer to a space, we mean some way that the vertices can be traversed to one and other; for our purposes we look at three spaces: a graph $G=(V,E)$, continuous Euclidean $\mathbb{R}^n$ and polar $(r, \phi, \theta)$. <br> <br>

In our definition of what we are aiming for, it assumes that there is some singular distance $k$ that exists which is equal for all vertices to the centre. However, there isn't always a guarantee of this. Hence, we refraim this as a minimisation problem. Since the goal is to achieve equidistance, an equivalent idea is to have the distances be as similar as possible. Let us have the set of distances $k_1, k_2, \ldots k_n$ where $k_i = \ell(\mathbf{v}_i, \mathbf{c} )$ , ideally we want $k_1 = k_2 = \dots = k_n$ however in cases where this is not possible, we want them to be a close together as possible. There are a few possible metrics we could use for this, but the most apt is variance. 

$$\sigma = \frac{\sum_{i=0}^{n} (k_i - \mu)^2}{n} = \frac{\sum_{i=0}^{n} k_i^2}{n} - \left(\frac{\sum_{i=0}^n k_i}{n}\right)^2$$

Minimising the mean or median of the distances is also viable, however that is cluster centrality, as opposed to equidistance. Thus our goal is to find $\mathbf{c} \in S$ such that $\sigma$ is minimised.

## Discrete Graph
Let $G=(V,E)$, where vertex $\mathbf{v}_i, \mathbf{c} \in V$. We define distance $\ell(\mathbf{v}_a \rightarrow \mathbf{v}_b)$ as the sum of weights of the edges for a given path $P$ between vertices $\mathbf{v}_a$ and $\mathbf{v}_b$. If we do not impose restrictions though we run into issues. If we allow for any path between two vertices, there are infinitely many paths (due to cycles) and thus the distance is undefined. If we restrict to simple paths (no vertices visited more than once), then the problem becomes NP-Hard. This is because our objective now requires us to consider all paths. Lets consider the case of 2 vertices $\mathbf{v}_1, \mathbf{v}_2$ and a candidate centre $\mathbf{c}$. We want to find a simple path $P_1: \mathbf{v}_1 \rightarrow \mathbf{c}$ and $P_2: \mathbf{v}_2 \rightarrow \mathbf{c}$ such that the distances are as close to equal as possible, thus our goal is:

$$\min_{\mathbf{c}, P_1, P_2} (\ell(P_1) - \ell(P_2))^2$$

There are $|V|!$ possible simple paths for each vertex, and we would need to consider it for all pairs of vertices and all possible centres, so naively $O(|V|^2)$ for two vertices. While there may be better approaches with dynamic programming, we can see this problem likely is NP-Hard as we can reduce it to the problem "Is there a simple path of length $k$ between vertices $\mathbf{v}_a$ and $\mathbf{v}_b$" (the [longest path problem](https://en.wikipedia.org/wiki/Longest_path_problem)). Therefore, we impose another restriction, that we only consider shortest paths between vertices. This allows us to use Djikstra's or A* to compute the shortest path between two vertices in polynomial time. Thus our objective becomes:

$$\min_{\mathbf{c} \in V} \sigma(\{\ell_{sp}(\mathbf{v}_i, \mathbf{c}) | i = 1 \ldots n\})$$

Where $\ell_{sp}$ is the shortest path distance between two vertices. This can be computed in $O(n (|E| + |V| \log |V|))$ time using Djikstra's algorithm from each vertex to the candidate centre. For each vertex we run Djikstra's, and so each node gets a list of distances to each candidate centre. We can then compute the variance (or any other metric) in $O(n)$ time for each candidate centre. We considered this approach for implementation, however due to the costs of using Google APIs for geographic graph mapping data, we only implemented it on simple graphs. 

## Euclidean Space
Now looking at Euclidean space, we have  $\mathbf{v}_i \in \mathbb{R}^n$, where the distance between any two vertices is defined as $\ell(\mathbf{v}_a, \mathbf{v}_b) = ||\mathbf{v}_a - \mathbf{v}_b||_2$, aka Euclidean distance; or geometrically the shortest path in the space between the two vertices. This leads to a much clearer geometric interpretation, where we can see that $\mathbf{c}$ has near equal distance lines to each vertex. This can be further visualised in 2D as fitting a circle around the vertices; or a sphere in 3D. For our purposes we will be working with 2D. For $n=2$ we can easily see that the point of equidistance is $\mathbf{c} = \frac{1}{2}(\mathbf{v}_1 + \mathbf{v}_2)$, or the midpoint of a straight line between the two points. For $n=3$ we know that it is defined in 2 dimensions as any triangle can have a circle fitted to it, with its centre called the circumcentre. One method of finding the circumcentre is to take two sides of the triangle and to find their perpendicular bisectors - where the perpendicular bisectors meet is the circumcentre !

![Circumcentre diagram](./md/images/circumcentre.png)
*Diagram showing the circumcentre of a triangle.*

We can generalise this a bit further when considering a circle equation. For 2D, we have $(x-p)^2 + (y-q)^2 = r^2$, giving us 3 variables: $p,q,$ and $r$ to solve for. With 3 points, we can do this with ease. Where it becomes interesting is when we consider $n > 3$, as there is no guarantee that a circle fits the points perfectly. Continuining with the geometric interpretation, we can reframe this as an optimisation problem. 

$$
\begin{aligned} 
& (x-p)^2 + (y-q)^2 = r^2 \\
\Rightarrow & - 2px - 2qy + (p^2 + q^2 - r^2) + x^2 + y^2 = 0  \\
\Rightarrow & Ax_i + By_i + C + x_i^2 + y_i^2 \approx 0 \forall i\\
\Rightarrow & \min_{A,B,C} \sum_i \left( Ax_i + By_i + C + x_i^2 + y_i^2 \right)^2 \\
\Rightarrow & \frac{\partial f}{\partial A} = \sum_i 2x_i \left( Ax_i + By_i + C + x_i^2 + y_i^2 \right) = 0,\\
& \frac{\partial f}{\partial B} = \sum_i 2y_i \left( Ax_i + By_i + C + x_i^2 + y_i^2 \right) = 0,\\
& \frac{\partial f}{\partial C} = \sum_i \left( Ax_i + By_i + C + x_i^2 + y_i^2 \right) = 0, \\
\Rightarrow & \begin{bmatrix}
\sum x_i^2 & \sum x_i y_i & \sum x_i \\
\sum x_i y_i & \sum y_i^2 & \sum y_i \\
\sum x_i & \sum y_i & n 
\end{bmatrix} \begin{bmatrix}
A \\ B \\ C
\end{bmatrix} = - \begin{bmatrix}
\sum x_i (x_i^2 + y_i^2) \\ \sum y_i (x_i^2 + y_i^2)  \\ \sum (x_i^2 + y_i^2)
\end{bmatrix}
\end{aligned}
$$

Once we solve for $A, B,$ and $C$, we can do the following to get back our original equation:
$$
\begin{aligned} 
p = -\frac{A}{2}, \quad q = -\frac{B}{2}, \quad r = \sqrt{p^2 + q^2 - C}
\end{aligned}
$$

This gives explicit answers, though optimises the equation as opposed to circle fititng - the squares make it subject to outliers. Another approach is to instead optimize:

$$
\min_{p,q,r} \sum_{i} \left( \sqrt{(x_i - p)^2 + (y_i - q)^2} - r \right)^2
$$

Where we can solve this by performing gradient descent, or finding the Jacobian of the residual $J$ w.r.t all the points, and doing:

$$
\[p, q, r\]^{(i+1)} = \[p,q,r\]^{(i)} - (J^T J)^{-1} J^T \[d_1, \ldots, d_n \]^T
$$

These methods would be successful and work across our 2D plane! However, when we are considering our original goal, it aims to try and find a central location for people to meet on our planet, and famously our planet is not flat. Thus, we shift gears and take what we have learnt from working in Cartesian space, and apply it to a sphere with polar coordinates.

## Polar Space
Working on a sphere now introduces polar coordinates, which aligns with latitude and longitude. We consider a point to lie somewhere on a sphere, which has the radius of the planet, which we call $R$. This point can be represented in $(x,y,z) \in \mathbb{R}^3$ or we can use the polar coordinate $(R, \theta, \phi)$. $\varphi$ is latitude, and $\lambda$ is longitude; and relates to the polar coordinates with $\theta = \frac{\pi}{2} - \varphi$ and $\phi = \lambda$. This represents the angle of the vector from the origin in each axis. 

![Spherical Polar coordinates](./md/images/Spherical_polar_coordinates.png)
*Diagram showing spherical polar coordinates*

In this space, we can convert between polar and cartesian coordinates with:

$$
\begin{aligned} 
\text{Polar to Cartesian:} \\
x = R \cos \varphi \cos \lambda 
& \quad y = R \cos \varphi \sin \lambda 
& z = R \sin \varphi \\
\end{aligned}
$$

and

$$
\begin{aligned} 
\text{Cartesian to Polar:} \\ 
R = \sqrt{x^2 + y^2 + z^2} 
& \quad \theta = \arccos \frac{z}{R} 
& \phi = \text{atan2}(y,x) 
\end{aligned}
$$

While we work in this spherical space, we do not want to use Euclidean distance, and instead great-circle distance. This is the arcdistance between two points on the surface of a sphere, measured along the arc of a circle.

![Great circle](./geographic-centre/md/images/greatcircle.png)
*Diagram showing great-circle distance on a sphere.*

We can find this distance with both polar and cartesian coordinates. Let two points $\mathbf{v}_1, \mathbf{v}_2$ on the surface of the planet have latitude and longitude $(\varphi_1, \lambda_1)$ and $(\varphi_2, \lambda_2)$ respectively. We can find the angle between thme with:

$$
  \Delta \sigma = \arccos \left( \sin \varphi_1 \sin \varphi_2 + \cos \varphi_1 \cos \varphi_2 \cos|\lambda_1 - \lambda_2| \right)
$$ 

Or we can find the angle with their vectors $\mathbf{p_1}, \mathbf{p_2}$:

$$
\begin{aligned}
\Delta \sigma &= \arccos(\mathbf{v}_1 \cdot \mathbf{v}_2) \\
&=  \arcsin|\mathbf{v}_1 \times \mathbf{v}_2| \\
&= \arctan\left( \frac{|\mathbf{v}_1 \times \mathbf{v}_2|}{\mathbf{v}_1 \cdot \mathbf{v}_2} \right)
\end{aligned}
$$

We then multiply the angle by $R$ to get the arcdistance. With our distance defined we can use it to solve the problem that we have. For $n=2$, we can solve directly. The approach we used was taken from [this website](https://www.movable-type.co.uk/scripts/latlong.html), which throughout was a useful point of reference to learn about arcdistances. We can find the latitude and longitude of the midpoint $(\varphi_m, \lambda_m)$ like so:

$$
\begin{aligned}
B_x &= \cos \varphi_2 \cos |\lambda_1 - \lambda_2| \\
B_y &= \cos \varphi_2 \sin |\lambda_1 - \lambda_2| \\
\varphi_m &= \text{atan2}\left( 
  \sin \varphi_1 + \sin \varphi_2, 
  \sqrt{\left( \cos \varphi_1 + B_x \right)^2 + B_y^2} \right) \\
\lambda_m &= \lambda_1 + \text{atan2}\left( B_y, \cos \varphi_1 + B_x\right)
\end{aligned}
$$

For $n=3$, this introduced a new challenge. Considering the complexity of the above formula, I was concerned that it would sprial into a confusing mess of algebra, however thats where I shifted my approach to think similar to how we solved this in 2D Euclidean. There, we took the perpendicular bisectors of the triangle, and looked at where they met. We can apply a similar logic. We construct a triangular prism by defining planes between our vertices $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3 $. By choosing two sides of the prism, we can find the perpendicular planar bisectors between them. Where those planes meet will be a line that passes through the sphere, and where that line crosses the sphere is the point of equidistance. 

We make a plane $P_{1,2}$ between $\mathbf{v}_1$ and $\mathbf{v}_2$ with $(\mathbf{v}_1 \times \mathbf{v}_2) \cdot \mathbf{x} = 0$. We can then find a perpendicular plane at its centre by taking the cross product of the plane with a vector on the centre line, which is just $\frac{1}{2}(\mathbf{v}_1 + \mathbf{v}_2)$, hence we can make the two perpendicular planes $P_{1,2}^{\perp}$ and $P_{1,3}^{\perp}$ with:

$$
\begin{aligned}
P_{i,j}^{\perp}&: \left( (\mathbf{v}_i \times \mathbf{v}_j) \times \frac{1}{2}(\mathbf{v}_i + \mathbf{v}_j) \right) \cdot \mathbf{x} = 0 \\
&: \mathbf{d}_{i,j} \mathbf{x}= 0 \\
&: a_{i,j}x + b_{i,j}y + c_{i,j}z = 0
\end{aligned}
$$

With two planes, we need to find the line where they intersect. Since it passes through the origin, we can simply parameterize a vector by $t$; so $x=t, y=ty_c, z=tz_c$, letting our directional vector be $(1, y_c, z_c)$. Plugging this into our line equations we get:

$$
a_{1,2} + b_{1,2}y_c + c_{1,2}z_c = 0 \\
a_{1,3} + b_{1,3}y_c + c_{1,3}z_c = 0 
$$

This is a linear system of equations, where we can solve for $y_c$ and $z_c$ with:

$$
\begin{aligned}
y_c &= - \left( (a_{1,2} c_{1,3} - a_{1,3} c_{1,2}) / (b_{1,2} c_{1,3} - b_{1,3} c_{1,2}) \right) \\
z_c &= - \left( (a_{1,2} b_{1,3} - a_{1,3} b_{1,2}) / (b_{1,2} c_{1,3} - b_{1,3} c_{1,2}) \right)
\end{aligned}
$$

This defines our line of intersection, and we can use it to calculate where it intersects our sphere of radius $R$. 

$$
\begin{aligned}
t_c &= 1 + y_c^2 + z_c^2 \\
t &= \frac{R}{\sqrt{t_c}}
\end{aligned}
$$
Thus our midpoint on the surface is 

$$
\mathbf{c} = \left[ t, ty_c, tz_c\right]^{T}
$$

Which we can convert back into latitude and longitude if we so desire. This method works for 3 points, and shows how working in the cartesian world is powerful when polar coordinates become too difficult. Now for $n > 3$ we have a similar problem to Euclidean space, where there is no guarantee of a point of equidistance. Hence, we have to find a point that minimises the variance of distances. Using our distance formulas from earlier, we consider some hypothetical centre $\mathbf{c}$ and list of vertices $\mathbf{v}_1, \mathbf{v}_2, \ldots \mathbf{v}_n$, and we want to minimise the variance of the distances between them. We could work in polar coordinates, however the distance equation is large, complex and poorly defined for certain values, so we instead look at the arcdistance equations with our vectors. We get the following: 

$$
\sigma^2(\mathbf{c}) = \frac{1}{n}\sum_{i=1}^{n} \arctan\left(\frac{|\mathbf{v}_i \times \mathbf{c}|}{\mathbf{v}_i \cdot \mathbf{c}}\right)^2 - \frac{1}{n^2}\left(\sum_{i=1}^n \arctan\frac{|\mathbf{v}_i \times \mathbf{c}|}{\mathbf{v}_i \cdot \mathbf{c}} \right)^2
$$

We use $\arctan$ because there are no invalid values. $\arccos$ and $\arcsin$ fail outside of $[-1,1]$, so $\arctan$ gives us additional stability when solving this problem. We need to minimize variance $\sigma^2$, which we can do with stochastic gradient descent:

$$\mathbf{c}^{(t+1)} = \mathbf{c}^{(t)} - \alpha \frac{\partial}{\partial \mathbf{c}}\sigma^2(\mathbf{c}^{(t)})$$

Thus we need to take the derivative of that monster of an equation. So, let me break it down for you Mark. We break it into pieces we can use for a larger chain rule. 

$$
\begin{aligned}
\ell &= \arctan(u) & u &= v/w \\
v &= |\mathbf{v}_i \times \mathbf{c}| & w &= \mathbf{v}_i \cdot \mathbf{c}
\end{aligned}
$$

With our pieces, we proceed to take their derivatives with respect to $\mathbf{c}$:

$$
\begin{aligned}
\frac{\partial w}{\partial \mathbf{c}} &= \mathbf{v}_i \\
\frac{\partial v}{\partial \mathbf{c}} &= \frac{1}{\left| \mathbf{v}_i \times \mathbf{c} \right|} \begin{bmatrix}
y_i^2 + z_i^2 & -x_i y_i & -x_i z_i \\
-x_i y_i & x_i^2 + z_i^2 & -y_i z_i \\
-x_i z_i & -y_i z_i & x_i^2 + y_i^2 
\end{bmatrix} \mathbf{c} = \frac{1}{\left| \mathbf{v}_i \times \mathbf{c} \right|} K_i \mathbf{c} \\
\Rightarrow \frac{\partial u}{\partial \mathbf{c}} &= \frac{1}{(\mathbf{v}_i \cdot \mathbf{c})^2} 
\left[ \frac{\mathbf{v}_i \cdot \mathbf{c}}{| \mathbf{v}_i \times \mathbf{c} |} K_i \mathbf{c} - \mathbf{v}_i | \mathbf{v}_i \times \mathbf{c} | \right] \\
\Rightarrow \frac{\partial \ell}{\partial \mathbf{c}} &= \frac{\partial u}{\partial \mathbf{c}} \cdot \left( \frac{1}{1+\left(\frac{|\mathbf{v}_i \times \mathbf{c}|}{\mathbf{v}_i \cdot \mathbf{c}}\right)^2} \right)
= \frac{\partial u}{\partial \mathbf{c}} \cdot \left( \frac{(\mathbf{v}_i \cdot \mathbf{c})^2}{(\mathbf{v}_i \cdot \mathbf{c})^2 + |\mathbf{v}_i \times \mathbf{c}|^2} \right) \\
&= \frac{1}{(\mathbf{v}_i \cdot \mathbf{c})^2 + |\mathbf{v}_i \times \mathbf{c}|^2} \left[ \frac{\mathbf{v}_i \cdot \mathbf{c}}{| \mathbf{v}_i \times \mathbf{c} |} K_i \mathbf{c} - \mathbf{v}_i | \mathbf{v}_i \times \mathbf{c} | \right] \\
&= \frac{1}{|\mathbf{v}_i|^2|\mathbf{c}|^2} \left[ \frac{\mathbf{v}_i \cdot \mathbf{c}}{| \mathbf{v}_i \times \mathbf{c} |} K_i \mathbf{c} - \mathbf{v}_i | \mathbf{v}_i \times \mathbf{c} | \right] \\
\Rightarrow \frac{\partial \\\sigma^2}{\partial \mathbf{c}} &= 
\frac{2}{n}\sum_{i=1}^n \frac{\partial \ell}{\partial \mathbf{c}} \arctan\left(\frac{|\mathbf{v}_i \times \mathbf{c}|}{\mathbf{v}_i \cdot \mathbf{c}}\right) - 
\frac{2}{n^2}\left(\sum_{i=0}^n \frac{\partial \ell}{\partial \mathbf{c}} \right) 
\left( \sum_{i=0}^n \arctan\left(\frac{|\mathbf{v}_i \times \mathbf{c}|}{\mathbf{v}_i \cdot \mathbf{c}}\right)\right)
\end{aligned}
$$

This beautiful equation gives us a $3\times 1$ vector, describing the derivative of the variance in each axis. This is what we use in our SGD, where we found that a nice intial value of $\mathbf{c}^{(0)}$ is the average of the latitude and longitudes, generally placing it within the goal. In terms of effeciency, each iteration we use calculate our breakdown terms, as we can just reuse them throughout the equation, reducing the number of terms we actually need to calculate. 

$$
\begin{aligned}
\mathbf{s}_i &= \frac{1}{v^2 + w^2} \left[ \frac{w}{v} K_i \mathbf{c}^{(t)} - v \mathbf{v}_i \right] \\
\mathbf{c}^{(t+1)} &= \mathbf{c}^{(t)} - \alpha \left(
\frac{2}{n}\sum_{i=1}^n \mathbf{s}_i \ell  -
\frac{2}{n^2}\left( \sum_{i=0}^n \mathbf{s}_i \right) \left( \sum_{i=0}^n \ell\right)
\right)
\end{aligned}
$$

We repeat this from $\mathbf{c}^{(0)}$ until we either converge to a degree of tolerance, or it diverges or enters a cycle. It is worth noting that after each iteration, we normalise $\mathbf{c}^{(t+1)}$ such that $||\mathbf{c}^{(t+1)}|| = R$, this way we remain on the surface of the planet. We effectively reproject our point back onto the planet.

# Implementation
When I originally created this for A-Levels, my solution focused on implementing the applied world approach, over the Graph or Euclidean solutions. I used PyQT5 to create an interface, and the GoogleMaps API to make queries between locations.Turns out that when left alone that is expensive and highly not worth it (accidentally nearly owed them £2000!). When I recreated the project, I switched to use a web interface with JavaScript and Leaflet, that used a Flask backend to rig it directly to my previous code. This was later reworked to just use JavaScript, to remove any reliance on a server. <br> <br>

We broke down the problem to use two main classes of a \`Point\` and a \`Calculator\`. The \`Point\` class was used to easily work between Cartesian coordinates; latitude/longitude; and addresses. This was users could enter either an address or a latitude/longitude, and then it would find out all the other information by calculating it out. This way we could easily do different operations between points, and functions can take them in with all the information prepared for solving it, regardless of the mechanism ($n=2, n=3$ or $n > 3$). The \`Calculator\` was a static class which contained all the functions to go and solve the midpoints. This included many helper functions as well. The most important improvements I made was to minimise the number of repeated operations. We maintained several arrays that contained the dot product, the absolute cross product, etc. so that we could easily reference them multiple times, and only calculate each term once. We also stored the points we found, so that we could display them honing in on the target point as it converges, which makes it look quite a bit more pretty. <br> <br>

These classes would be used to communicate with the interface, displaying the info with a GoogleMaps inspired map. We implemented several views, including satellite and street, which gave the user a bit more customisability. The method to enter the points was simple, either using latitude/longitude or an address could be searched, and if it was found it would be used. <br> <br>

We also implemented an option to instead minimize the mean distance, as opposed to the variance. This finds a more central location, but more importantly minimizes the total travel distance. This is useful if the goal is to reduce overall travel, as opposed to making it equal for all parties. We also experimented with a third option, which uses a weighted addition of both variance and mean distance, allowing the user to balance between equidistance and total distance. <br> <br>
Here is a screenshot of the original implementation: 

![Original implementation](./md/images/example.png)
*Original Python implementation using PyQT5 and Google Maps API.*

And here is a screenshot of the JavaScript implementation:

![Leaflet implementation](./md/images/example2.png)
*Updated JavaScript implementation using Leaflet.*

# Evaluation
For my A-Level project this was very successful! I managed to achieve an A* grade, and I learnt alot about mathematics, geometry and calculus. It was both enjoyable and really interesting to explore the problem and solve it from the ground up. This was before I was in University, with access to many resources, or knowing what to search or look into - thus I spent days in my classroom drawing circles and spheres, trying to calculate formulas and understanding what equidistance means. The moment I stumbled across the idea of optimisation with derivatives changed the game entirely, and it was me figuring out what optimisation is by myself - it was meaningful and felt like true learning! It was a challenging but rewarding experience, and I am proud of the work I did. <br> <br>

For this project, when I revisited it, it was nice to work it into the web, showing the skills I had picked up across my university life. It was a fun project to reimplement, and I enjoyed the challenge of optimising the code to run efficiently in JavaScript. It was also interesting to see how much I had learnt about structuring code and engineering software since my A-Levels. Overall, I am pleased with how this project turned out, and it remains a personal favourite of mine. Especially for all of that MATHS!! <br> <br>

There are still many features that I would love to implement ! 
- Implementing the graph based solution, using real world road data, and Djikstra's algorithm to find shortest paths, to then find the point of minimum variance.
- Adding more interactivity to the map, such as being able to drag points around and see the centre update in real-time.
- Allowing for more complex weighting schemes, such as giving certain points more importance in the calculation.
- More visualisations, such as showing the circles of equal distance around the centre point.
- 3D rendering of the Earth and points, to better visualise the problem in its true form.
- Options for minimisation goal: with variance, mean, median, range, etc.
- Better convergence detection, such as adaptive learning rates, or momentum based approaches. 
- Proof of convergence for the $n > 3$ cases. This would involve showing that $\lim_{t\to\infty} ||\mathbf{c}^{(t+1)} - \mathbf{c}^{(t)}|| = 0$  