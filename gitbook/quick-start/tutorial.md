# Tutorial

This tutorial focus on the analysis of a single panel truss with the geometry, loads and support conditions described below:

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FkJb8j7MKBeFBgdS4LByN%2Fimage.png?alt=media\&token=c887bf8c-ef7b-4308-9403-7ba582246ba8)

The hypothesis of our analysis will be:

* The force applied on the top has magnitude of **10 kN**.
* The left support is a pin (restraint on x, y) and the right support a roller (restraint on y).

The set of lines for this exercise is available in the previous page. As mentioned before, the load (blue) and reaction directions (green) are repressented as lines:

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2Fra2qMBdUYdaB7Kucjo8v%2Fimage.png?alt=media\&token=812d7628-2e7f-4660-b788-9e4c6db59e1a)

### 0. Initialise the plug in <a href="#id-1.-making-the-form-diagram" id="id-1.-making-the-form-diagram"></a>

In the toolbar of IGS go to the buton `Initialise IGS` and initialise the session. This activate IGS commands. You should see a screen like the one below in which you should press yes to the [Terms & Conditions](../additional-information/legal-terms.md).

![](<../.gitbook/assets/image (133).png>)

### 1. Making the Form Diagram <a href="#id-1.-making-the-form-diagram" id="id-1.-making-the-form-diagram"></a>

In the toolbar of IGS go to the function `Create Form Diagram` and select the option `FromLines`. The FormDiagram will be created and you can notice a difference in the colour of **internal edges** (structure) and **external edges** (loads and reactions).

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FpxPRKkwWJXSRYEnbjdzo%2Fimage.png?alt=media\&token=e12fb1e4-b770-474b-aef8-7d9d05d0d470)

The Form Diagram edges will be stored in a new layer created, at `IGS >> FormDiagram`. The future Force Diagram will also be drawn in the dedicated created layer `IGS >> ForceDiagram`.

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2F65RGYV4SUBgiz8w7Y0Uk%2Fimage.png?alt=media\&token=a1ad65b2-8d33-4e8d-b2ee-76f495fb5307)

The input lines will be hidden from the canvas, to avoid overlap with the newly created Form Diagram. If you need to view them again you need to type the command `Show` in Rhino, or click with the right button in the icon over the main toolbar, as shown below. The input edges should remain hidden during this tutorial.

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FyIdljQ2HZYg8QR6Kf7nj%2Fimage.png?alt=media\&token=acd45cfd-12bc-4bdb-8341-16f618b53872)

### 2.2. Setting loaded edges <a href="#id-2.2.-setting-loaded-edges" id="id-2.2.-setting-loaded-edges"></a>

The truss is an isostatic example in which there's only one load applied. We can chose the magnitude of this force freely. Click over the Assign Forces button. Select the edge representing the load and apply a magnitude of **-10 kN** since the force should push the panel. The edges will display numered and in this case you should apply the force to the edge #0.

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FZnmRYirQZHmzxbn6D5eW%2Fimage.png?alt=media\&token=b9fde3f7-a250-4600-bd7b-40f3b9615587)

After we hit OK, the forces applied are shown in the edges with an arrow. Verify that the arrow direction corresponds to the desired direction of the applied loads.

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2Fufxx57B5u1IMpOG0U71M%2Fimage.png?alt=media\&token=32f0da49-dcd6-4478-a14b-123ecf15e8b1)

### 2.3. Setting supports <a href="#id-2.3.-setting-supports" id="id-2.3.-setting-supports"></a>

Supports should be assigned to the nodes where reaction forces are applied. Go to the function `Identify Anchors` and select the two nodes in the base of the single panel. These nodes will be highlighted in red as in the figure below:

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2F5Gzt8LnxRIB46CCQMz1z%2Fimage.png?alt=media\&token=a1ff5b16-0436-4093-be7a-cc24a94e491d)

### 2.4. Compute the Force Diagram <a href="#id-2.4.-compute-the-force-diagram" id="id-2.4.-compute-the-force-diagram"></a>

After setting the loads we can compute the equilibrium by calculating the force diagram in the button `Create Force Diagram`, the force diagram is automatically generated right to the form diagram. The result should be as below:

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2F1jHSfAkfu4FNTLJ49ZM5%2Fimage.png?alt=media\&token=8ee4f090-8d99-427c-bf07-d44b51b9da33)

Note that the reaction forces now display also the value and direction. The default visualisation for form and force is the red-blue colouring. **Blue** represents **compression** and **red** **tension**. At this point, the scale and location of the force diagram is automatically set by IGS.

### 2.5. Display Settings <a href="#id-2.5.-display-settings" id="id-2.5.-display-settings"></a>

A series of display options can be modified to help to visualise the diagrams. These options are organised in the two tabs of the `Display Settings` menu: FormObject and Force Object, as depicted below:

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FbRibJMpF5wCFFNLnIVjS%2Fimage.png?alt=media\&token=56c05e51-4ef3-4285-8afc-9bf19527c7c5)

Therefore, the red/blue colouring can be turned on and off (_forcecolors_). Equally the edge and vertex labels can be turned on and off. Additionally, force labels, indicating the magnitude the force on the edges are available for both diagrams. For the Form Diagram, pipes can be drawn in the edges with thickness proportional to the load carried. The scale of these pipes can also be modified in the display settings panel.The scale and the location of the Force diagram can be modified in the appropriate functions over the **IGS** Menu Display > `ForceDiagram Location` and `ForceDiagram Scale` .

### 2.6. Inspect Diagrams. <a href="#id-2.6.-inspect-diagrams" id="id-2.6.-inspect-diagrams"></a>

To analyse the magnitude of the forces in specific edges three options are available in the Button `Inspect Diagrams`. An **EdgesTable** can be displayed with information about all the forces in the structure, additionally, information about one specific edge of the structure can be queried with the option **EdgeInformation**, and the duality can be inspected with the function **ForcePolygons.**

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2F5dcOUqsFc1U50D6onvyN%2Fimage.png?alt=media\&token=453e7b53-b01d-4781-9de0-61b2ac699072)

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2FDyHSVUZBHN39T8ORK3nq%2Fimage.png?alt=media\&token=37088628-0ccc-4a21-b68d-3db6a8cf5b48)

![](https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MdX4hXGftusLhGYoC90%2Fuploads%2F9HQoJKSEPfVdjpQHcTR8%2Fimage.png?alt=media\&token=3eb7e6d0-be7d-43c6-abb9-1fda97eba5dd)
