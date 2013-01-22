bin/buildoutChangelog of lizard-area
===================================================


0.9.12 (unreleased)
-------------------

- Nothing changed yet.


0.9.11 (2013-01-22)
-------------------

- Added filter to select only active areas for three.


0.9.10 (2013-01-22)
-------------------

- Nothing changed yet.


0.9.9 (2013-01-22)
------------------

- Replace suffix in date field by the synchronizaton of areas pp418.


0.9.8 (2013-01-14)
------------------

- Update logging message.


0.9.7 (2013-01-11)
------------------

- Update logger message, set description field to allow a blank value.


0.9.6 (2013-01-10)
------------------

- Fix "Server communication failure" on "Bewerk geometry op kaart" in 
  Beheer/Maatrelen pp262.


0.9.5 (2012-12-13)
------------------

- Fix task to synchronize 'aanafvoergebieden' pp396.


0.9.4 (2012-10-11)
------------------

- Added new view class to check if an area exists, pp391.


0.9.3 (2012-06-05)
------------------

- Fix sync not working because it tried to create a new geoobjectgroup.


0.9.2 (2012-05-30)
------------------

- bugfix permissions for linked areas


0.9.1 (2012-05-30)
------------------

- Default to first superuser as creator of area geoobject group.


0.9 (2012-05-29)
----------------

- bugfix for arealink api used in combination with permissions (pp 328)
- missing migration step for empty arealinks


0.8 (2012-05-29)
----------------

- Fixed bug in sync_area by runnig the task with 'auto' user.


0.7 (2012-05-29)
----------------

- add function part to wfs area synchronisation which adds empty arealinks for all KRW areas (pp 219)


0.6 (2012-05-25)
----------------

- Fixed  'IntegrityError' on running 'synchronize_geoobjects_...' tasks


0.5 (2012-05-25)
----------------

- Set logging for synchronization of 'aanafvoergebieden'.

- Fixed tests.


0.4 (2012-05-09)
----------------

- Add view for bounds of set of areas.

- Updated task synchronize_geoobjects to match lizard-task 0.5.


0.3.3 (2012-04-25)
------------------

- Updated fields for 'Gebiedsinformatie' portlet, Pp #193.

- Removed 'watertype_krw' field from 'Communique' model.

- Added functionality to create/update waterbodies for 'aanafvoergebieden'
  during the synchronisation proces with 'geovoorziening'.


0.3.2 (2012-04-24)
------------------

- Added additional info to 'Informatie KRW-waterlichaam' (AreaPropertyView)
  view, issue #181.


0.3.1 (2012-04-18)
------------------

- Removed print statements.
- Make it possible to select a flat area list by flat=true on the url


0.3 (2012-04-10)
----------------

- area link form now lists deel aan-afvoergebieden as well.

- api/catchment-areas (using AreaViewForTree) now has:
  - aan-afvoergebieden and deel aan-afvoergebieden
  - AreaViewForTree parent node is now optional
  (- TODO: AreaViewForTree only lists objects that are active)


0.2.10 (2012-04-05)
-------------------

- Fixes the issue that a user with the right credentials could not access the
  screen to manage the coupling of KRW water bodies and catchment areas (Pp
  222).
- Removes the requirement on Python 2.7 (Python 2.6 should work also).


0.2.9 (2012-03-23)
------------------

- Chenges to synchronize 'aanafvoergebieden' with secure 'geovoorziening'.


0.2.8 (2012-03-12)
------------------

- Nothing changed yet.


0.2.7 (2012-03-08)
------------------

- Add dependency to migration.


0.2.6 (2012-03-06)
------------------

- Defer geometry field in area manager.


0.2.5 (2012-02-27)
------------------

- Add property pattern to Area model (lizardsystem/lizard-portal#18).


0.2.4 (2012-02-26)
------------------

- added name to links in the area link portal


0.2.3 (2012-02-24)
------------------

- Add property water_manager to Area model (lizardsystem/lizard-portal#18).
- Updates
  - nens-graph to 0.,
  - lizard-measure to 1.9 (from 1.5.8).


0.2.2 (2012-02-23)
------------------

- Added natural_key to Area model.

- Pinned lizard_api 0.7


0.2.1 (2012-02-23)
------------------

- Limit and start added to area api.

- id_name field configuration for added filter option.

- string, bool or number field also dict allowed with value as id.

- html snippet for related areas.

- Improved performance of AreaViewForTree by reducing database calls.


0.2 (2012-02-17)
----------------

- Change unicode method of area


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
