import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import altair as alt

# 设置页面配置
st.set_page_config(
    page_title="数据可视化展示平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 3rem !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stSubheader {
        color: #34495e;
        text-align: center;
    }
    .stSidebar {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 页面标题
st.title("📊 高级数据可视化展示")
st.markdown("---")

# 生成示例数据
@st.cache_data
def generate_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-06-30', freq='D')
    base_values = np.sin(np.linspace(0, 4*np.pi, len(dates))) * 50 + 100
    noise = np.random.normal(0, 5, len(dates))
    values = base_values + noise
    
    df = pd.DataFrame({
        '日期': dates,
        '数值A': values,
        '数值B': values * 0.8 + np.random.normal(0, 3, len(dates)),
        '类别': np.random.choice(['类型1', '类型2', '类型3'], len(dates))
    })
    return df

df = generate_data()

# 侧边栏配置
st.sidebar.image("https://www.python.org/static/community_logos/python-logo-generic.svg", width=200)
st.sidebar.title("📊 控制面板")

# 数据筛选
st.sidebar.header("🔍 数据筛选")
date_range = st.sidebar.date_input(
    "选择日期范围",
    value=(df['日期'].min(), df['日期'].max()),
    min_value=df['日期'].min(),
    max_value=df['日期'].max()
)

category = st.sidebar.multiselect(
    "选择类别",
    options=df['类别'].unique(),
    default=df['类别'].unique()
)

# 图表类型选择
chart_type = st.sidebar.selectbox(
    "选择图表类型",
    ["组合图表", "高级分析", "分布分析"]
)

# 数据过滤
mask = (df['日期'].dt.date >= date_range[0]) & (df['日期'].dt.date <= date_range[1])
filtered_df = df[mask & df['类别'].isin(category)]

# 主要内容区域
if chart_type == "组合图表":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 时间序列趋势")
        fig_line = px.line(filtered_df, x='日期', y=['数值A', '数值B'],
                          title='双指标对比',
                          template='plotly_white')
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("🎯 散点分布")
        fig_scatter = px.scatter(filtered_df, x='数值A', y='数值B',
                                color='类别', title='相关性分析',
                                template='plotly_white')
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("📊 类别分布")
        fig_hist = px.histogram(filtered_df, x='类别',
                              color='类别',
                              title='类别统计',
                              template='plotly_white')
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)

        st.subheader("📦 箱线图分析")
        fig_box = px.box(filtered_df, x='类别', y=['数值A', '数值B'],
                        title='数值分布对比',
                        template='plotly_white')
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)

elif chart_type == "高级分析":
    st.subheader("🔄 交互式数据探索")
    
    # 热力图
    pivot_data = filtered_df.pivot_table(
        values='数值A',
        index=filtered_df['日期'].dt.day_name(),
        columns=filtered_df['日期'].dt.month,
        aggfunc='mean'
    )
    
    fig_heatmap = px.imshow(pivot_data,
                           title='数值分布热力图',
                           template='plotly_white')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # 3D散点图
    fig_3d = px.scatter_3d(filtered_df,
                          x='数值A',
                          y='数值B',
                          z=filtered_df['日期'].astype(np.int64),
                          color='类别',
                          title='3D数据可视化')
    st.plotly_chart(fig_3d, use_container_width=True)

else:
    st.subheader("📊 分布分析")
    
    # 小提琴图
    fig_violin = px.violin(filtered_df,
                          x='类别',
                          y='数值A',
                          box=True,
                          points="all",
                          title='数值分布小提琴图')
    st.plotly_chart(fig_violin, use_container_width=True)
    
    # 密度等高线图
    fig_density = px.density_contour(filtered_df,
                                   x='数值A',
                                   y='数值B',
                                   title='密度等高线图')
    fig_density.update_traces(contours_coloring="fill")
    st.plotly_chart(fig_density, use_container_width=True)

# 数据统计信息
st.sidebar.markdown("---")
st.sidebar.header("📊 数据统计")
st.sidebar.write("数据概览：")
st.sidebar.dataframe(filtered_df.describe().round(2), height=300)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Created with ❤️ using Streamlit</p>
        <p>数据更新时间：%s</p>
    </div>
    """ % datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    unsafe_allow_html=True
)