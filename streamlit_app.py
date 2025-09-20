#!/usr/bin/env python3
"""
Streamlit Web Application for A2A AI Agent
Local Artisan Content Strategist System for India
"""

import streamlit as st
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configure page
st.set_page_config(
    page_title="A2A AI Agent - Artisan Content Strategist",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from artisan_ai_agent import ArtisanProfile, CraftType, ContentType
from profile_manager import ProfileManager, get_profile_template
from gcs_image_analyzer import GCSCraftImageAnalyzer
from content_strategist import ContentStrategist
from specialized_recommendations import SpecializedRecommendationEngine

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    try:
        profile_manager = ProfileManager()
        image_analyzer = GCSCraftImageAnalyzer()
        content_strategist = ContentStrategist()
        specialized_engine = SpecializedRecommendationEngine()
        return profile_manager, image_analyzer, content_strategist, specialized_engine
    except Exception as e:
        st.error(f"Error initializing system: {e}")
        return None, None, None, None

def main():
    """Main Streamlit application"""
    st.title("🎨 A2A AI Agent - Artisan Content Strategist")
    st.markdown("*Empowering Local Artisans in India with AI-powered Content Strategy*")
    
    # Initialize system
    if not st.session_state.initialized:
        with st.spinner("Initializing AI Agent System..."):
            components = initialize_system()
            if all(components):
                (st.session_state.profile_manager, 
                 st.session_state.image_analyzer,
                 st.session_state.content_strategist,
                 st.session_state.specialized_engine) = components
                st.session_state.initialized = True
                st.success("✅ System initialized successfully!")
            else:
                st.error("❌ Failed to initialize system")
                st.stop()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["🏠 Dashboard", "👤 Profiles", "🖼️ Image Analysis", "📋 Content Strategy"]
    )
    
    # Route to different pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "👤 Profiles":
        show_profiles_page()
    elif page == "🖼️ Image Analysis":
        show_image_analysis_page()
    elif page == "📋 Content Strategy":
        show_content_strategy_page()

def show_dashboard():
    """Dashboard overview page"""
    st.header("📊 Dashboard Overview")
    
    profiles = st.session_state.profile_manager.list_profiles()
    craft_stats = st.session_state.profile_manager.get_craft_statistics()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Artisans", len(profiles))
    with col2:
        st.metric("Craft Types", len(craft_stats))
    with col3:
        st.metric("Active Profiles", len(profiles))
    with col4:
        st.metric("System Status", "✅ Online")
    
    # Charts
    if craft_stats:
        st.subheader("📈 Craft Distribution")
        st.bar_chart(craft_stats)
    
    # Recent profiles
    st.subheader("👥 Recent Artisan Profiles")
    if profiles:
        for profile in profiles[-3:]:
            with st.expander(f"👤 {profile['name']} - {profile['specialization'].title()}"):
                st.write(f"Location: {profile['location']}")
                st.write(f"Experience: {profile['experience_years']} years")
    else:
        st.info("No artisan profiles found. Create your first profile.")

def show_profiles_page():
    """Artisan profiles management page"""
    st.header("👤 Artisan Profile Management")
    
    tab1, tab2 = st.tabs(["📝 Create Profile", "📋 View Profiles"])
    
    with tab1:
        create_profile_form()
    
    with tab2:
        list_profiles()

def create_profile_form():
    """Form to create new artisan profile"""
    st.subheader("📝 Create New Artisan Profile")
    
    with st.form("create_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Artisan Name *")
            location = st.text_input("Location *")
            craft_options = [craft.value.title() for craft in CraftType if craft != CraftType.UNKNOWN]
            specialization = st.selectbox("Craft Specialization *", craft_options)
            experience_years = st.number_input("Years of Experience *", min_value=0, max_value=80, value=5)
        
        with col2:
            signature_style = st.text_area("Signature Style (optional)")
            target_audience = st.text_area("Target Audience (optional)")
            platforms = st.multiselect(
                "Social Media Platforms",
                ["instagram", "youtube", "facebook", "pinterest"],
                default=["instagram", "facebook"]
            )
        
        submitted = st.form_submit_button("Create Profile")
        
        if submitted and name and location and specialization:
            try:
                profile_id = st.session_state.profile_manager.create_profile(
                    name=name,
                    location=location,
                    specialization=CraftType(specialization.lower()),
                    experience_years=experience_years,
                    signature_style=signature_style if signature_style else None,
                    target_audience=target_audience if target_audience else None,
                    social_media_platforms=platforms if platforms else None
                )
                
                st.success(f"✅ Profile created successfully! ID: {profile_id}")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error creating profile: {e}")

def list_profiles():
    """List all artisan profiles"""
    st.subheader("📋 All Artisan Profiles")
    
    profiles = st.session_state.profile_manager.list_profiles()
    
    if not profiles:
        st.info("No artisan profiles found.")
        return
    
    for profile in profiles:
        with st.expander(f"👤 {profile['name']} - {profile['specialization'].title()}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Location:** {profile['location']}")
                st.write(f"**Experience:** {profile['experience_years']} years")
            with col2:
                st.write(f"**Created:** {profile['created_at'][:10]}")
                if st.button(f"🗑️ Delete", key=f"delete_{profile['id']}"):
                    st.session_state.profile_manager.delete_profile(profile['id'])
                    st.rerun()

def show_image_analysis_page():
    """Image analysis page with GCS integration"""
    st.header("🖼️ Craft Image Analysis")
    
    profiles = st.session_state.profile_manager.list_profiles()
    if not profiles:
        st.warning("⚠️ No artisan profiles found. Please create a profile first.")
        return
    
    profile_options = {f"{p['name']} - {p['specialization'].title()}": p['id'] for p in profiles}
    selected_profile_key = st.selectbox("Select Artisan Profile", list(profile_options.keys()))
    
    if selected_profile_key:
        profile_id = profile_options[selected_profile_key]
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'webp']
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                st.write("**Image Details:**")
                st.write(f"Filename: {uploaded_file.name}")
                st.write(f"Size: {uploaded_file.size} bytes")
            
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        result = st.session_state.image_analyzer.analyze_uploaded_image(
                            uploaded_file, profile_id
                        )
                        
                        if result:
                            show_analysis_results(result)
                        else:
                            st.error("❌ Failed to analyze image")
                    
                    except Exception as e:
                        st.error(f"❌ Error analyzing image: {e}")

def show_analysis_results(result: Dict):
    """Display image analysis results"""
    st.success("✅ Analysis completed!")
    
    analysis = result['analysis']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Craft Type", analysis['craft_type'].title())
    with col2:
        st.metric("Complexity", analysis['complexity_level'].title())
    with col3:
        st.metric("Confidence", f"{analysis['confidence_score']:.2f}")
    
    # Recommendations
    if 'content_recommendations' in result:
        st.subheader("💡 Content Recommendations")
        
        for rec in result['content_recommendations']['general'][:3]:
            with st.expander(f"💡 {rec['title_suggestion']}"):
                st.write(f"**Type:** {rec['content_type'].replace('_', ' ').title()}")
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Best Time:** {rec['best_time_to_post']}")
                st.write(f"**Platforms:** {', '.join(rec['target_platforms'])}")

def show_content_strategy_page():
    """Content strategy generation page"""
    st.header("📋 Content Strategy Generator")
    
    profiles = st.session_state.profile_manager.list_profiles()
    if not profiles:
        st.warning("⚠️ No artisan profiles found.")
        return
    
    profile_options = {f"{p['name']} - {p['specialization'].title()}": p['id'] for p in profiles}
    selected_profile_key = st.selectbox("Select Artisan Profile", list(profile_options.keys()))
    
    if selected_profile_key:
        profile_id = profile_options[selected_profile_key]
        profile = st.session_state.profile_manager.get_profile(profile_id)
        
        if st.button("📋 Generate Content Strategy", type="primary"):
            with st.spinner("Generating strategy..."):
                try:
                    general_strategy = st.session_state.content_strategist.generate_content_strategy(profile)
                    
                    st.success("✅ Content strategy generated!")
                    
                    for rec in general_strategy[:5]:
                        with st.expander(f"💡 {rec.title_suggestion} (Priority: {rec.priority_score:.2f})"):
                            st.write(f"**Type:** {rec.content_type.value.replace('_', ' ').title()}")
                            st.write(f"**Description:** {rec.description}")
                            st.write(f"**Best Time:** {rec.best_time_to_post}")
                            st.write(f"**Reasoning:** {rec.reasoning}")
                
                except Exception as e:
                    st.error(f"❌ Error generating strategy: {e}")

if __name__ == "__main__":
    main()