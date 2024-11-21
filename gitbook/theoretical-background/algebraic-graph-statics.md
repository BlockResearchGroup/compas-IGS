# Algebraic graph statics (AGS)

## Motivation for algebraic construction of reciprocal diagrams

Despite its strengths, computerised (interactive) graphic statics still has some drawbacks. The process of constructing drawings can easily become tedious and time-consuming and demands a profound familiarity with the specific geometric constructions involved. Furthermore, since the drawings produced by the CAD tools and interactive implementations are generated in a procedural manner according to the corresponding graphic statics ‘‘recipe’’, they tend to be designed for specific types of structures. Modifications to the initial setup of the drawing (e.g. the number and/or connectivity of structural elements, order of the loads, ...) thus require a complete redraw of the entire construction. Although the process of making a graphic statics construction is important for teaching and learning, as it helps to get familiarised with the specific geometric and structural relationships between different elements of such construction, it is clear that it is inconvenient for research or practical \[and design] purposes."

![Figure 1: Procedural graphic statics, from form to force diagrams.](<../.gitbook/assets/image (185).png>)

Algebraic Graph Statics (AGS) a method to encode the graphical information from GS in an algebraic description. The graphical link between the form and force diagrams (i.e. the diagrams need to be reciprocal) can be translated algebraically using the mathematical description for graphs. The figure below is an example of a single panel truss analysed with AGS:

![Figure 2: Form and Force diagram of a single panel truss (Van Mele et al., 2014)](<../.gitbook/assets/image (104).png>)

AGS allows for the generation of force diagrams for properlly loaded form diagrams representing structures. This opens the possibilites of inserting the data of a real structure, with its boundary conditions to the datastructure of AGS to compute its equilibrium.

![Figure 3: From structure to form and force diagrams.](<../.gitbook/assets/image (179).png>)

## References

Van Mele, T., & Block, P. (2014). Algebraic graph statics. _CAD Computer Aided Design_, _53_, 104–116. [https://doi.org/10.1016/j.cad.2014.04.004](https://www.sciencedirect.com/science/article/pii/S0010448514000682?via%3Dihub)
