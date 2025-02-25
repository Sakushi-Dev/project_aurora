from data_handler import (
    load_user_char_name,
    load_prompts,
    load_set,
    read_json,
    user_gender_path,
    user_language_path
)

def read_settings():
    settings = read_json(user_language_path)
    language = settings["language"]
    gender = read_json(user_gender_path)["user_gender"]
    return language, gender

def prepare_data(language, gender, user_name, char_name):
    # Load data from various prompts
    data = load_prompts(char=char_name)
    data.update(load_prompts(utility=True))
    
    # Replace placeholders in all text fields
    for key, text in data.items():
        replaced_text = text.replace("{{user}}", user_name).replace("{{char}}", char_name)
        if key == "system_rule":
            replaced_text = replaced_text.replace("{{language}}", language).replace("{{gender}}", gender)
        data[key] = replaced_text

    # Language of first message
    first_message = data.pop("first_message")
    split_fm = first_message.split("//")
    if language == "english":
        data.update({"first_message": split_fm[0]})
    else:
        data.update({"first_message": split_fm[1]})

    return data

def build_prompts(data):
    # Define different sections of prompts
    assistant_prompts_first = {"first_message": data["first_message"]}
    system_prompts_char = {
        "description": data["description"],
        "personality_summary": data["personality_summary"],
        "specific_rules": data["specific_rules"],
        "scenario": data["scenario"],
        "examples_dialogue": data["examples_dialogue"]
    }
    assistant_prompts_prefill = {
        "assistant_prefill": data["assistant_prefill"],
        "assistant_impersonation_prefill": data["assistant_impersonation_prefill"]
    }
    system_prompts_utility = {
        "impersonation": data["impersonation"],
        "system_rule": data["system_rule"],
    }
    
    # Prepare API request prompts
    system_char_prompt = [{"type": "text", "text": txt} for txt in system_prompts_char.values()]
    system_utility_prompt = [{"type": "text", "text": txt} for txt in system_prompts_utility.values()]
    assistant_first_message = [{"role": "assistant", "content": txt, "history": True} for txt in assistant_prompts_first.values()]
    assistant_prefill = [{"role": "assistant", "content": txt} for txt in assistant_prompts_prefill.values()]

    system_prompt = system_utility_prompt + system_char_prompt
    assistant_prompt = assistant_prefill  # first_message is handled separately

    return assistant_first_message, system_prompt, assistant_prompt

def get_prompts():
    language, gender = read_settings()
    # Load char setting and convert to lower case once
    char_name = load_set(char=True)
    # Load user and character names
    user_name = load_user_char_name(user=True)
    
    data = prepare_data(language, gender, user_name, char_name)
    first_message, system_prompt, assistant_prompt = build_prompts(data)
    return first_message, system_prompt, assistant_prompt, user_name, char_name


(
    first_message,
    system_prompt,
    assistant_prompt,
    user_name,
    char_name
) = get_prompts()
