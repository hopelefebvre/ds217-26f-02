"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Returns systolic readings from encounter records"""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Returns the mean systolic BP or None if no systolic BP readings"""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Counts the number of distinct patients in the encounters list."""
    patient_ids = []
    for encounter in encounters:
        patient_ids.append(encounter["patient_id"])
    unique_patient_ids = set(patient_ids)
    return len(unique_patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Create follow-up list of unique patient IDs whose systolic reading is at or above cutoff."""
    followup_list = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            followup_list.append(encounter["patient_id"])
    return list(set(followup_list)) 
