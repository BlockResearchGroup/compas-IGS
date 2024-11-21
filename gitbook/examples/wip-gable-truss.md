---
description: >-
  This example shows how to find the geometry of a truss with top constant force
  by setting constraints to form and force diagram.
---

# Constant-force truss

This example deals with the following non-triangulated truss:

![](<../.gitbook/assets/image (46).png>)

This truss was form found to a equally distributed load which we will assume here as **10 kN** at each node. We want to compute the equilibrium and generate the force diagram for this structure and perform bi-directional modifications with IGS.

### 1. Form Diagram with loads and support

We input the FormDiagram with the function `Create FormDiagram` using the lines provided in the Rhino file, applied loads and reactions are translated as lines in the diagram. The result look like this:

![](<../.gitbook/assets/image (101).png>)

Now we assign loads with the button `Assign Forces`. This predefined shape allows the selection of only one independent edge. We select one of the edges representing the applied loads and assign the load **+10**. Here edge #13 was selected.

![](<../.gitbook/assets/image (186).png>)

We press OK and validate the sign of the applied load, we must also restraint the two extremities vertices assigning it as supports/anchors using the button `Identify Anchors`. The result will look like the following image:

![](<../.gitbook/assets/image (33).png>)

With this information updated we can go to the drawing of the Force Diagram.

### 2. Drawing of the Force Diagram

We press the button `Create Force Diagram` which generated the ForceDiagram highlighted in the following image. We observe that the force 10 kN is not only applied to the edge selected as independent but also to the other applied loads. Therefore the input geometry was already form-found to such load case. The reaction forces are ballanced on the vertical 20 kN at each support.

![](<../.gitbook/assets/image (120).png>)

Anoter particularity of this solution is that the bottom chord has constant tensile force equals 31.2 kN (edges 0, 1, 5, 16, 18) while in the upper chord the forces vary from  37.1 kN (edges 20, 10) to 31.2 kN (edge 9). The following can be observed with the tools available over the `Inspect Diagrams` function, such as the `EdgesTable` shown below:

![](<../.gitbook/assets/image (44).png>)

On the next section we will impose constraints to form find the truss such as the edges in the top chord have constant force equals 30 kN.

### 3. Impose constraints to the problem.

We will apply the required constraints in 4 steps:

First, the default constraints are applied affecting the leaf edges (loads and reactions) and the vertices connected to it. This can be done pressing the button `Apply Default Constraints`.

![](<../.gitbook/assets/image (166).png>)

Second, we assign target forces to the top chord. In the button `Assign edge constraints` over the option `ForceMagnitude` we assign 30 kN to edges 7, 9, 10, 11, 20.

![](<../.gitbook/assets/image (99).png>)

Third, multiple solutions for a constant top chord exist, in this tutorial we will intially look for the one which keep the bottom chord flat. To do that we click once more to the `Assign edge constraint` button over the option `EdgeOrientation` and select edges 0, 1, 5, 16, 18 in the bottom chord. The display should look like below:

![](<../.gitbook/assets/image (45).png>)

Finally, to preserve the load case we assign target edges also to the applied loads. On the function `Assign edge constraints` option `ForceMagnitude` we assign 10 kN to the applied loads. The result look like below:

![](<../.gitbook/assets/image (57).png>)

Once the constraints above are set we can go to the bi-directional update of the form and force diagrams.

### 4. Bi-directional update

To update the diagrams, we click on the button `Update both diagrams`. The result is depicted below:

![](<../.gitbook/assets/image (117).png>)

On the image below we see the overlap of the initial and final solutions. The dual edges of the top chord need to be moved to a circle with radius equals 30 kN. The modifications that would have to be done manually are displayed in the next Figure:

![](<../.gitbook/assets/image (138).png>)

### 5. Additional modifications

One additional modification will be performed. The top and bottom chord are constrained to the same target force 30 kN. As a consequence the bottom chord can no longer be flat. Therefore we remove that constraint and assign target edges to the bottom chord. The final state of the constraints applied should look like below:

![](<../.gitbook/assets/image (51).png>)

Now, we can apply the update to form and force diagrams and the result is the double constant truss below:

![](<../.gitbook/assets/image (81).png>)

### 5. Advanced visualisation

To finalise we show a few advanced visualisations available in IGS. On the settings menu the diagram can be rotated of 90 degrees. In this way when the diagrams are in equilibrium the form and force corresponding edges are perpendicular to each other instead of parallel. The figure below shows how to activate this function on the ForceObject Settings.

![](<../.gitbook/assets/image (105).png>)

An extra visualisation is available with the Unified Diagram. This diagram unifies form and force diagram in the same plot. Different unified diagrams can be drawn for different values of alpha. Alpha is de parameter that changes the shape of the unified diagram to follow form or force. On the figure below you see the final example of this page with the unified diagram for different alphas.&#x20;

![](<../.gitbook/assets/image (34).png>)

That's it!
