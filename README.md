# Synthetic Data Generator (SDG) Blender Add-on

A blender addon for generating synthetic data for machine learning. The goal of this-addon is to speed up the learning process of object detection models by fine-tuning them
with synthetic data.

## Installation
The add-on requires Blender version 3.1.2 and Blender Annotation Tool (BAT) commit 4a77482. This repository with the correct commit
is avaiable [here.](https://github.com/karolyartur/blender_annotation_tool/tree/4a77482090874f1f625c4e84271afad83fa38fbd)

The add-on also requires the Import-EXport: Wavefront OBJ format add-on version 3.9.0. In theory it is an already
installed package in this version of Blender, you just need to enable it.

To install the add-on, download the repository as a zip file. Then, in Blender, navigate to Edit>Preferences> Addons and click Install. Select the downloaded zip. 
The addon should then appear in the list of addons (in the Object category). 
Click the checkbox to activate the addon.

After installation, the addon can be use in the Layout tab's N menu.


![Image showing the SDG Panel at the N Panel](https://github.com/user-attachments/assets/4a9806be-1cc1-44a6-bd73-b3d51ab4abdc)

## How is the data generated?

In short, we have a Plane object and we basically drop the imported objects onto the Plane. It uses Blender's built-in
physic simulation to achieve this. After we dropped the objects a render and mask is generated at the specified output.
The mask is an EXR file, which has different channels. To open this file's channels you need to use [this.](https://github.com/karolyartur/exr_reader)

## Usage

The SDG panel consists of 3 main component: 
### Setup Scene
The first is the Setup scene box. Here you change the texture of the plane.
If you don't specify any image file, it will use the sample one in the misc folder.
You don't need to use this, you can just create a Plane object with its default name.

### Import Tools

The second box is the import tools box. You need to specify an import direcory where your OBJ files are located. Your OBJ files need to be inside their respective
folder, usually named after the class name which you want to use later in your machine learning. Here is an example folder structure:

![map structure of tools that may be imported](https://github.com/user-attachments/assets/203b64ee-bb06-4848-8a2b-90a1668430b8)

The reason for this structure is the following: For example you have a Combination Pliers object and you created different variaton of this object. For example
one variaton is closed, the second one is slightly open and the third one is fully open. You may want to handle them as a single instance, so this is the way for it.
Here is what's inside the Combination Pliers folder:

![content of combination pliers folder](https://github.com/user-attachments/assets/30fc434b-7532-4d2a-9983-7c5e512c5259)

If you don't specify the the import folder, it will use the example toolset in the misc folder.

### Generate Data
The last component is the generate data box. Here you can specify how many image-mask pair you want to create, and what is the maximum and minimal number of objects
you want on your renders. You need to specify the output folder or it will tell you to specify it. The generated data will be put in two folders. One for the images in 'renders',
and one for the masks called 'annotations'. Here is a visualization as to what data gets created:

![render-mask pair example with overlap](https://github.com/user-attachments/assets/44fe0689-aff9-430b-b8b3-c719894dd2a6)



