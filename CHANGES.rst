bin/buildoutChangelog of lizard-area
===================================================


0.1.11 (unreleased)
-------------------

- Nothing changed yet.


0.1.10 (2012-02-13)
-------------------

- communique api change


0.1.9 (2012-02-13)
------------------

- Added area_link table, for many2many relations between areas (aanafvoergebieden and krw gebieden)


0.1.8 (2012-02-07)
------------------

- Fixed error in test.

- Fixed syntax errors.


0.1.7 (2012-02-06)
------------------

- Changed function to view a tree of 'aanafvoergebieden'.


0.1.6 (2012-02-06)
------------------

- Added functionality to retrieve waterbody/area data (scenario 550).

- Added functionality to keep last changes on communique.description
  (#4).

- Added functonality to view area/woterbody information.

- Added functionality to create a tree of 'aanafvoergebieden'.


0.1.5 (2012-01-31)
------------------

- Added functionality to synchronize area objects with remote wfs.

- Created management command and celery task to run synchronisation as
  periodic task.


0.1.4 (2012-01-30)
------------------

- Added lizard-security to Area model.

- Fixes tests.

- Switches to postgis for testing.


0.1.3 (2011-12-09)
------------------

- Changed datamodel, removed unused fields

- Created api for communiqué and area properties


0.1.2 (2011-12-07)
------------------

- Added functionality to area service for remote combobox communication.


0.1.1 (2011-11-07)
------------------

- Added Area.extent function (it disappeared).


0.1 (2011-11-07)
----------------

- Created geoobjects and moved it to lizard-geo.

- Created initial tests.

- Created initial migration.

- Created initial adapter.

- Created initial api.

- Created geoobject.py helper library.

- Added admin.

- Initial models.

- Initial library skeleton created by nensskel.  [Jack Ha]
