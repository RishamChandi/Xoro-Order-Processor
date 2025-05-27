from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_order():
    """Handle file upload and return Xoro template"""
    if request.method == "POST":
        # TODO: Handle file upload and processing
        pass
    return render_template_string("""
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="orderfile">
        <input type="submit">
    </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
