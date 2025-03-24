import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "categorization_app")))
import app as categorizer_app

categorizer_app.run()
