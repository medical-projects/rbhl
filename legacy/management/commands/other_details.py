import csv

from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone
from opal import models as opal_models
from rbhl import models
from legacy.build_lookup_list import build_lookup_list
from legacy.models import (
    Details,
    DiagnosticAsthma,
    DiagnosticOther,
    DiagnosticOutcome,
    DiagnosticRhinitis,
    DiagnosticTesting,
    OtherFields,
    PatientNumber,
    SuspectOccupationalCategory,
)

from ..utils import to_bool, to_date, to_float, to_int


_sensitivies_translation = {
    "Rats": (
        "animals (rats)", "rat", 'animals - rats', '(rats)', 'animals rats'
    ),
    "Mice": (
        "mouse", 'animals mice', 'animals (mice)', 'animals - mice', '(mice)',
        'animals- mice', '(mouse)', 'animals (mouse)', 'animals (mice)'
    ),
    "Rats and mice": (
        'animals rats & mice', 'rats & mice', 'animals - rats & mice',
        'rat /mouse', 'animals rats and mice', '-rats & mice', 'rats and dogs',
        '(rats & mice)', 'mice/rat', 'animals - rat and mouse',
        'animals (rats & mice)', 'animals rat & mouse',
        'animals- mice and rats', 'rat and  mouse', 'rat/mouse',
        'mouse & rat', '(rat & mouse)', 'animals (rat or mouse)'
        'rat and mouse', 'animals rats and mice', 'animals rats & mice'
    ),
    "Bakers amylase": (
        '(bakers amylase)',
        'enzymes - (bakers amylase)',
        '( bakers amylase)',
        'enzymes -(bakers amylase)',
        'enzymes -bakers amylase',
        'enzymes - bakers amylase',
        "enzymes - other (bakers amylase)",
        'enzymes - bakers amylase'
    ),
    "Alpha amylase": [
        'enzymes - alpha amylase',
        'enzymes - other (alpha amylase)',
        'enzymes - other - alpha amylase',
        'enzymes -alpha amylase',
        'enzymes - (alpha amylase)',
        'enzymes - other(alpha amylase)',
        'enzymes - other alpha amylase',
        '(alpha amylase)',
        'enzymes  (alpha amylase)',
        'enzymes - other, alpha amylase',
        'enzymes alpha amylase',
    ],
    "Morphine": [
        '-morphine',
        '(morphine)',
        'pharmaceuticals - morphine'
    ],
    "Amylase": [
        "enzymes - other (amylase)",
        "enzymes - amylase",
        "(amylase)",
        "enzymes - (amylase)"
    ]
}


def generate_sensitivies_lut():
    sensitivites_lut = {}
    for i, v in _sensitivies_translation.items():
        for y in v:
            sensitivites_lut[y] = i
        sensitivites_lut[i.lower()] = i
    return sensitivites_lut


def clean_sensitivies(sensitivities, sensitivities_lut):
    cleaned = [
        i.strip() for i in sensitivities.split("\n") if i.strip()
    ]

    cleaned = [sensitivities_lut.get(i.lower(), i) for i in cleaned]
    cleaned = list(set([
        i.strip() for i in sensitivities.split("\n") if i.strip()
    ]))
    return "\n".join(sorted(cleaned))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_name", help="Specify import file")

    def build_details(self, patientLUT, rows):

        for row in rows:

            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield Details(
                patient=patient,
                created=timezone.now(),
                date_referral_received=to_date(row["Date referral written"]),
                referral_type=row["referral"],
                referral_reason=row["Referral_reason"],
                fire_service_applicant=row["Fireapplicant"],
                systems_presenting_compliant=row["reason_other"],
                referral_disease=row["Referral_disease"],
                geographical_area=row["Geographical_area"],
                geographical_area_other=row["Geographical_other"],
                site_of_clinic=row["Site of Clinic"],
                other_clinic_site=row["Other Clinic Site"],
                clinic_status=row["Clinic_status"],
                previous_atopic_disease=row["AtopicDisease"],
                has_asthma=to_bool(row["Asthma"]),
                has_hayfever=to_bool(row["Hayfever"]),
                has_eczema=to_bool(row["Eczema"]),
                is_smoker=row["Smoker"],
                smokes_per_day=to_int(row["No_cigarettes"]),
                referring_doctor=row["Referring_doctor"],
                specialist_doctor=row["Specialist_Dr"],
                attendance_date=to_date(row["Attendance_date"]),
            )

    def convert_details(self, patient, episode):
        """
        Maps
        Details.date_referral_received" -> Referral.date_referral_received
        Details.attendance_date -> Referral.date_first_appointment
        Details.referral_type -> Referral.referral_type
        Details.referral_type -> Referral.referral_type
        Details.referral_reason -> Referral.referral_reason
        Details.fire_service_applicant -> Employment.firefighter
        Details.systems_presenting_compliant ->     Referral.comments
        Details.referral_disease -> Referral.referral_disease
        Details.specialist_doctor -> ClinicLog.seen_by
        Details.referring_doctor -> Referral.referrer_name
        Details.geographical_area or Details.geographical_area_other ->
            Referral.geographical_area
        Details.is_smoker = SocialHistory.smoker
        Details.smokes_per_day = SocialHistory.cigerettes_per_day
        """

        details = patient.details_set.all()[0]
        if not details:
            return
        clinic_log = episode.cliniclog_set.all()[0]

        if not clinic_log.seen_by:
            if details.specialist_doctor:
                clinic_log.seen_by = details.specialist_doctor
                clinic_log.save()

        if details and details.site_of_clinic:
            if details.site_of_clinic == "Other":
                clinic_log.clinic_site = details.site_of_clinic
            else:
                clinic_log.clinic_site = details.other_clinic_site
            clinic_log.save()

        referral = episode.referral_set.all()[0]

        REFERRAL_FIELDS = [
            "date_referral_received",
            "referral_type",
            "referral_reason",
        ]

        for referral_field in REFERRAL_FIELDS:
            if not getattr(referral, referral_field):
                details_value = getattr(details, referral_field)
                if details_value:
                    setattr(referral, referral_field, details_value)

        if not referral.referral_disease:
            referral_disease = details.referral_disease
            # this is a strangely common error
            if referral_disease == "Pulmonary fibrosis(eg: Asbestos related disease":
                referral_disease = "Pulmonary fibrosis(eg: Asbestos related disease)"
            referral.referral_disease = referral_disease

        if not referral.referral_type:
            referral_type = details.referral_type
            if referral_type:
                if referral_type.lower() == 'other (self)':
                    referral_type = "Self"
                elif referral_type == "self":
                    referral_type = "Self"
                elif referral_type == "Other doctor- GP":
                    referral_type = "GP"
                referral.referral_type = referral_type

        if not referral.geographical_area:
            area = details.geographical_area
            if area:
                if area == "SouthThames":
                    area = "South Thames"
                elif area == "North thames":
                    area = "North Thames"
                elif area.lower() == "other" and details.geographical_area_other:
                    area = details.geographical_area_other
                referral.geographical_area = area

        if not referral.referrer_name:
            if details.referring_doctor:
                referral.referrer_name = details.referring_doctor

        if not referral.date_first_appointment:
            if details.attendance_date:
                referral.date_first_appointment = details.attendance_date
        referral.save()

        employment = episode.employment_set.all()[0]
        if employment.firefighter is None:
            fsa = details.fire_service_applicant
            if fsa:
                fire_service_lut = {"no": False, "yes": True}
                employment.firefighter = fire_service_lut.get(fsa.lower())
                employment.save()

        social_history = episode.socialhistory_set.all()[0]
        if not social_history.smoker:
            if details.is_smoker:
                if details.is_smoker == "Currently":
                    social_history.smoker = "Current"
                else:
                    social_history.smoker = details.is_smoker

        if not social_history.cigerettes_per_day:
            if details.smokes_per_day:
                social_history.cigerettes_per_day = details.smokes_per_day
        social_history.save()

        clinic_log = episode.cliniclog_set.all()[0]
        if not clinic_log.presenting_complaint:
            clinic_log.presenting_complaint = details.systems_presenting_compliant
        clinic_log.save()

    def build_suspect_occupational_category(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            def get_year(some_str):
                if some_str and len(some_str) == 2:
                    as_int = int(some_str)
                    if as_int < 21:
                        return "20{}".format(some_str)
                    else:
                        return "19{}".format(some_str)
                return some_str

            def none_if_0(some_str):
                if some_str == 0:
                    return
                return some_str

            yield SuspectOccupationalCategory(
                patient=patient,
                created=timezone.now(),
                is_currently_employed=to_bool(row["Employed"]),
                suspect_occupational_category=row["Occupation_category"],
                job_title=row["Occupation_other"],
                exposures=row["Exposures"],
                employer=row["Employer"],
                is_employed_in_suspect_occupation=row["Current_employment"],
                month_started_exposure=row["Date started"],
                year_started_exposure=row["Dates_st_Exposure_Y"],
                month_finished_exposure=row["Date Finished"],
                year_finished_exposure=row["Dates_f_Exposure_Y"],
            )

    def convert_suspect_occupational_category(self, patient, episode, sensitivites_lut):
        """
        Maps

        SuspectOccupationalCategory.job_title
            -> Employment.job_title
        SuspectOccupationalCategory.employer_name
            -> Employment.employer
        SuspectOccupationalCategory.suspect_occupational_category
            -> Employment.employment_category
        SuspectOccupationalCategory.is_employed_in_suspect_occupation
            -> Employment.employed_in_suspect_occupation
        SuspectOccupationalCategory.exposures
            -> Employment.exposures
        """
        # TODO this sometimes returns multiple
        suspect_occupational_category = patient.suspectoccupationalcategory_set.all()[0]
        employment = episode.employment_set.all()[0]
        if not employment.job_title:
            employment.job_title = suspect_occupational_category.job_title

        if not employment.employment_category:
            emp_cat = suspect_occupational_category.suspect_occupational_category
            employment.employment_category = emp_cat

        if not employment.employer:
            emp_name = suspect_occupational_category.employer_name
            employment.employment_category = emp_name

        sus = suspect_occupational_category.is_employed_in_suspect_occupation
        if sus:
            employment.employed_in_suspect_occupation = sus

        existing_exposures = employment.exposures

        if not existing_exposures:
            existing_exposures = ""

        employment.exposures = clean_sensitivies("{}\n{}".format(
            existing_exposures, suspect_occupational_category.exposures,
        ), sensitivites_lut)
        employment.save()

    def build_diagnostic_testing(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield DiagnosticTesting(
                patient=patient,
                created=timezone.now(),
                antihistimines=to_bool(row["Antihistimines"]),
                skin_prick_test=to_bool(row["SkinPrick_test"]),
                atopic=row["Atopic"],
                specific_skin_prick=to_bool(row["SpecificSkinPrick"]),
                serum_antibodies=to_bool(row["Serum_antibodies"]),
                bronchial_prov_test=to_bool(row["BronchialProvTest"]),
                change_pc_20=row["ChangePC20"],
                nasal_prov_test=to_bool(row["NasalProvTest"]),
                positive_reaction=to_bool(row["PositiveReaction"]),
                height=row["Height"],
                fev_1=to_float(row["FEV1"]),
                fev_1_post_ventolin=to_float(row["FEV1PostVentolin"]),
                fev_1_percentage_protected=to_int(row["FEV1%pred"]),
                fvc=to_float(row["FVCpPreVentolin"]),
                fvc_post_ventolin=to_float(row["FVCPostVentolin"]),
                fvc_percentage_protected=to_int(row["FVC%pred"]),
                is_serial_peak_flows_requested=to_bool(row["SerialPERF"]),
                has_spefr_variability=row["PERFVariablility"],
                is_returned=to_bool(row["Returned?"]),
                is_spefr_work_related=row["PERFWorkRelate"],
                ct_chest_scan=to_bool(row["CTChestScan"]),
                ct_chest_scan_date=to_date(row["CTdate"]),
                full_lung_function=to_bool(row["FullPulFunTest"]),
                full_lung_function_date=to_date(row["LFTdate"]),
            )

    def convert_diagnostic_testing(self, patient, episode):
        """
        Maps

        DiagnosticTesting.height
            -> Demographics.height
        DiagnosticTesting.skin_prick_test
            -> creates a skin prick test
        DiagnosticTesting.serum_antibodies
            -> ClinicLog.immunology_oem
        DiagnosticTesting.atopic
            -> ClinicLog.atopic
        DiagnosticTesting.fev_1
            -> RbhlDiagnosticTesting.fev_1
        DiagnosticTesting.fev_1_post_ventolin
            -> RbhlDiagnosticTesting.fev_1_post_ventolin
        DiagnosticTesting.fev_1_percentage_protected
            -> RbhlDiagnosticTesting.fev_1_percentage_protected
        DiagnosticTesting.fvc
            -> RbhlDiagnosticTesting.fvc
        DiagnosticTesting.fvc_post_ventolin
            -> RbhlDiagnosticTesting.fvc_post_ventolin
        DiagnosticTesting.ct_chest_scan
            -> RbhlDiagnosticTesting.ct_chest_scan
        DiagnosticTesting.ct_chest_scan_date
            -> RbhlDiagnosticTesting.ct_chest_scan_date
        DiagnosticTesting.full_lung_function
            -> RbhlDiagnosticTesting.full_lung_function
        DiagnosticTesting.full_lung_function_date
            -> RbhlDiagnosticTesting.full_lung_function_date
        """
        legacy_diagnostic_testing = patient.diagnostictesting_set.all()[0]

        height = patient.demographics_set.all()[0].height
        if height:
            if legacy_diagnostic_testing.height:
                height = to_int(legacy_diagnostic_testing.height)
                patient.demographics_set.update(
                    height=height
                )

        clinic_log = None

        if legacy_diagnostic_testing.serum_antibodies:
            clinic_log = episode.cliniclog_set.all()[0]
            clinic_log.immunology_oem = legacy_diagnostic_testing.serum_antibodies

        if legacy_diagnostic_testing.atopic:
            if not clinic_log:
                clinic_log = episode.cliniclog_set.all()[0]
            clinic_log.atopic = legacy_diagnostic_testing.atopic

        if clinic_log:
            clinic_log.save()

        if legacy_diagnostic_testing.antihistimines:
            skin_prick_test  = models.SkinPrickTest(episode=episode)
            skin_prick_test.antihistimines = legacy_diagnostic_testing.antihistimines
            skin_prick_test.save()

        SPIROMETRY_FIELDS = [
            "fev_1", "fev_1_post_ventolin", "fev_1_percentage_protected",
            "fvc", "fvc_post_ventolin", "fvc_percentage_protected"
        ]

        if any([
            getattr(legacy_diagnostic_testing, i) for i in SPIROMETRY_FIELDS
        ]):
            spirometry  = models.Spirometry(episode=episode)
            for field in SPIROMETRY_FIELDS:
                field_value = getattr(legacy_diagnostic_testing, field)
                setattr(spirometry, field, field_value)
            spirometry.save()

        if any([
            legacy_diagnostic_testing.ct_chest_scan,
            legacy_diagnostic_testing.ct_chest_scan_date,
            legacy_diagnostic_testing.full_lung_function,
            legacy_diagnostic_testing.full_lung_function_date
        ]):
            other_investigations = models.OtherInvestigations(
                episode=episode
            )
            ct_scan = legacy_diagnostic_testing.ct_chest_scan
            ct_scan_date = legacy_diagnostic_testing.ct_chest_scan_date
            lung_function = legacy_diagnostic_testing.full_lung_function
            lung_function_date = legacy_diagnostic_testing.full_lung_function_date
            other_investigations.ct_chest_scan = ct_scan
            other_investigations.ct_chest_scan_date = ct_scan_date
            other_investigations.full_lung_function = lung_function
            other_investigations.full_lung_function_date = lung_function_date
            other_investigations.save()

    def build_diagnostic_outcome(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield DiagnosticOutcome(
                patient=patient,
                created=timezone.now(),
                diagnosis=row["Diagnosis"],
                diagnosis_date=to_date(row["Date of Diagnosis"]),
                referred_to=row["Diagnosis_referral"],
            )

    def convert_diagnostic_outcome(self, patient, episode):
        """
        diagnosis -> Clinic Log.diagnosis_outcome
        referred_to -> Clinic Log.referred_to
        diagnosis date -> clinic date if not populated
        """
        diagnosis_outcome = patient.diagnosticoutcome_set.all()[0]
        clinic_log = episode.cliniclog_set.all()[0]
        clinic_log.diagnosis_outcome = diagnosis_outcome.diagnosis
        clinic_log.referred_to = diagnosis_outcome.referred_to
        if not clinic_log.clinic_date:
            clinic_log.clinic_date = diagnosis_outcome.diagnosis_date
        clinic_log.save()

    def build_diagnostic_asthma(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield DiagnosticAsthma(
                patient=patient,
                created=timezone.now(),
                asthma=to_bool(row["DiagnosisAsthma"]),
                is_exacerbated_by_work=to_bool(row["AsthmaExacerbate"]),
                has_infant_induced_asthma=to_bool(row["AsthmaOccInt"]),
                occupational_asthma_caused_by_sensitisation=to_bool(
                    row["AsthmaOccSen"]
                ),
                sensitising_agent=row["AsthmaOccSenCause"],
                has_non_occupational_asthma=to_bool(row["AsthmaNonOcc"]),
            )

    def convert_to_diagnosis_asthma(self, patient, episode, sensitivities_lut):
        legacy_asthma = patient.diagnosticasthma_set.all()[0]

        if any([
            legacy_asthma.asthma,
            legacy_asthma.is_exacerbated_by_work,
            legacy_asthma.has_infant_induced_asthma,
            legacy_asthma.occupational_asthma_caused_by_sensitisation,
            legacy_asthma.has_non_occupational_asthma
        ]):
            asthma = models.Asthma(episode=episode)

            asthma.sensitivities = clean_sensitivies(
                legacy_asthma.sensitising_agent, sensitivities_lut
            )
            # order of priority for what overrides
            # occupational asthma caused by sensitisation > is exacerbated by work >
            # has irritant induced asthma > has non occupational asthma

            option = ""

            if legacy_asthma.occupational_asthma_caused_by_sensitisation:
                option = models.Asthma.OCCUPATIONAL_CAUSED_BY_SENSITISATION
            elif legacy_asthma.is_exacerbated_by_work:
                option = models.Asthma.EXACERBATED_BY_WORK
            elif legacy_asthma.has_infant_induced_asthma:
                option = models.Asthma.IRRITANT_INDUCED
            elif legacy_asthma.has_non_occupational_asthma:
                option = models.Asthma.NON_OCCUPATIONAL

            asthma.trigger = option
            asthma.save()

    def build_diagnostic_rhinitis(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            # FIXME: there is a single row where this field has the value "x"
            # in the data as of 2019/03/25.  The surrounding data makes it look
            # like this is a typo (since there is no surrounding data).
            RhinitisNonOcc = row["RhinitisNonOcc"]
            if RhinitisNonOcc != "x":
                has_non_occ_rhinitis = to_bool(RhinitisNonOcc)
            else:
                has_non_occ_rhinitis = None

            yield DiagnosticRhinitis(
                patient=patient,
                created=timezone.now(),
                rhinitis=to_bool(row["DiagnosisRhinitis"]),
                work_exacerbated=to_bool(row["RhinitisExacerbate"]),
                occupational_rhinitis_caused_by_sensitisation=to_bool(
                    row["RhinitisOccSen"]
                ),
                rhinitis_occupational_sensitisation_cause=row[
                    "RhinitisOccSenCause"
                ],
                has_non_occupational_rhinitis=has_non_occ_rhinitis,
            )

    def convert_to_diagnosis_rhinitis(self, patient, episode, sensitivities_lut):
        legacy_rhinitis = patient.diagnosticrhinitis_set.all()[0]

        if any([
            legacy_rhinitis.rhinitis,
            legacy_rhinitis.work_exacerbated,
            legacy_rhinitis.occupational_rhinitis_caused_by_sensitisation,
            legacy_rhinitis.has_non_occupational_rhinitis
        ]):
            rhinitis = models.Rhinitis(episode=episode)

            # order of priority for what overrides
            # occupational_rhinitis_caused_by_sensitisation > work_exacerbated >
            # has non occupational asthma

            option = ""

            if legacy_rhinitis.occupational_rhinitis_caused_by_sensitisation:
                option = models.Rhinitis.OCCUPATIONAL_CAUSED_BY_SENSITISATION
            elif legacy_rhinitis.work_exacerbated:
                option = models.Rhinitis.EXACERBATED_BY_WORK
            elif legacy_rhinitis.has_non_occupational_rhinitis:
                option = models.Rhinitis.NON_OCCUPATIONAL

            rhinitis.trigger = option

            rhinitis.sensitivities = clean_sensitivies(
                legacy_rhinitis.rhinitis_occupational_sensitisation_cause,
                sensitivities_lut
            )

            rhinitis.save()

    def build_diagnostic_other(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield DiagnosticOther(
                patient=patient,
                created=timezone.now(),
                copd=to_bool(row["ChronicAirFlow"]),
                emphysema=to_bool(row["Emphsema"]),
                copd_with_emphysema=to_bool(row["COPD&emph"]),
                # copd_is_occupational=row[""],
                malignancy=to_bool(row["Malignancy"]),
                malignancy_is_occupational=to_bool(row["MalignancyType"]),
                malignancy_type=row["MalignancyTypeChoice"],
                malignancy_type_other=row["MalignancyTypeChoiceOther"],
                NAD=to_bool(row["NAD"]),
                diffuse_lung_disease=to_bool(row["DiffuseLungDis"]),
                diffuse_lung_disease_is_occupational=to_bool(
                    row["DiffuseLungDisChoice"]
                ),
                diffuse_lung_disease_type=row["DiffuseLungDisType"],
                diffuse_lung_disease_type_other=row["DiffuseLungDisTypeOther"],
                benign_pleural_disease=to_bool(row["BenignPleuralDis"]),
                benign_pleural_disease_type=row["BenignPleuralDisType"],
                other_diagnosis=to_bool(row["OtherDiag"]),
                other_diagnosis_is_occupational=to_bool(
                    row["OtherDiagChoice"],
                ),
                other_diagnosis_type=row["OtherDiagChoiceType"],
                other_diagnosis_type_other=row["OtherDiagOther"],
            )

    def convert_to_diagnosis_other(self, patient, episode):
        other = patient.diagnosticother_set.all()[0]

        if any([
            other.copd,
            other.emphysema,
            other.copd_with_emphysema,
        ]):
            chronic_air_flow_limitation = models.ChronicAirFlowLimitation(
                episode=episode
            )
            if other.copd_with_emphysema:
                chronic_air_flow_limitation.copd = True
                chronic_air_flow_limitation.emphysema = True
            else:
                chronic_air_flow_limitation.copd = bool(other.copd)
                chronic_air_flow_limitation.emphysema = bool(other.emphysema)
            chronic_air_flow_limitation.occupational = bool(other.copd_is_occupational)
            chronic_air_flow_limitation.save()

        if any([
            other.malignancy,
            other.malignancy_type,
            other.malignancy_type_other
        ]):
            malignancy = models.Malignancy(episode=episode)

            if other.malignancy_type_other:
                malignancy.malignancy_type = other.malignancy_type_other
            elif other.malignancy_type:
                malignancy.malignancy_type = other.malignancy_type

            malignancy.occupational = bool(other.malignancy_is_occupational)
            malignancy.save()

        if other.NAD:
            clinic_log = episode.cliniclog_set.all()[0]
            clinic_log.no_appreciable_disease = True

        if any([
            other.diffuse_lung_disease,
            other.diffuse_lung_disease_type,
            other.diffuse_lung_disease_type_other,
        ]):
            diffuse_lung_disease = models.DiffuseLungDisease(episode=episode)
            lung_disease_type = other.diffuse_lung_disease_type_other

            if not lung_disease_type:
                lung_disease_type = other.diffuse_lung_disease_type
            diffuse_lung_disease.disease_type = lung_disease_type
            occupational = other.diffuse_lung_disease_is_occupational
            diffuse_lung_disease.occupational = bool(occupational)
            diffuse_lung_disease.save()

        if any([
            other.benign_pleural_disease,
            other.benign_pleural_disease_type,
        ]):
            benign_pleural_disease = models.BenignPleuralDisease(episode=episode)
            disease_type = other.benign_pleural_disease_type
            if other.benign_pleural_disease_type:
                if other.benign_pleural_disease_type == "Difuse":
                    benign_pleural_disease.disease_type = "Diffuse"
                else:
                    benign_pleural_disease.disease_type = disease_type
            benign_pleural_disease.save()

        if any([
            other.other_diagnosis_type,
            other.other_diagnosis_type_other,
            other.other_diagnosis,
        ]):
            other_diagnosis = models.OtherDiagnosis(episode=episode)
            condition = ""
            if other.other_diagnosis_type_other:
                condition = other.other_diagnosis_type_other
            elif other.other_diagnosis_type:
                condition = other.other_diagnosis_type
            condition = condition.strip()

            if condition.lower() == "acute pneumonitis":
                condition = "Chemical pneumonitis"

            if condition.lower() == "building related illness":
                condition = "Building related symptoms"

            if condition.lower() == "hyperventilation":
                condition = "Breathing pattern disorder"
            other_diagnosis.diagnosis_type = condition
            other_diagnosis.occupational = bool(other.other_diagnosis_is_occupational)
            other_diagnosis.save()

    def build_other(self, patientLUT, rows):
        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue

            yield OtherFields(
                patient=patient,
                created=timezone.now(),
                other_det_num=row["OtherDet_Num"],

                referral=row["referral"],
                # reason_other=row["reason_other"],
                # occupation_other=row["Occupation_other"],
                asthma_relate_work=row["AsthmaRelateWork"],
                chronic_air_flow=row["ChronicAirFlow"],
                chronic_air_flow_choice=row["ChronicAirFlowChoice"],
                chronic_obstructive_brinchitis=row[
                    "ChronicObstructiveBrinchitis"
                ],
            )

    def flush(self):
        Details.objects.all().delete()
        SuspectOccupationalCategory.objects.all().delete()
        DiagnosticTesting.objects.all().delete()
        DiagnosticOutcome.objects.all().delete()
        DiagnosticAsthma.objects.all().delete()
        DiagnosticRhinitis.objects.all().delete()
        DiagnosticOther.objects.all().delete()
        OtherFields.objects.all().delete()

    @transaction.atomic
    def convert_legacy_to_rbhl(self):
        referral_types = [
            'Company or Group OHS doctor',
            'GP',
            'Hospital Doctor(Brompton)',
            'Hospital Doctor(Other)',
            'Medico-legal',
            'Other doctor',
            'Occ Health',
            'Self',
            'Company or Group OHS nurse',
            'Resp nurse community',
        ]

        for referral_type in referral_types:
            if not opal_models.ReferralType.objects.filter(
                name__iexact=referral_type
            ).exists():
                opal_models.ReferralType.objects.get_or_create(
                    name=referral_type
                )

        diagnosis_outcomes = [
            "Known",
            "Not established referred to someone else",
            "Not established lost to follow-up",
            "Not reached despite investigation",
            "Not established patient withdrew",
            "Investigations continuing"
        ]

        for diagnosis_outcome in diagnosis_outcomes:
            models.DiagnosisOutcome.objects.get_or_create(
                name=diagnosis_outcome
            )

        qs = opal_models.Patient.objects.exclude(details=None)
        qs = qs.prefetch_related(
            "diagnosticother_set",
            "details_set",
            "suspectoccupationalcategory_set",
            "diagnostictesting_set",
            "diagnosticoutcome_set",
            "diagnosticasthma_set",
            "diagnosticrhinitis_set",
            "diagnosticother_set",
            "demographics_set",
        )

        episodes = opal_models.Episode.objects.filter(
            patient__in=qs
        ).prefetch_related(
            "cliniclog_set",
            "employment_set",
            "referral_set",
            "socialhistory_set",
        )

        if not qs.count() == episodes.count():
            raise ValueError("not all patients have a single episode")

        patient_id_to_episode = {
            i.patient_id: i for i in episodes
        }
        sensitivities_lut = generate_sensitivies_lut()
        for patient in qs:
            self.convert_details(
                patient, patient_id_to_episode[patient.id]
            )
            self.convert_suspect_occupational_category(
                patient, patient_id_to_episode[patient.id],
                sensitivities_lut
            )
            self.convert_diagnostic_testing(
                patient, patient_id_to_episode[patient.id]
            )
            self.convert_diagnostic_outcome(
                patient, patient_id_to_episode[patient.id]
            )
            self.convert_to_diagnosis_asthma(
                patient, patient_id_to_episode[patient.id],
                sensitivities_lut
            )
            self.convert_to_diagnosis_rhinitis(
                patient, patient_id_to_episode[patient.id],
                sensitivities_lut
            )
            self.convert_to_diagnosis_other(
                patient, patient_id_to_episode[patient.id]
            )

        build_lookup_list(models.ClinicLog, models.ClinicLog.presenting_complaint)
        build_lookup_list(models.Employment, models.Employment.job_title)

    @transaction.atomic
    def create_legacy(self, file_name):
        self.flush()
        with open(file_name, encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))

        patient_ids = (row["Patient_num"] for row in rows)
        patient_nums = PatientNumber.objects.filter(value__in=patient_ids)
        patientLUT = {p.value: p.patient for p in patient_nums}

        # TODO: print missing patient IDs here

        # REMAINING FIELDS
        Details.objects.bulk_create(self.build_details(patientLUT, rows))

        SuspectOccupationalCategory.objects.bulk_create(
            self.build_suspect_occupational_category(patientLUT, rows)
        )

        DiagnosticTesting.objects.bulk_create(
            self.build_diagnostic_testing(patientLUT, rows)
        )
        DiagnosticOutcome.objects.bulk_create(
            self.build_diagnostic_outcome(patientLUT, rows)
        )
        DiagnosticAsthma.objects.bulk_create(
            self.build_diagnostic_asthma(patientLUT, rows)
        )
        DiagnosticRhinitis.objects.bulk_create(
            self.build_diagnostic_rhinitis(patientLUT, rows)
        )
        DiagnosticOther.objects.bulk_create(
            self.build_diagnostic_other(patientLUT, rows)
        )
        OtherFields.objects.bulk_create(self.build_other(patientLUT, rows))

        for row in rows:
            patient = patientLUT.get(row["Patient_num"], None)

            if patient is None:
                continue
            # CONVERTED FIELDS

            demographics = patient.demographics_set.get()
            demographics.hospital_number = row["Hospital Number"]
            demographics.save()

        msg = "Imported {} other details rows".format(len(rows))
        self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        self.create_legacy(options["file_name"])
        self.convert_legacy_to_rbhl()
