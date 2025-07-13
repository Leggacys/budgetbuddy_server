import asyncio
from app import create_app, setup_app

app = create_app()

async def main():
    await setup_app()
    
    # Print all registered endpoints for debugging
    print("\n" + "="*50)
    print("🚀 REGISTERED ENDPOINTS:")
    print("="*50)
    
    endpoint_count = 0
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"{methods:10} {rule.rule}")
        endpoint_count += 1
    
    print("="*50)
    print(f"📊 Total endpoints: {endpoint_count}")
    print(f"📡 Server starting on http://0.0.0.0:5000")
    print("="*50 + "\n")
    
    await app.run_task(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    asyncio.run(main())
    