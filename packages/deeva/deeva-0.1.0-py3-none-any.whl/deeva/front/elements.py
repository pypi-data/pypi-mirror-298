from .utils import *
import random
from functools import partial
from pathlib import Path

import streamlit as st
import pandas as pd

from configs import configs
from vis import plot_progress_pie
from utils import render_html


@st.dialog("Confirmation")
def confirmation_dialogue(arg, session_state):
    st.markdown("Are you sure you want to make changes to the source?")

    blank_line()
    _, col1, col2 = st.columns([0.5, 0.25, 0.25])
    with col1:
        if st.button('No', use_container_width=True):
            st.rerun()
    with col2:
        if st.button('Yes', use_container_width=True):
            session_state[arg] = True
            st.rerun()


def box_sizes_table(session_state):
    medium_low = f"{round(session_state['medium_low'], 1)}%"
    medium_high = f"{round(session_state['medium_high'], 1)}%"

    table = pd.DataFrame(dict(
        low=['0%', medium_low, medium_high],
        high=[medium_low, medium_high, '100%']),
        index=['Small', 'Medium', 'Big']
    )

    st.table(table)


def stats_block(label, metrics, n_samples=20, width=26, height=37):
    render_html('styles/stats_block.html', width=width, height=height)

    if f'show_first_board_{label}' not in st.session_state:
        st.session_state[f'show_first_board_{label}'] = True

    with st.form(key=label, clear_on_submit=False):
        col1, _, col2 = st.columns([20, 55, 25])
        with col1:
            st.form_submit_button('⇆', on_click=partial(switch_board, label=label))
        with col2:
            with st.container(border=True):
                st.markdown(f"<span style='font-size: 1vw; font-weight: bold;'>{label}</span>", unsafe_allow_html=True)

        if st.session_state[f'show_first_board_{label}']:

            row1 = st.columns(2)
            row2 = st.columns(2)

            for col, metric_name in zip(row1 + row2, metrics.keys()):
                tile = col.container(border=True)
                tile.metric(metric_name, len(metrics[metric_name]))

        else:
            corrupted = {k: v for k, v in metrics.items() if len(v) > 0}
            for tab, key in zip(st.tabs(corrupted.keys()), corrupted.keys()):
                if key == 'Correct':
                    symbol = '✅'
                else:
                    symbol = '❌'
                with tab:
                    col1, col2 = st.columns([70, 30])
                    with col1:
                        filenames = random.sample(corrupted[key], min(len(corrupted[key]), n_samples))
                        output_text = "<hr style='width:100%;margin-bottom:0.3em;margin-top:0.3em;border-width:2px'>".join(
                            [symbol + Path(filename).name for filename in filenames])
                        st.markdown(f'<div class="scrollable-text">{output_text}</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown(
                            f"<h1 style='text-align: center; color: black; webkit-text-stroke-width: 0.1vw; webkit-text-stroke-color: #FAFAFA;'>{len(metrics[key])}</h1>",
                            unsafe_allow_html=True)


def page_var(key, page_name, session_state):
    return session_state[f'{page_name}_{key}']


def caching_handler(page_name, data, total, session_state):
    _page_var = partial(page_var,
                        page_name=page_name,
                        session_state=session_state)

    # set background
    render_html(
        html_filepath='styles/background.html',
        uri=configs.URI['black_background'])

    col1, col2 = st.columns([0.15, 0.85])
    # use cached stats or not
    col1.toggle(
        label='Use cached',
        key=f'{page_name}_use_cached',
        on_change=reset_input_page_toggles,
        args=[page_name, session_state],
        disabled=data is None)

    col1.divider()

    # sample or use entire dataframe
    col1.toggle(
        label='Sample',
        value=False,
        key=f'{page_name}_sample_randomly',
        disabled=_page_var('use_cached'))

    # sample ratio
    col1.select_slider(
        label='Percentage',
        options=range(5, 101, 5),
        value=10,
        key=f'{page_name}_slider',
        disabled=not _page_var('sample_randomly'))

    col1.divider()

    # to cache collected stats or not
    col1.toggle(
        label='Cache',
        key=f'{page_name}_cache',
        on_change=reset_input_page_toggles,
        args=[page_name, session_state],
        disabled=_page_var('use_cached'))

    # to remove from cache or not
    col1.toggle(
        label='Forget cached',
        key=f'{page_name}_forget_cached',
        on_change=backup,
        args=[f'{page_name}_forget_cached', session_state],
        disabled=_page_var('use_cached') | _page_var('cache'))

    app_gray = not _page_var('cache') or _page_var('use_cached')
    disk_gray = app_gray or _page_var('forget_cached')
    bin_gray = not _page_var('forget_cached')

    render_html(
        html_filepath='animations/slider.html',
        uri=configs.URI['app'],
        x=60,
        y=36,
        size=4,
        label='App',
        key='app',
        scale='gray' if app_gray else 'colored')

    render_html(
        html_filepath='animations/slider.html',
        uri=configs.URI['disk'],
        x=76,
        y=34,
        size=4,
        label='Disk',
        key='disk',
        scale='gray' if disk_gray else 'colored')

    render_html(
        html_filepath='animations/slider.html',
        uri=configs.URI['bin'],
        x=58.5,
        y=53,
        size=10.5,
        label='∅',
        key='bin',
        scale='gray' if bin_gray else 'colored')

    if _page_var('use_cached'):
        render_html(
            html_filepath='animations/arrows.html',
            x=74.2,
            y=39.5,
            size=0.6,
            direction=90,
            key='disk_to_app')

    if _page_var('cache'):
        render_html(
            html_filepath='animations/arrows.html',
            x=74.2,
            y=38.5,
            size=0.6,
            direction=-90,
            key='app_to_disk')

    if _page_var('forget_cached'):
        render_html(
            html_filepath='animations/arrows.html',
            x=80,
            y=50,
            size=0.6,
            direction=40,
            key='cash_to_bin')

    col1.divider()
    if col1.button(
            label="Let's go",
            use_container_width=True,
            disabled=total < 100,
            key=f'{page_name}_go'
    ):
        session_state[f'{page_name}_input_page'] = False
        st.rerun()

    with col2:
        sample_ratio = _page_var('slider') / 100
        sample_size = total
        if _page_var('sample_randomly'):
            sample_size = int(sample_ratio * total)

        session_state[f'{page_name}_sample_size'] = sample_size

        color = '#859e32'
        if _page_var('use_cached'):
            color = 'gray'
            sample_size = total

        _, pie_col = st.columns([0.3, 0.7])
        with pie_col:
            plot_progress_pie(
                x=sample_size,
                total=total,
                label=page_name.capitalize(),
                color=color)

    return session_state
