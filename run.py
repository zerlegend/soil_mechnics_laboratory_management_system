from smlms import app

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("An error occurred:", e)