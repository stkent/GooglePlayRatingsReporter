# GooglePlayReviewScraper
A short python script that scrapes Google Play Store pages for app review counts.

# Setup
Create a new file called "tokens.py" in the root directory of the repository. Add a line of the form

```python
HIPCHAT_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

where "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" is a valid token for v1 of the HipChat API.

Create a new file called "configuration.json" in the root directory of the repository. Add a json object of the form

```json
{
    "App 1 Name": {
        "room_name": "hipchat-room-name-for-app-1",
        "scrape_url": "https://play.google.com/store/apps/details?id=com.example.app1&hl=en"
    },
    "App 2 Name": {
        "room_name": "hipchat-room-name-for-app-2",
        "scrape_url": "https://play.google.com/store/apps/details?id=com.example.app2&hl=en"
    }
}
```

# License

```
Copyright 2016 Stuart Kent

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
