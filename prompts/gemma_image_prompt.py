def generate_prompt(context):
    theme_role = context.get('theme_role')
    sd_prompt = context.get('sd_prompt')
    instruction = {
        "bold": "vibrant colors, contrast lighting",
        "minimal": "neutral background, modern design, subtle tones",
        "luxury": "golden accents, soft shadows, upscale",
        "fun": "cartoon elements, bright palette, confetti, quirky icons",
        "techy": "futuristic UI overlays, glowing edges, holographic visuals"
    }
    return f"""You are an expert in {theme_role} setting the theme and AI prompt engineering. Given a Stable Diffusion prompt, optimize it to create a vivid, high-quality image. {instruction.get(theme_role)}
    Original Stable Diffusion prompt: {sd_prompt}
    Output only optimized prompt in the form of json. The JSON should be structured exactly as follows:
    "optimized_prompt": prompt 
    """
