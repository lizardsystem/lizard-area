lizard-area
==========================================

Introduction
------------

Store geo objects representing areas and manage them. Use the Lizard
viewer to view categorized areas. Use the REST API to browse through
categories, KRW-waterlichamen (krw-areas) and (deel)
aan/afvoergebieden (catchment-areas).


Development installation
------------------------

The first time, you will have to run the bootstrap script to set up
setuptools and buildout::

    $> python bootstrap.py

Then run buildout to set everything up::

    $> bin/buildout

Note that on Microsoft Windows it is called ``bin\buildout.exe``.

You will have to re-run buildout when ``setup.py`` or ``buildout.cfg`` have
been modified, for example directly by you or through an update of your working
directory.

The current package is installed as a "development package", so
changes in .py files are automatically available (just like with
``python setup.py develop``).

The app lizard-area uses a SpatiaLite database, although this will
probably be overwritten at the site level. The repository already
contains a SpatiaLite database, so you should not need to create one
yourself. In case you want to create a new SpatiaLite database,
execute the following command::

  $> spatialite lizard-area.db < init_spatialite-2.3.sql
  spatialite lizard-area.db < init_spatialite-2.3.sql
  SpatiaLite version ..: 2.3.0	Supported Extensions:
        - 'VirtualShape'        [direct Shapefile access]
        - 'VirtualText          [direct CSV/TXT access]
        - 'VirtualNetwork       [Dijkstra shortest path]
        - 'RTree'               [Spatial Index - R*Tree]
        - 'MbrCache'            [Spatial Index - MBR cache]
        - 'VirtualFDO'          [FDO-OGR interoperability]
        - 'SpatiaLite'          [Spatial SQL - OGC]
  PROJ.4 version ......: Rel. 4.7.1, 23 September 2009
  GEOS version ........: 3.1.0-CAPI-1.5.0

The above snippet assumes you already have installed SpatiaLite.


Import shapefile
----------------

Use the import_shape management command to import a shape file::

  $> bin/django import_shapefile <path-to-shapefile> <username> [parent-field]

Please note that this command has to be tailored to the shape files at
hand. It probably cannot not be used as is.

A GeoObjectGroup will be created with all GeoObjects pointing to
it. There will also be a category with all GeoObjects in it.

(later)

A shapefile can be uploaded in the frontend if you are an
AreaAdministrator. The AreaAdministrator is automatically filled in too.


Area administrators
-------------------

Needs updating.

After importing shapefiles you can add an AreaAdministrator to a
GeoObjectGroup. Every GeoObjectGroup can point to one and only one
AreaAdministrator.

Django auth.Group is used to determine which TABLES a user can
see or edit. AreaAdministrator is used to determine which ROWS a user can
see or edit.


Communique/Area
----------

An Area is a subclass of Communique. It inherits all properties and
add its own. Communique is a subclass of GeoObject.

When deleting Communique or Area objects, use GeoObjectGroup, because
only then the GeoObjects are deleted too. Each GeoObjectGroup in
lizard-area represent a shapefile.


Visualizing areas
-----------------

Area layouts are now static.
