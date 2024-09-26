# User Agent Generator

A simple library to generate fake user agents for various platforms and browsers. This library can be useful for web scraping, testing, and simulating user behavior in web applications.

## Features

- Generates random user agents for multiple platforms:
  - Chrome
  - Firefox
  - Safari
  - Microsoft Edge
  - Internet Explorer
  - Android
  - iOS
  - Linux
  - Mac
  - Windows
- Customizable version and build numbers
- Easy to use and integrate into your projects

## Installation

You can install the package using pip:

```bash
pip install useragent-generator
```

## Usage
Here’s how to use the UserAgentGenerator class in your project:

## Example
```py
from spoofagent import UserAgentGenerator

# Create an instance of the generator
generator = UserAgentGenerator()

# Generate user agents for different platforms
chrome_ua = generator.generate_user_agent('chrome')
firefox_ua = generator.generate_user_agent('firefox')
safari_ua = generator.generate_user_agent('safari')
edge_ua = generator.generate_user_agent('edge')
ie_ua = generator.generate_user_agent('ie')
android_ua = generator.generate_user_agent('android')
ios_ua = generator.generate_user_agent('ios')
linux_ua = generator.generate_user_agent('linux')
mac_ua = generator.generate_user_agent('mac')
windows_ua = generator.generate_user_agent('windows')

# Print the generated user agents
print("Chrome User Agent:", chrome_ua)
print("Firefox User Agent:", firefox_ua)
print("Safari User Agent:", safari_ua)
print("Edge User Agent:", edge_ua)
print("Internet Explorer User Agent:", ie_ua)
print("Android User Agent:", android_ua)
print("iOS User Agent:", ios_ua)
print("Linux User Agent:", linux_ua)
print("Mac User Agent:", mac_ua)
print("Windows User Agent:", windows_ua)
```

## Customizing User Agents
You can customize the version and build numbers when generating user agents:
```py
custom_ua = generator.generate_user_agent('chrome', version='89', build='1234')
print("Custom Chrome User Agent:", custom_ua)
```

## Platform Options
The following platforms are supported:

- chrome
- firefox
- safari
- edge
- ie
- android
- ios
- linux
- mac
- windows