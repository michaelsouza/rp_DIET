import os
import time
from openai import OpenAI

client = OpenAI()


def read_article(file_path):
    """
    Read the article content from a file.

    Args:
    file_path (str): Path to the article file.

    Returns:
    str: Content of the article.
    """
    print(f"📂 Reading article from: {file_path}")
    with open(file_path, "r") as f:
        return f.read()


def extract_paragraphs(article_content, topic):
    """
    Extract paragraphs related to a specific topic and summarize the article.

    Args:
    article_content (str): The full content of the article.
    topic (str): The topic to focus on for extraction.

    Returns:
    str: Extracted and summarized content in Markdown format.
    """
    tic = time.time()
    system_message = f"""
    You will be provided with an article delimited by triple quotes. Your tasks are:
    1. Extract the title of the article.
    2. Extract paragraphs related to {topic}.
    3. Keep the food-related content.
    4. Use clear and simple language.
    5. Format the output as a MARKDOWN object with three sections: 'Title', 'Summary', and 'Content'.    
    """
    print(f"🔍 Extracting paragraphs related to '{topic}'...")
    user_message = f'"""{article_content}"""'

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the GPT-4o-mini model
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # Lower temperature for more focused output
    )

    chat_response_content = response.choices[0].message.content

    toc = time.time()
    print(f"   ✅ Extraction completed in {toc - tic:.2f} seconds.")

    return chat_response_content


def format_output(extracted_data):
    """
    Format the extracted data as Markdown.

    Args:
    extracted_data (str): The extracted and summarized content.

    Returns:
    str: Formatted Markdown content.
    """
    print("📝 Formatting output...")
    return extracted_data


def get_output_file_path(file_path):
    """
    Generate the output file path.

    Args:
    file_path (str): Path to the input file.

    Returns:
    str: Path for the output file.
    """
    input_file_name = os.path.basename(file_path)
    output_file_name = f"{os.path.splitext(input_file_name)[0]}.md"
    return os.path.join(os.path.dirname(file_path), output_file_name)


def process_article(file_path: str, topic="low-carb diets"):
    """
    Process an article: read, extract relevant content, format, and save.

    Args:
    file_path (str): Path to the input article file.
    topic (str): The topic to focus on for extraction. Defaults to "low-carb diets".
    """
    print(f"\n🚀 Processing article: {file_path}")
    article_content = read_article(file_path)
    extracted_data = extract_paragraphs(article_content, topic)
    formatted_output = format_output(extracted_data)

    print(formatted_output)

    # Generate output Markdown file
    output_file_path = get_output_file_path(file_path)

    # Save extracted data as Markdown
    print(f"💾 Saving output to: {output_file_path}")
    with open(output_file_path, "w") as f:
        f.write(formatted_output)

    print(f"✅ Article processing complete!")


if __name__ == "__main__":
    references_folder = "references"
    print(f"🔎 Searching for articles in: {references_folder}")
    for file in os.listdir(references_folder):
        if file.endswith(".txt"):
            file_path = os.path.join(references_folder, file)
            output_file_path = get_output_file_path(file_path)
            if os.path.exists(output_file_path):
                print(f"⚠️  Output file already exists: {output_file_path}")
                continue
            process_article(file_path)
            print("\n")

    print("🎉 All articles processed successfully!")
