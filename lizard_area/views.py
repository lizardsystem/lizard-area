# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.loader import get_template

from lizard_map.views import AppView
from lizard_area.models import Category, Area


class ApiView(AppView):
    """Show contents of the API in a view. Experimental.
    """
    template_name = 'lizard_area/api.html'


class Homepage(AppView):
    """Show categories. When clicking on a category, display contents.
    """
    def categories(self):
        return Category.objects.all()

    template_name = 'lizard_area/homepage.html'

def area_links_panel(request):
    """
    see and edit links between areas
    """


    area_ident = request.GET.get('object_id' )

    area = get_object_or_404(Area, ident=area_ident)

    output = []


    if area.area_class == Area.AREA_CLASS_KRW_WATERLICHAAM:
        output.append({
            'name': 'Aan/afvoergebieden',
            'object_type': 'aan_afvoergebied',
            'template': 'toestand-aan-afvoergebied',
            'headertab': 'watersysteem',
            'items': Area.objects.filter(Q(arealink_a__area_b=area)|Q(arealink_b__area_a=area)).distinct()
        })

    elif area.area_class == Area.AREA_CLASS_AAN_AFVOERGEBIED:
        related_areas = Area.objects.filter(Q(arealink_a__area_b=area)|Q(arealink_b__area_a=area)).distinct()

        if related_areas.exists():
            output.append({
                'name': 'KRW waterlichaam',
                'object_type': 'krw_waterlichaam',
                'template': 'krw-overzicht',
                'headertab': 'beleid',
                'items': related_areas
            })

        if area.parent is not None:
            output.append({
                'name': 'Onderdeel van',
                'items': [area.parent]
            })

        childs = area.get_children()
        if childs.exists():
            output.append({
                'name':'Deelgebieden',
                'items': childs
            })

 
    c = RequestContext(request, {
        'area': area,
        'related_areas': output
    })

    t = get_template('lizard_area/linked_areas.html')

    return HttpResponse(t.render(c),  mimetype="text/plain")
