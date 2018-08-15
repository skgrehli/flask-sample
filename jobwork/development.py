# Run a test server.
from jobwork.app import app
app.run(host='0.0.0.0', port=8080, debug=True)