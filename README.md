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
