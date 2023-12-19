# cs2-stickers-blender
A Blender add-on for adding CS2 style stickers to models

The panel appears under "misc" in the Blender side panel, choose the image files for the stickers you wish to use, and run the script.
The stickers are created as node groups into the active material or the active object per the parameters selected. If you have created multiple stickers via the add-on they will be overlapping each other in the node tree.

The node group has three outputs, UV, Color and Alpha. The UV can be used to manually add stickers via nodes, the color and alpha outputs are meant to be used to actually create the shaders and mix them together

The add-on is currently in beta, technical issues are possible. 
