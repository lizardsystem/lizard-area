# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from lizard_map.views import AppView
from lizard_area.models import Category


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
