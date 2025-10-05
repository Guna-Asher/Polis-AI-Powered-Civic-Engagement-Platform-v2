import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Polis - Civic Engagement Platform",
    page_icon="🏛️",
    layout="wide"
)

# API configuration - use service name in Docker, localhost for dev
import os
try:
    # Try to connect to backend service (works in Docker)
    response = requests.get("http://backend:8000/api/health", timeout=2)
    API_BASE_URL = "http://backend:8000"
except:
    # Fall back to localhost for development
    API_BASE_URL = "http://localhost:8000"

st.sidebar.markdown(f"**API Base URL:** `{API_BASE_URL}`")

def main():
    st.sidebar.title("Polis Navigation")
    page = st.sidebar.radio("Go to", [
        "🏛️ Legislation Explorer", 
        "💬 Provide Feedback", 
        "📊 Civic Pulse Dashboard"
    ])
    
    if "🏛️ Legislation Explorer" in page:
        show_legislation_explorer()
    elif "💬 Provide Feedback" in page:
        show_feedback_form()
    elif "📊 Civic Pulse Dashboard" in page:
        show_civic_pulse()

def show_legislation_explorer():
    st.title("🧠 AI Legislation Translator")
    st.markdown("Upload complex legislation documents and get plain-language summaries with clause-by-clause breakdowns.")
    
    uploaded_file = st.file_uploader(
        "Upload Legislation Document", 
        type=['pdf', 'txt'],
        help="Upload PDF or text document of legislation"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing legislation with AI..."):
                # Upload and process legislation
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_BASE_URL}/api/legislation/upload", files=files)
                
                if response.status_code == 200:
                    legislation_data = response.json()
                    
                    # Display summary
                    st.header(legislation_data['title'])
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("📋 Executive Summary")
                        st.info(legislation_data['summary'])
                        
                        # Key points
                        st.subheader("🎯 Key Points")
                        for point in legislation_data['key_points']:
                            st.write(f"• {point}")
                    
                    with col2:
                        st.subheader("📊 Document Info")
                        st.metric("Clauses Identified", len(legislation_data['clauses']))
                        st.metric("Document Type", uploaded_file.type)
                        st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                    
                    # Clause breakdown
                    st.subheader("🔍 Clause-by-Clause Breakdown")
                    for i, clause in enumerate(legislation_data['clauses']):
                        with st.expander(f"**Clause {i+1}**: {clause['text'][:100]}...", expanded=i==0):
                            st.write(clause['text'])
                            st.caption(f"Clause ID: {clause['id']}")
                            
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            st.info("Make sure the backend service is running on port 8000")
    else:
        st.info("👆 Please upload a legislation document to get started. You can use any PDF or text file.")

def show_feedback_form():
    st.title("📊 Structured Sentiment Engine")
    st.markdown("Provide your feedback on legislation using structured inputs that help policymakers understand public sentiment.")
    
    # Mock legislation data
    sample_clauses = [
        {
            "id": "clause_1", 
            "text": "Allocate $500M for renewable energy research and development programs to advance solar, wind, and geothermal technologies."
        },
        {
            "id": "clause_2", 
            "text": "Set carbon emission reduction targets of 50% by 2030 compared to 2020 levels for all industrial sectors."
        },
        {
            "id": "clause_3", 
            "text": "Provide tax credits of up to $7,500 for electric vehicle purchases and establish charging infrastructure grants."
        }
    ]
    
    st.subheader("📝 Provide Your Feedback")
    
    feedback_data = []
    
    for i, clause in enumerate(sample_clauses):
        st.markdown("---")
        st.write(f"### Clause {i+1}")
        st.info(f"**{clause['text']}**")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Sentiment slider
            sentiment = st.select_slider(
                "Your position",
                options=["Strongly Oppose", "Oppose", "Neutral", "Support", "Strongly Support"],
                key=f"sentiment_{clause['id']}",
                help="Select your level of support or opposition"
            )
            
            # Smart tags
            tags = st.multiselect(
                "Relevant concerns/benefits",
                ["#CostConcern", "#EnvironmentalBenefit", "#ImplementationIssue", 
                 "#PrivacyConcern", "#EconomicImpact", "#SocialJustice", "#JobCreation",
                 "#InflationImpact", "#PublicHealth", "#TechnologyAdvancement"],
                key=f"tags_{clause['id']}",
                help="Select tags that represent your main concerns or reasons for support"
            )
        
        with col2:
            # Free text
            free_text = st.text_area(
                "Additional comments (optional)",
                key=f"text_{clause['id']}",
                height=120,
                placeholder="Explain your position, suggest improvements, or share specific concerns..."
            )
        
        feedback_data.append({
            "clause_id": clause['id'],
            "clause_text": clause['text'],
            "sentiment": sentiment.lower().replace(" ", "_"),
            "tags": tags,
            "free_text": free_text
        })
    
    if st.button("📤 Submit All Feedback", type="primary"):
        if feedback_data:
            try:
                with st.spinner("Submitting your feedback..."):
                    response = requests.post(
                        f"{API_BASE_URL}/api/feedback/submit",
                        json=feedback_data
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Thank you for your feedback! Your input has been recorded and will help inform policymakers.")
                        st.balloons()
                    else:
                        st.error("❌ Error submitting feedback. Please try again.")
                        
            except Exception as e:
                st.error(f"🔌 Connection error: {str(e)}")
                st.info("Make sure the backend service is running on port 8000")
        else:
            st.warning("Please provide feedback for at least one clause.")

def show_civic_pulse():
    st.title("📈 Civic Pulse Dashboard")
    st.markdown("Real-time analytics showing public sentiment, key concerns, and demographic breakdowns of legislation feedback.")
    
    try:
        with st.spinner("Loading civic pulse data..."):
            response = requests.get(f"{API_BASE_URL}/api/analytics/pulse")
            
            if response.status_code == 200:
                pulse_data = response.json()
                
                # Overall metrics
                st.subheader("📊 Overall Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Feedback", pulse_data['total_feedback'])
                with col2:
                    support_rate = (pulse_data['sentiment_distribution']['support'] + 
                                  pulse_data['sentiment_distribution']['strongly_support']) * 100
                    st.metric("Overall Support", f"{support_rate:.1f}%")
                with col3:
                    opposition_rate = (pulse_data['sentiment_distribution']['oppose'] + 
                                     pulse_data['sentiment_distribution']['strongly_oppose']) * 100
                    st.metric("Overall Opposition", f"{opposition_rate:.1f}%")
                with col4:
                    neutral_rate = pulse_data['sentiment_distribution']['neutral'] * 100
                    st.metric("Neutral/Undecided", f"{neutral_rate:.1f}%")
                
                # Sentiment distribution chart
                st.subheader("🎭 Public Sentiment Distribution")
                sentiment_df = pd.DataFrame([
                    {"Sentiment": "Strongly Oppose", "Percentage": pulse_data['sentiment_distribution']['strongly_oppose'] * 100, "Color": "#ff4b4b"},
                    {"Sentiment": "Oppose", "Percentage": pulse_data['sentiment_distribution']['oppose'] * 100, "Color": "#ffa36c"},
                    {"Sentiment": "Neutral", "Percentage": pulse_data['sentiment_distribution']['neutral'] * 100, "Color": "#ffe66d"},
                    {"Sentiment": "Support", "Percentage": pulse_data['sentiment_distribution']['support'] * 100, "Color": "#6cff87"},
                    {"Sentiment": "Strongly Support", "Percentage": pulse_data['sentiment_distribution']['strongly_support'] * 100, "Color": "#4bff6c"}
                ])
                
                fig = px.bar(sentiment_df, x='Sentiment', y='Percentage', 
                             color='Sentiment', color_discrete_map={
                                 "Strongly Oppose": "#ff4b4b",
                                 "Oppose": "#ffa36c", 
                                 "Neutral": "#ffe66d",
                                 "Support": "#6cff87",
                                 "Strongly Support": "#4bff6c"
                             })
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tag cloud visualization
                st.subheader("🏷️ Key Concerns & Support Themes")
                if pulse_data['tag_cloud']:
                    tags_df = pd.DataFrame([
                        {"Tag": tag, "Count": count} for tag, count in pulse_data['tag_cloud'].items()
                    ])
                    
                    fig = px.treemap(tags_df, path=['Tag'], values='Count',
                                    color='Count', color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Clause-level sentiment
                st.subheader("📑 Clause-by-Clause Sentiment Analysis")
                if pulse_data['clause_sentiments']:
                    cols = st.columns(len(pulse_data['clause_sentiments']))
                    
                    for i, (clause_id, sentiments) in enumerate(pulse_data['clause_sentiments'].items()):
                        with cols[i]:
                            st.write(f"**{clause_id.replace('_', ' ').title()}**")
                            
                            sentiment_values = list(sentiments.values())
                            sentiment_labels = [label.replace('_', ' ').title() for label in sentiments.keys()]
                            colors = ['#ff4b4b', '#ffa36c', '#ffe66d', '#6cff87', '#4bff6c']
                            
                            fig = go.Figure(data=[go.Pie(
                                labels=sentiment_labels, 
                                values=sentiment_values,
                                hole=.3,
                                marker_colors=colors
                            )])
                            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                            st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.error("Error fetching analytics data")
                
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the backend service is running on port 8000")

if __name__ == "__main__":
    main()