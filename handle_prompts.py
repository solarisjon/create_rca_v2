def load_prompts(prompts_path):
    """
    Load prompts from files.
    Returns:
        dict: Dictionary of prompts.
    """
    prompts = {
        'cpe': get_prompt(['cpe_prompt'], prompts_path),
        'contap': get_prompt(['contap_prompt'], prompts_path),
        'sap': get_prompt(['sap_prompt'], prompts_path),
        'netapp': get_prompt(['netapp_prompt'], prompts_path),
        'initial_analysis': get_prompt(['initial_analysis_prompt'], prompts_path),
        'formal_rca': get_prompt(['formal_rca_prompt'], prompts_path),
        'context': get_prompt(['context'], prompts_path)
    }
    return prompts

def get_prompt(prompts_list, prompts_path):
    """
    Retrieve a prompt from a list of prompt files.
    Args:
        prompts_list (list): List of prompt filenames.
    Returns:
        str: The combined prompt text from the files.
    """
    prompt = ""
    for p in prompts_list:
        with open(f"{prompts_path}/{p}", 'r', encoding='utf-8') as file:
            prompt += file.read()
    return prompt