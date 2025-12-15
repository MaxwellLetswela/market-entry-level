import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="KasiPay Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .positive-change {
        color: #10B981;
        font-weight: bold;
    }
    .negative-change {
        color: #EF4444;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">💰 KasiPay Performance Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Small-Level Analysis for Hyper-Local FinTech Growth</p>', unsafe_allow_html=True)

# Generate synthetic data
def generate_kasipay_data():
    # Market penetration data
    np.random.seed(42)
    n_stalls = 96
    stall_ids = [f"T{i:03d}" for i in range(1, n_stalls + 1)]
    
    payment_methods = ['Cash', 'KasiPay', 'SnapScan', 'Zapper', 'Cash, EFT']
    reasons = ['Verification too difficult', 'Phone too old', "Don't trust apps", 'Need M-Pesa', 'Happy with cash']
    
    market_data = []
    for i, stall_id in enumerate(stall_ids):
        uses_kasipay = i < 24  # 25% market share
        primary = 'Cash'
        secondary = 'KasiPay' if uses_kasipay else np.random.choice(['SnapScan', 'Zapper', 'None', 'None'])
        
        reason = None if uses_kasipay else np.random.choice(reasons, p=[0.4, 0.2, 0.2, 0.15, 0.05])
        
        market_data.append({
            'Stall_ID': stall_id,
            'Primary_Payment_Method': primary,
            'Secondary_Payment_Method': secondary,
            'Uses_KasiPay': uses_kasipay,
            'Reason_For_Not_Using': reason,
            'Daily_Transaction_Count': np.random.randint(5, 100)
        })
    
    market_df = pd.DataFrame(market_data)
    
    # Onboarding funnel data
    funnel_data = {
        'Funnel_Stage': ['App Download', 'Account Created', 'ID Uploaded', 'Profile Verified', 'First Transaction', 'Active User (30-day)'],
        'Users': [500, 350, 180, 120, 110, 84],
        'Drop-off_Count': [0, 150, 170, 60, 10, 26],
        'Drop-off_Rate': [0, 0.30, 0.48, 0.33, 0.08, 0.24]
    }
    funnel_df = pd.DataFrame(funnel_data)
    
    # Review sentiment data
    review_texts = [
        "Low fees are great but the signup was a nightmare. My ID verification failed 3 times.",
        "Love this app! So easy to pay at my local spaza now.",
        "Why can't I use M-Pesa to top up my wallet? Makes no sense. Verification also took 2 days.",
        "Gave up. Too difficult to sign up. Sticking with cash.",
        "Good app. Would be perfect if it worked with M-Pesa.",
        "Verification process needs improvement but otherwise great!",
        "M-Pesa integration please! That's all I ask.",
        "Fast transactions once you're set up. Setup was painful though.",
        "Best app for township payments!",
        "Can't believe how easy it is to pay now. No more cash problems."
    ]
    
    sentiment_scores = [-0.5, 0.9, -0.8, -1.0, 0.7, -0.3, 0.6, 0.3, 0.8, 0.9]
    keywords_verification = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
    keywords_mpesa = [0, 0, 1, 0, 1, 0, 1, 0, 0, 0]
    keywords_fees = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    review_data = {
        'Review_ID': [f'R{i:03d}' for i in range(1, 151)],
        'Date': pd.date_range(start='2024-01-01', periods=150, freq='D'),
        'Rating': np.random.choice([1, 2, 3, 4, 5], 150, p=[0.1, 0.15, 0.2, 0.3, 0.25]),
        'Review_Text': np.random.choice(review_texts, 150),
        'Sentiment_Score': np.random.normal(0.35, 0.5, 150),
        'Keyword_Verification': np.random.choice([0, 1], 150, p=[0.7, 0.3]),
        'Keyword_M-Pesa': np.random.choice([0, 1], 150, p=[0.6, 0.4]),
        'Keyword_Fees': np.random.choice([0, 1], 150, p=[0.95, 0.05])
    }
    
    # Clip sentiment scores
    review_data['Sentiment_Score'] = np.clip(review_data['Sentiment_Score'], -1, 1)
    review_df = pd.DataFrame(review_data)
    
    # Weekly metrics data
    dates = pd.date_range(start='2024-01-01', periods=24, freq='W')
    intervention_week = 13
    
    weekly_users = []
    weekly_dropoff = []
    weekly_satisfaction = []
    weekly_tickets = []
    
    for week in range(24):
        if week < intervention_week:
            users = 7 + np.random.randn() * 1.5
            dropoff = 0.71 + np.random.randn() * 0.05
            satisfaction = 3.4 + np.random.randn() * 0.2
            tickets = 45 + np.random.randn() * 5
        else:
            users = 13 + np.random.randn() * 1.5
            dropoff = 0.41 + np.random.randn() * 0.03
            satisfaction = 4.1 + np.random.randn() * 0.15
            tickets = 20 + np.random.randn() * 3
            
        weekly_users.append(max(5, users))
        weekly_dropoff.append(max(0.3, min(0.8, dropoff)))
        weekly_satisfaction.append(max(2.5, min(5, satisfaction)))
        weekly_tickets.append(max(10, tickets))
    
    weekly_df = pd.DataFrame({
        'Week': range(1, 25),
        'Date': dates,
        'Weekly_New_Active_Users': weekly_users,
        'Onboarding_Dropoff_Rate': weekly_dropoff,
        'Avg_Customer_Satisfaction': weekly_satisfaction,
        'Support_Tickets_Onboarding': weekly_tickets
    })
    
    return market_df, funnel_df, review_df, weekly_df

# Load data
market_df, funnel_df, review_df, weekly_df = generate_kasipay_data()

# Calculate KPIs
market_share = (market_df['Uses_KasiPay'].sum() / len(market_df)) * 100
avg_sentiment = review_df['Sentiment_Score'].mean()
verification_complaints = review_df['Keyword_Verification'].sum()
mpesa_requests = review_df['Keyword_M-Pesa'].sum()

# Pre/Post metrics
pre_avg_users = weekly_df.iloc[:12]['Weekly_New_Active_Users'].mean()
post_avg_users = weekly_df.iloc[12:]['Weekly_New_Active_Users'].mean()
pre_avg_dropoff = weekly_df.iloc[:12]['Onboarding_Dropoff_Rate'].mean()
post_avg_dropoff = weekly_df.iloc[12:]['Onboarding_Dropoff_Rate'].mean()
pre_avg_satisfaction = weekly_df.iloc[:12]['Avg_Customer_Satisfaction'].mean()
post_avg_satisfaction = weekly_df.iloc[12:]['Avg_Customer_Satisfaction'].mean()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3082/3082383.png", width=100)
    st.title("KasiPay Analytics")
    st.markdown("---")
    
    selected_view = st.selectbox(
        "Dashboard View",
        ["Overview", "Market Analysis", "Onboarding Funnel", "Customer Feedback", "Impact Analysis"]
    )
    
    st.markdown("---")
    st.markdown("### Key Dates")
    st.info("📅 **Onboarding Improved:** March 25, 2024")
    st.warning("🎯 **Target Market:** Township Informal Traders")
    
    st.markdown("---")
    st.markdown("### Data Summary")
    st.metric("Total Stalls Surveyed", f"{len(market_df):,}")
    st.metric("Total Reviews Analyzed", f"{len(review_df):,}")
    st.metric("Weeks of Data", "24")

# Main content based on selected view
if selected_view == "Overview":
    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Market Share",
            f"{market_share:.1f}%",
            f"{market_share:.1f}% of target stalls"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Onboarding Drop-off",
            f"{post_avg_dropoff:.1%}",
            f"{(pre_avg_dropoff - post_avg_dropoff):.1%}",
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        user_change = ((post_avg_users - pre_avg_users) / pre_avg_users) * 100
        st.metric(
            "Weekly New Users",
            f"{post_avg_users:.0f}",
            f"{user_change:.0f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        sat_change = ((post_avg_satisfaction - pre_avg_satisfaction) / 5) * 100
        st.metric(
            "Customer Satisfaction",
            f"{post_avg_satisfaction:.1f}/5.0",
            f"{sat_change:.0f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    # Quick charts
    st.markdown("---")
    st.subheader("📊 Performance at a Glance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Market share pie chart
        fig = px.pie(
            values=[market_share, 100-market_share],
            names=['KasiPay Users', 'Non-Users'],
            title=f'Market Share: {market_share:.1f}%',
            color_discrete_sequence=['#667eea', '#e2e8f0']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        sentiment_counts = pd.cut(
            review_df['Sentiment_Score'],
            bins=[-1, -0.5, 0, 0.5, 1],
            labels=['Very Negative', 'Negative', 'Positive', 'Very Positive']
        ).value_counts()
        
        fig = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            title='Customer Sentiment Distribution',
            color=sentiment_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(xaxis_title='Sentiment', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)

elif selected_view == "Market Analysis":
    st.header("📍 Market Analysis")
    
    col1, col2 = st.columns(2)
    
with col1:
    # Key Insights
     st.markdown("---")
    st.subheader("🎯 Key Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Top Issue Found: Verification Process**
        - 71% drop-off during ID verification (now 41%)
        - Top negative keyword: "verification"
        - Most frequent support ticket topic
        """)
        
        st.success("""
        **Immediate Action Taken:**
        1. Simplified ID upload process
        2. Added real-time validation
        3. Reduced verification time from 2 days to 2 hours
        """)
    
    with col2:
        st.warning("""
        **Top Feature Request: M-Pesa Integration**
        - Requested in 42% of all reviews
        - Critical for user retention
        - Key to expanding market reach
        """)
        
        st.info("""
        **Strategic Response:**
        1. Created partnership guide for M-Pesa
        2. Initiated technical feasibility study
        3. Estimated implementation: Q3 2024
        """)
    
    
        # Payment methods breakdown
        payment_counts = {}
        for method in ['KasiPay', 'SnapScan', 'Zapper', 'EFT']:
            count = market_df.apply(
                lambda x: method in str(x['Secondary_Payment_Method']) or 
                         method in str(x['Primary_Payment_Method']), 
                axis=1
            ).sum()
            payment_counts[method] = count
        
        payment_counts['Cash Only'] = len(market_df) - sum(payment_counts.values())
        
        fig = px.bar(
            x=list(payment_counts.keys()),
            y=list(payment_counts.values()),
            title='Payment Methods Used by Stalls',
            color=list(payment_counts.values()),
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_title='Payment Method', yaxis_title='Number of Stalls')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Reasons for not using KasiPay
        reasons_df = market_df[market_df['Reason_For_Not_Using'].notna()]
        reason_counts = reasons_df['Reason_For_Not_Using'].value_counts()
        
        fig = px.pie(
            values=reason_counts.values,
            names=reason_counts.index,
            title='Top Barriers to Adoption',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Stalls by transaction volume
    st.subheader("📈 Stalls by Daily Transaction Volume")
    
    fig = px.histogram(
        market_df,
        x='Daily_Transaction_Count',
        nbins=20,
        title='Distribution of Daily Transactions',
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        xaxis_title='Daily Transactions',
        yaxis_title='Number of Stalls',
        showlegend=False
    )
    
    # Add KasiPay users highlight
    kasipay_users = market_df[market_df['Uses_KasiPay']]
    if not kasipay_users.empty:
        fig.add_trace(go.Histogram(
            x=kasipay_users['Daily_Transaction_Count'],
            name='KasiPay Users',
            marker_color='#10B981',
            opacity=0.7
        ))
    
    fig.update_layout(barmode='overlay')
    st.plotly_chart(fig, use_container_width=True)

elif selected_view == "Onboarding Funnel":
    st.header("🔄 Onboarding Funnel Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Funnel chart
        fig = go.Figure(go.Funnel(
            y=funnel_df['Funnel_Stage'],
            x=funnel_df['Users'],
            textinfo="value+percent initial",
            marker={"color": ["#EF4444", "#F59E0B", "#F59E0B", "#F59E0B", "#10B981", "#10B981"]}
        ))
        
        fig.update_layout(
            title="User Onboarding Funnel",
            showlegend=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Funnel Metrics")
        
        for idx, row in funnel_df.iterrows():
            if idx > 0:  # Skip app download
                prev_users = funnel_df.iloc[idx-1]['Users']
                conversion = (row['Users'] / prev_users) * 100
                
                st.metric(
                    label=f"{row['Funnel_Stage']}",
                    value=f"{row['Users']:,}",
                    delta=f"{conversion:.1f}% conversion",
                    delta_color="normal" if conversion > 30 else "inverse"
                )
                st.progress(min(conversion/100, 1.0))
    
    # Drop-off reasons
    st.subheader("📉 Drop-off Analysis")
    
    dropoff_data = funnel_df[funnel_df['Drop-off_Count'] > 0].copy()
    dropoff_data['Stage'] = dropoff_data['Funnel_Stage']
    dropoff_data['Lost Users'] = dropoff_data['Drop-off_Count']
    
    fig = px.bar(
        dropoff_data,
        x='Stage',
        y='Lost Users',
        color='Drop-off_Rate',
        title='Users Lost at Each Stage',
        color_continuous_scale='Reds'
    )
    fig.update_layout(xaxis_title='Funnel Stage', yaxis_title='Users Lost')
    st.plotly_chart(fig, use_container_width=True)

elif selected_view == "Customer Feedback":
    st.header("🗣️ Customer Feedback Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating distribution
        rating_counts = review_df['Rating'].value_counts().sort_index()
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            title='Customer Rating Distribution',
            color=rating_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(xaxis_title='Rating (1-5)', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Keyword frequency
        keywords = ['Verification', 'M-Pesa', 'Fees']
        counts = [verification_complaints, mpesa_requests, review_df['Keyword_Fees'].sum()]
        
        fig = px.bar(
            x=keywords,
            y=counts,
            title='Top Keywords in Customer Feedback',
            color=counts,
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_title='Keyword', yaxis_title='Mentions')
        st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment over time
    st.subheader("📈 Sentiment Trend Over Time")
    
    review_df['Week'] = review_df['Date'].dt.isocalendar().week
    weekly_sentiment = review_df.groupby('Week')['Sentiment_Score'].mean().reset_index()
    
    fig = px.line(
        weekly_sentiment,
        x='Week',
        y='Sentiment_Score',
        title='Average Weekly Sentiment Score',
        markers=True
    )
    
    # Add intervention line
    intervention_week = 13
    fig.add_vline(
        x=intervention_week,
        line_dash="dash",
        line_color="red",
        annotation_text="Onboarding Improved",
        annotation_position="top right"
    )
    
    fig.update_layout(
        xaxis_title='Week',
        yaxis_title='Sentiment Score (-1 to 1)',
        yaxis_range=[-1, 1]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent reviews
    st.subheader("📝 Recent Customer Reviews")
    
    recent_reviews = review_df.sort_values('Date', ascending=False).head(10)
    
    for _, review in recent_reviews.iterrows():
        sentiment_color = "🟢" if review['Sentiment_Score'] > 0.3 else "🟡" if review['Sentiment_Score'] > -0.3 else "🔴"
        
        with st.expander(f"{sentiment_color} Rating: {review['Rating']}/5 - {review['Date'].strftime('%Y-%m-%d')}"):
            st.write(review['Review_Text'])
            st.caption(f"Sentiment: {review['Sentiment_Score']:.2f}")

else:  # Impact Analysis
    st.header("📊 Impact Analysis: Before vs After Onboarding Improvements")
    
    # Weekly metrics comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Weekly active users with intervention line
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weekly_df['Week'],
            y=weekly_df['Weekly_New_Active_Users'],
            mode='lines+markers',
            name='Weekly New Users',
            line=dict(color='#667eea', width=3)
        ))
        
        fig.add_vline(
            x=13,
            line_dash="dash",
            line_color="red",
            annotation_text="Onboarding Improved",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title='Weekly New Active Users',
            xaxis_title='Week',
            yaxis_title='Users',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Onboarding drop-off rate
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weekly_df['Week'],
            y=weekly_df['Onboarding_Dropoff_Rate'] * 100,
            mode='lines+markers',
            name='Drop-off Rate (%)',
            line=dict(color='#EF4444', width=3)
        ))
        
        fig.add_vline(
            x=13,
            line_dash="dash",
            line_color="red"
        )
        
        fig.update_layout(
            title='Onboarding Drop-off Rate',
            xaxis_title='Week',
            yaxis_title='Drop-off Rate (%)',
            yaxis_range=[30, 80]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Before/After comparison
    st.subheader("📈 Key Metric Improvements")
    
    metrics_comparison = pd.DataFrame({
        'Metric': ['Weekly New Users', 'Onboarding Drop-off', 'Customer Satisfaction', 'Support Tickets'],
        'Before': [pre_avg_users, pre_avg_dropoff, pre_avg_satisfaction, weekly_df.iloc[:12]['Support_Tickets_Onboarding'].mean()],
        'After': [post_avg_users, post_avg_dropoff, post_avg_satisfaction, weekly_df.iloc[12:]['Support_Tickets_Onboarding'].mean()],
        'Improvement': [
            f"+{((post_avg_users - pre_avg_users)/pre_avg_users)*100:.0f}%",
            f"-{(pre_avg_dropoff - post_avg_dropoff)*100:.0f}%",
            f"+{((post_avg_satisfaction - pre_avg_satisfaction)/5)*100:.0f}%",
            f"-{((weekly_df.iloc[:12]['Support_Tickets_Onboarding'].mean() - weekly_df.iloc[12:]['Support_Tickets_Onboarding'].mean())/weekly_df.iloc[:12]['Support_Tickets_Onboarding'].mean())*100:.0f}%"
        ]
    })
    
    fig = go.Figure(data=[
        go.Bar(name='Before', x=metrics_comparison['Metric'], y=metrics_comparison['Before'], marker_color='#EF4444'),
        go.Bar(name='After', x=metrics_comparison['Metric'], y=metrics_comparison['After'], marker_color='#10B981')
    ])
    
    fig.update_layout(
        title='Before vs After Onboarding Improvements',
        xaxis_title='Metric',
        yaxis_title='Value',
        barmode='group'
    )
    
    # Add improvement annotations
    for i, row in metrics_comparison.iterrows():
        fig.add_annotation(
            x=row['Metric'],
            y=max(row['Before'], row['After']) + 0.1,
            text=row['Improvement'],
            showarrow=False,
            font=dict(size=12, color='black')
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Support tickets trend
    st.subheader("🛠️ Support Ticket Reduction")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_df['Week'],
        y=weekly_df['Support_Tickets_Onboarding'],
        mode='lines+markers',
        name='Weekly Support Tickets',
        line=dict(color='#F59E0B', width=3)
    ))
    
    fig.add_vline(
        x=13,
        line_dash="dash",
        line_color="red"
    )
    
    fig.update_layout(
        title='Weekly Onboarding Support Tickets',
        xaxis_title='Week',
        yaxis_title='Number of Tickets',
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 1rem;'>
        <small>KasiPay Analytics Dashboard • Last Updated: August 2024 • Data Sources: App Analytics, Customer Surveys, Manual Observation</small>
    </div>
""", unsafe_allow_html=True)
