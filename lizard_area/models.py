# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from treebeard.al_tree import AL_Node

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

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
    source_log = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lizard-area:api:geo_object_group',
                       kwargs={'pk': self.pk})


class GeoObject(models.Model):
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


class MapnikXMLStyleSheet(models.Model):
    """
    Mapnik styles in XML can be uploaded
    """
    name = models.CharField(max_length=128)
    style = models.TextField(
        default='', null=True, blank=True,
        help_text=('Dit veld wordt indien leeg '
                   'gevuld met de inhoud van het bronbestand.'))
    source_file = models.FileField(
        upload_to="lizard_area/mapnik_xml_stylesheets/",
        help_text='Bronbestand.')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Load source file in field style and save if style is
        empty.

        The original file is stored in source_file.
        """
        if self.style:
            super(MapnikXMLStyleSheet, self).save(*args, **kwargs)
        else:
            # Load file
            super(MapnikXMLStyleSheet, self).save(*args, **kwargs)
            f = open(self.source_file.path, 'r')
            for line in f.readlines():
                self.style += line
            f.close()
            return super(MapnikXMLStyleSheet, self).save(*args, **kwargs)


class Category(AL_Node):
    """
    Categories that are displayed in the ui.
    """
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    geo_object_groups = models.ManyToManyField(
        GeoObjectGroup, null=True, blank=True)

    parent = models.ForeignKey('Category', blank=True, null=True)
    mapnik_xml_style_sheet = models.ForeignKey(
        MapnikXMLStyleSheet,
        blank=True, null=True)

    # For treebeard.
    node_order_by = ['name']

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.slug)

    def get_absolute_url(self):
        return reverse('lizard-area:api:category', kwargs={'slug': self.slug})


#############################

class DataAdministrator(models.Model):
    """
    Administrators of all kinds of data.

    The administrator can be an organization.
    """
    name = models.CharField(max_length=128, unique=True)

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

    def __unicode__(self):
        return '%s - %s' % (self.ident, self.name)

    def get_absolute_url(self):
        return reverse('lizard-area:api:communique', kwargs={'pk': self.pk})


class Area(Communique, AL_Node):
    """
    KRW waterlichamen en (deel) aan-/afvoergebieden.
    """

    AREA_CLASS_KRW_WATERLICHAAM = 1
    AREA_CLASS_AAN_AFVOERGEBIED = 2
    AREA_CLASS_DEEL_AAN_AFVOERGEBIED = 3

    AREA_CLASS_CHOICES = (
        (AREA_CLASS_KRW_WATERLICHAAM, 'krw waterlichaam'),
        (AREA_CLASS_AAN_AFVOERGEBIED, 'aan-/afvoer gebied'),
        (AREA_CLASS_DEEL_AAN_AFVOERGEBIED, 'deel aan-/afvoergebied'), )

    AREA_CLASS_DICT = dict(AREA_CLASS_CHOICES)

    parent = models.ForeignKey('Area', null=True, blank=True)
    data_administrator = models.ForeignKey(DataAdministrator)
    area_class = models.IntegerField(
        choices=AREA_CLASS_CHOICES, default=AREA_CLASS_KRW_WATERLICHAAM)

    # For treebeard.
    node_order_by = ['name']

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return '%s (%s - %s)' % (
            self.name, self.AREA_CLASS_DICT[self.area_class],
            self.data_administrator)

    def get_absolute_url(self):
        return reverse('lizard-area:api:area', kwargs={'pk': self.pk})
