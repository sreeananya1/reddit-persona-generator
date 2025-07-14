# Reddit User Persona Generator

This script analyzes Reddit user profiles and generates a detailed persona using LLMs.

## How to Use

 Step 1: Install requirements
```bash
pip install praw openai python-dotenv
```

Step 2: Create `.env` file
```
OPENAI_API_KEY=your_openai_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
```

 Step 3: Run the script
```bash
python reddit_persona_generator.py --url https://www.reddit.com/user/kojied/
```

## Output
Generates a `.txt` file with the user's inferred persona.

## Files
- reddit_persona_generator.py
- README.md
- kojied_persona.txt
- Hungry-Move-6603_persona.txt
