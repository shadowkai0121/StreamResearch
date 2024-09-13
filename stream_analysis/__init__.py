from dotenv import load_dotenv
load_dotenv()

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
font_path = os.path.join(os.getenv("DEFAULT_FONT_PATH"), os.getenv("DEFAULT_FONT_NAME"), os.getenv("DEFAULT_FONT_FILENAME"))
fm.fontManager.addfont(font_path)
font = fm.FontProperties(
    fname=font_path
)
matplotlib.rc('font', family=font.get_name())
