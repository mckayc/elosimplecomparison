from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    
    # Example route
    @app.route('/')
    def index():
        return render_template('index.html')  # Example template rendering
    
    return app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
