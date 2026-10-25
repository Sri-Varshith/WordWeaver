def validate_words(start_word, target_word, dictionary):
    """
    Validates start and target words.
    Returns a tuple (is_valid: bool, error_message: str).
    """
    if len(start_word) != 4 or len(target_word) != 4:
        return False, "Both words must be exactly 4 letters long."
    
    if not start_word.isalpha() or not target_word.isalpha():
        return False, "Words must contain alphabetic characters only."
    
    start_lower = start_word.lower()
    target_lower = target_word.lower()
    
    if start_lower not in dictionary:
        return False, f"Start word '{start_word}' is not in the dictionary."
    
    if target_lower not in dictionary:
        return False, f"Target word '{target_word}' is not in the dictionary."
    
    return True, ""
