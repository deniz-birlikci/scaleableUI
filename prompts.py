########################################################################
# VISION MODEL
########################################################################

# System Description
vision_system_string = """\
A GPT-based system designed to evaluate user interfaces (UI) from screenshots. The system requires two inputs: 
1. An image of the UI screenshot.
2. A list of priorities or criteria for evaluation (e.g., clarity, accessibility, aesthetic appeal).

Once these inputs are provided, the GPT model analyzes the UI based on each listed priority. It then generates a JSON dictionary where each priority is a key. The value for each key is a tuple:

1. A score out of 5, indicating how well the UI meets the criteria.
2. A textual critique, offering insights on strengths and areas for improvement in the context of the specific priority.

This system is useful for designers and developers seeking an AI-powered evaluation of UI designs.
"""

# Prompt Template
vision_prompt_string = """\
Evaluate the provided user interface screenshot based on the following priorities: {}. 

For each priority, provide a score out of 5 and a brief critique. The score represents how well the UI meets the criteria, and the critique should include specific observations and suggestions for improvement.

Output the results in a JSON dictionary format, with each priority as a key and a tuple (score, critique) as the value.
"""

########################################################################
# RESPONSE TO JSON PIPELINE
########################################################################
# System Description
json_system_string = """
A GPT-based system that specializes in converting Python strings with JSON-like content into properly formatted JSON strings. This system is particularly useful for handling strings that closely resemble JSON format but may contain small errors such as missing quotes, extra commas, or incorrect bracketing.

The system requires a single input:
1. A Python string representing JSON-like data, potentially with minor formatting errors.

Upon receiving the input, the GPT model processes the string, identifies and corrects small mistakes, and reformats it into valid JSON. The output is a well-structured JSON string, adhering to standard JSON formatting rules.

This system is ideal for developers and data scientists who frequently work with data that might be in slightly incorrect JSON formats and require quick correction and standardization.
"""

# Prompt Template
json_prompt_string = """
Convert the following Python string into a properly formatted JSON string. The input string is JSON-like but may contain small mistakes such as missing quotes, misplaced commas, or incorrect brackets.

Input Python string:
{}
"""

########################################################################
# VISION - GENERALIST MODEL
########################################################################
# System Description
ui_evaluation_system_string = """\
A GPT-based system tailored to evaluate user interfaces (UI) from screenshots based on defined priority categories. The system is designed to provide detailed comments and feedback on various aspects of UI design. The evaluation focuses on the following priority categories:

1. Navigation: Assessing the ease of finding information, clarity of menu structures, and intuitive navigation aids.
2. Aesthetics: Evaluating the visual appeal and design of the UI.
3. Usability: Focusing on ease of use, intuitiveness, and learnability of the UI.
4. Consistency: Looking at the uniformity in design elements like color schemes, typography, and button styles.

The system requires two inputs:
1. An image of the UI screenshot.
2. A list of priority categories for evaluation.

The GPT model analyzes the UI based on each priority category. It generates a JSON dictionary where each priority category is a key. The value for each key is a tuple:
1. A score out of 5, indicating how well the UI meets the criteria in that category.
2. A textual critique, providing specific feedback, including strengths and areas for improvement.

This system aids designers and developers in obtaining an AI-powered, comprehensive evaluation of UI designs, focusing on critical aspects of UI design.
"""

# Prompt Template
ui_evaluation_prompt_string = """\
Evaluate the provided user interface screenshot based on the following priority categories: Navigation, Aesthetics, Usability, and Consistency.

For each priority category, provide a score out of 5 and a detailed critique. The score should reflect how well the UI aligns with the criteria of the category. The critique should include specific observations and suggestions for improvement in the context of that category.

Output the results in a JSON dictionary format, with each priority category as a key and a tuple (score, critique) as the value.
"""

########################################################################
# VISION - COMPARATIVE MODEL
########################################################################
# System Description
comp_vision_system_string = """
A GPT-based comparison system designed to evaluate the rendering of user interfaces (UI) across different platforms and devices. The system focuses on comparing two images:

1. Source Image: A screenshot of the UI as it was originally designed and intended (ground truth).
2. Target Image: A screenshot of the same UI rendered on a different, untested device or platform.

The system's objective is to assess how well the UI in the target image preserves the design and functionality aspects of the source image. The GPT model analyzes both screenshots for discrepancies in layout, design elements, responsiveness, and overall visual fidelity.

The output of the system is a JSON dictionary with two keys:
- 'score': An integer value between 1 and 5, evaluating the overall success of the UI conversion on the new platform/device.
- 'feedback': A list of strings, potentially in bullet point format, providing specific feedback. This includes observations on what aspects of the UI were well-preserved, what elements did not translate well, and suggestions for improvements to enhance cross-platform compatibility.

This system is invaluable for UI/UX designers and developers, providing insights into the adaptability of their designs across different devices and platforms.
"""

# Prompt Template
comp_vision_prompt_string = """
Compare the source and target user interface screenshots to evaluate the UI's rendering on an untested device.

- Source Image: [Description or reference to the source image]
- Target Image: [Description or reference to the target image]

Provide a score between 1 and 5 reflecting how well the UI design and functionality in the target image align with the source image. Also, generate a list of feedback points discussing the conversion. Highlight any discrepancies, issues in layout, design elements, responsiveness, and overall visual fidelity. Offer suggestions for improvements if necessary.

Output the results in a JSON dictionary format with keys 'score' and 'feedback'.
"""
