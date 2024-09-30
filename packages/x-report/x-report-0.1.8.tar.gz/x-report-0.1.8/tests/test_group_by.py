# Sample Data
import pandas as pd

from xreport.pipeline import DataPipeline
from xreport.stages.groupby_stage import GroupByStage
from xreport.stages.source_stage import SourceStage

data = pd.DataFrame({
    'Category': ['A', 'A', 'B', 'B', 'C'],
    'Class': ['a', 'a', 'b', 'B', 'z'],
    'Value': [10, 15, 10, 20, 30],
    'Quantity': [1, 2, 3, 4, 5]
})

# Define the pipeline
pipeline = DataPipeline(
    'Group By Pipeline',
    'Sample pipeline with group by operation',
    SourceStage("Initial Data", "Sample data", data)
)

# Add the GroupByStage
pipeline.add_stage(
    GroupByStage(
        "Group by Category",
        "Group by Category and aggregate Value and Quantity",
        group_by_columns=['Category','Class'],
        agg_funcs={'Value': 'sum', 'Quantity': 'mean'}
    )
)

# Run the pipeline
result_df = pipeline.run()
html_report = pipeline.generate_report()
with open('report_gb.html', 'w') as file:
    file.write(html_report)

