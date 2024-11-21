# Interactive AGS

The initial Algebraic Graph Statics (AGS) publication (Van Mele et al., 2014) has been succeeded by studies focusing on a bi-directional modification: modifying the force diagram and updating the form diagram (Alic et al., 2017) and modifying both diagrams based on user-defined sets of constraints (Maia Avelino et al., 2021). The following chart illustrate these extensions:

![](../.gitbook/assets/iags\_diagrams-03.png)

We focus on the contributions of these two extensions below:

**b) Bi-directional AGS:** On this extension the form diagram is updated after geometric variations are imposed in the force diagram. The Newton's method is used to update iteratively the position of the form diagram. The optimisation the minimises the residual reflecting the how far the new form diagram is from generating the imposed force diagram. The Jacobian Matrix to guide the modifications on the form diagram nodal position is computed analytically. This enables the update of the form diagram for precisely executed movements on the force diagram.

**C) Interactive AGS:** On this extension the solving of the equilibrium is done geometrically, by guaranteeing that the diagrams are reciprocal. The update can, therefore, happen in both directions within the same framework (form->force and form<-force). Aditionally constraints are imposed to both diagrams and a simultaneously modification (form<->force) is possible based on force target constraints and orientation constraints.

IGS is an implementation of **c)**. The constraints of IGS are properly defined in the [constraints in IGS](constraints-in-igs.md) page. The examples of the [funicular arch](../examples/2..md) and [constant force truss](../examples/wip-gable-truss.md) explore how theese constraints can be assigned and the equilibrium can be updated from the constraints defined by IGS.

More theoretical background is available in the references below.

## References

Van Mele, T., & Block, P. (2014). Algebraic graph statics. _CAD Computer Aided Design_, _53_, 104–116. [https://doi.org/10.1016/j.cad.2014.04.004](https://www.sciencedirect.com/science/article/pii/S0010448514000682?via%3Dihub)

Alic, V., & Åkesson, D. (2017). Bi-directional algebraic graphic statics. _CAD Computer Aided Design_, _93_, 26–37. [https://doi.org/10.1016/j.cad.2017.08.003](https://www.sciencedirect.com/science/article/pii/S0010448517301446)

Maia Avelino, R., Lee, J., Van Mele, T., & Block, P. (2021). An interactive implementation of algebraic graphic statics for geometry-based teaching and design of structures. _International Fib Symposium - Conceptual Design of Structures 2021_, 447–454. [https://doi.org/10.35789/fib.PROC.0055.2021.CDSymp.P054](https://doi.org/10.35789/fib.PROC.0055.2021.CDSymp.P054)
