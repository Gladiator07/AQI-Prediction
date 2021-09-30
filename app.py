from aqi_forecast import fetch_future_air_data
import plotly.express as px
import streamlit as st
import pickle
import numpy as np

st.title("AQI Prediction(A project by Toufiq Rahatwilkar)")
st.markdown("---")
st.markdown("#")
from datetime import date, timedelta

def plot_air_data(data,air_contents):
    """
    Plots air content wrt time
    """
    st.info("💡 All the air contents are in micro-gram per meter-cube")
    for air_content in air_contents:
        
        st.subheader(f"{air_content} (µg / m^3) vs time")
        fig = px.line(x=data["time"],y=data[air_content])
        fig.update_layout(
            xaxis_title = "time (24-hour)",
            yaxis_title = f"{air_content}"
        )
        st.plotly_chart(fig)
        st.markdown("---")


def air_content_mean(data):
    """
    Takes the mean of the whole day
    """

    co = (data["co"].mean()) / 1000
    no = data["no"].mean()
    no2 = data["no2"].mean()
    o3 = data["o3"].mean()
    so2 = data["so2"].mean()
    pm2_5 = data["pm2_5"].mean()
    pm10 = data["pm10"].mean()
    nh3 = data["nh3"].mean()


    return pm2_5,pm10,no,no2,nh3,co,so2,o3

def compare_aqi(predicted_aqi):

    if predicted_aqi <= 50:
        st.success("Air quality is good, People are no longer exposed to health risk")
        st.markdown("---")
    elif predicted_aqi > 50 and predicted_aqi <=100:
        st.success("Air Quality is moderate, Acceptable air quality for healthy adults but still pose threat to sensitive individual")
        st.markdown("---")

    elif predicted_aqi > 100 and predicted_aqi <=200:
        st.warning("Air Quality is Poor, which can have health issues such as difficulty in breathing")
        st.markdown("---")

    elif predicted_aqi >200 and predicted_aqi <=300:
        st.warning("Air Quality is unhealthy, can provoke health difficulties especially to the young kids and elderly people")
        st.markdown("---")
    
    elif predicted_aqi > 300 and predicted_aqi <=400:
        st.error("Air Quality is severe, may lead to chronic health issues")
        st.markdown("---")
    
    elif predicted_aqi >400:
        st.error("AQI is exceeding 400 is highly unacceptable to human - can lead to premature death")
        st.markdown("---")

model = pickle.load(open("aqi_rf.pkl", 'rb'))



city = st.text_input("Enter the city name: ")

if city:
    data_today, data_first, data_second, data_third, data_fourth, data_fifth, pre_data_first,pre_data_second,pre_data_third, pre_data_fourth, pre_data_fifth = fetch_future_air_data(city)
    if data_today is not None:
        today = date.today()
        today_disp = date.today().strftime("%d-%m-%Y")
        first_day = (today + timedelta(days=1)).strftime("%d-%m-%Y")
        second_day = (today + timedelta(days=2)).strftime("%d-%m-%Y")
        third_day = (today + timedelta(days=3)).strftime("%d-%m-%Y")
        fourth_day = (today + timedelta(days=4)).strftime("%d-%m-%Y")
        fifth_day = (today + timedelta(days=5)).strftime("%d-%m-%Y")

        pre_first_day = (today - timedelta(days=1)).strftime("%d-%m-%Y")
        pre_second_day = (today - timedelta(days=2)).strftime("%d-%m-%Y")
        pre_third_day = (today - timedelta(days=3)).strftime("%d-%m-%Y")
        pre_fourth_day = (today - timedelta(days=4)).strftime("%d-%m-%Y")
        pre_fifth_day = (today - timedelta(days=5)).strftime("%d-%m-%Y")
        


        
        st.sidebar.subheader("Select the date to get the data (for previous 4 days)")
        option = st.sidebar.selectbox("Pick a date", (pre_first_day, pre_second_day, pre_third_day, pre_fourth_day))
        st.sidebar.subheader("Select the date to get the forecast (for next 5 days)")
        option = st.sidebar.selectbox("Pick a date", (today_disp, first_day, second_day, third_day, fourth_day))
        # st.sid
        air_content_to_show = st.sidebar.multiselect("Select the air contents", ("co","no","no2","o3","so2","pm2_5","pm10","nh3"))

        button = st.sidebar.button("Submit")

        if button:
            if option == today_disp:
                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(data_today)

                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for today {today_disp} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(data_today, air_content_to_show)

                
            elif option == first_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(data_first)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for tomorrow {first_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(data_first, air_content_to_show)


            elif option == second_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(data_second)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {second_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(data_second, air_content_to_show)

            elif option == third_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(data_third)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {third_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(data_third, air_content_to_show)

            elif option == fourth_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(data_fourth)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {fourth_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(data_fourth, air_content_to_show)
        
            elif option == pre_first_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(pre_data_first)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {pre_first_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(pre_data_first, air_content_to_show)


            elif option == pre_second_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(pre_data_second)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {pre_second_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(pre_data_second, air_content_to_show)

            elif option == pre_third_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(pre_data_third)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {pre_third_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(pre_data_third, air_content_to_show)

            elif option == pre_fourth_day:

                pm2_5,pm10,no,no2,nh3,co,so2,o3 = air_content_mean(pre_data_fourth)
                predicted_aqi = model.predict(np.array([[pm2_5,pm10,no,no2,nh3,co,so2,o3]]))[0]
                st.subheader(f"The forecasted AQI for {pre_fourth_day} is: **{predicted_aqi:.2f}**")
                st.write("")
                compare_aqi(predicted_aqi)
                plot_air_data(pre_data_fourth, air_content_to_show)
        else:
            pass




