import flet as ft
import requests
from datetime import datetime
from collections import defaultdict

API_KEY = "3bf8a245154c533680c3a4b0b1e0b1d3"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def main(page: ft.Page):
    page.title = "Weather App"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0e27"
    page.window_width = 1400
    page.window_height = 900

    temp_unit = "C"
    search_history = []
    
    # --- DEFAULT CITY TO LOAD ON STARTUP ---
    DEFAULT_CITY = "Manila"

    def c_to_f(c): return (c * 9/5) + 32
    def convert_temp(v): return c_to_f(v) if temp_unit == "F" else v
    def unit_label(): return "°F" if temp_unit == "F" else "°C"

    def fetch_weather(city: str):
        try:
            r = requests.get(
                BASE_URL,
                params={"q": city, "appid": API_KEY, "units": "metric"},
                timeout=10,
            )
            r.raise_for_status()
            return r.json(), None
        except Exception as e:
            return None, str(e)

    def fetch_forecast(city: str):
        try:
            r = requests.get(
                FORECAST_URL,
                params={"q": city, "appid": API_KEY, "units": "metric"},
                timeout=10,
            )
            r.raise_for_status()
            return r.json(), None
        except Exception as e:
            return None, str(e)

    # THEME TOGGLE
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#f0f4f8"
            theme_btn.icon = "dark_mode"
            # ***FIXED: Color Hex Value***
            forecast_title.color = "#000000" # BLACK
            # FIX: Also fix the history_column title color
            history_column.controls[0].color = "#000000" # BLACK 
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#0a0e27"
            theme_btn.icon = "light_mode"
            # ***FIXED: Color Hex Value***
            forecast_title.color = "#ffffff" # WHITE
            # FIX: Also fix the history_column title color
            history_column.controls[0].color = "#ffffff" # WHITE 
        page.update()

    theme_btn = ft.IconButton(
        icon="light_mode",
        icon_color="#64b5f6",
        icon_size=28,
        on_click=toggle_theme,
    )

    # UNIT SWITCH
    def toggle_unit(e):
        nonlocal temp_unit
        temp_unit = "F" if e.control.value else "C"
        # FIX: Check if city_input has a value before attempting to re-search
        if city_input.value:
            search_weather(None)
        page.update()

    unit_switch = ft.Switch(
        value=False, label="°C / °F", on_change=toggle_unit
    )

    # UI ELEMENTS
    city_input = ft.TextField(
        hint_text="e.g., London, Tokyo, New York",
        border_color="#1e88e5",
        focused_border_color="#42a5f5",
        text_size=16,
        height=60,
        prefix_icon="location_city",
        expand=True,
        on_submit=lambda e: search_weather(e),
        # SET DEFAULT CITY VALUE IN INPUT FIELD
        value=DEFAULT_CITY,
    )

    result_container = ft.Container(expand=True)
    forecast_row = ft.Row(
        scroll="auto",
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    forecast_title = ft.Text(
        "5-Day Forecast",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#ffffff",
    )

    history_column = ft.Column(spacing=10)
    details_grid = ft.Column(spacing=15)

    def create_detail_card(label, value):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=14, color="#90caf9"),
                    ft.Text(
                        value,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#ffffff",
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=20,
            bgcolor="#283593",
            border_radius=15,
            width=180,
        )

    def render_current_weather(data):
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        icon = data["weather"][0]["icon"]
        city_name = data["name"]
        country = data["sys"]["country"]

        # FIX: Replace details_grid usage with the content from render_current_weather
        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        f"{city_name}, {country}",
                        size=48,
                        weight=ft.FontWeight.BOLD,
                        color="#ffffff",
                    ),
                    ft.Text(
                        datetime.now().strftime(
                            "%A, %B %d, %Y | %I:%M %p"
                        ),
                        size=16,
                        color="#90caf9",
                    ),

                    ft.Row(
                        [
                            ft.Image(
                                src=f"https://openweathermap.org/img/wn/{icon}@4x.png",
                                width=180,
                                height=180,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"{convert_temp(temp):.0f}{unit_label()}",
                                        size=80,
                                        weight=ft.FontWeight.BOLD,
                                        color="#ffffff",
                                    ),
                                    # FIXED description visibility
                                    ft.Text(
                                        description,
                                        size=26,
                                        color="#90caf9",
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                        f"Feels like {convert_temp(feels_like):.0f}{unit_label()}",
                                        size=16,
                                        color="#64b5f6",
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Container(height=30),

                    ft.Row(
                        [
                            create_detail_card("💧 Humidity", f"{humidity}%"),
                            create_detail_card("🌡️ Pressure", f"{pressure} hPa"),
                            create_detail_card("💨 Wind Speed", f"{wind_speed} m/s"),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            ),
            padding=40,
            bgcolor="#1a237e22",
            border_radius=20,
        )

    def render_forecast_cards(forecast_data):
        forecast_row.controls.clear()
        daily = defaultdict(list)

        for entry in forecast_data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            icon = entry["weather"][0]["icon"]
            desc = entry["weather"][0]["description"]
            daily[date].append((temp, icon, desc))

        for date, entries in list(daily.items())[:5]:
            # The original logic for max/min is correct for a single day
            max_temp = max(t for t, _, _ in entries)
            min_temp = min(t for t, _, _ in entries)
            avg_temp = sum(t for t, _, _ in entries) / len(entries)
            
            # Use the icon/description from the midday (around 12/15:00) entry for better accuracy
            midday_entry = entries[len(entries) // 2]
            icon = midday_entry[1]
            desc = midday_entry[2]

            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_name = date_obj.strftime("%a")
            date_str = date_obj.strftime("%b %d")

            forecast_row.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(day_name, size=18, weight=ft.FontWeight.BOLD, color="#ffffff"),
                            ft.Text(date_str, size=12, color="#90caf9"),
                            ft.Image(
                                src=f"https://openweathermap.org/img/wn/{icon}@2x.png",
                                width=70,
                                height=70,
                            ),
                            ft.Text(
                                f"{convert_temp(avg_temp):.0f}{unit_label()}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#ffffff",
                            ),
                            ft.Text(
                                f"↑{convert_temp(max_temp):.0f}{unit_label()} ↓{convert_temp(min_temp):.0f}{unit_label()}",
                                size=12,
                                color="#64b5f6",
                            ),
                            ft.Text(desc.title(), size=12, color="#90caf9", text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=20,
                    bgcolor="#283593",
                    border_radius=15,
                    width=160,
                )
            )

    def update_history(city):
        if city not in search_history:
            search_history.append(city)
        if len(search_history) > 5:
            search_history.pop(0)

        history_column.controls.clear()
        
        # ***FIXED: Color Hex Value (for initial load and state)***
        history_column.controls.append(
            ft.Text("Recent Searches", size=18, weight=ft.FontWeight.BOLD, 
                    color="#ffffff" if page.theme_mode == ft.ThemeMode.DARK else "#000000") 
        )

        for c in reversed(search_history):
            history_column.controls.append(
                ft.Container(
                    content=ft.Text(c, size=14, color="#90caf9"),
                    padding=10,
                    bgcolor="#283593",
                    border_radius=8,
                    on_click=lambda e, city=c: quick_search(city),
                )
            )

    def quick_search(city):
        city_input.value = city
        search_weather(None)

    def search_weather(e):
        city = city_input.value.strip()
        if not city:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter a city name", color="#ffffff"),
                bgcolor="#d32f2f",
            )
            page.snack_bar.open = True
            page.update()
            return

        # Show loading indicator
        result_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.ProgressRing(color="#42a5f5"),
                    ft.Text("Loading weather data...", size=16, color="#90caf9"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=50,
            alignment=ft.alignment.center,
        )
        page.update()

        weather_data, error = fetch_weather(city)
        forecast_data, forecast_error = fetch_forecast(city)

        if error or (weather_data and weather_data.get('cod') == 404):
            # FIX: Handle OpenWeatherMap's 404 response explicitly
            result_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon("error_outline", size=64, color="#ef5350"),
                        ft.Text(
                            "City not found",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            # ***FIXED: Color Hex Value***
                            color="#ffffff" if page.theme_mode == ft.ThemeMode.DARK else "#000000",
                        ),
                        ft.Text(f"Could not find weather data for '{city}'.", size=14, color="#90caf9", text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=50,
                alignment=ft.alignment.center,
            )
            # Clear forecast row on error
            forecast_row.controls.clear()
            page.update()
            return

        result_container.content = render_current_weather(weather_data)
        if not forecast_error:
            render_forecast_cards(forecast_data)
        
        # FIX: The city name from API might be capitalized differently, so use it for history
        update_history(weather_data["name"])
        page.update()

    header_row = ft.Row(
        [
            ft.Text(
                "Weather App",
                size=36,
                weight=ft.FontWeight.BOLD,
                color="#42a5f5",
            ),
            ft.Container(expand=True),
            unit_switch,
            theme_btn,
        ]
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=header_row,
                        padding=ft.padding.only(left=40, right=40, top=30, bottom=20),
                    ),

                    ft.Container(
                        content=ft.Row(
                            [
                                city_input,
                                ft.ElevatedButton(
                                    "Get Weather",
                                    icon="search",
                                    on_click=search_weather,
                                    bgcolor="#1e88e5",
                                    color="#ffffff",
                                    height=50,
                                    width=150,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=ft.padding.symmetric(horizontal=40),
                    ),

                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(content=result_container, expand=True),
                                ft.Container(
                                    content=history_column,
                                    width=200,
                                    padding=20,
                                    bgcolor="#1a237e22",
                                    border_radius=15,
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=ft.padding.symmetric(horizontal=40, vertical=20),
                        expand=True,
                    ),

                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            [
                                forecast_title,
                                ft.Container(
                                    content=forecast_row,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            spacing=15,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(left=40, right=40, bottom=30),
                    ),
                ],
                spacing=0,
            ),
            expand=True,
        )
    )
    
   
    search_weather(None)


ft.app(target=main)