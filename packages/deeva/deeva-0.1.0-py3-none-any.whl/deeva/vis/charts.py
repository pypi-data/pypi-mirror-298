import math
import os
import random
from copy import deepcopy
from math import ceil

import cv2
import matplotlib.colors as mcl
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.optimize import fsolve
from sklearn.cluster import KMeans

from .utils import crop_aggregate_box, get_rect_vertices, hex_to_rgba, generate_proportional_centroids
from .utils import get_planet_texture, plotly_fig2array, solve_distance
from configs import VW, VH, HUE_RANGES
from configs.utils import get_image_uri
from utils import render_html


def plot_matching(matching, seed=12345):
    np.random.seed(seed)

    def get_points():
        get_y_images = np.vectorize(lambda x: np.random.uniform(x + 20, 100, 1)[0])
        get_y_labels = np.vectorize(lambda x: np.random.uniform(0, x - 20, 1)[0])

        x_images = np.random.normal(loc=10, scale=30, size=len(matching['Lonely images']))
        wrong_gen_mask_images = (x_images < 0) | (x_images > 100)
        if any(wrong_gen_mask_images):
            x_images[wrong_gen_mask_images] = np.random.uniform(1, 50, size=np.sum(wrong_gen_mask_images))
        y_images = get_y_images(x_images) if x_images.size > 0 else []

        x_labels = np.random.normal(loc=90, scale=30, size=len(matching['Lonely labels']))
        wrong_gen_mask_labels = (x_labels < 0) | (x_labels > 100)
        if any(wrong_gen_mask_labels):
            x_labels[wrong_gen_mask_labels] = np.random.uniform(50, 100, size=np.sum(wrong_gen_mask_labels))
        y_labels = get_y_labels(x_labels) if x_labels.size > 0 else []

        return x_images, x_labels, y_images, y_labels

    x_images, x_labels, y_images, y_labels = get_points()

    df = pd.DataFrame(
        {'x': np.hstack((x_images, x_labels)), 'y': np.hstack((y_images, y_labels)),
         'size': np.repeat(1, x_images.size + x_labels.size),
         'color': np.hstack(
             (np.repeat('Lonely image', x_images.size), np.repeat('Lonely label', x_labels.size))),
         'id': np.hstack((np.arange(0, x_images.size) + 1, np.arange(0, x_labels.size) + 1)),
         'count': np.hstack(
             (np.repeat(x_images.size, x_images.size), np.repeat(x_labels.size, x_labels.size)))
         })

    df['hover'] = df['color'] + ': ' + df['id'].astype(str) + '/' + df['count'].astype(str)

    fig = px.scatter(
        df, x="x", y="y", size="size", color='color',
        color_discrete_map={'Lonely image': '#83c5be', 'Lonely label': '#ffcb69'},
        opacity=0.2, hover_name='hover', hover_data={k: False for k in df.columns}
    )

    fig.add_scatter(
        x=[10], y=[90], marker=dict(size=0.08 * VW, color='#83c5be', line=dict(width=0.0016 * VW, color='DarkSlateGrey')),
        opacity=0.8, mode='markers+text', text=f"{len(matching['Matched images'])}", textposition="middle center",
        textfont=dict(size=0.014 * VW, color='black', family='Arial'), name='Matched images', hoverinfo='none'
    )

    fig.add_scatter(
        x=[90], y=[10], marker=dict(size=0.08 * VW, color='#ffcb69', line=dict(width=0.0016 * VW, color='DarkSlateGrey')),
        opacity=0.8, mode='markers+text', text=f"{len(matching['Matched labels'])}", textposition="middle center",
        textfont=dict(size=0.014 * VW, color='black', family='Arial'), name='Matched labels', hoverinfo='none'
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        hoverlabel=dict(font=dict(size=0.01 * VW)),
        legend=dict(
            orientation='h', xanchor="center", x=0.5, y=1.1,
            font=dict(family="sans-serif", size=0.008 * VW, color="white"),
            title_text=''
        ),
        height=0.455 * VH
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_overall_pies(annotations_pie, backgrounds_pie, images_pie):
    annotations_labels = ['yolo', 'voc', 'corrupted_labels']
    backgrounds_labels = ['images', 'backgrounds']
    images_labels = ['png', 'jpg', 'jpeg', 'corrupted_images']

    annotations_colors = {label: color for label, color in
                          zip(annotations_labels, ['#F4A300', '#D83F6C', '#6A1B9A'])}
    backgrounds_colors = {label: color for label, color in
                          zip(backgrounds_labels, ['#736565', '#46b3bd'])}
    images_colors = {label: color for label, color in
                     zip(images_labels, ['#8BC34A', '#FF5722', '#3F51B5', '#9C27B0'])}

    titles = ['Labels', 'Data', 'Images']

    pies = [go.Pie(
        labels=[label for label, value in zip(labels, values) if value > 0],
        values=[value for value in values if value > 0],
        marker=dict(colors=[colors[label] for label, value in zip(labels, values) if value > 0],
                    line=dict(color='#181818', width=0.002 * VW)),
        hoverinfo='label + value',
        textinfo='text',
        text=[f'{(value / sum(values)) * 100:.3g}%' if value > 0 else '' for value in values],
        hole=.88,
        sort=False,
        opacity=1,
        title=title,
        titlefont=dict(size=0.012 * VW, color='#999', family='Arial'),
        outsidetextfont=dict(size=0.009 * VW, color='#F5F5F5', family='Arial')
    ) for labels, values, colors, title in
        zip([annotations_labels, backgrounds_labels, images_labels],
            [annotations_pie, backgrounds_pie, images_pie],
            [annotations_colors, backgrounds_colors, images_colors],
            titles)]

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[None, {'type': 'domain'}],
               [{'type': 'domain'}, None],
               [None, {'type': 'domain'}]]
    )

    fig.add_trace(pies[0], row=1, col=2)
    fig.update_traces(domain=dict(x=[0.5, 0.9], y=[0.6, 1]), row=1, col=2)

    fig.add_trace(pies[1], row=2, col=1)
    fig.update_traces(domain=dict(x=[0.1, 0.5], y=[0.3, 0.7]), row=2, col=1)

    fig.add_trace(pies[2], row=3, col=2)
    fig.update_traces(domain=dict(x=[0.5, 0.9], y=[0, 0.4]), row=3, col=2)

    fig.update_layout(
        title='General  Overview',
        title_font=dict(family="Arial", size=18, color='#F5F5F5'),
        title_x=0,
        title_y=0.95,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="v",  # Place the legend horizontally below the chart
            yanchor="bottom",
            y=0.45,
            xanchor="right",
            x=1.2,
            font=dict(size=0.0085 * VW, color='#F5F5F5', family='Arial')
        ),
        hoverlabel=dict(font=dict(size=0.01 * VW)),
        autosize=False,
        height=0.8 * VH,
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0.05 * VH,  # bottom margin
            t=0,  # top margin
            pad=0  # padding
        ),
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_overlap_pie(labels, values, width, height, colors=None,
                     title=None, title_width=8, display_counts=True):

    total = sum(values)
    text = [value if value > 0 else '' for value in values]
    hover_info = 'label + percent'

    if not display_counts:
        percentages = [(value / total) * 100 for value in values]
        text = [f'{percentage:.2g}%' if percentage > 0 else '' for percentage in percentages]
        hover_info = 'label + value'

    fig = go.Figure([go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#181818', width=0.02 * width)),
        textfont=dict(size=0.01 * VW),
        hoverinfo=hover_info,  # Display label and percentage on hover
        textinfo='text',  # Display actual values on the pie chart
        text=text,
        hole=.3,
        sort=False,
        opacity=0.9,
    )])

    fig.update_layout(
        # Set the background color to fully transparent
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(font=dict(size=0.01 * VW)),
        autosize=False,
        width=width,
        height=height,
        margin=go.layout.Margin(
            l=0.01 * VW,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0.02 * VH,  # top margin
            pad=0  # padding
        ),
        showlegend=False
    )

    st.plotly_chart(fig, config={'displayModeBar': False,
                                 'modeBarButtonsToRemove': ['toImage', 'sendDataToCloud', 'toggleHover']})

    if title:
        st.markdown(f"<p style='text-align: center; width: {title_width}vw; font-family: Arial, sans-serif; "
                    f"font-size: 1vw; font-weight: bold; color: #666'>{title}</p>",
                    unsafe_allow_html=True)


def plot_classes(annotation_stats):
    class_counts = annotation_stats['class_name'].value_counts().sort_values(ascending=False)
    df_instances = pd.DataFrame({'Class': class_counts.index, 'Instances': class_counts.values})

    image_counts = annotation_stats.groupby('class_name')['filename'].nunique()
    df_images = pd.DataFrame({'Class': image_counts.index, 'Images': image_counts.values})

    # Merge the two dataframes on the 'Class' column
    df_merged = pd.merge(df_instances, df_images, on='Class')

    # Create a new dataframe suitable for px
    df_plot = pd.melt(df_merged, id_vars=['Class'], value_vars=['Instances', 'Images'],
                      var_name='Metric', value_name='Count')

    max_counts = df_plot.groupby('Metric')['Count'].max()

    # Calculate the 10% threshold for each group
    thresholds = max_counts * 0.1

    fig = go.Figure()

    color_map_normal = {
        'Instances': '#33D113',  # Soft Blue
        'Images': '#B113D1',  # Soft Green
    }

    # Loop through each unique metric in your DataFrame
    for metric in df_plot['Metric'].unique():
        # Filter the DataFrame for each metric
        filtered_df = df_plot[df_plot['Metric'] == metric]
        marker_color = np.where(filtered_df['Count'] < thresholds[metric], '#D62728',
                                color_map_normal[metric]).tolist()

        # Add a bar trace only if there are relevant data points for this metric
        if not filtered_df.empty:
            fig.add_trace(go.Bar(
                x=filtered_df['Count'],
                y=filtered_df['Class'],
                name=metric,
                orientation='h',
                text=filtered_df['Count'],
                textposition='auto',
                marker_color=marker_color
            ))

    # Update trace text font size for bar labels
    fig.update_traces(textfont=dict(size=0.01 * VW, color='#F5F5F5', family='Arial'),
                      textangle=0, textposition="outside", cliponaxis=False)

    # Update axes titles font size
    fig.update_xaxes(title_text='Count', title_font=dict(size=0.011 * VW), tickfont=dict(size=0.01 * VW, color='#999'))
    fig.update_yaxes(title_text='Class', title_font=dict(size=0.011 * VW), tickfont=dict(size=0.01 * VW, color='#999'),
                     showgrid=False)

    # Hide grid for X-axis as well
    fig.update_yaxes(type='category', showgrid=False)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=0.73 * VW,
        height=0.4 * VH,
        margin=dict(
            l=0.047 * VW,  # left margin
            r=0.01 * VW,  # right margin
            b=0.093 * VH,  # bottom margin
            t=0.0093 * VH,  # top margin
        ),
        font=dict(
            size=0.013 * VW,  # Font size of the text inside markers
            family='Arial',  # Font family of the text inside markers
        ),
        legend=dict(x=-0.4, y=0, font=dict(size=0.009 * VW, color='#F5F5F5', family='Arial')),
        xaxis_range=[0, df_plot['Count'].max() * 1.1],
        bargap=0.1,  # Adjust bar width here
        bargroupgap=0.25  # Adjust group gap as needed
    )

    fig.update(layout_coloraxis_showscale=False)

    # Update hover label font size
    fig.update_layout(
        hoverlabel=dict(
            namelength=-1,
            font=dict(
                size=0.01 * VW,  # Change this to the desired font size
            ),
        ),
        legend=dict(title=None)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displaylogo': False,
                                                           'displayModeBar': False,
                                                           'scrollZoom': True})



def plot_co_occurrences(annotation_stats):
    occurrences = pd.crosstab(annotation_stats['filename'], annotation_stats['class_name'])
    binary = occurrences.map(lambda x: 1 if x > 0 else 0)

    self_occurrences = np.sum((occurrences > 1), axis=0)
    co_occurrences = binary.T.dot(binary)

    np.fill_diagonal(co_occurrences.values, self_occurrences)

    image_counts = annotation_stats.groupby('class_name')['filename'].nunique().loc[co_occurrences.index]
    total_matrix = np.outer(image_counts, image_counts)

    co_occurrences_normalized = co_occurrences / total_matrix
    co_occurrences_normalized = co_occurrences_normalized/ co_occurrences_normalized.values.sum()

    co_occurrences = co_occurrences.iloc[::-1, :]
    co_occurrences_normalized = co_occurrences_normalized.iloc[::-1, :]

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=co_occurrences.values,
        x=co_occurrences.columns,
        y=co_occurrences.index,
        colorscale=['rgba(0,0,0,0)'] + px.colors.sequential.Electric,
        visible=True,  # Show this trace by default
        name="Total",
        hovertemplate="%{z}<br><br>x: %{x}<br>y: %{y}<extra></extra>",
        hoverlabel=dict(align='left')
    ))

    # Add trace for Normalized co-occurrences
    fig.add_trace(go.Heatmap(
        z=co_occurrences_normalized.values,
        x=co_occurrences_normalized.columns,
        y=co_occurrences_normalized.index,
        colorscale=['rgba(0,0,0,0)'] + px.colors.sequential.Electric,
        visible=False,  # Hide this trace initially
        name="Normalized",
        hovertemplate="%{z:.2g}<br><br>x: %{x}<br>y: %{y}<extra></extra>",
        hoverlabel=dict(align='left')
    ))

    # Define the layout and dropdown menu
    fig.update_layout(
        coloraxis_colorbar=dict(title="Co-occurrence Frequency"),
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Total",
                        method="update",
                        args=[{"visible": [True, False]}]  # Show Total and hide Normalized
                    ),
                    dict(
                        label="Normalized",
                        method="update",
                        args=[{"visible": [False, True]}]  # Hide Total and show Normalized
                    )
                ],
                direction="down",
                pad={"r": 0.01 * VW, "t": 0},
                showactive=True,
                x=0.78,
                xanchor="left",
                y=1.2,
                yanchor="top",
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#909090', size=0.008 * VW),
                bordercolor='#909090'
            )
        ],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            size=0.008 * VW,  # Font size of the text inside markers
            family='Arial',  # Font family of the text inside markers
        ),
        legend=dict(x=-0.4, y=0, font=dict(size=0.006 * VW, color='#F5F5F5', family='Arial')),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        hoverlabel=dict(
            namelength=-1,
            font=dict(
                size=0.009 * VW,  # Change this to the desired font size
            ),
        ),
        height=0.41 * VH
    )

    fig.update_xaxes(title_text='', title_font=dict(size=0.01 * VW), tickfont=dict(size=0.01 * VW, color='#999'))
    fig.update_yaxes(title_text='', title_font=dict(size=0.01 * VW), tickfont=dict(size=0.01 * VW, color='#999'),
                     showgrid=False)

    fig.update_layout(title='Co-occurrence Matrix', title_font=dict(family="Arial", size=20, color='#F5F5F5'))
    st.plotly_chart(fig, use_container_width=True, config={'displaylogo': False,
                                                           'displayModeBar': False,
                                                           'scrollZoom': True})


class PlotAnnotations:
    def __init__(self, annotation_stats, plot_type, colormap):
        self.scatter_opacity = min(0.4, 1000 / annotation_stats.shape[0])

        self.colormap = colormap
        self.annotation_stats = annotation_stats
        self.plot_type = plot_type
        self.plot_config = {'displaylogo': False,
                            'displayModeBar': False,
                            'scrollZoom': True}

    @staticmethod
    def update(fig, x_title=None, y_title=None, width=0.21*VW, height=0.32 * VH, font_size=0.013 * VW):
        fig.update_layout(
            autosize=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            width=width,
            height=height,
            margin=dict(
                l=0,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=0.02 * VH,  # top margin
                pad=0.02 * VH  # padding
            ),
            font=dict(
                size=font_size,  # Font size of the text inside markers
                family='Arial',  # Font family of the text inside markers
            ),
            showlegend=False,
            xaxis_title=x_title,
            yaxis_title=y_title,
            hoverlabel=dict(  # Add this line
                font_size=0.008 * VW,  # Change the size as needed
            ),
        )

    def centers(self):
        if self.plot_type == 'Scatter':
            fig = px.scatter(self.annotation_stats, x="x_center", y="y_center", color='class_name',
                             opacity=self.scatter_opacity, color_discrete_map=self.colormap)

        else:
            fig = px.density_heatmap(self.annotation_stats, x='x_center', y='y_center', nbinsx=10,
                                     histnorm='percent', histfunc='count',
                                     color_continuous_scale=['rgba(0,0,0,0)'] + px.colors.sequential.thermal)

        self.update(fig, 'X_CENTER', 'Y_CENTER')

        fig.update_xaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])
        fig.update_yaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])

        st.plotly_chart(fig, use_container_width=False, config=self.plot_config)

    def sizes(self):
        if self.plot_type == 'Scatter':
            fig = px.scatter(self.annotation_stats, x="width", y="height", color='class_name',
                             opacity=self.scatter_opacity, color_discrete_map=self.colormap)
        else:
            fig = px.density_heatmap(self.annotation_stats, x='width', y='height', nbinsx=10,
                                     histnorm='percent', histfunc='count',
                                     color_continuous_scale=['rgba(0,0,0,0)'] + px.colors.sequential.thermal)

        self.update(fig, 'WIDTH', 'HEIGHT')
        fig.update_xaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])
        fig.update_yaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])

        st.plotly_chart(fig, use_container_width=False, config=self.plot_config)

    def boxes(self):
        fig = go.Figure()
        rectangles = self.annotation_stats.groupby(['class_name', 'size'], observed=False)[['width', 'height']].median().reset_index()

        for _, row in rectangles.iterrows():
            x_center = random.uniform(0.3, 0.7)
            y_center = random.uniform(0.3, 0.7)
            x0 = x_center - row['width'] / 2
            x1 = x_center + row['width'] / 2
            y0 = y_center - row['height'] / 2
            y1 = y_center + row['height'] / 2
            fig.add_shape(
                type="rect",
                xref="x",
                yref="y",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(
                    color='black',
                    width=0.0016 * VW,
                ),
                fillcolor=self.colormap[row['class_name']],
                opacity=0.5,

            )
            fig.add_trace(
                go.Scatter(
                    x=[x0, x0, x1, x1, 0],
                    y=[y0, y1, y1, y0, 0],
                    fill="toself",
                    mode='lines',
                    hoverinfo='text',
                    text=f"{row['size'].capitalize()} {row['class_name']}",
                    hoverlabel=dict(
                        font_size=0.008 * VW,
                        font_family='Rockwell',
                        font_color='white'
                    ),
                    opacity=0
                )
            )

        self.update(fig, 'X', 'Y')
        fig.update_yaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])
        fig.update_xaxes(showgrid=False, showticklabels=False, title_standoff=0.008 * VW, autorange=False, range=[0, 1])

        st.plotly_chart(fig, use_container_width=False, config=self.plot_config)

    def distribution(self):
        if self.annotation_stats['class_name'].nunique() > 1:
            fig = px.histogram(self.annotation_stats, x="box_size", nbins=20, color='class_name',
                               color_discrete_map=self.colormap)

            # Add dropdown menu to the histogram using Plotly update buttons
            fig.update_layout(
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(label="Counts",
                                 method="update",
                                 args=[{"barnorm": 'counts'}, {"barnorm": 'counts'}]),
                            dict(label="Fraction",
                                 method="update",
                                 args=[{"barnorm": 'fraction'}, {"barnorm": 'fraction'}])
                        ]),
                        direction="down",
                        pad={"r": 0.01 * VW, "t": 0},
                        showactive=False,
                        x=-0.3,
                        xanchor="left",
                        y=0.95,
                        yanchor="top",
                        bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#909090', size=0.008 * VW),
                        bordercolor='#909090'
                    ),])

        else:
            fig = px.histogram(self.annotation_stats, x="box_size", nbins=20, color='class_name',
                               color_discrete_map=self.colormap, marginal='violin')

        self.update(fig, 'BOX SIZE', 'FRACTION', width=0.365 * VW, height=0.43 * VH)

        fig.update_xaxes(showgrid=False,  title_standoff=0.015 * VW)
        fig.update_yaxes(showgrid=False,  title_standoff=0.013 * VW)

        fig.update_traces(marker_line_width=0.0005 * VW, marker_line_color="black")

        fig.update_layout(
            margin=dict(
                l=0,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=0.04 * VH,  # top margin

            ))

        if self.annotation_stats['class_name'].nunique() > 1:
            fig.update_layout(
                legend=dict(
                    orientation="v",  # Place the legend horizontally below the chart
                    y=0.1,
                    x=-0.3,
                    font=dict(
                        family="sans-serif",
                        size=0.007 * VW,  # Adjust font size of the legend
                        color="white",
                    ),
                ),
                showlegend=True)

        st.plotly_chart(fig, config=self.plot_config)

    def counts(self):
        data = self.annotation_stats['size'].value_counts()
        values = data.values
        labels = [label.upper() for label in data.index]

        total = sum(data.values)

        colors = {
            "SMALL": '#E6C419',
            "MEDIUM": '#14B59D',
            "BIG": '#9D14B5'
        }

        relevant_colors = [colors[key] for key in labels]

        text = [value if value > 0 else '' for value in values]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=relevant_colors, line=dict(color='#272727', width=0.005 * VW)),  # Add black outlines for contrast
                    textfont=dict(size=0.011 * VW),
                    hoverinfo='label+percent',  # Display label and percentage on hover
                    textinfo='text',  # Display actual values on the pie chart
                    text=text,
                    hole=.4  # Create a donut chart for a more modern look
                )
            ]
        )
        self.update(fig, height=0.33 * VH)
        fig.update_layout(
            legend=dict(
                orientation="v",  # Place the legend horizontally below the chart
                yanchor="bottom",
                y=0.8,
                xanchor="right",
                x=1.2,
                font=dict(
                    family="sans-serif",
                    size=0.007 * VW,  # Adjust font size of the legend
                    color="white",
                ),
            ),
            annotations=[
                dict(
                    text=str(total),  # The text you want to display
                    showarrow=False,
                    font=dict(size=0.012 * VW, color='gray'),  # Adjust the size as needed
                    x=0.5,
                    y=0.5,
                    xanchor='center',
                    yanchor='middle'
                )],
            showlegend=True,
            margin=dict(
                l=0.016 * VW,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=0.046 * VH,  # top margin
                pad=0  # padding
            ),
        )

        st.plotly_chart(fig, use_container_width=True)


@st.cache_data(show_spinner=False)
def plot_color_distribution(tones, start_x=21, start_y=60, biggest=13,
                            sat_ratio=0.5, n_samples=1000, sampling_factor=5):

    sizes, textures = [], []
    color_cols = [color for (color, _, _) in HUE_RANGES[:-1]]

    for hue, color_col in zip(tones['hue'].unique(), color_cols):
        hue_tones = tones[tones['hue'] == hue]
        summ = hue_tones['count'].sum()
        hue_n_samples = hue_tones.shape[0]

        n_samples = min(hue_n_samples, n_samples)
        n_samples = n_samples // sampling_factor * sampling_factor
        hue_tones['z'] = sat_ratio * hue_tones['sat']/255 + (1 - sat_ratio) * hue_tones['value']/255
        hue_tones = hue_tones.sample(n_samples)
        hue_tones = hue_tones.sort_values('z', ascending=True)
        value_to_sat_ratio = hue_tones['value'].mean() / hue_tones['sat'].mean()

        z = hue_tones['z'].values.reshape(-1, n_samples//sampling_factor)

        # Convert HSV to RGB and then to hexadecimal color
        # noinspection PyTypeChecker
        color_codes = [mcl.rgb2hex(mcl.hsv_to_rgb((hue/180, x, min(1, value_to_sat_ratio * x)))) for x in
                       np.linspace(np.min(z), np.max(z), 11)]
        # Create a 2D array for the z-axis (color intensity in this case)
        # n_samples = hue_tones.shape[0]//sampling_factor
        # z = hue_tones['z'][:n_samples].values.reshape(-1, n_samples // sampling_factor)

        # Create a colorscale as a list of pairs
        colorscale = [(s, c) for s, c in zip(np.linspace(0, 1, 11), color_codes)]

        # Create the contour plot
        fig = go.Figure(data=go.Heatmap(z=z, colorscale=colorscale, zsmooth='best', showscale=False))

        fig.update_layout(
            width=1000,
            height=1000,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',

            showlegend=False)

        fig.update_xaxes(showticklabels=False, showgrid=False, showline=False, ticks='')
        fig.update_yaxes(showticklabels=False, showgrid=False, showline=False, ticks='')

        im_arr = plotly_fig2array(fig)
        planet_texture = get_planet_texture(im_arr)

        sizes.append(summ)
        textures.append(planet_texture)

    # Normalize sizes
    norm_factor = 1.0 / sum(sizes)
    sizes = [size * norm_factor for size in sizes]

    # Create a list of tuples (size, texture, color_col) sorted by size in descending order
    color_size_texture = [(size, texture, color_col) for size, texture, color_col in
                          sorted(zip(sizes, textures, color_cols), reverse=True)]

    biggest_size = color_size_texture[0][0]

    # Draw planets
    for i, (size, texture, color) in enumerate(color_size_texture):
        if size >= biggest_size / 4:
            true_size = biggest / biggest_size * size
            render_html('animations/static_planet.html', uri=get_image_uri(texture), size=true_size, x=start_x,
                        y=start_y, rotation_time=30, planet_name=color, key=f'planet_{color}')

            start_x += true_size / 2 + biggest / 6


class PlotCBS:
    def __init__(self, image_stats, canvas_path, n_segments=5):
        canvas = cv2.imread(canvas_path)
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        canvas = cv2.resize(canvas, (200, 200))

        self.image_stats = image_stats
        self.stacked_canvas = np.tile(canvas, (n_segments, 1))
        self.h, self.w = self.stacked_canvas.shape[:2]

    def get_contrast_distribution(self):
        std_dev = np.std(self.stacked_canvas)

        contrast_values = self.image_stats['overall']['RMS_contrast'].values
        sampled_contrast_values = sorted(np.random.choice(contrast_values, size=self.w, replace=True))

        contrast_array = np.repeat(sampled_contrast_values, self.h, axis=0).reshape(self.w, self.h).T
        contrast_array = np.repeat(contrast_array[:, :, np.newaxis], 3, axis=2)

        contrast_canvas = ((self.stacked_canvas - np.mean(self.stacked_canvas)) / std_dev) * contrast_array + \
                            np.mean(self.stacked_canvas)

        return contrast_canvas

    def get_brightness_distribution(self):
        stacked_canvas_lab = cv2.cvtColor(self.stacked_canvas, cv2.COLOR_RGB2Lab)
        l_channel, a_channel, b_channel = cv2.split(stacked_canvas_lab)

        brightness_values = self.image_stats['overall']['brightness'].values
        sampled_brightness_values = sorted(np.random.choice(brightness_values, size=self.w, replace=True))

        brightness_array = np.repeat(sampled_brightness_values, self.h, axis=0).reshape(self.w, self.h).T * 255/100
        l_channel = l_channel - np.mean(l_channel) + brightness_array
        l_channel = np.clip(l_channel, 0, 255).astype('uint8')

        brightness_canvas_lab = cv2.merge([l_channel, a_channel, b_channel])
        brightness_canvas = cv2.cvtColor(brightness_canvas_lab, cv2.COLOR_Lab2RGB)

        return brightness_canvas

    def get_saturation_distribution(self):
        stacked_canvas_hsv = cv2.cvtColor(self.stacked_canvas, cv2.COLOR_RGB2HSV)
        h_channel, s_channel, v_channel = cv2.split(stacked_canvas_hsv)
        s_mean = s_channel.mean()

        saturation_values = self.image_stats.xs('sat', level=1, axis=1).mean(axis=1).values

        sampled_saturation_values = sorted(np.random.choice(saturation_values, size=self.w, replace=True))

        saturation_array = np.repeat(sampled_saturation_values, self.h, axis=0).reshape(self.w, self.h).T

        s_channel = s_channel / s_mean * saturation_array
        s_channel = np.clip(s_channel, 0, 255).astype('uint8')

        saturation_canvas_hsv = cv2.merge([h_channel, s_channel, v_channel])
        saturation_canvas = cv2.cvtColor(saturation_canvas_hsv, cv2.COLOR_HSV2RGB)

        return saturation_canvas

    @staticmethod
    def postprocess(canvas):
        canvas = np.clip(canvas, 0, 255).astype(np.uint8)
        width = ceil(0.0016 * VW)
        canvas = cv2.copyMakeBorder(
            canvas, width, width, width, width,
            cv2.BORDER_CONSTANT, value=[100, 100, 100])

        return canvas

    def plot(_self):
        contrast_canvas = _self.postprocess(_self.get_contrast_distribution())
        brightness_canvas = _self.postprocess(_self.get_brightness_distribution())
        saturation_canvas = _self.postprocess(_self.get_saturation_distribution())
        neutral_canvas = _self.postprocess(_self.stacked_canvas)

        fig_contrast = px.imshow(contrast_canvas)
        fig_brightness = px.imshow(brightness_canvas)
        fig_saturation = px.imshow(saturation_canvas)
        fig_neutral = px.imshow(neutral_canvas)

        fig = go.Figure()
        fig.add_trace(fig_contrast.data[0])
        fig.add_trace(fig_brightness.data[0])
        fig.add_trace(fig_saturation.data[0])
        fig.add_trace(fig_neutral.data[0])

        fig.update_layout(
            width=0.73 * VW,
            height=0.32 * VH,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(r=0, l=0, t=0.02*VW, b=0),
            showlegend=False,
            hovermode=False)

        fig.update_xaxes(showticklabels=False, showgrid=False, showline=False, ticks='')
        fig.update_yaxes(showticklabels=False, showgrid=False, showline=False, ticks='')

        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=list([
                        dict(label="Saturation",
                             method="update",
                             args=[{"visible": [False, False, True, False]}]),
                        dict(label="Contrast",
                             method="update",
                             args=[{"visible": [True, False, False, False]}]),
                        dict(label="Brightness",
                             method="update",
                             args=[{"visible": [False, True, False, False]}])]),
                    direction='down',
                    active=None,
                    pad={"r": 0.01 * VW},
                    showactive=False,
                    x=-0.1,
                    xanchor="left",
                    y=0.65,
                    yanchor="top",
                    bgcolor='rgb(30,30,30)',
                    font=dict(color='white', size=0.008 * VW),
                    bordercolor='white'
                )
            ]
        )

        st.plotly_chart(fig)


def plot_image_shapes(image_stats):
    data = image_stats['overall'][['height', 'width', 'n_channels']]
    data['type'] = np.where(data['n_channels'] == 3, 'Colored', 'Gray')
    data = data.drop('n_channels', axis=1)

    data = data.value_counts().reset_index()
    data.columns = ['HEIGHT', 'WIDTH', 'TYPE', 'COUNT']

    fig = px.scatter(data, x="WIDTH", y="HEIGHT",
                     size="COUNT", color="TYPE", log_x=True, size_max=0.031 * VW,
                     color_discrete_map={'Colored': 'purple',
                                         'Gray': 'gray'},
                     opacity=0.9
                     )

    fig.update_layout(
        width=0.36 * VW,
        height=0.28 * VH,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(r=0, l=0, t=0, b=0))

    fig.update_traces(mode='markers', marker=dict(sizemode='area', line_width=0.001 * VW, line_color='white'))

    fig.update_xaxes(showticklabels=False, showgrid=False, showline=False, ticks='')
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False, ticks='')

    st.plotly_chart(fig)


def plot_progress_pie(x, total, label='progress', color='red'):
    labels = [label, ' ']
    values = [x, total - x]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.75,
                                 hoverinfo='label+value')])

    fig.update_traces(marker=dict(colors=[color, 'rgba(0,0,0,0)'], line=dict(color='#262626', width=0.005 * VW),
                                  pattern=dict(shape=["x"])),
                      textposition='outside', textinfo='text', sort=False,  hoverlabel_font_size=0.01 * VW)

    # Update the layout of the chart
    fig.update_layout(
        height=0.65 * VH,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=[
            dict(
                text=str(x),  # The text you want to display
                showarrow=False,
                font=dict(size=0.019 * VW, color='gray'),  # Adjust the size as needed
                x=0.5,
                y=0.5,
                xanchor='center',
                yanchor='middle'
            )],
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displaylogo': False,
                                                           'displayModeBar': False,
                                                           'scrollZoom': True})


@st.cache_data(show_spinner=False)
def plot_overlap_box(overlap_stats, colormap, sample_size=5000):

    overlap_stats = overlap_stats[overlap_stats['overlap_size'] > 0]
    if overlap_stats['relate'].nunique() > 1:
        overlap_stats['relate'] = 'All'
    if overlap_stats['relate_with'].nunique() > 1:
        overlap_stats['relate_with'] = 'All'

    overlap_stats_relate = overlap_stats[['relate', 'relate_size', 'overlap_size']]
    overlap_stats_with = overlap_stats[['relate_with', 'with_size', 'overlap_size']]

    overlap_stats_with.columns = ['relate', 'relate_size', 'overlap_size']
    overlap_stats_combined = pd.concat([overlap_stats_relate, overlap_stats_with], axis=0)

    overlap_stats_combined['ratio'] = overlap_stats_combined['overlap_size']/overlap_stats_combined['relate_size'] * 100
    if overlap_stats_combined.shape[0] > sample_size:
        overlap_stats_combined = overlap_stats_combined.sample(sample_size).sort_values('relate', ascending=False)

    fig = px.box(overlap_stats_combined, x="relate", y="ratio", points='all', color='relate',
                 color_discrete_map=colormap)

    fig.update_layout(
        autosize=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=0.35 * VW,
        height=0.35 * VH,
        font=dict(
            size=0.01 * VW,  # Font size of the text inside markers
            family='Arial',  # Font family of the text inside markers
        ),
        showlegend=False,
        xaxis_title=None,
        yaxis_title='Overlap ratio',
        hoverlabel=dict(  # Add this line
            font_size=0.008 * VW,  # Change the size as needed
        ),
        margin=dict(r=0, l=0, t=0, b=0))

    fig.update_xaxes(showgrid=False, title_standoff=0.008 * VW, title_font=dict(size=0.0125 * VW),
                     tickfont=dict(size=0.01 * VW, color='#999'))
    fig.update_yaxes(showgrid=False, title_standoff=0.008 * VW, title_font=dict(size=0.0125 * VW),
                     tickfont=dict(size=0.01 * VW, color='#999'))

    fig.update_traces(marker_line_width=0.0005 * VW, marker_line_color="black")

    st.plotly_chart(fig, use_container_width=True)


def plot_overlap(overlap_stats, matching_dict, circle1_name,
                 circle2_name, colormap, n_cases, n_images, path):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6])

    n_clusters = n_cases
    if overlap_stats[overlap_stats['overlap_size'] > 0].shape[0] > 0:
        n_clusters -= 1

    overlap_stats['relate_overlap_ratio'] = overlap_stats['overlap_size'] / overlap_stats['relate_size']
    overlap_stats['with_overlap_ratio'] = overlap_stats['overlap_size'] / overlap_stats['with_size']

    overlap_stats = overlap_stats.fillna(0)  # in case of 0/0 division

    if circle1_name == circle2_name:
        clustering_data = overlap_stats[overlap_stats['overlap_size'] > 0][['relate_overlap_ratio']]
        centroids_init = np.linspace(0, 1, n_clusters).reshape(-1, 1)
    else:
        clustering_data = overlap_stats[overlap_stats['overlap_size'] > 0][['relate_overlap_ratio', 'with_overlap_ratio']]
        centroids_init = generate_proportional_centroids(n_clusters)

    km = KMeans(n_clusters=n_clusters, init=centroids_init)
    km.fit(clustering_data)

    overlap_stats['case'] = np.zeros(overlap_stats.shape[0])
    overlap_stats['case'][overlap_stats['overlap_size'] > 0] = np.array(km.labels_) + 1

    case_counts = overlap_stats['case'].value_counts()
    slider_range = case_counts.index.tolist()
    labels = [f'case {i}' for i in range(1, n_cases + 1)]
    labels_images = []
    for i in labels:
        labels_images.append(i)
        labels_images.extend([''] * (n_images-1))

    overlaps = []
    for i in slider_range:
        relevant_stats = overlap_stats[overlap_stats['case'] == i]

        selected_pairs = relevant_stats[relevant_stats['filename'].isin(matching_dict.keys())].sample(n_images, replace=True)
        selected_pairs['image_filepath'] = selected_pairs['filename'].apply(
            lambda x: os.path.join(path, 'images', matching_dict[x]))

        circle1_size = np.median(relevant_stats['relate_size'])
        circle2_size = np.median(relevant_stats['with_size'])

        radius1 = np.sqrt(circle1_size / np.pi)
        radius2 = np.sqrt(circle2_size / np.pi)

        circle_overlap_size = np.median(relevant_stats['overlap_size'])
        circle_overlap_size = min(circle1_size, circle2_size, circle_overlap_size)

        # Initial guess for the distance
        initial_guess = radius1 + radius2 - math.sqrt(circle_overlap_size)
        distance = fsolve(solve_distance, initial_guess, args=(radius1, radius2, circle_overlap_size))[0]

        # Define the centers of the circles
        center1 = (0, 0)
        center2 = (distance, 0)

        # Calculate the overlap center
        overlap_center_x = (center1[0] * radius2 + center2[0] * radius1) / (radius1 + radius2)
        overlap_center_y = (center1[1] * radius2 + center2[1] * radius1) / (radius1 + radius2)

        theta = np.linspace(0, 2 * np.pi, 100)

        x1 = center1[0] + radius1 * np.cos(theta)
        y1 = center1[1] + radius1 * np.sin(theta)

        x2 = center2[0] + radius2 * np.cos(theta)
        y2 = center2[1] + radius2 * np.sin(theta)

        x3 = overlap_center_x + 0.02 * np.cos(theta)
        y3 = overlap_center_y + 0.02 * np.sin(theta)

        circle1_overlap = math.ceil(circle_overlap_size / circle1_size * 100)
        circle2_overlap = math.ceil(circle_overlap_size / circle2_size * 100)

        relevant_instances_ratio = round(relevant_stats.shape[0] / overlap_stats.shape[0] * 100, 1)
        if relevant_instances_ratio == 0:
            relevant_instances_ratio = '< 0.1'

        overlap_text = ("<span style='font-weight:bold;font-size:25px'>Overlap</span><br><br>"
                        "<span style='font-weight:bold;font-size:18px;color:{}'>{}</span>:  {}%<br>"
                        "<span style='font-weight:bold;font-size:18px;color:{}'>{}</span>:  {}%").format(colormap[circle1_name],
                                                                         circle1_name.capitalize(),
                                                                         circle1_overlap, colormap[circle2_name],
                                                                         circle2_name.capitalize(), circle2_overlap)
        overlaps.append(circle1_overlap)
        circle1 = go.Scatter(x=x1, y=y1, mode='markers', fill='toself',
                             fillcolor=colormap[circle1_name],
                             opacity=0.8, line=dict(color='black', width=1),
                             hoverinfo='none', visible=False, showlegend=False)

        circle2 = go.Scatter(x=x2, y=y2, mode='markers', fill='toself',
                             fillcolor=colormap[circle2_name],
                             opacity=0.8, line=dict(color='black', width=1),
                             hoverinfo='none', visible=False, showlegend=False)

        overlap = go.Scatter(x=x3, y=y3, mode='lines', fill='toself',
                             fillcolor='black',
                             opacity=0, line=dict(color='black', width=3),
                             hoverinfo='text', text=overlap_text, visible=False, showlegend=False)

        fig.add_annotation(x=center1[0], y=center1[1], text=circle1_name.upper(),
                           showarrow=False, visible=False,
                           font=dict(color="black", size=max(1, radius1 / (radius2 + radius1) * VW / 40)))

        fig.add_annotation(x=center2[0], y=center2[1], text=circle2_name.upper(),
                           showarrow=False, visible=False,
                           font=dict(color="black", size=max(1, radius2 / (radius2 + radius1) * VW / 40)))

        fig.add_annotation(x=distance/2, y=max(radius1, radius2) + 0.02, visible=False,
                           showarrow=False, font=dict(color="white", size=0.01 * VW),
                           text=f'{relevant_stats.shape[0]} relations ({relevant_instances_ratio}%)')

        fig.add_traces([circle1, circle2, overlap], rows=[1, 1, 1], cols=[1, 1, 1])

        # Add the image trace to the second subplot
        for (_, pair) in selected_pairs.iterrows():
            img = cv2.imread(pair.image_filepath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cropped_img, pair = crop_aggregate_box(img, pair, square=pair.overlap_size == 0, padding=0.1)

            image_trace = px.imshow(cropped_img).data[0]
            image_trace.update(visible=False, hovertemplate=None, hoverinfo='skip')
            fig.add_trace(image_trace, row=1, col=2)

            relate_x_rect, relate_y_rect = get_rect_vertices(cropped_img, pair.relate_x, pair.relate_y,
                                                             pair.relate_w, pair.relate_h)

            with_x_rect, with_y_rect = get_rect_vertices(cropped_img, pair.with_x, pair.with_y,
                                                         pair.with_w, pair.with_h)

            box1 = go.Scatter(
                    x=relate_x_rect,
                    y=relate_y_rect,
                    mode='lines',
                    line=dict(color=hex_to_rgba(colormap[circle1_name], alpha=1, factor=1), width=2),
                    fill='toself',  # This fills the area inside the lines
                    fillcolor=hex_to_rgba(colormap[circle1_name], alpha=0.25, factor=0.5),  # Fill color with opacity
                    name=circle1_name,
                    visible=False,
                    hoverinfo='text',
                    text=circle1_name
                )

            box2 = go.Scatter(
                    x=with_x_rect,
                    y=with_y_rect,
                    mode='lines',
                    line=dict(color=hex_to_rgba(colormap[circle2_name], alpha=1, factor=1), width=2),
                    fill='toself',  # This fills the area inside the lines
                    fillcolor=hex_to_rgba(colormap[circle2_name], alpha=0.25, factor=0.5),  # Fill color with opacity
                    name=circle2_name,
                    visible=False,
                    hoverinfo='text',
                    text=circle2_name
                )

            boxes = [box1, box2]
            if pair.relate_size < pair.with_size:
                boxes = boxes[::-1]

            fig.add_traces(boxes, rows=[1, 1], cols=[2, 2])

    # Make the first set of traces visible
    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True
    fig.data[3].visible = True
    fig.data[4].visible = True
    fig.data[5].visible = True
    fig.layout.annotations[0].visible = True
    fig.layout.annotations[1].visible = True
    fig.layout.annotations[2].visible = True

    steps = []
    image_steps = []

    for i in range(len(slider_range)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"annotations": []}],
            label=labels[i]
        )
        step["args"][0]["visible"][i * (3 + n_images*3)] = True
        step["args"][0]["visible"][i * (3 + n_images*3) + 1] = True
        step["args"][0]["visible"][i * (3 + n_images*3) + 2] = True
        step["args"][0]["visible"][i * (3 + n_images*3) + 3] = True  # Update the image visibility
        step["args"][0]["visible"][i * (3 + n_images*3) + 4] = True  # Update the image visibility
        step["args"][0]["visible"][i * (3 + n_images*3) + 5] = True  # Update the image visibility

        annotation1 = deepcopy(fig.layout.annotations[i * 3])
        annotation2 = deepcopy(fig.layout.annotations[i * 3 + 1])
        annotation3 = deepcopy(fig.layout.annotations[i * 3 + 2])

        annotation1.visible = True
        annotation2.visible = True
        annotation3.visible = True

        step["args"][1]["annotations"] = [annotation1, annotation2, annotation3]
        steps.append(step)

        for j in range(n_images):
            image_step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)},
                      {"annotations": []}],
                label=labels_images[i*n_images + j]
            )

            image_step["args"][0]["visible"][i * (3 + n_images*3)] = True
            image_step["args"][0]["visible"][i * (3 + n_images*3) + 1] = True
            image_step["args"][0]["visible"][i * (3 + n_images*3) + 2] = True
            image_step["args"][0]["visible"][i * (3 + n_images*3) + 3 + 3*j] = True
            image_step["args"][0]["visible"][i * (3 + n_images*3) + 4 + 3*j] = True
            image_step["args"][0]["visible"][i * (3 + n_images*3) + 5 + 3*j] = True

            image_step["args"][1]["annotations"] = [annotation1, annotation2, annotation3]

            image_steps.append(image_step)

    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Overlap: "},
            pad={"t": 50},
            steps=steps,
            ticklen=0,  # Adjust the length of the tick marks
            tickcolor="black",  # Change the color of the tick marks
            font=dict(color="#999", size=18),  # Adjust the font color and size of the slider labels
            x=0.02,  # Adjust the horizontal position of the slider
            y=0.1,  # Adjust the vertical position of the slider
            len=0.34,  # Adjust the length of the slider
            bordercolor='gray',
            bgcolor="black",
            transition={"duration": 500, "easing": "cubic-in-out"},

        ),

        dict(
            active=0,
            currentvalue={"prefix": ""},
            pad={"t": 50},
            steps=image_steps,
            ticklen=3,  # Adjust the length of the tick marks
            tickcolor="white",  # Change the color of the tick marks
            font=dict(color="#999", size=18),  # Adjust the font color and size of the slider labels
            x=0.48,  # Adjust the horizontal position of the slider
            y=0.1,  # Adjust the vertical position of the slider
            len=0.5,  # Adjust the length of the slider,
            bordercolor='gray',
            bgcolor="black",  # Change the background color of the slider
            transition={"duration": 500, "easing": "cubic-in-out"},
        )
    ]

    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.43,
            xanchor="center",  # changed
            x=0.43,
            font=dict(size=0.01 * VW, color='#999')
        ),
        sliders=sliders,
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0),
        height=0.35 * VH,  # Use a fixed height for better control
    )

    fig.update_traces(hoverlabel_font_size=18)  # Adjusted for readability

    fig.update_xaxes(showticklabels=False, showgrid=False, showline=False, ticks='')
    fig.update_yaxes(showticklabels=False, showgrid=False, showline=False, ticks='')

    st.plotly_chart(fig, use_container_width=True, config={'displaylogo': False,
                                                           'displayModeBar': False,
                                                           'scrollZoom': True})


