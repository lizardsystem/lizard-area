# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from treebeard.al_tree import AL_Node

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from lizard_geo.models import GeoObject
from lizard_geo.models import GeoObjectGroup

logger = logging.getLogger(__name__)

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


class AreaCode(NameAbstract):
    """Area code, used by communique."""
    pass


class Status(NameAbstract):
    """Area status, used by communique."""
    pass


class AreaType(NameAbstract):
    """Area type, used by communique."""
    pass


class Province(NameAbstract):
    """Province, used by communique."""
    pass


class Municipality(NameAbstract):
    """Municipality, used by communique."""
    pass


class Basin(NameAbstract):
    """Basin ("stroomgebied"), used by communique."""
    pass


class WaterManagementArea(NameAbstract):
    """Water management area ("waterbeheergebied"), used by communique."""
    pass


class Communique(GeoObject):
    """
    Communique: summary and status of an area.

    TODO: make lookup tables of some fields.
    TODO: Rename fields?
    """

    # i.e. Reeuwijkse plassen
    name = models.CharField(max_length=128)

    # i.e. "NL13_11"
    code = models.ForeignKey(AreaCode, null=True, blank=True)

    # i.e. "Kunstmatig"
    status = models.ForeignKey(Status, null=True, blank=True)

    # i.e. "M27 - Matig grote ondiepe laagveenplassen"
    area_type = models.ForeignKey(AreaType, null=True, blank=True)

    # i.e. "Zuid-Holland"
    province = models.ForeignKey(Province, null=True, blank=True)

    # i.e. "Reeuwijk"
    municipality = models.ForeignKey(Municipality, null=True, blank=True)

    # Stroomgebied. i.e. "Rijn-West"
    basin = models.ForeignKey(Basin, null=True, blank=True)

    # Waterbeheergebied. i.e. "Hoogheemraadschap van Rijnland"
    watermanagementarea = models.ForeignKey(
        WaterManagementArea, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.ident, self.name)

    def get_absolute_url(self):
        return reverse('lizard_area_api_communique', kwargs={'pk': self.pk})


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
        return reverse('lizard_area_api_area', kwargs={'pk': self.pk})
