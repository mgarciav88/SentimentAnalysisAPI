def select_dominant_language(dominant_language_response: dict) -> dict:
    language_choices = dominant_language_response.get('Languages')
    return max(language_choices, key=lambda lang: lang.get('Score'))


def select_batch_dominant_language(batch_dominant_language_response: dict) -> str:
    languages_set = set(select_dominant_language(result).get('LanguageCode')
                        for result in batch_dominant_language_response.get('ResultList'))

    return languages_set.pop() if len(languages_set) == 1 else None
