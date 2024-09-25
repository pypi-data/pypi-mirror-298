from vitalDSP.health_analysis.interpretation_engine import InterpretationEngine
from vitalDSP.health_analysis.health_report_visualization import HealthReportVisualizer
from vitalDSP.health_analysis.html_template import render_report

# from vitalDSP.health_analysis.file_io import FileIO
import numpy as np


class HealthReportGenerator:
    """
    A class to generate a health report based on feature data, including interpretations, visualizations, and contradictions/correlations.

    This class handles the process of interpreting feature data (e.g., heart rate variability, ECG/PPG data),
    generating visualizations for features, and rendering the final HTML report.

    Attributes:
        feature_data (dict): Dictionary containing feature names as keys and their corresponding values.
        segment_duration (str): Duration of the segment, either "1_min" or "5_min". Default is "1 min".
        interpreter (InterpretationEngine): Instance of InterpretationEngine to interpret feature data.
        visualizer (HealthReportVisualizer): Instance of HealthReportVisualizer to create visualizations.
    """

    def __init__(
        self, feature_data, segment_duration="1 min", feature_config_path=None
    ):
        """
        Initializes the HealthReportGenerator with the provided feature data and segment duration.

        Args:
            feature_data (dict): Dictionary containing feature names as keys and their corresponding values as values.
                                Example: {"nn50": 35, "rmssd": 55, "sdnn": 70}
            segment_duration (str): The duration of the analyzed segment, either '1 min' or '5 min'. Default is '1 min'.
            feature_config_path (str, optional): Path to a custom feature YAML configuration file. If not provided, the default config will be used.

        Example Usage:
            >>> feature_data = {"nn50": 45, "rmssd": 70, "sdnn": 120}
            >>> generator = HealthReportGenerator(feature_data, segment_duration="5 min", feature_config_path="path/to/config.yml")
            >>> report_html = generator.generate()
        """
        self.feature_data = feature_data
        self.segment_duration = segment_duration
        self.interpreter = InterpretationEngine(feature_config_path)
        self.visualizer = HealthReportVisualizer(self.interpreter.config)

    def generate(self, filter_status="all"):
        """
        Generates the complete health report by interpreting the features, generating visualizations, and rendering an HTML report.

        The report will include the description of each feature, its interpretation (in-range, above range, or below range),
        any detected contradictions, correlations, and visualizations for each feature.

        Returns:
            str: HTML content of the generated health report.

        Example Usage:
            >>> feature_data = {"nn50": 45, "rmssd": 70, "sdnn": 120}
            >>> generator = HealthReportGenerator(feature_data, segment_duration="5 min")
            >>> report_html = generator.generate()
            >>> with open('health_report.html', 'w') as file:
            >>>     file.write(report_html)
        """
        # report_content = {}
        segment_values = {}  # To store segmented interpretations

        # Step 1: Interpret each feature with the loaded configuration
        for feature_name, values in self.feature_data.items():
            # Calculate the mean of the feature's values
            mean_value = sum(values) / len(values)

            # Interpret based on the mean value
            interpretation = self.interpreter.interpret_feature(
                feature_name, mean_value, self.segment_duration
            )
            range_status = self.interpreter.get_range_status(
                feature_name, mean_value, self.segment_duration
            )

            # Skip features not matching the filter status
            if filter_status != "all" and range_status != filter_status:
                continue

            median_value = np.median(values)
            stddev_value = np.std(values)
            # Store aggregated information
            segment_values[feature_name] = {
                "description": interpretation["description"],
                "value": values,  # Store the list of values for the feature
                "median": median_value,  # Median value
                "stddev": stddev_value,  # Standard deviation
                "interpretation": interpretation["interpretation"],
                "normal_range": interpretation["normal_range"],
                "contradiction": interpretation.get("contradiction", None),
                "correlation": interpretation.get("correlation", None),
                "range_status": range_status,  # Based on the mean value
            }

        # Step 2: Generate visualizations for all features (pass all segments of data)
        visualizations = self.visualizer.create_visualizations(self.feature_data)

        # Step 3: Provide all visualizations for each feature
        selected_visualizations = visualizations

        # Step 4: Render the report
        report_html = render_report(segment_values, selected_visualizations)

        return report_html

    def _generate_feature_report(self, feature_name, value):
        """
        Generates the interpretation report for an individual feature including its description, normal range,
        interpretation (based on the range), contradictions, and correlations.

        Args:
            feature_name (str): The name of the feature to generate the report for (e.g., "NN50", "RMSSD").
            value (float): The value of the feature (e.g., 35.0 for NN50).

        Returns:
            dict: A dictionary containing:
            - "description": Description of the feature.
            - "value": The actual feature value.
            - "interpretation": Interpretation of the value based on the normal range.
            - "normal_range": The normal range of the feature.
            - "contradiction": Contradictions with related features.
            - "correlation": Correlations with related features.

        Example Usage:
            >>> feature_name = "NN50"
            >>> value = 45
            >>> generator = HealthReportGenerator(feature_data)
            >>> feature_report = generator._generate_feature_report(feature_name, value)
            >>> print(feature_report)
            {
                "description": "Number of significant changes in heart rate. High NN50 suggests healthy parasympathetic activity.",
                "value": 45,
                "interpretation": "Normal parasympathetic activity. No immediate concern.",
                "normal_range": [10, 50],
                "contradiction": "Low NN50 contradicts high RMSSD, as both should indicate parasympathetic activity.",
                "correlation": "Positively correlated with RMSSD, as both represent short-term heart rate variability."
            }
        """
        # Interpret the feature using the InterpretationEngine
        feature_info = self.interpreter.interpret_feature(
            feature_name, value, self.segment_duration
        )

        # Add the description, interpretation, contradiction, and correlation to the report
        feature_report = {
            "description": feature_info.get("description", "No description available."),
            "value": value,
            "interpretation": feature_info.get(
                "interpretation", "No interpretation available."
            ),
            "normal_range": feature_info.get(
                "normal_range", "No normal range available."
            ),
            "contradiction": feature_info.get(
                "contradiction", "No contradiction found."
            ),
            "correlation": feature_info.get("correlation", "No correlation found."),
        }

        return feature_report
