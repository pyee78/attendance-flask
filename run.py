from attendance import app

# saves time when running in debug mode
# - don't have to set variables or restart server after changes
if __name__ == '__main__':
    app.run(debug=True)
