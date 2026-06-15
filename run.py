from app import create_app

app = create_app()

if __name__ == '__main__':
    # This prints out every single active URL path Flask knows about on startup!
    print("\n=== FLASK ACTIVE ROUTING MAP ===")
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.rule} --> Endpoint: {rule.endpoint} (Methods: {list(rule.methods)})")
    print("=================================\n")

    app.run(host='127.0.0.1', port=8080, debug=True)