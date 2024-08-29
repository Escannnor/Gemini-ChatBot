# import google.generativeai as genai
# import pandas as pd
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def insights(file):
#     data = pd.read_csv(file).to_string()

#     genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
# # Choose a model that's appropriate for your use case.
#     model = genai.GenerativeModel('gemini-1.5-flash')

#     prompt = f"""{data}
#     Given the provided CSV data, please analyze it as a data analyst would when presenting insights to a non-technical manager. Your analysis should include:

# 1. Data Overview: Briefly describe the type of data and its key components.

# 2. Key Trends: Identify and explain the most significant patterns or changes observed in the data.

# 3. Variable Relationships: Highlight any important connections between different data points.

# 4. Standout Observations: Point out any notably high or low values, outliers, or unusual patterns.

# 5. Comparative Analysis: If applicable, compare different categories, time periods, or segments within the data.

# 6. Potential Impact Factors: Suggest possible reasons for the observed trends or patterns.

# 7. Actionable Insights: Provide at least 3-5 practical, data-driven recommendations based on your analysis.

# 8. Visual Representation Ideas: Describe how you would visualize 1-2 key insights to make them more understandable.

# 9. Unexpected Findings: Mention any surprising or counterintuitive insights from the data.

# 10. Limitations and Further Investigation: Note any areas where the data might be insufficient and suggest additional data points that could enhance the analysis.

# Please explain all concepts in plain language, avoiding technical jargon. Use analogies or real-world examples where appropriate to make the insights more relatable.

# Your analysis should be thorough yet accessible, providing valuable insights that could directly impact decision-making. Aim for a balance between high-level overview and specific, actionable details.

# If you need any clarification about specific columns or data points, please ask."""
#     prompt2 = f"""{data}
# Imagine you're the data analyst for our company. You've just analyzed our latest data and need to present your findings to the CEO in a brief, clear meeting. Your goal is to provide practical insights and actionable recommendations. Please structure your response as follows:

# 1. Brief Data Summary: In one sentence, what kind of data did you look at?

# 2. Three Key Findings: What are the most important things you discovered? Explain each in 1-2 simple sentences.

# 3. What This Means for Us: How do these findings impact our business? Use plain language and real-world examples.

# 4. Recommendations: Give 3 specific, practical actions we should take based on this data. Be clear about what to do and why.

# 5. One Surprise: What's one unexpected thing you found? Why is it interesting?

# 6. Next Steps: What's one area we should investigate further, and why?

# Remember, you're talking directly to the CEO. Use simple language, avoid jargon, and focus on what matters for the business. Be confident in your analysis and recommendations."""

    
#     response = model.generate_content(prompt2)
#     if response.text:
#         analysis_text = response.text
#     return {"analysis": analysis_text}
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_plot_instructions(file, graph_type):
    # Read the CSV file and convert it to a string
    data = pd.read_csv(file).to_string()

    # Configure the OpenAI API key
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

    # Choose a model appropriate for your use case
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Define the prompt for generating plot instructions
    prompt = f"""{data}
    Based on the provided CSV data, please generate instructions to create a {graph_type} that will help visualize the data effectively. The instructions should include:

1. The columns to be used for the x-axis and y-axis.
2. Any color-coding or grouping by categories if applicable.
3. Suggestions for titles, labels, and any other annotations to make the plot informative.

Please provide clear and concise instructions for creating the {graph_type}."""

    # Generate content based on the prompt
    try:
        response = model.generate_content(prompt)
        plot_instructions = response.text if response.text else "No response generated."
    except Exception as e:
        plot_instructions = f"An error occurred: {str(e)}"
    
    return {"plot_instructions": plot_instructions}

def plot_and_save_graph(file, instructions, output_path):
    # Read the CSV data
    data = pd.read_csv(file)

    # Extract plot details from the instructions
    lines = instructions.split('\n')
    x_col = y_col = title = x_label = y_label = None
    for line in lines:
        if "x-axis" in line.lower():
            x_col = line.split(':')[-1].strip()
        if "y-axis" in line.lower():
            y_col = line.split(':')[-1].strip()
        if "title" in line.lower():
            title = line.split(':')[-1].strip()
        if "x-label" in line.lower():
            x_label = line.split(':')[-1].strip()
        if "y-label" in line.lower():
            y_label = line.split(':')[-1].strip()
    
    # Validate that the columns exist in the DataFrame
    if x_col not in data.columns or y_col not in data.columns:
        print(f"Columns not found in the data: {x_col}, {y_col}")
        return

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_col], data[y_col], marker='o')
    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    plt.grid(True)
    
    # Save the plot as a PNG file
    plt.savefig(output_path)
    print(f"Graph saved as {output_path}")

# Example usage
if __name__ == "__main__":
    # Define the file path
    file_name = "euro2024_players.csv"  # Change to your CSV file name
    base_dir = os.path.dirname(__file__)  # Get the directory of the current script
    file_path = os.path.join(base_dir, file_name)  # Construct the full file path

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        # Specify the type of graph you want
        graph_type = "line plot"  # Change to your desired graph type, e.g., "bar chart", "scatter plot", etc.
        plot_result = get_plot_instructions(file_path, graph_type)
        
        # Print the instructions
        print("Plot Instructions:")
        print(plot_result["plot_instructions"])

        # Define the output path for the PNG file
        output_path = os.path.join(base_dir, "output_graph.png")

        # Plot the graph based on the instructions and save it as a PNG file
        plot_and_save_graph(file_path, plot_result["plot_instructions"], output_path)
