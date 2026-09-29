#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Defines a usable encounter: has three fields, a systolic reading that can be read as an int, and a systolic reading that is plausible (between 60 and 250 inclusive).

    Returns two values: the list of usable encounters, and how many data
    rows were skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    with data_path.open("r", encoding="utf-8") as data_file:
        rows = data_file.readlines()
    encounters = []
    skipped = 0
    for row in rows[1:]:                      # removes rows[0] (header line)
        if not row.strip():                   # skips blank lines
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")       #sets split at commas
        if len(fields) != 3:                  #checks for 3 fields, otherwise skips
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, systolic = fields
        try:
            systolic = int(systolic)           #checks if systolic is an int, otherwise skips
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
        else:                                  #checks if systolic is in plausible range, otherwise skips
            if systolic < 60 or systolic > 250:
                print(f"Skipping {patient_id}: recording error systolic {systolic}")
                skipped += 1
            else:                               #if all checks pass, adds the encounter to the list
                encounters.append({"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic})
    return encounters, skipped


def main():
    """This generates two reports from the clinic data: 1 being a vitals report with usable encounters, skipped rows, and summary statistics and 2 being a follow-up list of patients with systolic readings at or above a cutoff value."""
    encounters, skipped = read_encounters(DATA_PATH)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
    # TODO: read the file back and print it, so you can see what was saved.
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.
    readings = systolic_readings(encounters)
    mean = mean_systolic(readings)
    count = count_patients(encounters)
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "vitals_report.txt"
    lines = []
    lines.append(f"Usable encounters: {len(encounters)}")
    lines.append(f"Skipped rows: {skipped}")
    lines.append(f"Patients seen: {count}")
    lines.append(f"Mean systolic: {mean:.1f} mmHg")
    lines.append(f"Highest systolic: {max(readings)} mmHg")
    lines.append(f"Lowest systolic: {min(readings)} mmHg")
    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines))
    with report_path.open("r", encoding="utf-8") as report_file:
        print(report_file.read())

    fu_path = OUTPUT_DIR / "followup_list.txt"
    cutoff = 130
    followup = patients_at_or_above(encounters, cutoff)
    lines = []
    lines.append(f"Cutoff: {cutoff} mmHg")
    lines.append("Reason: Assuming this is a primary care clinic, 130 is the systolic cutoff where real intervention (lifestyle changes or meds) would be considered.")
    lines.extend(followup)
    with fu_path.open("w", encoding="utf-8") as fu_file:
        fu_file.write("\n".join(lines))
    with fu_path.open("r", encoding="utf-8") as fu_file:
        print(fu_file.read())

if __name__ == "__main__":
    main()
