from django.utils import timezone
import datetime
from django.views.generic import ListView, DetailView
from plugins.lab.models import Bloods


class UnresultedList(ListView):
    queryset = Bloods.objects.filter(bloodresult=None).exclude(
        room=""
    ).prefetch_related(
        "patient__demographics_set"
    )
    template_name = 'patient_lists/unresulted_list.html'

    def get_ordering(self):
        order_param = self.request.GET.get("order")
        if not order_param:
            return "-blood_date"
        if order_param == "name":
            return "patient__demographics__first_name"

        if order_param == "-name":
            return "-patient__demographics__first_name"

        return order_param


class YourRecentlyResultedList(ListView):
    model = Bloods
    template_name = 'patient_lists/recently_resulted.html'
    AMOUNT = 50

    def initials(self):
        first_name = self.request.user.first_name or " "
        surname = self.request.user.last_name or " "
        return "{}{}".format(first_name[0], surname[0]).strip().upper()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).exclude(
            assay_date=None
        )
        initials = self.initials()
        if initials:
            qs = qs.filter(
                patient__episode__cliniclog__seen_by__icontains=self.initials()
            )
            return qs.order_by("-assay_date")[:self.AMOUNT]
        return qs.none()


class RecentlyRecievedSamples(ListView):
    model = Bloods
    template_name = 'patient_lists/recently_received_samples.html'

    def get_querset(self, *args, **kwargs):
        two_months_ago = timezone.now() - datetime.timedelta(60)
        return Bloods.objects.filter(
            blood_date__gte=two_months_ago.date()
        ).prefetch_related(
            "patient__demographics_set"
        ).prefetch_related(
            "patient__episode_set"
        )

    def get_rows(self, queryset):
        rows = []
        order_param = self.request.GET.get("order")
        if not order_param:
            queryset = queryset.order_by("-blood_date")

        for instance in queryset:
            episode = list(instance.patient.episode_set.all())[-1]
            referral = episode.referral_set.last()
            employer = episode.employment_set.last()
            oh_provider = ""
            ref_number = ""
            if employer:
                oh_provider = employer.oh_provider
            if referral:
                ref_number = referral.reference_number
            rows.append({
                "Name": instance.patient.demographics_set.all()[0].name,
                "OH Provider": oh_provider,
                "Their ref number": ref_number or "",
                "Blood number": instance.blood_number,
                "Exposure": instance.exposure,
                "Sample received": instance.blood_date or "",
                "Report submitted": instance.report_st or "",
                "patient_id": instance.patient_id
            })

        if order_param:
            reverse = False
            if order_param.startswith("-"):
                reverse = True
                order_param = order_param.lstrip("-")
            return sorted(rows, key=lambda x: x[order_param], reverse=reverse)
        return rows

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["rows"] = self.get_rows(ctx["object_list"])
        return ctx


class LabReport(DetailView):
    model = Bloods
    template_name = "lab_report.html"
