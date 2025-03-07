import random
import yaml
from pathlib import Path
from typing import Dict, Tuple, Optional
from jinja2 import Environment


class PromptBuilder:
    def __init__(
            self,
            char_name: str,
            user_name: str,
            language: str,
            gender: str,
            text_length: str = "short",
            mood: Optional[str] = None,
            time_sense: Optional[str] = None,
            memory: Optional[str] = None
            ):
        from globals import FOLDER

        self.char_name = char_name.lower()
        self.user_name = user_name.lower()
        self.language = language.lower()
        self.gender = gender.lower()

        # parameters for response length
        self.text_length = text_length

        # Optional parameters (dynamic prompts)
        self.mood = mood
        self.time_sense = time_sense
        self.memory = memory

        self.utility = FOLDER["utility"]
        self.char_spec = FOLDER[f"{self.char_name}_spec"]

        self.prompt_id_1 = "SYS-PROMPT-IMPERSONATION-001"
        self.prompt_id_2 = "SYS-PROMPT-RULES-001"
        self.prompt_id_3 = "SYS-PROMPT-CHARACTER-001"
        
        self.jinja_env = Environment(
            variable_start_string='{',
            variable_end_string='}'
        )

    def random_response_length(self) -> Tuple[int, int]:
        length_map = {
            "short": (30, 60, 70, 120),
            "medium": (60, 90, 100, 150),
            "long": (90, 120, 130, 180)
        }
        
        if self.text_length not in length_map:
            print(f"Invalid text length: {self.text_length}")
            return 50, 100  # Default fallback values
        
        values = length_map[self.text_length]
        min_random = random.randint(values[0], values[1])
        max_random = random.randint(values[2], values[3])
        
        return min_random, max_random

    
    def load_yaml(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
        
    def template_prompt(self) -> Dict[str, str]:
        yaml_paths = {file.stem: file for file in self.utility.glob("*.yaml")}
        
        template_dict = {}
        for path in yaml_paths.values():
            yaml_content = self.load_yaml(path)
            if isinstance(yaml_content, dict):
                for var_name, var_value in yaml_content.items():
                    template_dict[f"{var_name}_template"] = var_value

        output = {}
        for key, value in template_dict.items():
            if key != "prefill_system_rules_template":
                template = self.jinja_env.from_string(value)
                output[key.replace('_template', '')] = template.render(
                    char_name=self.char_name.title(),
                    user_name=self.user_name.title(),
                    language=self.language.title(),
                    gender=self.gender.title()
                )
            else:
                output[key] = value

        return output
    

    def build_system_prompt(self) -> Tuple[str, str]:
        templates = self.template_prompt()
        
        impersonation = f"""
[{self.prompt_id_1}]
{templates['impersonation']}
[/{self.prompt_id_1}]
"""

        system_rule = f"""
[{self.prompt_id_2}]
{templates['system_rule']}
[/{self.prompt_id_2}]
"""
        
        return impersonation, system_rule
        
    def build_character_prompt(self) -> str:
        file_map = {
            "Description": self.char_spec/'description.txt',
            "Personality": self.char_spec/'personality_summary.txt',
            "Background": self.char_spec/'scenario.txt',
            "Specific_rules": self.char_spec/'specific_rules.txt',
            "Examples_dialog": self.char_spec/'examples_dialogue.txt'
        }

        char_content = {}
        for key, path in file_map.items():
            with open(path, "r", encoding="utf-8") as f:
                char_content[key] = (
                    f.read()
                    .replace("{{char}}", self.char_name.title())
                    .replace("{{user}}", self.user_name.title())
                )
        
        return f"""
[{self.prompt_id_3}]
#The character is constructed as follows:

Description: 
<description>
{char_content['Description']}
</description>

Personality:
<personality>
{char_content['Personality']}
</personality>

Background:
<background>
{char_content['Background']}
</background>

Specific rules:
<specific_rules>
{char_content['Specific_rules']}
</specific_rules>

Examples of dialogue:
<examples_dialog>
{char_content['Examples_dialog']}
</examples_dialog>

[/{self.prompt_id_3}]
"""
    
    def build_prompt(self) -> Tuple[str, str, str]:
        impersonation, system_rule = self.build_system_prompt()
        return impersonation, system_rule, self.build_character_prompt()
    
    def build_reminder_prompt(self) -> str:
        templates = self.template_prompt()
        min_random, max_random = self.random_response_length()

        prefill_system_rules = self.jinja_env.from_string(templates['prefill_system_rules_template']).render(
            char_name=self.char_name.title(),
            user_name=self.user_name.title(),
            prompt_id_1=self.prompt_id_1,
            prompt_id_2=self.prompt_id_2,
            prompt_id_3=self.prompt_id_3,
            memory=self.memory,
            mood=self.mood,
            time_sense=self.time_sense,
            min_random=min_random,
            max_random=max_random
        )

        return f"""
[START SYSTEM]
{templates['prefill_impersonation']}
[END SYSTEM]

{prefill_system_rules}

My response as {self.char_name.title()}:
"""
    
    
    def build_api_prompt(self, prompt:str, role:str = None) -> dict:
        '''No value for role gives System API prompt back'''

        if role == "user":
            return {"role": "user", "content": prompt.strip()}
        elif role == "assistant":
            return {"role": "assistant", "content": prompt.strip()}
        else:
            return {"type": "text", "text": prompt.strip()}
        
    
    def get_system_api(self) -> Tuple[dict, dict]:
        impersonation, system_rule, character_prompt = self.build_prompt()

        system_api = [
            self.build_api_prompt(impersonation),
            self.build_api_prompt(system_rule),
            self.build_api_prompt(character_prompt)
        ]

        return system_api
    

    def get_reminder_api(self) -> Tuple[dict]:
        reminder_prompt = self.build_reminder_prompt()

        reminder_api = [
            self.build_api_prompt(reminder_prompt, role="assistant")
        ]

        return reminder_api



# Example usage (Dynamic prompts are easily handled with this class)
"""
char = PromptBuilder(
    char_name="mia",
    user_name="james",
    language="english",
    gender="female"
)

system_api = char.get_system_api()

# Dynamic prompts#

char.mood = "happy"
char.time_sense = "past"
char.memory = "I remember you"
char.text_length = "medium"

reminder_api = char.get_reminder_api()
"""