import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import joblib
import datetime

st.set_page_config(
    page_title="Tashkent Air Quality Dashboard",
    page_icon="🌿",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(
            135deg,
            #F4F9FF 0%,
            #FFFFFF 50%,
            #F0FAF7 100%
        );
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.75);
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3, p, label {
        color: #243447;
        font-family: 'Inter', sans-serif;
    }

    h1 {
        font-weight: 800 !important;
        letter-spacing: -1.2px;
    }

    h2, h3 {
        font-weight: 700 !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #E1EBF4;
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 5px 20px rgba(48, 82, 120, 0.06);
        transition: all 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 9px 26px rgba(48, 82, 120, 0.11);
    }

    [data-testid="stMetricLabel"] {
        color: #71839A !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #218A98 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }

    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #E4EDF5;
        border-radius: 18px;
        padding: 10px;
        box-shadow: 0 5px 22px rgba(48, 82, 120, 0.045);
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    .section-label {
        color: #2999A6;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .dashboard-caption {
        color: #71839A !important;
        font-size: 0.98rem;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    hr {
        border-color: #DFEAF1 !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    .stSpinner > div {
        border-top-color: #2999A6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label">ENVIRONMENTAL MONITORING</div>',
    unsafe_allow_html=True
)

st.title("🌿 Tashkent Air Quality")

st.markdown(
    '<p class="dashboard-caption">'
    'Historical pollution data, real-time air quality '
    'and AI-powered predictions.'
    '</p>',
    unsafe_allow_html=True
)


URL_DATA = 'https://raw.githubusercontent.com/soliharustamxojayeva11-arch/Data-collection/720c180b1165943f356717d1220bd42684b625ba/data.csv'

try:
    with st.spinner("🌿 Loading historical data..."):
        data = pd.read_csv(URL_DATA)
        data.columns = data.columns.str.strip()

        if 'pm25' not in data.columns and len(data.columns) > 1:
            data.rename(
                columns={data.columns[1]: 'pm25'},
                inplace=True
            )

        data['pm25'] = pd.to_numeric(
            data['pm25'],
            errors='coerce'
        )

        data['date'] = pd.to_datetime(data['date'])
        data = data.dropna(subset=['pm25', 'date'])

    daily_average = (
            data.groupby('date')['pm25']
            .mean()
            .reset_index()
        )

except Exception as e:
    st.error(f"Failed to load data from GitHub. Error: {e}")

    daily_average = pd.DataFrame(
        columns=['date', 'pm25']
    )

    data = pd.DataFrame(
        columns=['date', 'pm25']
    )


if not daily_average.empty:

    fig = px.line(
        daily_average,
        x='date',
        y='pm25',
        title='Historical PM2.5 Concentration',
        labels={
            'date': 'Date',
            'pm25': 'PM2.5 concentration (µg/m³)'
        },
        template='plotly_white'
    )

    fig.update_traces(
        line_color='#2999A6',
        line_width=2,
        fill='tozeroy',
        fillcolor='rgba(41, 153, 166, 0.08)',
        hovertemplate=(
            '%{x|%d %b %Y}<br>'
            'PM2.5: %{y:.1f} µg/m³'
            '<extra></extra>'
        )
    )

    fig.update_layout(
        margin=dict(l=30, r=25, t=65, b=35),
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        hovermode='x unified',
        font=dict(
            family='Inter, sans-serif',
            color='#526579'
        ),
        title=dict(
            font=dict(size=19, color='#243447'),
            x=0.03
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#EAF0F5',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#EAF0F5',
            zeroline=False
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    peak_idx = daily_average['pm25'].idxmax()

    peak_day = daily_average.loc[
        peak_idx, 'date'
    ].strftime('%d.%m.%Y')

    peak_value = (
        f"{round(daily_average.loc[peak_idx, 'pm25'], 1)} µg/m³"
    )

    average_value = (
        f"{round(data['pm25'].mean())} µg/m³"
    )

    cleanest_idx = daily_average['pm25'].idxmin()

    cleanest_day = daily_average.loc[
        cleanest_idx, 'date'
    ].strftime('%d.%m.%Y')

    cleanest_value = (
        f"{round(daily_average.loc[cleanest_idx, 'pm25'], 1)} µg/m³"
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric(
            label='🔺 Peak Daily Level',
            value=peak_value,
            delta=peak_day,
            delta_color="inverse"
        )

    with col2:
        st.metric(
            label='📊 Average Level',
            value=average_value
        )

    with col3:
        st.metric(
            label='🍃 Cleanest Day',
            value=cleanest_value,
            delta=cleanest_day,
            delta_color="normal"
        )

else:
    st.info(
        "📊 Historical charts and metrics will appear here "
        "once the automated collector saves data to data.csv."
    )


st.markdown("---")

st.markdown(
    '<div class="section-label">LIVE MONITORING</div>',
    unsafe_allow_html=True
)

st.subheader("🌤️ Current Atmospheric Conditions")

token = st.secrets['WAQI_TOKEN']
city = 'Tashkent'

url_api = f'https://api.waqi.info/feed/{city}/?token={token}'

try:
    with st.spinner("🌬️ Connecting to WAQI..."):
        response = requests.get(
            url_api,
            timeout=15
        )

        response.raise_for_status()
        data_json = response.json()

    if data_json['status'] == 'ok':
        current_pm = data_json['data']['iaqi']['pm25']['v']
        city_name = data_json["data"]["city"]["name"]

        st.metric(
            label=f'🌬️ Current PM2.5 in {city_name}',
            value=f'{current_pm} µg/m³'
        )

    else:
        st.error(
            'Failed to fetch real-time data from WAQI API'
        )

except Exception as e:
    st.error(f'API Request Error: {e}' )

st.markdown("---")

st.markdown(
    '<div class="section-label">PREDICTIVE ANALYTICS</div>',
    unsafe_allow_html=True
)

st.subheader("🔮 AI Air Quality Prediction")


try:
    with st.spinner("✨ Loading AI model and generating predictions..."):

        model_ml = joblib.load('prophet_model.pkl')

        today = datetime.date.today()

        future_dates = [
            today + datetime.timedelta(days=i)
            for i in range(7)
        ]

        future = pd.DataFrame({
            'ds': future_dates
        })

        forecast = model_ml.predict(future)

        forecast_clean = forecast[
            ['ds', 'yhat']
        ].rename(
            columns={
                'ds': 'date',
                'yhat': 'predicted_pm25'
            }
        )

    fig_forecast = px.line(
        forecast_clean,
        x='date',
        y='predicted_pm25',
        title='Predicted PM2.5 Concentration · Next 7 Days',
        labels={
            'date': 'Forecast Date',
            'predicted_pm25': 'Predicted PM2.5 (µg/m³)'
        },
        template='plotly_white'
    )

    fig_forecast.update_traces(
        line_color='#E9A23B',
        line_width=3,
        line_dash='dash',
        mode='lines+markers',
        marker=dict(
            size=7,
            color='#E9A23B'
        ),
        hovertemplate=(
            '%{x|%d %b %Y}<br>'
            'Predicted PM2.5: %{y:.1f} µg/m³'
            '<extra></extra>'
        )
    )

    fig_forecast.update_layout(
        margin=dict(l=30, r=25, t=65, b=35),
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        hovermode='x unified',
        font=dict(
            family='Inter, sans-serif',
            color='#526579'
        ),
        title=dict(
            font=dict(size=19, color='#243447'),
            x=0.03
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#EAF0F5',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#EAF0F5',
            zeroline=False
        )
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

except Exception as e:
    st.warning(
        f"Could not load the prediction model. Error: {e}"
    )        
