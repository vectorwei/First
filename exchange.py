import streamlit as st
import requests
import json
import pandas as pd
from streamlit_echarts import st_echarts

st.set_page_config(page_title = "汇率换算器", layout="wide")

data = requests.get("http://papi.icbc.com.cn/icbc/iepa/oproxy/rest/nsexchanges/latest?t=0.42630200733392276").text
huilv = json.loads(data)["data"]

df = pd.DataFrame.from_dict(huilv)

st.sidebar.info("数据来源：中国工商银行")
st.sidebar.table(df[["currencyCHName", "reference"]])

name = df["currencyCHName"].values.tolist()
price = df["reference"].values.tolist()

selection = st.selectbox("请选择一个目标币种", name, key="1")
key = name.index(selection)
st.success("1"+selection+" ≈ "+str(round(float(price[key])/100, 4))+"人民币")
st.info("1人民币"+" ≈ "+str(round(1/(float(price[key])/100), 4))+selection)

option = {
    "title": {
    "text": '人民币与'+selection+"之间的汇率换算关系图",
    "subtext":'数据更新时间：'+ df["publishDate"].values.tolist()[key]+" "+df["publishTime"].values.tolist()[key]
  },
  "xAxis": {
    "type": 'category',
    "data": [selection+" → 人民币", "人民币 → "+selection]
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "data": [str(round(float(price[key])/100, 4)), str(round(1/(float(price[key])/100), 4))],
      "type": 'bar',
      "label": {
        "show": "true",
        "position": 'outside'
      },
      "showBackground": "true",
      "backgroundStyle": {
        "color": 'rgba(180, 180, 180, 0.2)'
      }
    }
  ]
};

st_echarts(options = option, height=500)