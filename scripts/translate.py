import asyncio
import re
import json
from openai import OpenAI
import os
from datetime import datetime
from hash import calculate_sha256, load_hashes, save_hashes
from get_feps import get_feps

# --- Script Configuration ---
INPUT_DIR = "./fep/fep"
OUTPUT_DIR = "./docs"
DEST_LANG = "ja"

# --- Configuration and Prompt Loading ---
def load_config():
    """Loads configuration from config.json."""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_prompt(target_language):
    """Loads and formats the system prompt from prompts/translate.md."""
    with open("prompts/translate.md", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    return prompt_template.replace("{{targetLanguage}}", target_language)

# --- Core Logic ---
def separate_frontmatter(content):
    """Separates YAML frontmatter from the main markdown content."""
    frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)
    match = frontmatter_pattern.match(content)
    if match:
        frontmatter = match.group(1)
        markdown_body = content[match.end():]
        return frontmatter, markdown_body
    return None, content

async def get_llm_translation(md_content, dest_lang, client, model, system_prompt):
    """Gets the full translated string from the LLM."""
    if not md_content.strip():
        return ""

    print("Sending Markdown to LLM for translation...")
    user_prompt = f"Please translate the following Markdown document into {dest_lang}. Adhere strictly to the guidelines in the system prompt and return only the translated Markdown content.\n\n---\n\n{md_content}"
    
    full_response = ""
    try:
        stream = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            stream=True
        )
        for chunk in stream:
            full_response += chunk.choices[0].delta.content or ""
        print("Successfully received full translation from LLM.")
        return full_response
    except Exception as e:
        print(f"Error during LLM stream processing: {e}")
        return None # Return None on error

async def process_single_file(input_file, output_file, dest_lang, client, system_prompt, model):
    """Processes a single file: hash check, translation, templating."""
    
    fep_id = os.path.splitext(os.path.basename(input_file))[0].replace("fep-", "")
    print(f"--- Processing FEP: {fep_id} ---")

    # --- Hash Check ---
    current_hash = calculate_sha256(input_file)
    if not current_hash:
        return
    
    stored_hashes = load_hashes()
    if stored_hashes.get(fep_id) == current_hash:
        print(f"Hash for {fep_id} is unchanged. Skipping translation.")
        return
    print(f"Hash for {fep_id} has changed or is new. Proceeding with translation.")

    try:
        with open("fep_ja_template.md", "r", encoding="utf-8") as f:
            output_template = f.read()

        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        translated_content = await get_llm_translation(original_content, dest_lang, client, model, system_prompt)
        if translated_content is None:
            print(f"Translation failed for {fep_id}. Skipping file update.")
            return

        translated_frontmatter, translated_body = separate_frontmatter(translated_content)
        md_h1_first = ""
        h1_pattern = re.compile(r"^\s*#\s+(.*)", re.MULTILINE)
        match = h1_pattern.search(translated_body)
        if match:
            md_h1_first = match.group(1).strip()
            translated_body = h1_pattern.sub("", translated_body, count=1).lstrip("\r\n")
        else:
            print("Warning: No H1 heading ('# ...') found in the translated body.")

        final_output = output_template.replace("{{frontmatter}}", f"---\n{translated_frontmatter}\n---" if translated_frontmatter else "")
        final_output = final_output.replace("{{md_h1_first}}", md_h1_first)
        final_output = final_output.replace("{{md_body}}", translated_body)
        final_output = final_output.replace("{{llm_model}}", model)
        final_output = final_output.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        final_output = final_output.replace("{{original_fep_location}}", f"https://codeberg.org/fediverse/fep/src/branch/main/fep/{fep_id}/{fep_id}.md")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
            
        print(f"Translation complete. Output written to '{output_file}'.")

        stored_hashes[fep_id] = current_hash
        save_hashes(stored_hashes)
        print(f"Updated hash for {fep_id} in hashes.json.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {fep_id}: {e}")

async def main():
    """Main function to run the batch translation process."""
    # --- Pre-flight Checks ---
    api_key_env = os.getenv("GEMINI_API_KEY")
    if not api_key_env:
        print("Warning: GEMINI_API_KEY environment variable not set. Trying to use key from config.json.")
        try:
            config = load_config()
            if config.get("llm", {}).get("api_key") == "API_KEY":
                print("Error: Please set the GEMINI_API_KEY environment variable or update the api_key in config.json.")
                return
        except FileNotFoundError:
            print("Error: config.json not found. Please set GEMINI_API_KEY environment variable.")
            return

    # --- Initialization ---
    config = load_config()
    llm_config = config.get("llm", {})
    api_key = os.getenv("GEMINI_API_KEY") or llm_config.get("api_key", "API_KEY")
    model = llm_config.get("model", "gemini-2.5-flash")
    base_url = llm_config.get("base_url")

    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = load_prompt(DEST_LANG)

    # --- Get list of FEPs and process them ---
    fep_files = get_feps()
    print(f"Found {len(fep_files)} FEPs to process.")

    for fep_filename in fep_files:
        input_path = os.path.join(os.path.join(INPUT_DIR, fep_filename), f"fep-{fep_filename}.md")
        output_path = os.path.join(os.path.join(OUTPUT_DIR, fep_filename), "index.md")
        
        if not os.path.isfile(input_path):
            print(f"Skipping non-file entry: {fep_filename}")
            continue

        await process_single_file(input_path, output_path, DEST_LANG, client, system_prompt, model)

if __name__ == "__main__":
    asyncio.run(main())
