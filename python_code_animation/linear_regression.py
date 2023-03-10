from manim import *
import numpy as np

class LinearRegression(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=8,
            y_length=6,
            axis_config={
                "numbers_to_include": np.arange(0, 11, 2),
                "color": WHITE,
                "stroke_width": 2,
                "tip_length": 0.15,
            },
            x_axis_config={
                "label": "$x$",
                "numbers_with_elongated_ticks": np.arange(0, 11, 2),
            },
            y_axis_config={
                "label": "$y$",
                "numbers_with_elongated_ticks": np.arange(0, 11, 2),
            },
        )
        axes.add_coordinate_labels(font_size=20, num_decimal_places=0)

        # Generate random data points
        x = np.random.rand(10) * 10
        y = x * 2 + 1 + np.random.randn(10) * 2

        # Create scatter plot
        scatter = Scatter(
            np.array([x, y, np.zeros_like(x)]).T,
            color=BLUE,
            radius=0.15,
            fill_opacity=0.8,
            stroke_width=0,
        )

        # Add scatter plot and axes to scene
        self.play(Create(axes), Create(scatter))

        # Perform linear regression
        m, b = np.polyfit(x, y, 1)

        # Create line of best fit
        line = axes.get_graph(lambda x: m*x+b, x_range=[0, 10], color=RED)

        # Add line of best fit to scene
        self.play(Create(line))

        # Show equation of line
        equation = MathTex("y=", f"{m:.2f}", "x+", f"{b:.2f}").scale(1.5).move_to(UP * 2)
        self.play(Create(equation))
        self.wait(2)
