import eenhoorntje_llm_lib.llm_cache
import eenhoorntje_llm_lib.utils
# from google.cloud import translate_v2 as translate
from google.cloud import translate
import os
import json

"""
def translate_with_google(sentence: str, source_lang: str, target_lang: str) -> str:
    cache_key = "GoogleTranslate" + "\n"
    cache_key += "Source: " + sentence + "\n"
    cache_key += "Source lang: " + source_lang + "\n"
    cache_key += "Target lang: " + target_lang
    output = eenhoorntje_llm_lib.llm_cache.cache.query(cache_key)
    if output:
        return output

    translate_client = translate.Client.from_service_account_json(eenhoorntje_llm_lib.utils.get_key("GOOGLE_KEY"))

    result = translate_client.translate(sentence, target_language=target_lang, source_language=source_lang, format_="text")
    res = result["translatedText"]
    res = res.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", "\"")
    eenhoorntje_llm_lib.llm_cache.cache.add(cache_key, res)
    return res
"""

# Imports the Google Cloud Translation library
from google.cloud import translate


def translate_with_google(
        sentence: str, source_lang: str, target_lang: str, is_llm=True, is_tags=False):
    cache_key = "GoogleTranslate" + "\n"
    if is_llm:
        cache_key = "GoogleTranslateLLM" + "\n"
    cache_key += "Source: " + sentence + "\n"
    cache_key += "Source lang: " + source_lang + "\n"
    cache_key += "Target lang: " + target_lang
    if is_tags:
        cache_key += "\nTags: True"
    output = eenhoorntje_llm_lib.llm_cache.cache.query(cache_key)
    if output:
        return output

    file_name = eenhoorntje_llm_lib.utils.get_key("GOOGLE_KEY")
    f = open(file_name, "r")
    json_content = f.read()
    content = json.loads(json_content)
    client = translate.TranslationServiceClient.from_service_account_json(eenhoorntje_llm_lib.utils.get_key("GOOGLE_KEY"))#translate.TranslationServiceClient()

    location = "us-central1"

    parent = f"projects/stage-tests/locations/{location}"
    project_id = content["project_id"]

    model_name = f"projects/{project_id}/locations/{location}/models/general/nmt"
    if is_llm:
        model_name = f"projects/{project_id}/locations/{location}/models/general/translation-llm"

    mime_type = "text/plain"
    if is_tags:
        mime_type = "text/html"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [sentence],
            "mime_type": mime_type,
            "source_language_code": source_lang,
            "target_language_code": target_lang,
            "model": model_name
        }
    )

    res = ""
    for translation in response.translations:
        res = translation.translated_text
    res = res.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", "\"")
    eenhoorntje_llm_lib.llm_cache.cache.add(cache_key, res)
    return res
