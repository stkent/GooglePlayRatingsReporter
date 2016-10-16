# GooglePlayRatingsReporter
A short python script that scrapes Google Play Store pages for app rating counts and reports changes to HipChat/Slack.

# Setup
Create a new file called "tokens.py" in the root directory of the repository. Add lines of the form

```python
HIPCHAT_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SLACK_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

where "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" is a valid token for the corresponding API. (You can safely omit either of these lines if you intend to use a single messaging service.)

Create a new file called "configuration.json" in the root directory of the repository. Add a json object of the form

```json
{
    "services": [
        "hipchat",
        "slack"
    ],
    "apps": [
        {
            "name": "App 1 Name ",
            "scrape_url": "https://play.google.com/store/apps/details?id=com.example.app1&hl=en",
            "channels": {
                "hipchat": "hipchat-channel-name-for-app-1"
            }
        },
        {
            "name": "App 2 Name",
            "scrape_url": "https://play.google.com/store/apps/details?id=com.example.app2&hl=en",
            "channels": {
                "hipchat": "hipchat-channel-name-for-app-2",
                "slack": "slack-channel-name-for-app-2"
            }
        }
    ]
}
```

Note that configuration Slack channel names must not include a leading #.

# License

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
