# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from datetime import datetime
from treebeard.al_tree import AL_Node

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from lizard_geo.models import GeoObject
from lizard_geo.models import GeoObjectGroup
from lizard_security.manager import FilteredGeoManager
from lizard_security.models import DataSet

logger = logging.getLogger(__name__)

############################


AREA_TYPES = (
    ('aanafvoergebied', 'aanafvoergebied'),
    ('peilgebied', 'peilgebied'),
)


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
        return reverse('lizard_area_api_category', kwargs={'slug': self.slug})


#############################

class NameAbstract(models.Model):
    """
    Abstract model with only a name as property.
    """
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class DataAdministrator(NameAbstract):
    """
    Administrators of all kinds of data.

    The administrator can be an organization.
    """
    pass


class Communique(GeoObject):
    """
    Communique: summary and status of an area.

    TODO: make lookup tables of some fields.
    TODO: Rename fields?
    """

    # i.e. Reeuwijkse plassen
    name = models.CharField(max_length=128, null=True, blank=True)

    # i.e. "NL13_11"
    code = models.CharField(max_length=128, null=True, blank=True)

    #
    description = models.TextField(default="")
    edited_by = models.TextField(max_length=150, null=True, blank=True)
    edited_at = models.DateField(null=True, blank=True)
    dt_latestchanged_krw = models.DateField(help_text='Time changed by GV',
                                            null=True, blank=True)
    surface = models.DecimalField(max_digits=10, decimal_places=1,
                                  null=True, blank=True)
    areasort = models.CharField(max_length=100, null=True, blank=True)
    areasort_krw = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.ident, self.name)

    def get_absolute_url(self):
        return reverse('lizard_area_api_communique', kwargs={'pk': self.pk})


class AreaLink(models.Model):
    """
    Link between areas of different type
    """
    area_a = models.ForeignKey('Area', related_name='arealink_a')
    area_b = models.ForeignKey('Area', related_name='arealink_b')
    link_type = models.CharField(max_length=24, default='',
                                 null=True, blank=True)


class AreaManager(FilteredGeoManager):
    def get_by_natural_key(self, ident):
        return self.get(ident=ident)

    def get_query_set(self):
        """
        Defer querying of the geometry field.

        Usually we need only the names.
        """
        return super(AreaManager, self).get_query_set().defer('geometry')


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
    # data_administrator could be removed)
    data_administrator = models.ForeignKey(DataAdministrator,
                                           null=True, blank=True)
    area_class = models.IntegerField(
        choices=AREA_CLASS_CHOICES, default=AREA_CLASS_KRW_WATERLICHAAM)
    is_active = models.BooleanField()
    dt_created = models.DateField(default=datetime.today())
    dt_latestchanged = models.DateField(blank=True, null=True)
    dt_latestsynchronized = models.DateField(blank=True, null=True)
    area_type = models.CharField(max_length=50, choices=AREA_TYPES,
                                 blank=True, null=True)
    supports_object_permissions = True
    data_set = models.ForeignKey(DataSet,
                                 null=True,
                                 blank=True)
    objects = AreaManager()

    # For treebeard.
    node_order_by = ['name']

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.ident)

    def get_absolute_url(self):
        return reverse('lizard_area_api_area', kwargs={'pk': self.pk})

    def extent(self):
        return self.geometry.transform(900913, clone=True).extent

    @property
    def water_manager(self):
        return '' if self.data_set is None else self.data_set.name

    def natural_key(self):
        return (self.ident, )


class AreaWFSConfiguration(models.Model):
    """Configuration to synchronize areas."""

    name = models.CharField(max_length=30, null=True, blank=True)
    area_type = models.CharField(max_length=50, choices=AREA_TYPES)
    host = models.CharField(max_length=128, null=True, blank=True)
    path = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=128, null=True, blank=True)
    maxFeatures = models.IntegerField(default=64000)
    typeName = models.CharField(max_length=50)
    cql_filter = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    password = models.CharField(max_length=64, null=True, blank=True)
    data_set = models.ForeignKey(DataSet)

    def __unicode__(self):
        return ("%s | %s" % (self.name, self.data_set))


class SynchronizationHistory(models.Model):
    """History of Syncronization run."""
    dt_start = models.DateTimeField()
    dt_finish = models.DateTimeField(null=True,
                                     blank=True)
    amount_updated = models.IntegerField(null=True,
                                         blank=True)
    amount_created = models.IntegerField(null=True,
                                         blank=True)
    amount_synchronized = models.IntegerField(null=True,
                                             blank=True)
    amount_deactivated = models.IntegerField(null=True,
                                             blank=True)
    amount_activated = models.IntegerField(null=True,
                                           blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    message = models.CharField(max_length=256)
    username = models.CharField(max_length=100)
    supports_object_permissions = True
    data_set = models.ForeignKey(DataSet,
                                 null=True,
                                 blank=True)
    objects = FilteredGeoManager()

    def __unicode__(self):
        return "%s - %s" % (self.dt_start, self.data_set)

    class Meta:
        ordering = ['-dt_start']
