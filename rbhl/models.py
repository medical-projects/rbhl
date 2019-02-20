"""
rbhl models.
"""
import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import fields

from opal import models
from opal.core.fields import enum
from opal.core import lookuplists

YN = enum('Yes', 'No')

"""
Core Opal models - these inherit from the abstract data models in
opal.models but can be customised here with extra / altered fields.
"""


def calculate_peak_expiratory_flow(height, age, sex):
    # below is the wrong equation that gives
    # close to the correct results... from
    # https://fpnotebook.com/Lung/Lab/PkExprtryFlwRt.htm
    # TODO this is for display purposes only
    if sex == "Male":
        return (((height * 0.0548) + 1.58) - (age * 0.041)) * 60

    if sex == "Female":
        return (((height * 0.0372) + 2.24) - (age * 0.03)) * 60

    # Below is an incorrect version of the right equation
    # import math

    # if sex == "Male":
    #     r = (0.544 * math.log(age)) - (0.0151 * age) - 74.7/(height + 5.48)
    # if sex == "Female":
    #     r = (0.376 * math.log(age)) - (0.0121 * age) - 58.8/(height + 5.63)
    # return math.exp(r)


class Demographics(models.Demographics):
    height = fields.IntegerField(blank=True, null=True, verbose_name='Height(cm)')

    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.date.today()
            return relativedelta(
                today,
                self.date_of_birth
            ).years

    def save(self, *args, **kwargs):
        print("{} {} {}".format(self.height, self.age, self.sex))
        if self.height and self.age and self.sex:
            pef = self.patient.peakexpiratoryflow_set.first()
            pef.save()
        super().save(*args, **kwargs)


class PeakExpiratoryFlow(models.PatientSubrecord):
    _is_singleton = True
    value = fields.IntegerField(blank=True, null=True)

    def calculate_peak_expiratory_flow(self):
        demographics = self.patient.demographics()
        height, age = demographics.height, demographics.age
        sex = demographics.sex

        if not height or not age or not sex:
            return

        return calculate_peak_expiratory_flow(height, age, sex)

    def save(self, *args, **kwargs):
        self.value = self.calculate_peak_expiratory_flow()
        super().save(*args, **kwargs)


class Location(models.Location): pass
class Allergies(models.Allergies): pass

class Diagnosis(models.Diagnosis):
    _title = 'Diagnosis'

class PastMedicalHistory(models.PastMedicalHistory): pass
class Treatment(models.Treatment): pass
class Investigation(models.Investigation): pass
class SymptomComplex(models.SymptomComplex): pass
class PatientConsultation(models.PatientConsultation): pass

# we commonly need a referral route, ie how the patient
# came to the service, but not always.
# class ReferralRoute(models.ReferralRoute): pass

"""
End Opal core models
"""

class ContactDetails(models.PatientSubrecord):
    _is_singleton = True
    _icon         = 'fa fa-phone'

    mobile = fields.CharField(blank=True, null=True, max_length=100)
    phone  = fields.CharField(blank=True, null=True, max_length=100)
    email  = fields.CharField(blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = "Contact details"


class RBHReferrer(lookuplists.LookupList):
    pass


class Referral(models.EpisodeSubrecord):
    _icon         = 'fa fa-level-up'
    _is_singleton = True

    # Deprecated
    referrer_title         = models.ForeignKeyOrFreeText(
        models.Title, verbose_name="Referrer title"
    )
    referrer_name = fields.CharField(
        blank=True, null=True, max_length=100, verbose_name="Referrer name"
    )
    date_of_referral       = fields.DateField(
        blank=True, null=True, verbose_name="Date of referral"
    )

    # Process tracking for admin staff
    date_referral_received = fields.DateField(
        blank=True, null=True, verbose_name="Date referral received"
    )
    # ??
    date_first_contact     = fields.DateField(
        blank=True, null=True, verbose_name="Date of first contact"
    )
    # Used by admin staff
    comments               = fields.TextField(blank=True, null=True)

    attendance = fields.NullBooleanField()
    date_first_appointment = fields.DateField(
        blank=True, null=True, verbose_name="Date of first appointment"
    )
    firefighter         = fields.NullBooleanField()


class Employer(lookuplists.LookupList):
    pass


class OHProvider(lookuplists.LookupList):
    pass


class Employment(models.EpisodeSubrecord):
    _icon         = 'fa fa-building-o'
    _is_singleton = True

    employer = fields.CharField(blank=True, null=True, max_length=100)
    oh_provider = fields.CharField(
        blank=True, null=True, max_length=100, verbose_name="OH provider"
    )


class ClinicLog(models.EpisodeSubrecord):
    _icon         = 'fa fa-hospital-o'
    _is_singleton = True

    seen_by           = fields.CharField(
        blank=True, null=True, max_length=100, verbose_name="Seen by"
    )
    clinic_date        = fields.DateField(blank=True, null=True)
    diagnosis_made    = fields.NullBooleanField(verbose_name="Diagnosis made")
    follow_up_planned = fields.NullBooleanField(verbose_name="Follow up planned")
    date_of_followup  = fields.DateField(
        blank=True, null=True, verbose_name="Date of follow up"
    )

    lung_function       = fields.NullBooleanField(
        verbose_name="Lung function"
    )
    lung_function_date  = fields.DateField(
        blank=True, null=True, verbose_name="Lung function date"
    )
    lung_function_attendance = fields.NullBooleanField(
        verbose_name="Lung function attendance"
    )

    histamine           = fields.NullBooleanField()
    histamine_date      = fields.DateField(
        blank=True, null=True, verbose_name="Histamine date"
    )
    histamine_attendance = fields.NullBooleanField(
        verbose_name="Histamine attendance"
    )

    peak_flow           = fields.NullBooleanField(
        verbose_name="Peak flow"
    )

    other_rbh_bloods    = fields.NullBooleanField(
        verbose_name="Other RBH bloods"
    )
    immunology_oem      = fields.NullBooleanField(
        verbose_name="Immunology OEM"
    )

    other_hospital_info = fields.NullBooleanField(
        verbose_name="Other hospital info"
    )
    other_oh_info       = fields.NullBooleanField(
        verbose_name="Other OH info"
    )
    other_gp_info       = fields.NullBooleanField(
        verbose_name="Other GP info"
    )
    work_samples        = fields.NullBooleanField(
        verbose_name="Work samples"
    )

    active              = fields.NullBooleanField()

    class Meta:
        verbose_name = "Clinic log"


    def days_since_first_attended(self):
        if not self.clinic_date:
            return None
        today = datetime.date.today()
        diff = today - self.clinic_date
        return diff.days


class Letter(models.EpisodeSubrecord):
    _icon = 'fa fa-envelope'

    text = fields.TextField(blank=True, null=True)


class PeakFlowDay(models.EpisodeSubrecord):
    _sort = '-date'

    date = fields.DateField(blank=True, null=True)
    treatment_taken = fields.CharField(max_length=200, blank=True, null=True)
    note = fields.TextField()

    day_num = fields.IntegerField(blank=True, null=True)
    trial_num = fields.IntegerField(blank=True, null=True)

    work_start = fields.IntegerField(blank=True, null=True)
    work_end   = fields.IntegerField(blank=True, null=True)

    flow_0000 = fields.IntegerField(blank=True, null=True, verbose_name="00:00")
    flow_0100 = fields.IntegerField(blank=True, null=True, verbose_name="01:00")
    flow_0200 = fields.IntegerField(blank=True, null=True, verbose_name="02:00")
    flow_0300 = fields.IntegerField(blank=True, null=True, verbose_name="03:00")
    flow_0400 = fields.IntegerField(blank=True, null=True, verbose_name="04:00")
    flow_0500 = fields.IntegerField(blank=True, null=True, verbose_name="05:00")

    flow_0600 = fields.IntegerField(blank=True, null=True, verbose_name="06:00")
    flow_0700 = fields.IntegerField(blank=True, null=True, verbose_name="07:00")
    flow_0800 = fields.IntegerField(blank=True, null=True, verbose_name="08:00")
    flow_0900 = fields.IntegerField(blank=True, null=True, verbose_name="09:00")
    flow_1000 = fields.IntegerField(blank=True, null=True, verbose_name="10:00")
    flow_1100 = fields.IntegerField(blank=True, null=True, verbose_name="11:00")
    flow_1200 = fields.IntegerField(blank=True, null=True, verbose_name="12:00")
    flow_1300 = fields.IntegerField(blank=True, null=True, verbose_name="13:00")
    flow_1400 = fields.IntegerField(blank=True, null=True, verbose_name="14:00")
    flow_1500 = fields.IntegerField(blank=True, null=True, verbose_name="15:00")
    flow_1600 = fields.IntegerField(blank=True, null=True, verbose_name="16:00")
    flow_1700 = fields.IntegerField(blank=True, null=True, verbose_name="17:00")
    flow_1800 = fields.IntegerField(blank=True, null=True, verbose_name="18:00")
    flow_1900 = fields.IntegerField(blank=True, null=True, verbose_name="19:00")
    flow_2000 = fields.IntegerField(blank=True, null=True, verbose_name="20:00")
    flow_2100 = fields.IntegerField(blank=True, null=True, verbose_name="21:00")
    flow_2200 = fields.IntegerField(blank=True, null=True, verbose_name="22:00")
    flow_2300 = fields.IntegerField(blank=True, null=True, verbose_name="23:00")

    class Meta:
        ordering = ["day_num"]



"""
Begin exploratory models during testing
"""


class Occupation(models.EpisodeSubrecord):
    _is_singleton = True
    currently_employed = fields.CharField(max_length=200, choices=YN, blank=True, null=True)
    job_title = fields.CharField(max_length=200, blank=True, null=True)
    name_of_employer = fields.CharField(max_length=200, blank=True, null=True)
    exposures = fields.TextField(blank=True, null=True)


class DiagnosisAsthma(models.EpisodeSubrecord):
    _is_singleton = True

    asthma = fields.CharField(max_length=200, blank=True, null=True)
    exacerbated_by_work = fields.CharField(max_length=200, blank=True, null=True)
    irritant_induced_asthma = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN
    )
    sensitisation = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN,
        verbose_name="Occupational asthma caused by sensitisation"
    )
    sensitising_agent = fields.TextField(blank=True, null=True)
    non_occupational_asthma = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN
    )


class DiagnosisRhinitis(models.EpisodeSubrecord):
    _is_singleton = True

    rhinitis = fields.CharField(max_length=200, blank=True, null=True)
    work_exacerbated = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN,
        verbose_name="Occupational asthma caused by sensitisation"
    )
    sensitisation = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN,
        verbose_name="Occupational rhinitis caused by sensitisation"
    )
    cause = fields.TextField(blank=True, null=True)
    non_occupational_rhinitis = fields.CharField(
        max_length=200, blank=True, null=True,
        choices=YN
    )
