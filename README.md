# SkyAlert

SkyAlert is an application that provides real-time weather updates and alerts specifically tailored for stargazing and astrophotography enthusiasts. It combines information from multiple data sources to determine the optimal conditions for a potentially good stargazing or astrophotography night in your locale.

## Features

- Real-time weather updates: SkyAlert fetches weather data from reliable sources and provides up-to-date information about temperature, humidity, wind speed, and cloud cover.

- Stargazing opportunity alerts: The application analyzes weather conditions and provides alerts when the conditions are favorable for stargazing or astrophotography, taking into account factors such as clear skies, low light pollution, and optimal moon phase.

- Customizable notifications: Users can choose their preferred notification methods, such as email, SMS, or push notifications, to receive alerts about potential stargazing opportunities.

- Location-based weather: SkyAlert uses geolocation to provide weather information specific to the user's location. Users can also search for weather conditions in different cities or regions.

## Installation

1. Clone the SkyAlert repository:

    ```shell
    git clone https://github.com/your-username/sky-alert.git
    ```

2. Run the application:

    ```shell
    uvicorn main:app --reload
    ```

## Usage

- Upon running the application, SkyAlert will fetch weather data and analyze it to determine if there is a potential stargazing or astrophotography opportunity in your locale.
- If favorable conditions are detected, the application will send alerts to the configured notification methods.
- Use the command-line interface to search for weather conditions in different locations or change notification settings.

## Contributing

Contributions to SkyAlert are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

SkyAlert is licensed under the [MIT License](LICENSE).
