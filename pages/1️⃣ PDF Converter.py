import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pdf_app")))
import app as pdf_app

pdf_app.run()
