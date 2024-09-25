import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


class HealthReportVisualizer:
    """
    A class responsible for creating visualizations of health feature data, including line plots and heatmaps.

    The class takes feature data and creates visualizations, such as normal distributions for ranges and heatmaps, and stores them as images.
    """

    def __init__(self, config):
        """
        Initializes the Visualization class by loading the feature configuration.

        Args:
            config (dict): Configuration data that includes normal ranges and interpretations for features.

        Example Usage:
            >>> visualization = Visualization(config)
        """
        if not isinstance(config, dict):
            raise TypeError("Config should be a dictionary.")
        self.config = config

    def _fetch_and_validate_normal_range(self, feature, value):
        """
        Fetches the normal range for a given feature, handles NaN, Inf values, and validates the feature.

        Args:
            feature (str): The feature name.
            value (float): The current value for the feature.

        Returns:
            tuple: (normal_min, normal_max, feature_names) where feature_names are ["Min Range", "Max Range", "Current Value"].

        Raises:
            ValueError: If the feature has NaN or invalid values, or normal range is not found.
        """
        normal_range = self._get_normal_range_for_feature(feature)
        if not normal_range:
            # return None
            raise ValueError(f"Normal range for feature '{feature}' not found.")

        normal_min, normal_max = normal_range
        # feature_names = ["Min Range", "Max Range", "Current Value"]

        # Handle NaN and Inf cases
        if np.isnan(normal_min) or np.isnan(normal_max) or np.isnan(value):
            raise ValueError(f"NaN value encountered in feature '{feature}'.")

        if np.isinf(normal_min):
            normal_min = -10 * abs(value)
        if np.isinf(normal_max):
            normal_max = 10 * abs(value)

        return normal_min, normal_max

    def create_visualizations(self, feature_data, output_dir="visualizations"):
        """
        Creates visualizations for the provided feature data and saves them as image files.

        Args:
            feature_data (dict): Dictionary containing feature values.
            output_dir (str): Directory where the visualizations will be saved.

        Returns:
            dict: Dictionary with feature names as keys and paths to the saved visualizations as values.

        Example Usage:
            >>> visualizations = visualization.create_visualizations(feature_data)
            >>> print(visualizations)
        """
        os.makedirs(output_dir, exist_ok=True)

        visualization_paths = {}

        for feature, values in feature_data.items():
            if isinstance(
                values, list
            ):  # Handle list (multiple segments) for each feature
                visualization_paths[feature] = {
                    "heatmap": os.path.normpath(
                        self._create_heatmap_plot(feature, values, output_dir)
                    ),
                    "bell_plot": os.path.normpath(
                        self._create_bell_shape_plot(feature, values, output_dir)
                    ),
                    "radar_plot": os.path.normpath(
                        self._create_radar_plot(feature, values, output_dir)
                    ),
                    "violin_plot": os.path.normpath(
                        self._create_violin_plot(feature, values, output_dir)
                    ),
                }
            else:
                # Handle single values
                visualization_paths[feature] = {
                    "heatmap": os.path.normpath(
                        self._create_heatmap_plot(feature, [values], output_dir)
                    ),
                    "bell_plot": os.path.normpath(
                        self._create_bell_shape_plot(feature, [values], output_dir)
                    ),
                    "radar_plot": os.path.normpath(
                        self._create_radar_plot(feature, [values], output_dir)
                    ),
                    "violin_plot": os.path.normpath(
                        self._create_violin_plot(feature, [values], output_dir)
                    ),
                }

        return visualization_paths

    def _create_bell_shape_plot(self, feature, values, output_dir):
        """
        Creates a bell shape plot with an overlaid histogram for better understanding.
        Caps outliers at 1.5 times the normal range.

        Args:
            feature (str): The name of the feature.
            values (list): List of values for the feature.
            output_dir (str): Directory where the plot will be saved.

        Returns:
            str: Path to the saved bell shape plot image.
        """
        normal_min, normal_max = self._fetch_and_validate_normal_range(
            feature, values[0]
        )

        # Outlier thresholds
        outlier_min = normal_min - 1.5 * (normal_max - normal_min)
        outlier_max = normal_max + 1.5 * (normal_max - normal_min)

        # Cap the values to fit the normal range
        capped_values = np.clip(values, outlier_min, outlier_max)

        # Generate histogram data with clear edges and a less dim color
        plt.figure(figsize=(8, 6))
        plt.hist(
            capped_values,
            bins=15,
            color="lightblue",
            alpha=0.7,
            edgecolor="black",
            label="Histogram",
        )

        # Generate x values for the bell curve
        x = np.linspace(outlier_min, outlier_max, 100)
        mean = (normal_min + normal_max) / 2
        stddev = (normal_max - normal_min) / 4
        y = np.exp(-((x - mean) ** 2) / (2 * stddev**2))

        # Plot the bell-shaped curve
        plt.plot(
            x,
            y * max(np.histogram(capped_values, bins=15)[0]),
            label="Bell Shape",
            color="blue",
        )

        # Mark the normal range and current value
        plt.axvline(
            normal_min, color="blue", linestyle="--", label=f"Normal Min: {normal_min}"
        )
        plt.axvline(
            normal_max, color="red", linestyle="--", label=f"Normal Max: {normal_max}"
        )
        plt.axvline(
            np.median(values),
            color="green",
            linestyle="-",
            label=f"Median: {np.median(values):.2f}",
        )

        # Title and labels
        plt.title(f"{feature} Bell Shape Plot with Histogram")
        plt.xlabel(f"{feature} Values")

        # Explicitly create the legend
        plt.legend(loc="upper right")

        # Save the plot
        filepath = os.path.join(output_dir, f"{feature}_bell_plot.png")
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

        return filepath

    def _create_violin_plot(self, feature, values, output_dir):
        """
        Creates an enhanced violin plot for visualizing the feature value compared to the normal range.

        Args:
            feature (str): The name of the feature.
            value (list): The values of the feature for the current segment.
            output_dir (str): Directory where the plot will be saved.

        Returns:
            str: Path to the saved violin plot image.
        """
        normal_min, normal_max = self._fetch_and_validate_normal_range(
            feature, values[0]
        )

        # Define the outlier threshold
        outlier_min = normal_min - 1.5 * (normal_max - normal_min)
        outlier_max = normal_max + 1.5 * (normal_max - normal_min)

        # Cap the values to fit within the plot and mark outliers
        capped_values = []
        for value in values:
            if value < outlier_min:
                capped_values.append(outlier_min)
            elif value > outlier_max:
                capped_values.append(outlier_max)
            else:
                capped_values.append(value)

        # Create data for the violin plot (normal distribution)
        data = np.random.normal(
            loc=(normal_max + normal_min) / 2,
            scale=(normal_max - normal_min) / 6,
            size=1000,
        )

        plt.figure(figsize=(8, 6))

        # Create violin plot for normal distribution
        sns.violinplot(data=data, color="lightgreen", inner="quartile")

        # Overlay shaded normal range
        plt.fill_between(
            [0, 1],
            normal_min,
            normal_max,
            color="lightblue",
            alpha=0.3,
            label="Normal Range",
        )

        # Add a horizontal line for the mean of the normal range
        mean_value = (normal_max + normal_min) / 2
        plt.axhline(
            mean_value,
            color="green",
            linestyle="--",
            label=f"Normal Range Mean: {mean_value:.2f}",
        )

        # Plot each value, marking capped values as outliers
        for value in capped_values:
            color = "red" if value == outlier_min or value == outlier_max else "blue"
            plt.scatter(0, value, color=color, zorder=5, s=100, edgecolors="black")

        plt.title(f"{feature} Violin Plot", fontsize=15)
        plt.xlabel(f"{feature} Values")

        # Add legend
        plt.legend(loc="upper right")

        # Save the plot
        filepath = os.path.join(output_dir, f"{feature}_violin_plot.png")
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

        return filepath

    def _create_heatmap_plot(self, feature, values, output_dir):
        """
        Creates a heatmap plot for visualizing the feature values with highlights for the normal range.

        Args:
            feature (str): The name of the feature.
            values (list): The list of values for the current segment.
            output_dir (str): Directory where the plot will be saved.

        Returns:
            str: Path to the saved heatmap plot image.
        """
        normal_min, normal_max = self._fetch_and_validate_normal_range(
            feature, values[0]
        )

        # Set outlier thresholds
        outlier_min = normal_min - 1.5 * (normal_max - normal_min)
        outlier_max = normal_max + 1.5 * (normal_max - normal_min)

        # Create x-axis values for the heatmap
        x = np.linspace(
            normal_min - 1.5 * (normal_max - normal_min),
            normal_max + 1.5 * (normal_max - normal_min),
            100,
        )
        y = np.exp(
            -((x - np.mean([normal_min, normal_max])) ** 2)
            / (2 * ((normal_max - normal_min) / 2) ** 2)
        )
        heatmap_data = np.outer(y, y)

        plt.figure(figsize=(8, 4))
        sns.heatmap(
            heatmap_data,
            cmap="coolwarm",
            cbar=False,
            xticklabels=False,
            yticklabels=False,
        )

        # Track the number of occurrences for each value
        value_counts = {}
        for value in values:
            capped_value = min(max(value, outlier_min), outlier_max)
            if capped_value in value_counts:
                value_counts[capped_value] += 1
            else:
                value_counts[capped_value] = 1

        # Plot scatter points with size based on frequency of the value
        for capped_value, count in value_counts.items():
            value_interp = np.interp(capped_value, x, np.linspace(0, 100, len(x)))
            scatter_size = 100 + (count - 1) * 50  # Increase size for repeated values
            plt.scatter(
                [value_interp],
                [50],
                color="#3498db",
                s=scatter_size,
                zorder=5,
                edgecolor="white",
            )

        # Mark the normal range
        plt.axvline(
            np.interp(normal_min, x, np.linspace(0, 100, len(x))),
            color="blue",
            linestyle="-",
            label="Normal Min",
        )
        plt.axvline(
            np.interp(normal_max, x, np.linspace(0, 100, len(x))),
            color="red",
            linestyle="-",
            label="Normal Max",
        )

        plt.title(f"Feature: {feature}\nNormal Range: [{normal_min}, {normal_max}]")
        plt.legend()

        # Save heatmap
        filepath = os.path.join(output_dir, f"{feature}_heatmap.png")
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

        return filepath

    def _create_radar_plot(self, feature, values, output_dir):
        """
        Creates an enhanced radar plot that shows how the feature value compares to the normal range.
        Each axis represents a different feature, and the plot shows how the current feature deviates
        from its normal range.

        Args:
            feature (str): The name of the feature.
            values (list): The list of values for the current segment.
            output_dir (str): Directory where the plot will be saved.

        Returns:
            str: Path to the saved radar plot image.
        """
        # Fetch normal range
        normal_min, normal_max = self._fetch_and_validate_normal_range(
            feature, values[0]
        )
        feature_names = ["Min Range", "Max Range", "Representative Value"]

        # Handle NaN and Inf cases
        if np.isnan(normal_min) or np.isnan(normal_max) or np.any(np.isnan(values)):
            raise ValueError(f"NaN value encountered in feature '{feature}'.")

        if np.isinf(normal_min):
            normal_min = -10 * abs(np.min(values))
        if np.isinf(normal_max):
            normal_max = 10 * abs(np.max(values))

        # Outlier thresholds
        outlier_min = normal_min - 1.5 * (normal_max - normal_min)
        outlier_max = normal_max + 1.5 * (normal_max - normal_min)

        # Cap the values to fit within the plot and mark outliers
        capped_values = np.clip(values, outlier_min, outlier_max)

        # Prepare the "normal range" triangle data
        normal_values = [normal_min, normal_max, (normal_min + normal_max) / 2]
        normal_values += normal_values[:1]  # Complete the loop

        # Prepare the "current value" triangle data: min, max, median of the capped values list
        current_value_triangle = [
            np.min(capped_values),
            np.max(capped_values),
            np.median(capped_values),
        ]
        current_value_triangle += current_value_triangle[:1]  # Complete the loop

        # Calculate angles for radar plot
        angles = np.linspace(0, 2 * np.pi, len(feature_names), endpoint=False).tolist()
        angles += angles[:1]  # Complete the loop for radar chart

        # Start plot
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Configure axes
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        plt.xticks(angles[:-1], feature_names)

        # Set radial limits based on min and max of normal and capped data
        y_min = min(normal_min, np.min(capped_values))
        y_max = max(normal_max, np.max(capped_values))
        plt.ylim(y_min, y_max)

        # Plot normal range triangle
        ax.plot(
            angles,
            normal_values,
            linewidth=2,
            linestyle="solid",
            color="green",
            label="Normal Range",
        )
        ax.fill(angles, normal_values, color="green", alpha=0.3)

        # Plot actual values triangle (min, max, median)
        ax.plot(
            angles,
            current_value_triangle,
            linewidth=2,
            linestyle="solid",
            color="blue",
            label="Actual Values",
        )
        ax.fill(angles, current_value_triangle, color="blue", alpha=0.3)

        # Add a scatter point for the median value on the third axis
        median_value = np.median(capped_values)
        ax.scatter(
            angles[2], median_value, color="red", zorder=5, s=150, edgecolors="black"
        )

        # Mark outliers
        for value in values:
            if value < outlier_min or value > outlier_max:
                ax.scatter(
                    angles[2],
                    median_value,
                    color="orange",
                    zorder=5,
                    s=150,
                    edgecolors="black",
                    label="Outlier",
                )

        # Add a legend
        plt.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

        # Save the plot
        filepath = os.path.join(output_dir, f"{feature}_radar_plot.png")
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

        return filepath

    def _get_normal_range_for_feature(self, feature):
        """
        Retrieves the normal range for a given feature from the loaded configuration.

        Args:
            feature (str): The name of the feature to get the normal range for.

        Returns:
            tuple: The (min, max) normal range values for the feature, or None if not found.

        Example Usage:
            >>> normal_range = visualization._get_normal_range_for_feature("RMSSD")
            >>> print(normal_range)  # Output: (20, 100)
        """
        feature_info = self.config.get(feature, {})
        normal_range = feature_info.get("normal_range", {}).get("1_min", None)
        if normal_range is not None:
            # Handle string '-inf' and 'inf' cases
            normal_range = [self._parse_inf_values(val) for val in normal_range]
        return normal_range

    def _parse_inf_values(self, val):
        """
        Parses 'inf' and '-inf' strings and converts them to numpy infinity values.

        Args:
            val (str or float): The value to parse.

        Returns:
            float: Parsed value where 'inf' or '-inf' are converted to np.inf or -np.inf respectively.

        Example Usage:
            >>> value = visualization._parse_inf_values("-inf")
            >>> print(value)  # Output: -inf
        """
        if isinstance(val, str):
            if val.lower() == "inf":
                return np.inf
            elif val.lower() == "-inf":
                return -np.inf
        return val
