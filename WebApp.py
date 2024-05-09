# a Streamlit web application that refreshes every 2 seconds, displays a counter that increments with each refresh

import streamlit as st
import pandas as pd
import time
from datetime import datetime

t=time.time()
date=datetime.fromtimestamp(t).strftime("%d-%m-%Y")
timestamp=datetime.fromtimestamp(t).strftime("%H:%M-%S")

from streamlit_autorefresh import st_autorefresh
#Initializes an autorefresh counter (count) with an interval of 2000 milliseconds (2 seconds) and a limit of 100 refreshes.
count = st_autorefresh(interval=2000, limit=100, key="NNcounter")

if count == 0:
    st.write("Count is zero")
else:
   st.write(f"Count: {count}")


df=pd.read_csv("Attendance_file/Attendance_"+date+".csv")

st.dataframe(df.style.highlight_max(axis=0))
