lizard-area
==========================================

Introduction
------------

Store geo objects representing areas and manage them.


GeoObject
---------

The model GeoObject contains all geometric objects. A geometric object
can (but not necessarily) represent an area. All GeoObject have a
foreign key to a GeoObjectGroup to make every single object managable.


Import shapefile
----------------

Use the import_shape management command to import a shape file::

  $> bin/django import_shapefile <path-to-shapefile> <username> [parent-field]

A GeoObjectGroup will be created with all GeoObjects pointing to
it. There will also be a category with all GeoObjects in it.

(later)

A shapefile can be uploaded in the frontend if you are an
AreaAdministrator. The AreaAdministrator is automatically filled in too.


Area administrators
-------------------

After importing shapefiles you can add an AreaAdministrator to a
GeoObjectGroup. Every GeoObjectGroup can point to one and only one
AreaAdministrator.

Django auth.Group is used to determine which TABLES a user can
see or edit. AreaAdministrator is used to determine which ROWS a user can
see or edit.


Communique
----------

Add communique by adding a communique object. Each communique must
point to a GeoObject.


Visualizing areas
-----------------

Area layouts are defined in LegendClass. If the adapter.layout
function is called with a custom mapnik-sql query, area coloring based
on values (measurements, constants, ..) is possible.
