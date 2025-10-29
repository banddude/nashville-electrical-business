import csv

def format_currency(value):
    return f"{int(value):,}"

def main():
    with open('business_plan_data.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    crew_data = {}
    for row in data:
        crew_count = int(row[0])
        crew_data[crew_count] = {
            'monthly_revenue': float(row[1]),
            'monthly_costs': float(row[2]),
            'monthly_profit': float(row[3]),
            'profit_margin': row[4]
        }

    with open('README.template.md', 'r') as f:
        template = f.read()

    # Calculations
    year_1_revenue_projection = crew_data[1]['monthly_revenue'] * 12
    year_1_profit_projection = crew_data[1]['monthly_profit'] * 12
    year_1_total_revenue_potential = crew_data[4]['monthly_revenue'] * 12

    monthly_revenue_table = ""
    for i in range(1, 5):
        monthly_revenue_table += f"| {i} | {format_currency(crew_data[i]['monthly_revenue'])} | {format_currency(crew_data[i]['monthly_costs'])} | {format_currency(crew_data[i]['monthly_profit'])} | {crew_data[i]['profit_margin']} |\n"


    # Replacements
    template = template.replace('{year_1_revenue_projection}', format_currency(year_1_revenue_projection))
    template = template.replace('{year_1_profit_projection}', format_currency(year_1_profit_projection))
    template = template.replace('{year_1_total_revenue_potential}', format_currency(year_1_total_revenue_potential))
    template = template.replace('{monthly_revenue_table}', monthly_revenue_table)

    template = template.replace('{crew_1_monthly_costs_total}', format_currency(crew_data[1]['monthly_costs']))
    template = template.replace('{crew_2_monthly_costs_total}', format_currency(crew_data[2]['monthly_costs']))
    template = template.replace('{crew_3_monthly_costs_total}', format_currency(crew_data[3]['monthly_costs']))
    template = template.replace('{crew_4_monthly_costs_total}', format_currency(crew_data[4]['monthly_costs']))

    with open('BIBLE/Nashville Electrical Business Plan - Projections.csv', 'r') as f:
        reader = csv.reader(f)
        projections_data = list(reader)

    monthly_operating_costs_table = "| Category | 1 Crew Monthly | 2 Crew Monthly | 3 Crew Monthly | 4 Crew Monthly |\n|---|---|---|---|---|"
    totals = [0, 0, 0, 0]
    for i in range(9, 18):
        row = projections_data[i]
        monthly_operating_costs_table += f"| {row[1]} | ${int(row[4].replace('$', '').replace(',', '')):,} | ${int(row[6].replace('$', '').replace(',', '')):,} | ${int(row[8].replace('$', '').replace(',', '')):,} | ${int(row[10].replace('$', '').replace(',', '')):,} |\n"
        totals[0] += int(row[4].replace('$', '').replace(',', ''))
        totals[1] += int(row[6].replace('$', '').replace(',', ''))
        totals[2] += int(row[8].replace('$', '').replace(',', ''))
        totals[3] += int(row[10].replace('$', '').replace(',', ''))

    total_costs_row = projections_data[18]
    monthly_operating_costs_table += f"| **Total Monthly Costs** | **${int(total_costs_row[4].replace('$', '').replace(',', '')):,}** | **${int(total_costs_row[6].replace('$', '').replace(',', '')):,}** | **${int(total_costs_row[8].replace('$', '').replace(',', '')):,}** | **${int(total_costs_row[10].replace('$', '').replace(',', '')):,}** |\n"

    template = template.replace('{monthly_operating_costs_table}', monthly_operating_costs_table)

    # Crew 1
    template = template.replace('{crew_1_annual_revenue}', format_currency(crew_data[1]['monthly_revenue'] * 12))
    template = template.replace('{crew_1_monthly_revenue}', format_currency(crew_data[1]['monthly_revenue']))
    template = template.replace('{crew_1_annual_profit}', format_currency(crew_data[1]['monthly_profit'] * 12))
    template = template.replace('{crew_1_profit_margin}', crew_data[1]['profit_margin'])
    template = template.replace('{crew_1_monthly_costs}', format_currency(crew_data[1]['monthly_costs']))

    # Crew 2
    template = template.replace('{crew_2_annual_revenue}', format_currency(crew_data[2]['monthly_revenue'] * 12))
    template = template.replace('{crew_2_monthly_revenue}', format_currency(crew_data[2]['monthly_revenue']))
    template = template.replace('{crew_2_monthly_costs}', format_currency(crew_data[2]['monthly_costs']))
    template = template.replace('{crew_2_monthly_profit}', format_currency(crew_data[2]['monthly_profit']))
    template = template.replace('{crew_2_annual_profit_8_months}', format_currency(crew_data[2]['monthly_profit'] * 8))
    template = template.replace('{crew_2_monthly_costs_total}', format_currency(crew_data[2]['monthly_costs']))

    # Crew 3
    template = template.replace('{crew_3_monthly_revenue}', format_currency(crew_data[3]['monthly_revenue']))
    template = template.replace('{crew_3_monthly_costs_total}', format_currency(crew_data[3]['monthly_costs']))
    template = template.replace('{crew_3_monthly_profit}', format_currency(crew_data[3]['monthly_profit']))
    template = template.replace('{crew_3_profit_margin}', crew_data[3]['profit_margin'])

    # Crew 4
    template = template.replace('{crew_4_monthly_revenue}', format_currency(crew_data[4]['monthly_revenue']))
    template = template.replace('{crew_4_monthly_costs_total}', format_currency(crew_data[4]['monthly_costs']))
    template = template.replace('{crew_4_monthly_profit}', format_currency(crew_data[4]['monthly_profit']))
    template = template.replace('{crew_4_profit_margin}', crew_data[4]['profit_margin'])

    # Break-Even
    month_1_net = crew_data[1]['monthly_profit'] - 16800
    month_2_cumulative = month_1_net + crew_data[1]['monthly_profit']
    template = template.replace('{month_1_net}', format_currency(month_1_net))
    template = template.replace('{month_2_cumulative}', format_currency(month_2_cumulative))

    # Annual Cash Flow
    year_1_net_profit = crew_data[1]['monthly_profit'] * 12 - 16800
    template = template.replace('{year_1_net_profit}', format_currency(year_1_net_profit))

    # Annual Metrics
    year_1_revenue_target = f"{format_currency(crew_data[1]['monthly_revenue'] * 12)} - {format_currency(crew_data[2]['monthly_revenue'] * 12)}"
    template = template.replace('{year_1_revenue_target}', year_1_revenue_target)

    # Milestones
    template = template.replace('{month_3_revenue_milestone}', format_currency(crew_data[1]['monthly_revenue']))
    template = template.replace('{month_6_revenue_milestone}', format_currency(crew_data[2]['monthly_revenue']))
    template = template.replace('{month_12_revenue_milestone}', format_currency(crew_data[4]['monthly_revenue']))
    template = template.replace('{year_1_profit_milestone}', format_currency(crew_data[4]['monthly_profit'] * 12))


    with open('README.md', 'w') as f:
        f.write(template)

if __name__ == '__main__':
    main()
