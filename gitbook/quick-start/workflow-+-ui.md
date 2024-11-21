# Workflow + UI

## IGS Workflow

The main elements of the general workflow are available in the toolbar and listed here:

![](<../.gitbook/assets/image (123).png>)

### 0. Initialisation

Before start working with IGS the plug-in needs to be initialised. Also functions to save and load session `.igs` files are available.

### 1. Create Form Diagram

The form diagram represents the members of a two-dimensional structure. These members carry axial forces (compression and tension). A particularity of IGS is that forces and reactions need to be drawn as edges in the diagrams. Hence, there a diagram is composed of **internal edges** and **leaf edges**. The former represents the internal members of the structure and the latter the imposed loads and reaction forces.

### 2. Assign Forces and Supports

After creating thee force diagram forces should be assigned to the structure. However, they can not be selected freely to all mebers. The number of edges to select corresponds to the degree-of-freedom of the initial form diagram. These edges are called **independent edges** and the button Check DOF can give you information about how many edges must be selected. Supports can also be assigned to vertices of the diagram.

### 3. Compute Force Diagram

The force diagram represents the equilibrium of the nodes in the form diagram. Both diagrams are reciprocal. This means that they have the same number of edges and each edge in the form diagram corresponds to a reciprocal edge in the force diagram. Besides, these edges are parallel, and the length of the edge in the force diagram corresponds to the magnitude of the force in the form diagram. Also, each vertice in the form diagram is represented by a closed polygon in the force diagram, that represents the equilibrium in that node. Similarly, each polygon in the form diagram can be represented by a vertex in the force diagram.

### 4. Unidirectonal Update

* **Modify Form Diagram:** Modifying the geometry of the structure, after forces are assigned and a first force diagram is computed, allows to study how different geometries will modify the equilibrium.
* **Modify Force Diagram:** The equilibrium can also be modified inversely. A modification can be performed in the force diagram, inducing a change in the form diagram. This can be used to form find structures for specific force constraints, or force intents.

### 5. Constraints and bi-directional Update

IGS also allow for automatic modifications of the form and force diagram based on user-assigned constraints. These constraints can be applied to the edges or vertices of the diagram.

* **Edge constraints:** allow to constraint the magnitude of the forces, and/or heir orientation. These constraints are assigned to the form diagram and are reflected to the force diagram.
* **Vertex constraints:** allow to constraint vertices to remain in a line, or consraint the vertices to be fixed (supports). Can be assigned to both diagrams.

It is important to know that the bi-directional solver is interative and will try to respect at most the constraints. However, for a given set of constraints the problem must be also infeasible and therefore it is important to select them carefully.

### 6. Structual information

Inspectors are available to get information about the forces within the structure and the constraints that are applied. Aditionally a measure of the efficiency/volume of material required to build the structure is given with the measure of the Loadpath.

### 7. Visualisation

The diagrams can have their display settings modified to serve specific purposes.

## IGS User Interface (UI) <a href="#rhinogs-user-interface-ui" id="rhinogs-user-interface-ui"></a>

There are three ways of accessing the functions and features of IGS:

* IGS dropdown menu (all functionalities and features available)\*
* IGS toolbar (most functionalities and features available)\*
* IGS list of commands (all functionalities and features available)

\*Note that the menu and toolbar are only available for IGS on Windows.

### 1. IGS Menu <a href="#id-1-rv2-menu" id="id-1-rv2-menu"></a>

The IGS menu is organised in the sequential order of the workflow steps. The IGS menu includes all available functions and features of IGS, and it is deepicted below:

![](<../.gitbook/assets/image (40).png>)

### 2. IGS Toolbar <a href="#id-2-rv2-toolbar" id="id-2-rv2-toolbar"></a>

The IGS toolbar is also organised in the sequential order of the workflow steps. The IGS toolbar includes most of the available functions and features of the plugin.

![](<../.gitbook/assets/image (103).png>)

### 3. IGS list of commands <a href="#id-2-rv2-toolbar" id="id-2-rv2-toolbar"></a>

The list of all commands of IGS (present in the toolbar or in the menu) is available in the [command API](../documentation/command-api.md).
