from data_handler import (
    load_user_char_name,
    load_prompts,
    load_set
)

char_choice = load_set(char=True)

user_name, char_name = load_user_char_name(user=True, char=char_choice.lower())

yaml_data = load_prompts(char=char_choice.lower())
yaml_data.update(load_prompts(utility=True))

# 3) Platzhalter ersetzen
for key, text in yaml_data.items():
    yaml_data[key] = text.replace("{{user}}", user_name).replace("{{char}}", char_name)



# 4) Prompts vorbereiten
placeholder = {
    "system_rule": yaml_data["system_rule"],
    #eleminiere trailing whitespace
}

#================= First Message =================

ordered_assistant_prompts_0 = {
    "first_message": yaml_data["first_message"]
}

#================= Charakter =================

ordered_system_prompts_0 = {
    "description": yaml_data["description"],
    "personality_summary": yaml_data["personality_summary"],
    "specific_rules": yaml_data["specific_rules"],
    "scenario": yaml_data["scenario"],
    "examples_dialogue": yaml_data["examples_dialogue"]
}

#================= Pre-fill =================

ordered_assistant_prompts_1 = {
    "assistant_prefill": yaml_data["assistant_prefill"],
    "assistant_impersonation_prefill": yaml_data["assistant_impersonation_prefill"],
}

#================= Jailbreak =================

ordered_system_prompts_1 = {
    "impersonation": yaml_data["impersonation"],
    "system_rule": yaml_data["system_rule"],
    
}
# ----------------------------------------
# 5) verschiedene Prompt-Typen vorbereiten
# ----------------------------------------
system_char_prompt = [{"type": "text", "text": txt} for txt in ordered_system_prompts_0.values()]
system_utility_prompt = [{"type": "text", "text": txt} for txt in ordered_system_prompts_1.values()]

first_message = [{"role": "assistant", "content": txt, "history": True} for txt in ordered_assistant_prompts_0.values()]
assistant_prefill = [{"role": "assistant", "content": txt} for txt in ordered_assistant_prompts_1.values()]


raw_system_prompts = [system_utility_prompt, system_char_prompt]
raw_assistant_prompts = [assistant_prefill]

first_message = [entry for entry in first_message]
system_prompt = [entry for raw in raw_system_prompts for entry in raw]
assistant_prompt = [entry for raw in raw_assistant_prompts for entry in raw]
# -----------------------
# 6) Testausgaben
# -----------------------

# entferne '#' vor print, um die Ausgabe zu sehen


#print(system_prompt)
#print(assistant_prompt)