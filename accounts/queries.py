from django.db.models import Q, F, Count, Avg, Max, Min, Case, When, Value
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import CustomUser
from django.db.models.functions import ExtractYear, Now
from django.db.models import ExpressionWrapper, DurationField, Sum


q1 = CustomUser.objects.filter(is_active=True)

q2 = CustomUser.objects.filter(email__endswith="@gmail.com")

q3 = CustomUser.objects.filter(city="Almaty")

q4 = CustomUser.objects.exclude(city="Almaty")

q5 = CustomUser.objects.filter(salary__gt=500000)

q6 = CustomUser.objects.filter(department="IT", country="Kazakhstan")

q7 = CustomUser.objects.filter(birth_date__isnull=True)

q8 = CustomUser.objects.filter(first_name__istartswith="A")

q9 = CustomUser.objects.count()

q10 = CustomUser.objects.order_by("-date_joined")[:20]

q11 = CustomUser.objects.values_list("city", flat=True).distinct()

q12 = CustomUser.objects.filter(department="Sales").count()

q13 = CustomUser.objects.filter(last_login__gte=timezone.now() - timedelta(days=7))

q14 = CustomUser.objects.filter(Q(first_name__icontains="bek") | Q(last_name__icontains="bek"))

q15 = CustomUser.objects.filter(salary__gte=300000, salary__lte=700000)

q16 = CustomUser.objects.filter(department__in=["IT", "HR", "Finance"])

q17 = CustomUser.objects.values("department").annotate(count=Count("id"))

q18 = CustomUser.objects.values("department").annotate(count=Count("id")).order_by("-count")

q19 = CustomUser.objects.values("city").annotate(count=Count("id")).order_by("-count")[:5]

q20 = CustomUser.objects.filter(last_login__isnull=True)

q21 = CustomUser.objects.aggregate(avg_salary=Avg("salary"))

q22 = CustomUser.objects.aggregate(max_salary=Max("salary"), min_salary=Min("salary"))

q23 = CustomUser.objects.filter(phone__contains="+7")

q24 = CustomUser.objects.annotate(full_name=Value("") + F("first_name") + Value(" ") + F("last_name"))

q25 = CustomUser.objects.annotate(birth_year=ExtractYear("birth_date")).order_by("birth_year")

q26 = CustomUser.objects.filter(birth_date__month=5)

q27 = CustomUser.objects.filter(role="manager", salary__gt=400000)

q28 = CustomUser.objects.filter(Q(role="employee") | Q(department="HR"))

q29 = CustomUser.objects.filter(is_active=True).values("city").annotate(count=Count("id"))

q30 = CustomUser.objects.order_by("date_joined")[:10]

q31 = CustomUser.objects.filter(city__startswith="A", salary__gt=300000)

q32 = CustomUser.objects.filter(Q(department__isnull=True) | Q(department=""))

q33 = CustomUser.objects.values("country").annotate(count=Count("id"), avg_salary=Avg("salary"))

q34 = CustomUser.objects.filter(is_staff=True).order_by("-last_login")

q35 = CustomUser.objects.exclude(email__contains="example.com")

avg_salary = CustomUser.objects.aggregate(a=Avg("salary"))["a"]
q36 = CustomUser.objects.filter(salary__gt=avg_salary)

q37 = CustomUser.objects.values("email").annotate(count=Count("id")).filter(count__gt=1)

q38 = CustomUser.objects.annotate(
    salary_level=Case(
        When(salary__lt=300000, then=Value("low")),
        When(salary__lte=700000, then=Value("medium")),
        When(salary__gt=700000, then=Value("high")),
    )
).order_by("salary_level")

q39 = CustomUser.objects.filter(date_joined__year=datetime.today().year)

q40 = CustomUser.objects.values("department").annotate(total_salary=Sum("salary"))

q41 = CustomUser.objects.filter(department="IT", last_login__isnull=True)

q42 = CustomUser.objects.filter(country="Kazakhstan").filter(Q(city__isnull=True) | Q(city=""))

q43 = CustomUser.objects.filter(birth_date__lt="1990-01-01", salary__isnull=False)

q44 = CustomUser.objects.annotate(
    years_since_joined=ExpressionWrapper(
        Now() - F("date_joined"),
        output_field=DurationField(),
    )
)

q45 = CustomUser.objects.filter(
    department="Sales",
    email__endswith="@gmail.com",
    salary__gt=350000
)

q46 = CustomUser.objects.order_by("country", "-salary")

q47 = CustomUser.objects.values("role").annotate(count=Count("id")).filter(count__gt=100)

q48 = CustomUser.objects.filter(last_login__lt=F("date_joined"))

q49 = CustomUser.objects.annotate(
    is_senior=Case(
        When(birth_date__lt="1985-01-01", then=Value(True)),
        default=Value(False),
    )
)

q50 = CustomUser.objects.values("department").annotate(
    avg_salary=Avg("salary"),
    count=Count("id"),
).filter(count__gte=20).order_by("-avg_salary")