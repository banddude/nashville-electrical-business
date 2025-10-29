import csv

def generate_financial_table():
    """Reads data from business_plan_data.csv and returns a markdown table."""
    with open('business_plan_data.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    markdown_table = "| " + " | ".join(header) + " |\n"
    markdown_table += '|' + '|'.join(['---'] * len(header)) + '|\n'

    for row in data:
        markdown_table += "| " + " | ".join(row) + " |\n"

    return markdown_table

def main():
    """Generates the README.md file from the template and data."""
    with open('README.template.md', 'r') as f:
        template = f.read()

    financial_table = generate_financial_table()
    
    readme_content = template.replace('{{financial_table}}', financial_table)

    with open('README.md', 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()