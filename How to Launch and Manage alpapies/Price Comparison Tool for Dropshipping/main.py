import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.product import (
    Product, Category, Vendor, ProductVendor, 
    PriceHistory, PriceAlert, ClickTracking, AffiliateProgram
)
from src.routes.user import user_bp
from src.routes.products import products_bp
from src.routes.affiliate import affiliate_bp
from src.routes.currency import currency_bp
from src.routes.marketplace import marketplace_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(affiliate_bp, url_prefix='/api/affiliate')
app.register_blueprint(currency_bp, url_prefix='/api')
app.register_blueprint(marketplace_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Initialize sample data if database is empty
    if Category.query.count() == 0:
        from src.services.data_collector import initialize_sample_data
        try:
            initialize_sample_data()
            print("Sample data initialized successfully")
        except Exception as e:
            print(f"Error initializing sample data: {str(e)}")
    
    # Initialize affiliate manager
    try:
        from src.services.affiliate_manager import initialize_affiliate_manager
        initialize_affiliate_manager()
        print("Affiliate manager initialized successfully")
    except Exception as e:
        print(f"Error initializing affiliate manager: {str(e)}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
