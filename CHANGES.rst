bin/buildoutChangelog of lizard-area
===================================================


0.1.6 (unreleased)
------------------

- Added functionality to retrieve waterbody/area data (scenario 550).


0.1.5 (2012-01-31)
------------------

- Added functionality to synchronize area objcten with remote wfs.

- Created management command and celery task to run sinchrnization as
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
