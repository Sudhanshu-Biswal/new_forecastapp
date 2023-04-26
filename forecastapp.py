import io, os, sys, setuptools, tokenize
import streamlit as st
from streamlit import caching
import pandas as pd
import numpy as np

#import pystan
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
import json
from prophet.serialize import model_to_json, model_from_json
import holidays

import altair as alt
import plotly as plt
import plotly.offline as pyoff
import plotly.graph_objs as go
import plotly.figure_factory as ff
import base64
import itertools
from datetime import datetime
import json

st.set_page_config(page_title="Forecast App",
                   initial_sidebar_state="collapsed",
                   page_icon="🔮")

tabs = ["Application", "About"]
page = st.sidebar.radio("Tabs", tabs)


@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner=True)
def load_csv(input):
    #df_input = pd.DataFrame(input)
    df_input = pd.read_csv(input, sep=None, engine='python', encoding='utf-8',
                           parse_dates=True,
                           infer_datetime_format=True)
    return df_input


def prep_data(df):
    df_input = df.rename({date_col: "ds", metric_col: "y"}, errors='raise', axis=1)
    st.markdown("The selected date column is now labeled as **ds** and the values columns as **y**")
    df_input = df_input[['ds', 'y']]
    df_input = df_input.sort_values(by='ds', ascending=True)
    return df_input

df = load_csv(input)
df = prep_data(df)                     
st.dataframe(df)

st.write(df.describe())

