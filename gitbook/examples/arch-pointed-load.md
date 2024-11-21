---
description: >-
  This example shows how an additional pointed load modifies the geometry of a
  funicular arch and how this additional load affect a triangulated structure.
---

# Arch pointed load

## 1. Funicular Arch&#x20;

The initial drawing is composed of  15 edges. The reactions and loads are drawn explicitly, according to the instructions from the [tutorial](../quick-start/tutorial.md). The cable is composed of straight edges, and these represent a discretisation of parabola shape.&#x20;

![](<../.gitbook/assets/image (68).png>)

If we `Check DOF`, we see that such a structure needs only one independent edge. This is related to the fact we are working with a funicular structure, which has its geometry already shaped according to the forces applied. The resultant form and force diagram are depicted below:&#x20;

![](<../.gitbook/assets/image (20).png>)

As mentioned in the previous classes, a structure is only funicular to a specific load case, therefore, the parabola arch in this section is only "funicular" for an equally distributed load. If we must add a new pointed load on the 4th load applied we must apply it as constraints. The default constraints are applied and target forces of 10 kN and 30 kN are applied as depicted in the figure below. The bi-directional update is executed and the result is also depicted.&#x20;

![](<../.gitbook/assets/image (69).png>)

![](<../.gitbook/assets/image (73).png>)

We see that the geometry of the arch is modified to accomodate the new load. This is similar to the case of a hanging chain subjected to a concentrated (larger) weight.

## 2. Triangulated Arch&#x20;

Now we look to the case that the the structure is properly triangulated (rigid). It can now take any externally applied load, i.e. the externally applied load is not associated with the structure's form. The following structure presents a triangulated version of the arch that can take any load since it now requires 5 independent edges (the value of 5 forces can be chosen freely/independently). Here we add an additional load to one of the nodes of the arch. Unlike the previous class, the structure is rigid, therefore the shape of the structure is not affected by the additional force, only the magnitude of the internal forces is increased.

![](<../.gitbook/assets/image (183).png>)
