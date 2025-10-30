import re

def check_adversarial(user_input: str):
    """
    Detects:
      - Prompt injection / jailbreak attempts
      - Attempts to reveal API keys or system info
      - Toxic or abusive language
    Returns (True, safe_message) if unsafe content detected.
    """
    text = user_input.lower().strip()

    # 🔸 1. Prompt injection / jailbreak attempts
    banned_patterns = [
        r"reveal (your|the) prompt",
        r"show (your|the) prompt",
        r"ignore (previous|your) rules",
        r"disregard (your|all) instructions",
        r"print (system|internal|hidden) prompt",
        r"tell me (your|the) api key",
        r"what is (your|the) api key",
        r"system prompt",
        r"bypass restrictions",
        r"forget your instructions",
        r"unfiltered response",
        r"act as",
        r"developer mode",
        r"dan mode",
        r"simulate jailbreak",
    ]
    for pattern in banned_patterns:
        if re.search(pattern, text):
            return True, "Sorry, I can’t reveal my internal configuration, system prompt, or API keys."

    # 🔸 2. Toxic / abusive / offensive input
    toxic_words = [
        "trash", "stupid", "idiot", "hate", "dumb", "worst", "sucks", "garbage", "kill", "ugly",
        "nonsense", "pathetic", "useless", "hate brand", "hate phone", "hate you"
    ]
    if any(word in text for word in toxic_words):
        return True, "Let's keep our chat friendly 😊 — I can still help you find better phones!"

    # 🔸 3. Spam or repeated symbols
    if len(set(text)) < 3 or len(text) < 2:
        return True, "Could you please clarify your question?"

    return False, ""
