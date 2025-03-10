import pandas as pd
import logging
import chardet
from schools.models import School
from datetime import datetime
import tempfile
import os

logger = logging.getLogger(__name__)

def import_schools_from_csv(csv_file) -> str:
    """
    Efficiently imports school data from a CSV file.
    - Supports file uploads (Django `request.FILES`) and direct file paths.
    - Uses Pandas for fast data processing.
    - Bulk inserts records efficiently using Django's `bulk_create`.
    """

    if hasattr(csv_file, 'read'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8") as temp_file:
            for chunk in csv_file.chunks():
                temp_file.write(chunk.decode('utf-8', errors='replace')) 
            csv_file = temp_file.name

    try:
        df = pd.read_csv(csv_file, dtype=str).dropna(subset=['URN'])
        df = df.where(pd.notna(df), None)

        date_columns = ['OpenDate', 'CloseDate']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce') 
            df[col] = df[col].astype('object').where(pd.notna(df[col]), None)

        school_objects = [
            School(
                urn=row.URN,
                name=row.EstablishmentName,
                status=row.EstablishmentStatus,
                open_date=row.OpenDate,  
                close_date=row.CloseDate,
                city=row.Town,
                postcode=row.Postcode,
                website=row.SchoolWebsite,
                phone_number=row.TelephoneNum,
            )
            for row in df.itertuples(index=False)
        ]
        School.objects.bulk_create(school_objects, ignore_conflicts=True)

        logger.info(f"✅ Imported {len(to_create)} new schools.")
        return f"Successfully imported {len(school_objects)} schools."

    except Exception as e:
        return f"Error importing CSV: {e}"

    finally:
        if hasattr(csv_file, 'read'):
            try:
                os.remove(csv_file)
            except Exception as e:
                logger.warning(f"Could not delete temp file {csv_file} - {e}")