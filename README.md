# ELSA Deck Creator

An automated tool for creating study decks in ELSA using AI-powered text splitting with Claude and Gemini models.

## Features

- AI-powered text splitting using multiple models:
  - Claude 3 Sonnet (Anthropic)
  - Gemini Pro (Google)
- Automated deck creation in ELSA
- User-friendly GUI interface
- Progress tracking
- Automatic link copying
- Multi-threaded operation

## Prerequisites

### Required Software
- Python 3.8+
- Bluestacks with ELSA app installed
- Chrome browser

### API Keys
Create a `.env` file with:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### Required Python Packages

```
pip install -r requirements.txt
```

## Installation

1. Clone the repository
2. Install requirements:
3. Add your API keys to `.env`
4. Prepare the required screenshots in `images/` folder

## Required Screenshots

Place these screenshots in the `images/` folder:
- bluestacks_icon.png
- elsa_icon.png
- discover_icon.png
- discover_icon2.png
- studysets_icon.png
- addbutton_icon.png
- studysetblank.png
- categoryblank.png
- ok_icon.png
- addphrases_icon.png
- search_icon.png
- check_icon.png
- add_icon.png
- finish_icon.png
- share_icon.png
- chrome_icon.png
- forward_icon.png
- copylink_icon.png

## Usage

1. Run the application:
2. Enter study set name
3. Input your text
4. Click "Preview Splits"
5. Choose your preferred AI split option
6. Click "Create Deck"
7. Wait for automation to complete
8. Copy the shared link from results

## Important Notes

- Don't move your mouse during automation
- Keep Bluestacks window visible
- Screen resolution should match reference images
- Make sure ELSA app is properly installed in Bluestacks

## Troubleshooting

### Automation Issues
- Verify all images in the `images` folder match your screen
- Ensure Bluestacks is running and visible
- Check if ELSA is properly installed

### AI Split Issues
- Verify API keys in `.env` file
- Check internet connection
- Ensure text input is not empty

### General Issues
- Check console output for error messages
- Verify all required packages are installed
- Make sure Python version is compatible

