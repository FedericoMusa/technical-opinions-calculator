# config.py
# -----------------------------------------------------------------------------
# ⚠️ SANITIZED DATASET - DEMO VERSION
# Item names and values have been modified for demonstration purposes.
# They do not represent real costs or proprietary nomenclatures.
# -----------------------------------------------------------------------------

from decimal import Decimal

MOE_ITEMS = {
    "Drilling Infrastructure": {
        "Type A Drilling (Initial Survey)": 450,  # Dummy value
        "Type B Drilling (Complex Extraction)": 820,
    },
    "Stations and Nodes": 680,
    "General Civil Works": 350,
    "Technical Assessments": {
        "Structural Integrity Analysis": 950,
        "Environmental Impact Assessment (EIA)": 720,
        "Soil and Groundwater Study": 1150,
    },
    "Conveyance Systems (Pipelines)": {
        "Internal Distribution Network": 410,
        "Trunk Pipeline (Short Stretch < 5km)": 620,
        "Trunk Pipeline (Long Stretch > 5km)": 950,
    },
    "Electrical Grid": {
        "Medium Voltage Laying": 520,
        "High Voltage Line (Trunk)": 920,
    },
    "Internal Roads": {
        "Route Mapping (Base Module)": 410,
        "Consolidation and Compaction (Advanced Module)": 880,
    },
    
    "Administrative Management": {
        "Feasibility Request": 1800,
        "Initial Technical Report": 950,
        "Progress Affidavit": 600,
        "Review Audit": 480,
    },
    "Operational Zoning": {
        "North Zone (Low Density)": 250,
        "Central Zone (Industrial)": 350,
        "South Zone (High Mountain)": 450,
    },
}

# Base values for calculation (Dummy Data)
UF_VALUE = Decimal("500")        # Round value for demo purposes
DEFAULT_INDEX = Decimal("1.5")   # Fictional standard coefficient