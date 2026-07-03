import pandas as pd
from rapidfuzz import fuzz


def get_recommendation(name_score, address_score, phone_match):
    if name_score >= 95 and phone_match:
        return "Safe to Merge", "High"

    elif name_score >= 85 and (phone_match or address_score >= 85):
        return "Review Manually", "Medium"

    else:
        return "Not a Duplicate", "Low"


def detect_duplicates(csv_path):

    df = pd.read_csv(csv_path)
    df.fillna("", inplace=True)

    duplicates = []

    threshold = 85

    total_records = len(df)

    for i in range(total_records):

        for j in range(i + 1, total_records):

            name1 = str(df.loc[i, "BusinessName"]).strip()
            name2 = str(df.loc[j, "BusinessName"]).strip()

            phone1 = str(df.loc[i, "Phone"]).strip()
            phone2 = str(df.loc[j, "Phone"]).strip()

            address1 = str(df.loc[i, "Address"]).strip()
            address2 = str(df.loc[j, "Address"]).strip()

            name_score = fuzz.ratio(name1.lower(), name2.lower())

            address_score = fuzz.ratio(
                address1.lower(),
                address2.lower()
            )

            phone_match = phone1 == phone2

            if (
                name_score >= threshold
                or
                (phone_match and address_score >= 80)
            ):

                recommendation, confidence = get_recommendation(
                    name_score,
                    address_score,
                    phone_match
                )

                duplicates.append({

                    "business1": name1,

                    "business2": name2,

                    "name_score": round(name_score, 2),

                    "address_score": round(address_score, 2),

                    "phone_match": "Yes" if phone_match else "No",

                    "recommendation": recommendation,

                    "confidence": confidence

                })

    if duplicates:
        pd.DataFrame(duplicates).to_csv(
            "duplicate_report.csv",
            index=False
        )

    stats = {

        "total": total_records,

        "duplicates": len(duplicates),

        "unique": total_records - len(duplicates),

        "threshold": threshold

    }

    return duplicates, stats