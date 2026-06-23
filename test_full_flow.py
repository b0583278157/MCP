import asyncio
import sys
sys.path.insert(0, '.')
from weather_Israel import open_weather_forecast_israel, enter_weather_forecast_city_israel, select_weather_forecast_city_israel, STATE

async def test_full_flow():
    print("=" * 60)
    print("Testing complete Jerusalem weather forecast flow")
    print("=" * 60)
    
    try:
        print("\n1. Opening browser...")
        result1 = await open_weather_forecast_israel()
        print(f"   Result: {result1}")
        print(f"   State: step={STATE['step']}, browser={'open' if STATE['browser'] else 'closed'}")
        
        print("\n2. Entering city (Jerusalem)...")
        result2 = await enter_weather_forecast_city_israel("Jerusalem")
        print(f"   Result: {result2}")
        print(f"   State: step={STATE['step']}, city_he={STATE.get('city_he', 'N/A')}")
        
        print("\n3. Selecting city and getting forecast...")
        result3 = await select_weather_forecast_city_israel()
        print(f"   Result (first 500 chars): {result3[:500]}...")
        
        if "ירושלים" in result3:
            print("\n✓ SUCCESS: Jerusalem forecast retrieved!")
        else:
            print("\n✗ WARNING: Jerusalem text not found in result")
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if STATE['browser']:
            await STATE['browser'].close()
            print("\nBrowser closed")

asyncio.run(test_full_flow())
