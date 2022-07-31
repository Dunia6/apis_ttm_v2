
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import Company, Employe
from apps.dash.models.technique import Cars
from utils.base_model import BaseModel, PaymentBaseModel
from utils.times import is_expired


class CoverCity(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="cities"
    )
    town = models.CharField(
        _("cover city"),
        max_length=200
    )
    code = models.CharField(
        _("code"),
        max_length=200,
        null=True
    )
    image = models.ImageField(
        _("picture of city"),
        null=True
    )
    latitude = models.FloatField(
        _("latitude"),
        null=True,
        default=None
    )
    longitude = models.FloatField(
        _("latitude"),
        null=True,
        default=None
    )

    def __str__(self) -> str:
        return f"{self.town}: #{self.pk}"


class Routing(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name="routing",
        on_delete=models.CASCADE
    )
    node = models.ForeignKey(
        CoverCity,
        verbose_name=_("Current CoverCity"),
        on_delete=models.CASCADE,
        related_name="route"
    )
    whereFrom = models.ForeignKey(
        "self",
        verbose_name=_("where from"),
        on_delete=models.SET_DEFAULT,
        related_name="predecessor",
        null=True, default=None
    )
    whereTo = models.ForeignKey(
        "self",
        verbose_name=_("where to"),
        related_name="successor",
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    orgine = models.ForeignKey(
        "self",
        verbose_name=_("orgine"),
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        help_text=_("the orgin of routing(first town)")
    )
    distance = models.FloatField(
        _("distance(Km)"),
        default=0.0
    )

    def __str__(self) -> str:
        return f"pk {self.pk } : Node {self.node}"


class PointOfSale(BaseModel):
    """ point of sale  """
    company = models.ForeignKey(
        Company,
        verbose_name=_("point-of-sale"),
        related_name="point_of_sale",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=200
    )
    town = models.ForeignKey(
        CoverCity,
        verbose_name=_("town of sale"),
        related_name="town_pos",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class PointOfSaleWorker(BaseModel):
    company = models.ForeignKey(
        Company,
        verbose_name=_("point-of-sale worker"),
        related_name="worker_saler",
        on_delete=models.CASCADE
    )
    worker = models.ForeignKey(
        Employe,
        verbose_name=_("worker"),
        related_name="worker",
        on_delete=models.CASCADE
    )
    pointOfSale = models.ForeignKey(
        PointOfSale,
        verbose_name=_("point-of-sale"),
        related_name="worker_pos",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.worker} {self.company}"


class JourneyClass(BaseModel):
    code = models.CharField(
        verbose_name=_("code_class"),
        max_length=10
    )
    name = models.CharField(
        verbose_name=_("name_class"),
        max_length=10
    )
    company = models.ForeignKey(
        Company,
        related_name="journey_class",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.name} : {self.code}'


class JourneyTarif(PaymentBaseModel):
    """
    """
    journey_class = models.ForeignKey(
        JourneyClass,
        on_delete=models.CASCADE,
        related_name='tarif'
    )
    route = models.ForeignKey(
        Routing,
        verbose_name=_("routes"),
        on_delete=models.CASCADE,
        related_name="tarif_routes"
    )

    adult = models.FloatField(
        verbose_name=_('tarif_adult'),
        default=0.0
    )
    child = models.FloatField(
        verbose_name=_('tarif_child'),
        default=0.0
    )
    baby = models.FloatField(
        verbose_name=_('tarif_baby'),
        default=0.0)

    taxe = models.FloatField(
        verbose_name=_('taxe'),
        default=0.0)
    actif = models.BooleanField(
        verbose_name=_('actif_tarif'),
        default=True
    )

    @property
    def pttc_adulte(self) -> float:
        # prix toute taxe confondu adulte
        return self.adult + self.taxe

    @property
    def pttc_child(self) -> float:
        # prix toute taxe confondu adulte
        return self.child + self.taxe

    @property
    def pttc_baby(self) -> float:
        # prix toute taxe confondu adulte
        return self.baby + self.taxe


class Journey(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name="journey",
        on_delete=models.CASCADE
    )
    numJourney = models.CharField(
        verbose_name=_("number of journey"),
        max_length=50
    )
    dateDeparture = models.DateField(
        verbose_name=_("date of departure")
    )
    dateReturn = models.DateField(
        verbose_name=_("date of departure")
    )
    hoursDeparture = models.TimeField(
        verbose_name=_("hours of departure")
    )
    hoursReturn = models.TimeField(
        verbose_name=_("hours of return")
    )
    cars = models.ForeignKey(
        Cars,
        verbose_name=_("cars"),
        related_name="cars_journies",
        on_delete=models.CASCADE,
    )
    route = models.ForeignKey(
        Routing,
        verbose_name=_("routing"),
        null=True,
        default=None,
        related_name="routing_journies",
        on_delete=models.SET_DEFAULT,
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.numJourney} {self.company}"

    @property
    def exprired(self) -> bool:
        timing = self.dateDeparture
        return is_expired(timing)
