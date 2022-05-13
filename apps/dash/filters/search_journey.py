"""
    copyright ttm
    ?adult=1&baby=0&child=0&dateDepart=2022-05-01&journeyClass=4&whereFrom=10&whereTo=6
      company = models.ForeignKey(
        Company, related_name="journey", on_delete=models.CASCADE)
    numJourney = models.CharField(_("number of journey"), max_length=50)
    dateDeparture = models.DateField(_("date of departure"))
    dateReturn = models.DateField(_("date of departure"))
    hoursDeparture = models.TimeField(_("hours of departure"))
    hoursReturn = models.TimeField(_("hours of return"))
    cars = models.ForeignKey(Cars, verbose_name=_(
        "cars"), on_delete=models.CASCADE, related_name="cars_journies")
    route = models.ForeignKey(Routing, verbose_name=_(
        "routing"), on_delete=models.SET_DEFAULT, related_name="routing_journies", null=True, default=None)
"""
from typing import Union, Optional
from typing import Any
from rest_framework import filters
from ..process.routes import RouteProcess


class SearchJourneyByDateFilters(filters.BaseFilterBackend):
    date_dep_name = "dateDepart"
    date_ret_name = "dateReturn"

    def filter_queryset(self, request, queryset, view):
        qs = queryset
        dateReturn: Optional[str] = request.query_params.get(self.date_dep_name, None)
        dateDeparture: Optional[str] = request.query_params.get(self.date_ret_name, None)
        #
        if dateDeparture:
            qs = qs.filter(dateDeparture=dateDeparture)
        if dateReturn:
            qs = qs.filter(dateReturn=dateReturn)
        return qs


class SearchJourneyByDestinationFilters(filters.BaseFilterBackend):
    where_to_name = "whereTo"

    def filter_queryset(self, request, queryset, view) -> Any:
        qs = queryset
        where_to = request.query_params.get(self.where_to_name)
        if where_to:
            qs = qs.filter(route__node=where_to)
        return qs


class SearchJourneyByDepartureFilters(filters.BaseFilterBackend):
    whereFrom = "whereFrom"

    def filter_queryset(self, request, queryset, view) -> Any:
        departure = []
        qs = queryset
        for journey in qs:
            inital_route = RouteProcess.firstroute(journey.route)
            if inital_route and inital_route.node.pk == self.whereFrom:
                departure.append(journey.route.node)

        #
        whereFrom = request.query_params.get(self.whereFrom)
        if whereFrom:
            qs = qs.filter(route__node__in=departure)
        return qs
