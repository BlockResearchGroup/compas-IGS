---
description: >-
  This example shows how perform addititonal modifications to the Maillart Truss
  my bodifying the force diagram "by hand"
---

# Manual Force Control

On this tutorial we will study modifications to the Maillart's truss geometry that are achieved by modifying the force diagram and observing the new geometry obtained in the structure. The initial geometry is depicted below

![](<../.gitbook/assets/image (161).png>)

This geometry is form-found for a uniformily distributed load case and the steps to find this are available in the [Maillart Truss](2.-maillart-truss.md) tutorial.

In this tutorial will assume that the load applied in the truss is a total of 50 kN, being **10 kN** at each node.

### 1. Creating Form and Force Diagram

As in the previous tutorials we draw the forces and reactions as edges and the input form diagram looks like the image below:

![](<../.gitbook/assets/image (172).png>)

This topology requires only one independent edge, which can be checked with the function `Check DOF`. By selecting one of the applied loads (in the figure below the central force was selected) and applying the force of **-10kN** the following form and force diagrams are retrieved:

![](<../.gitbook/assets/image (95).png>)

### 2. **Controlling forces on top chord using the Force Diagram**

In this section derive the form in response to specific force constraints, or in other words, modify the `ForceDiagram`and update the `FormDiagram`.&#x20;

Suppose that the structural designed realised that the force magnitude in the elements of our initial design of the Maillart's Roof is too high (**79kN**) and we need to propose alternate designs having this maximum force reduced incrementally, to 70 kN, 60 kN, and 50 kN. Besides reducing the magnitude of the constant force, we should keep the slope of the roof untouched, i.e. the upper chord should be fixed. We will tackle such a problem with graphic statics, and for solving it, we need to **change the geometry** of the **force diagram**:

First, we find the members with the highest force magnitude in both diagrams, corresponding to the upper chord of the truss. Here, these edges have the force 79 kN and are highlighted in the image below:

![](<../.gitbook/assets/image (7).png>)

Before we modify them in the ForceDiagram, we should properly fix the vertices in the form diagram that we intend to keep fixed. Click the `Fix FormDiagram Nodes` button in the toolbar fix the top chord nodes as in the figure below:&#x20;

![](<../.gitbook/assets/image (124).png>)

After finding the right edges in the ForceDiagram and set proper constraints in the FormDiagram, we can modify the ForceDiagram, to shorten the length of the edges in the ForceDiagram.&#x20;

The inclination of the top chords must remain the same since we want the slope on the roof to remain unchanged. Therefore, the nodes in the Force Diagram will move along the original direction of the edges. The right ends of these edges are connected to the edges of external loads and they should not be modified. Thus, we move the nodes on the left side. Draw a line of 70 kN as a reference in the ForceDiagram (step 1). Suppose the struts connecting top and bottom chords should be kept vertical, then all the left nodes would still be in one vertical line after being moved. Draw a vertical guideline, which intersects with the left line (step 2). Now move the vertices along the original edge until the guideline. (step 3, step 4). Last but not least, update the FormDiagram.

![](<../.gitbook/assets/image (52).png>)

![](<../.gitbook/assets/image (29).png>)

Once the Form Diagram is updated it will look like in the pictures below. The reduction in the forces in the structure resulted in an increase in the depth of the truss. (The original bottom chord is shown in grey).

![](<../.gitbook/assets/image (111).png>)

We continue and move the left-extreme nodes in the force diagram further inside, in order to reduce the length of the segments dual to the upper chord, now to a maximum of 60 kN. The new structure is depicted below:

![](<../.gitbook/assets/image (85).png>)

To finish, we repeat the procedure to a maximum force of 50 kN and the result is shown below.

![](<../.gitbook/assets/image (121).png>)

As the truss goes deeper, the forces in the members are reduced. The last iteration shows a geometry quite similar to the one presented in the Chiasso Shed, displayed in the next image. Reducing these loads to save up in concrete and reinforcement was certainly present in the original design iterations by Robert Maillart.

![](<../.gitbook/assets/image (139).png>)

### **3. Controlling forces on bottom chord using the Force Diagram**

Last, we can also modify the structure such as the forces are constant in the bottom chord instead of in the top members. This would present structural interest especially in the case where the structure would have a cable running beneath, instead of concrete beams, because in this way the force carried by the cable would be the same all over the structure.

We first apply the same set of constraints to the nodes on the upper part of the roof. This guarantees that they won't move as we update the force diagram.

Then, we identify that the bottom elements have a radial distribution in the force diagram. If we want all these elements to have a constant force they must all be contained within a circumference having a similar length. Here we draw the circumference that in our scales matches the radius with 40 kN. And we move all nodes to coincide with the intersection between the circle and the original compressive members, as in the image below.&#x20;

![](<../.gitbook/assets/image (42).png>)

Then, we update the Form Diagram and the equilibrium looks like the following:

![](<../.gitbook/assets/image (148).png>)

Verify using one of the functions available in `Inspect Diagrams` to check that the bottom chord in the structures has indeed a constant force of 40 kN as highlighted in the picture below:

![](<../.gitbook/assets/image (176).png>)
