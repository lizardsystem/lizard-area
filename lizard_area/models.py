# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from treebeard.al_tree import AL_Node

from django.contrib.auth.models import User
from django.contrib.gis.db import models

logger = logging.getLogger(__name__)


class GeoObjectGroup(models.Model):
    """
    Geo objects are grouped.

    These are starting points to navigate through all geo objects.

    Examples of groups:
    - Alle aan-/afvoergebieden van een waterschap
    - Alle deel aan-/afvoergebieden van 1 deelgebied
    - Alle krw waterlichamen

    TODO: Automatically fill in slug
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    # legend = models.ForeignKey(LegendClass, null=True, blank=True)
    # "source"

    created_by = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class GeoObject(AL_Node):
    """
    Geo objects storage.

    Ident MUST be unique. When importing shapefiles references are
    done using ident.

    Parents are used for deel aan-/afvoergebieden.
    """
    ident = models.CharField(max_length=16, unique=True)
    geometry = models.GeometryField(srid=4326)
    geo_object_group = models.ForeignKey(GeoObjectGroup)
    objects = models.GeoManager()

    # verwijzing naar "bron locatie" string

    def __unicode__(self):
        return '%s (%s)' % (self.ident, self.geo_object_group)

############################

class Category(AL_Node):
    """
    Categories that are displayed in the ui.
    """
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    geo_object_groups = models.ManyToManyField(
        GeoObjectGroup, null=True, blank=True)

    parent = models.ForeignKey('Category', blank=True, null=True)

    # For treebeard.
    node_order_by = ['name']

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.slug)

# class MapnikStyle(models.Model):
#     """
#     Mapnik styles in XML can be uploaded
#     """
#     name = models.CharField(max_length=128, unique=True)
#     slug = models.SlugField()
#     source_file = models.FileField()

#     def __unicode__(self):
#         return self.name


#############################

class AreaAdministrator(models.Model):
    """
    Administrators of areas.

    The administrator can be an organization.
    """
    name = models.CharField(max_length=128, unique=True)
    geo_object_groups = models.ManyToManyField(
        GeoObjectGroup, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Communique(GeoObject):
    """
    Communique: summary and status of an area.

    TODO: make lookup tables of some fields.
    TODO: Rename fields?
    """

    # i.e. Reeuwijkse plassen
    name = models.CharField(max_length=128)

    # i.e. "NL13_11"
    code = models.CharField(max_length=128, null=True, blank=True)

    # i.e. "Kunstmatig"
    status = models.CharField(max_length=128, null=True, blank=True)

    # i.e. "M27 - Matig grote ondiepe laagveenplassen"
    area_type = models.CharField(max_length=128, null=True, blank=True)

    # i.e. "Zuid-Holland"
    province = models.CharField(max_length=128, null=True, blank=True)

    # i.e. "Reeuwijk"
    municipality = models.CharField(max_length=128, null=True, blank=True)

    # Stroomgebied. i.e. "Rijn-West"
    basin = models.CharField(max_length=128, null=True, blank=True)

    # Waterbeheergebied. i.e. "Hoogheemraadschap van Rijnland"
    watermanagementarea = models.CharField(
        max_length=128, null=True, blank=True)
