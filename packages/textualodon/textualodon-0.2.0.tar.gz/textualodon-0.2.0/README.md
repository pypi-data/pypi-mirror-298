# Textualodon
Mastodon in your CLI! Created with an excellent [Textual](https://github.com/textualize/textual) framework.

## WARNING
This project is in a very early stage of development. It will be heavily refactored in the future.

## Features
- [x] Login using own development tokens
- [x] Show home, local and global timeline
- [x] Visual difference between post, boost and replies
- [x] Favourite a post
- [x] Boost a post
- [x] Bookmark a post
- [x] Write new post
- [x] Add CW to post
- [x] Set post language
- [x] Choose post visibility
- [x] Add poll to post
- [x] Open post details to see post comments and ancestors
- [x] Vote in polls

## To do
Too much to write right now. I want to implement as much of the Mastodon API as possible and feasible for a console app.

## Installation
### From pypi
1.
```python
pip install textualodon
```
2. Run the app
```bash
textualodon
```
### From source
1. Clone this repo
```bash
git clone https://codeberg.org/djvdq/Textualodon
```
2. I recommend using a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the application
```bash
textual run textualodon.py
```
### API keys and first setup
At first run, you will need to provide your own development tokens. To do this, follow these steps:
1. Navigate to your Mastodon account and go to "Preferences" → "Development".
2. On that page click "New application" in the upper right corner.
3. In "Application name" you can write whatever you like, this field can't be empty.
4. Scroll the page down and click "Submit". Next, you will use your own tokens to login.

Now, go back to your running Textualodon app.
1. Enter your instance url (e.g. mastodon.social)
2. Copy the "Client key" from Mastodon to the "Client ID" field in Textualodon app.
3. Copy the "Client secret" from Mastodon to the "Client secret" field in Textualodon app.
4. Click "Login", a new tab will open in your browser.
5. Copy your authorization token and paste it into the "Grant token" field in Textualodon app.
6. Click "Login" again.
7. Reopen the app to see your home timeline.
