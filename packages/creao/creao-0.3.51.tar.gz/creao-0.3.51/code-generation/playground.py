from typing import List
from pydantic import BaseModel
import json
from openai import OpenAI
import os
import subprocess

# Load your OpenAI API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

# Define a class to represent the schema of the response
class FileStructure(BaseModel):
    code: str
    path: str

class CodeResponse(BaseModel):
    files: List[FileStructure]


def build_and_run():
    # Define the Next.js project directory
    nextjs_project_dir = '../website/nextjs-dashboard'

    # Step 1: Build the application
    try:
        print("Building the Next.js application...")
        build_process = subprocess.run(
            ['npm', 'run', 'build'],  # Use ['yarn', 'build'] if you prefer yarn
            check=True,
            capture_output=True,
            text=True,
            cwd=nextjs_project_dir  # Set the working directory
        )
        print("Build successful.")
    except subprocess.CalledProcessError as e:
        print("Build failed with error:")
        print(e.stderr)

    # Step 2: Run the application
    try:
        print("Starting the Next.js application...")
        run_process = subprocess.run(
            ['npm', 'start'],  # Use ['yarn', 'start'] if you prefer yarn
            check=True,
            capture_output=True,
            text=True,
            cwd=nextjs_project_dir  # Set the working directory
        )
        print("Application is running.")
    except subprocess.CalledProcessError as e:
        print("Failed to start the application:")
        print(e.stderr)

def read_history():
    """
    Read the history.md file to retrieve the history of the project.
    :return: Content of history.md as a string.
    """
    md_file_path = 'history.md'
    try:
        with open(md_file_path, 'r') as file:
            history = file.read()
        print("Successfully read history.md.")
        return history
    except Exception as e:
        print(f"Error reading history.md: {e}")
        return ""

def read_components():
    """
    Read the components.tsx file to retrieve the components.
    :return: Content of components.tsx as a string.
    """
    tsx_file_path = 'component.md'
    try:
        with open(tsx_file_path, 'r') as file:
            components = file.read()
        print("Successfully read components.tsx.")
        return components
    except Exception as e:
        print(f"Error reading components.tsx: {e}")
        return ""

def read_global_css():
    """
    Read the global.css file to retrieve Tailwind CSS styles.
    :return: Content of global.css as a string.
    """
    css_file_path = '../website/nextjs-dashboard/app/ui/global.css'
    try:
        with open(css_file_path, 'r') as file:
            global_css = file.read()
        print("Successfully read global.css.")
        return global_css
    except Exception as e:
        print(f"Error reading global.css: {e}")
        return ""
    
def read_api_doc():
    """
    Read the api-doc.md file to retrieve the API documentation.
    :return: Content of api-doc.md as a string.
    """
    md_file_path = 'api_doc.md'
    try:
        with open(md_file_path, 'r') as file:
            api_doc = file.read()
        print("Successfully read api_doc.md.")
        return api_doc
    except Exception as e:
        print(f"Error reading api_doc.md: {e}")
        return ""
    
def read_head_nav_tsx():
    """
    Read the head-nav.tsx file to retrieve the Tailwind CSS styles.
    :return: Content of head-nav.tsx as a string.
    """
    tsx_file_path = '../website/nextjs-dashboard/app/ui/dashboard/nav/head-nav-links.tsx'
    try:
        with open(tsx_file_path, 'r') as file:
            head_nav_tsx = file.read()
        print("Successfully read head-nav.tsx.")
        return head_nav_tsx
    except Exception as e:
        print(f"Error reading head-nav.tsx: {e}")
        return ""
    
def read_aws_sdk_lib():
    """
    Read the aws-sdk-lib file to retrieve the AWS SDK library.
    :return: Content of aws-sdk-lib as a string.
    """
    lib_file_path = '../website/nextjs-dashboard/app/lib/awsConfig.ts'
    try:
        with open(lib_file_path, 'r') as file:
            aws_sdk_lib = file.read()
        print("Successfully read awsConfig.ts")
        return aws_sdk_lib
    except Exception as e:
        print(f"Error reading awsConfig.ts {e}")
        return ""

def get_gpt4_response_with_code(prompt, global_css, head_nav_tsx, api_doc, aws_sdk_lib, history, component):
    """
    Function to interact with GPT-4 and enforce an output schema containing code.
    The generated code will incorporate TailwindCSS styles from the global.css.
    
    :param prompt: User input or question (string)
    :param global_css: The Tailwind CSS styles from global.css.
    :return: The response from GPT-4 (string)
    """
    
    # Define the system message for output schema enforcement
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful assistant for Next.js development. "
            "Your response must always include a block of code, and also the file path for this code"
            "The response should follow this structure: "
            "1. Code block that demonstrates the solution. "
            "3. add 'use client' on top of the page.tsx code, we only generate client-side page.tsx code"
            "4. Use Tailwind CSS for styling based on the global.css content I provide. "
            "5. all the main pages are under the dashboard folder, and the API is under the api folder"
            "6. Next.js app under folder ../website/nextjs-dashboard, which has the app structure,"
            "7. can you create all necessary new pages and update the head-nav-links.tsx existing pages"
            "8. head nav is udner '../website/nextjs-dashboard/app/ui/dashboard/nav/head-nav-links.tsx'"
            "9. the design must look good, and the code must be clean and well-organized"
            "10. while developing the route.ts api (next.js app) use the api provided in the api_doc.md file, and don't try to implement the logic yourself"
            "11. if there is a component available in the component.md file, import and use it, don't create a new one"
            f"Here is the Tailwind CSS you should use: {global_css}"
            f"Here is the current head-nav.tsx content: {head_nav_tsx}"
            f"here is the current api_doc.md content: {api_doc}"
            f"here is the current aws-sdk-lib content: {aws_sdk_lib}"
            f"here is available component to use: {component}"
        )
    }
    
    # The user prompt
    user_message = {
        "role": "user",
        "content": prompt
    }

    try:
        # Make the API call to the GPT-4 model
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",  # Specify the GPT-4 model
            messages=[system_message, user_message],
            response_format=CodeResponse,
        )
        # Extract the assistant's response
        assistant_message = response.choices[0].message.content
        return assistant_message

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "There was an error while processing your request."

def replace_page_tsx(code):
    """
    Replaces the content of page.tsx under the dashboard/tool directory with the provided code.
    
    :param code: The code string to write into the page.tsx file.
    """
    tsx_file_path = '/Users/yutongpang/dev/creao/website/nextjs-dashboard/app/dashboard/tool/page.tsx'
    try:
        with open(tsx_file_path, 'w') as file:
            file.write(code)
        print(f"Successfully replaced the content of {tsx_file_path}")
    except Exception as e:
        print(f"Error while writing to the file: {e}")

# Example usage
if __name__ == "__main__":
    # Define the prompt for GPT-4

    # Read the global.css file
    global_css = read_global_css()
    head_nav_tsx = read_head_nav_tsx()
    api_doc = read_api_doc()
    aws_sdk_lib = read_aws_sdk_lib()
    history = read_history()
    component = read_components()
    prompt = """
    Now I want to create a new page called photo album:
    which will let user upload multiple image and diplay the photo in a gallery, when click it, it enlarge 50%
    Can you help me create this page.tsx?
    """
    # Call GPT-4 to generate the page.tsx with the Tailwind CSS incorporated
    response = get_gpt4_response_with_code(prompt, global_css, head_nav_tsx, api_doc, aws_sdk_lib, history, component)

    # Try to parse the JSON response (assuming the API returned JSON-formatted text)
    try:
        json_response = json.loads(response)
        files = json_response["files"]
        for file_item in files:
            code = file_item["code"]
            path = file_item["path"]
            # if there is no file exist
            directory_path = os.path.dirname(path)
            # Create the parent directory if it doesn't exist
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                print(f"Directory {directory_path} created for file {path}")
            else:
                print(f"Directory {directory_path} already exists")
            with open(path, 'w') as file:
                file.write(code)

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
    except KeyError as e:
        print(f"Missing expected 'code' key in the response: {e}")
