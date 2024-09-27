from flask import Flask, render_template, request, jsonify, session, send_file
from search_engine import SearchEngine

# WSGI
app = Flask(__name__)

# Session setup
app.secret_key = "thiskeyshouldntbeherebutfornowitisoktonotuseenviromentalvariables"

# After user's search create files for download
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        users_query = request.form.get("query")
        session["users_query"] = users_query  # Store query in session
        
        search = SearchEngine()
        try:
            # Process parsed results
            results = search.google_search(users_query)
            if results:
                filename_json = f"{users_query}.json"
                filename_csv = f"{users_query}.csv"
                search.save_to_json(results, filename_json)  # Save only parsed results
                search.save_to_csv(results, filename_csv)
            else:
                print("No results found.")
        except Exception as e:
            print(f"Sorry, we had some issue: {e}")

    return render_template("index.html")


@app.route('/download_json', methods=['POST'])
def download_json():
    users_query = session.get("users_query", None)
    if users_query:
        path = f"/path/{users_query}.json"
        try:
            return send_file(path, as_attachment=True, download_name="data_in_json.json", mimetype="application/json")
        except FileNotFoundError:
            return "File not found. Please perform a search first.", 404
    else:
        return "No query found in session.", 400
    
    
@app.route('/download_csv', methods=['POST'])
def download_csv():
    users_query = session.get("users_query", None)
    if users_query:
        path = f"/path/{users_query}.csv"
        print(path)
        try:
            return send_file(path, as_attachment=True, download_name="data_in_csv.csv", mimetype="text/csv")
        except FileNotFoundError:
            return "File not found. Please perform a search first.", 404
    else:
        return "No query found in session.", 400

if __name__ == '__main__':
    app.run(debug=True)