
# -----------------------------------------------
# LOGGER settings
# -----------------------------------------------
# LOGLEVEL: logging has to be defined
LOG_LEVEL = 10  # DEBUG: 10
# LOG_LEVEL = 20  # INFO: 20
# LOG_LEVEL = 30  # WARNING: 30
# LOG_LEVEL = 40  # ERROR: 40
# LOG_LEVEL = 50  # CRITICAL: 50
# LOG_LEVEL = 100 # DISABLED: 100

# Optional: write log data to file
# LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs/')

# Optional: show log code line
LOG_SHOWLINES = False

# -----------------------------------------------
## all devices
# -----------------------------------------------
DEVICES =[
    {
        "device": "GB172BKG",
        "source": "devices/templates/ha/GB172BKG"
    },
    {
        "device": "GB172BKGA",
        "source": "devices/templates/ha/GB172BKG"
    },
]
