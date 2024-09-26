import mdr_python_api.api

from mdr_python_api.api import enable_mock, init, health_check, register_meta_data
import json

mdr_python_api.api.init("https://chief-woodcock.dev-ml-platform.dev.czi.team", 443)

# Define the metadata schema (as already created)
metadata_schema = {
    "Internal_id": "_case_ids",
    "Dataset_name": "object_id",
    "Assay": "loinc_method",
    "Age": {
        "age_at_index": "age_at_index",
        "age_at_imaging": "age_at_imaging"
    },
    "Ethnicity": {
        "race": "race",
        "ethnicity": "ethnicity"
    },
    "Sex": "sex",
    "Tissue": {
        "body_part_examined": "body_part_examined",
        "loinc_system": "loinc_system"
    },
    "Published_at": "study_year",
    "Universal_ids": {
        "submitter_id": "submitter_id",
        "study_uid": "study_uid"
    },
    "Project_description": "study_description"
}

# Define the metadata with the necessary label and other fields
label = "MIDR"
version = "1.0"
owner = "mcaton"
url = "https://data.midrc.org/explorer"

# Convert the metadata schema to a JSON string
metadata_schema_json = json.dumps(metadata_schema)

# Register the metadata with MDR API
try:
    object_id = register_meta_data(
        label=label,
        version=version,
        owner=owner,
        url=url,
        md=metadata_schema_json  
    )
    print(f"Metadata registered successfully with label '{label}' and version '{version}' and the result object id {object_id}.")
except Exception as e:
    print(f"Failed to register metadata: {str(e)}")
    
# search example
mdr_python_api.api.search_meta_data(".*IDR")
