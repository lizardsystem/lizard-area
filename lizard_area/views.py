# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from lizard_map.views import AppView


def dummy(request):
    pass


class Homepage(AppView):
    template_name = 'lizard_area/homepage.html'

