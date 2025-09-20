#!/usr/bin/env python3
"""
Social Media Manager Streamlit Interface
Integrated interface for AI Agent Manager with storytelling capabilities
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List

# Import integrated system components
from agent_integration import IntegratedAIAgentSystem
from ai_agent_manager import SocialMediaPlatform, StoryType, ContentAssetType
from artisan_ai_agent import CraftType

# Configure page
st.set_page_config(
    page_title="Social Media Manager - A2A AI Agent",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'integrated_system' not in st.session_state:
    st.session_state.integrated_system = None

@st.cache_resource
def initialize_integrated_system():
    """Initialize the integrated AI agent system"""
    try:
        return IntegratedAIAgentSystem()
    except Exception as e:
        st.error(f"Error initializing system: {e}")
        return None

def main():
    """Main Streamlit application for Social Media Manager"""
    
    st.title("📱 Social Media Manager & Storytelling Hub")
    st.markdown("*Complete social media management powered by AI storytelling*")
    
    # Initialize system
    if st.session_state.integrated_system is None:
        with st.spinner("Initializing Social Media Manager..."):
            st.session_state.integrated_system = initialize_integrated_system()
            if st.session_state.integrated_system:
                st.success("✅ Social Media Manager initialized successfully!")
            else:
                st.error("❌ Failed to initialize system")
                st.stop()
    
    # Sidebar navigation
    st.sidebar.title("📋 Social Media Hub")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Dashboard",
            "👤 Artisan Setup", 
            "📱 Social Profiles",
            "📖 Story Generator",
            "📅 Content Calendar",
            "🔗 Complete Workflow"
        ]
    )
    
    # Route to different pages
    if page == "🏠 Dashboard":
        show_social_dashboard()
    elif page == "👤 Artisan Setup":
        show_artisan_setup()
    elif page == "📱 Social Profiles":
        show_social_profiles_page()
    elif page == "📖 Story Generator":
        show_story_generator_page()
    elif page == "📅 Content Calendar":
        show_content_calendar_page()
    elif page == "🔗 Complete Workflow":
        show_complete_workflow_page()

def show_social_dashboard():
    """Social media dashboard overview"""
    st.header("📊 Social Media Dashboard")
    
    system = st.session_state.integrated_system
    social_profiles = system.social_media_manager.social_profiles
    content_assets = system.social_media_manager.content_assets
    story_contents = system.social_media_manager.story_contents
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Artisans", len(social_profiles))
    with col2:
        total_profiles = sum(len(profiles) for profiles in social_profiles.values())
        st.metric("Social Profiles", total_profiles)
    with col3:
        st.metric("Content Assets", len(content_assets))
    with col4:
        st.metric("Stories Created", len(story_contents))
    
    # Recent activity
    if story_contents:
        st.subheader("🔄 Recent Stories")
        recent_stories = sorted(story_contents.values(), key=lambda x: x.created_at, reverse=True)[:3]
        
        for story in recent_stories:
            with st.expander(f"📖 {story.title}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {story.story_type.value.replace('_', ' ').title()}")
                    st.write(f"**Created:** {story.created_at.strftime('%Y-%m-%d')}")
                with col2:
                    st.write(f"**Tone:** {story.emotional_tone}")
                    st.write(f"**Platforms:** {len(story.platform_adaptations)}")

def show_artisan_setup():
    """Complete artisan onboarding"""
    st.header("👤 Complete Artisan Setup")
    
    with st.form("artisan_onboarding"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Artisan Name *")
            location = st.text_input("Location *")
            craft_options = [craft.value.title() for craft in CraftType if craft != CraftType.UNKNOWN]
            specialization = st.selectbox("Craft Specialization *", craft_options)
            experience_years = st.number_input("Years of Experience *", min_value=0, max_value=80, value=5)
        
        with col2:
            signature_style = st.text_area("Signature Style")
            target_audience = st.text_area("Target Audience")
        
        # Social media setup
        st.subheader("📱 Social Media Setup")
        platforms = st.multiselect(
            "Select Platforms",
            ['instagram', 'facebook', 'youtube', 'pinterest'],
            default=['instagram', 'facebook']
        )
        
        # Create platform setup data
        platforms_setup = []
        for platform in platforms:
            username = st.text_input(f"{platform.title()} Username")
            profile_url = st.text_input(f"{platform.title()} Profile URL")
            if username and profile_url:
                platforms_setup.append({
                    'platform': platform,
                    'username': username,
                    'profile_url': profile_url
                })
        
        # Craft image upload
        st.subheader("🖼️ Craft Image")
        uploaded_file = st.file_uploader(
            "Upload craft image for analysis",
            type=['jpg', 'jpeg', 'png', 'webp']
        )
        
        # Story preferences
        story_types = st.multiselect(
            "Story Types to Generate",
            [story_type.value.replace('_', ' ').title() for story_type in StoryType],
            default=["Origin Story", "Craft Journey"]
        )
        
        submitted = st.form_submit_button("🚀 Complete Setup")
        
        if submitted and name and location and specialization:
            with st.spinner("Setting up artisan profile..."):
                try:
                    # Prepare data
                    artisan_data = {
                        'name': name,
                        'location': location,
                        'specialization': specialization.lower(),
                        'experience_years': experience_years,
                        'signature_style': signature_style or None,
                        'target_audience': target_audience or None,
                        'social_media_platforms': platforms
                    }
                    
                    social_media_setup = {'platforms': platforms_setup}
                    story_preferences = {
                        'story_types': [s.lower().replace(' ', '_') for s in story_types],
                        'target_platforms': platforms or ['instagram', 'facebook']
                    }
                    
                    # Run complete workflow
                    result = st.session_state.integrated_system.complete_artisan_workflow(
                        artisan_data=artisan_data,
                        uploaded_image_file=uploaded_file,
                        social_media_setup=social_media_setup,
                        story_preferences=story_preferences
                    )
                    
                    st.success("✅ Artisan setup completed successfully!")
                    st.balloons()
                    
                    # Show results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Stories Generated", len(result.get('story_content', [])))
                    with col2:
                        st.metric("Social Profiles", len(result.get('social_media_profiles', [])))
                    with col3:
                        st.metric("Content Assets", len(result.get('content_assets', [])))
                    
                except Exception as e:
                    st.error(f"❌ Error during setup: {e}")

def show_social_profiles_page():
    """Social media profiles management"""
    st.header("📱 Social Media Profiles")
    
    system = st.session_state.integrated_system
    artisan_profiles = system.profile_manager.list_profiles()
    
    if not artisan_profiles:
        st.warning("No artisans found. Please create an artisan profile first.")
        return
    
    # Artisan selection
    profile_options = {f"{p['name']} ({p['specialization']})": p['id'] for p in artisan_profiles}
    selected_artisan = st.selectbox("Select Artisan", list(profile_options.keys()))
    
    if selected_artisan:
        artisan_id = profile_options[selected_artisan]
        social_profiles = system.social_media_manager.get_artisan_social_profiles(artisan_id)
        
        if social_profiles:
            for platform, profile in social_profiles.items():
                with st.expander(f"📱 {platform.title()}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Username:** {profile.username}")
                        st.write(f"**Followers:** {profile.followers_count:,}")
                    
                    with col2:
                        st.write(f"**Engagement:** {profile.engagement_rate:.2%}")
                        st.write(f"**Frequency:** {profile.posting_frequency}")
        else:
            st.info("No social profiles found for this artisan.")

def show_story_generator_page():
    """AI story generator interface"""
    st.header("📖 AI Story Generator")
    
    system = st.session_state.integrated_system
    artisan_profiles = system.profile_manager.list_profiles()
    
    if not artisan_profiles:
        st.warning("No artisans found. Please create an artisan profile first.")
        return
    
    # Artisan selection
    profile_options = {f"{p['name']} ({p['specialization']})": p['id'] for p in artisan_profiles}
    selected_artisan = st.selectbox("Select Artisan", list(profile_options.keys()))
    
    if selected_artisan:
        artisan_id = profile_options[selected_artisan]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📖 Single Story")
            
            story_type = st.selectbox(
                "Story Type",
                [story_type.value.replace('_', ' ').title() for story_type in StoryType]
            )
            
            target_platforms = st.multiselect(
                "Target Platforms",
                ['instagram', 'facebook', 'youtube', 'pinterest'],
                default=['instagram', 'facebook']
            )
            
            if st.button("Generate Story"):
                with st.spinner("Generating story..."):
                    try:
                        artisan_profile = system.profile_manager.get_profile(artisan_id)
                        story_type_enum = StoryType(story_type.lower().replace(' ', '_'))
                        
                        story_content = system.storytelling_engine.generate_story_content(
                            artisan_profile=artisan_profile,
                            craft_analysis=None,
                            story_type=story_type_enum,
                            target_platforms=target_platforms
                        )
                        
                        system.social_media_manager.story_contents[story_content.story_id] = story_content
                        system.social_media_manager.save_data()
                        
                        st.success("✅ Story generated!")
                        
                        # Display story
                        with st.expander("View Generated Story"):
                            st.write(f"**Title:** {story_content.title}")
                            st.write(f"**Hook:** {story_content.hook}")
                            st.text_area("Narrative", story_content.narrative, height=150)
                            st.write(f"**CTA:** {story_content.call_to_action}")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col2:
            st.subheader("🔗 Marketing Chain")

            if st.button("Generate Marketing Chain"):
                with st.spinner("Generating marketing stories..."):
                    try:
                        story_ids = system.generate_marketing_story_chain(
                            artisan_profile_id=artisan_id,
                            marketing_objectives={'primary_goal': 'Increase brand awareness'}
                        )
                        
                        st.success(f"✅ Generated {len(story_ids)} marketing stories!")
                        
                        for story_id in story_ids:
                            story = system.social_media_manager.story_contents[story_id]
                            with st.expander(f"📖 {story.title}"):
                                st.write(f"**Type:** {story.story_type.value.replace('_', ' ').title()}")
                                st.write(f"**Hook:** {story.hook}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

def show_content_calendar_page():
    """Content calendar interface"""
    st.header("📅 Content Calendar")
    
    system = st.session_state.integrated_system
    artisan_profiles = system.profile_manager.list_profiles()
    
    if not artisan_profiles:
        st.warning("No artisans found.")
        return
    
    # Artisan selection
    profile_options = {f"{p['name']} ({p['specialization']})": p['id'] for p in artisan_profiles}
    selected_artisan = st.selectbox("Select Artisan", list(profile_options.keys()))
    
    if selected_artisan:
        artisan_id = profile_options[selected_artisan]
        
        days = st.slider("Calendar Duration (days)", 7, 30, 14)
        
        if st.button("📅 Generate Calendar"):
            with st.spinner("Creating content calendar..."):
                try:
                    calendar = system.create_content_calendar(
                        artisan_profile_id=artisan_id,
                        days=days,
                        include_stories=True
                    )
                    
                    st.success("✅ Calendar generated!")
                    
                    # Show calendar summary
                    total_content = sum(len(day.get('suggested_posts', [])) for day in calendar.values())
                    story_days = sum(1 for day in calendar.values() if day.get('story_content'))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Content", total_content)
                    with col2:
                        st.metric("Story Days", story_days)
                    with col3:
                        st.metric("Coverage", f"{days} days")
                    
                    # Show first few days
                    st.subheader("📅 Upcoming Content")
                    for date, content in list(calendar.items())[:7]:
                        with st.expander(f"📅 {date}"):
                            if content.get('suggested_posts'):
                                for post in content['suggested_posts']:
                                    st.write(f"• {post['title']} ({post['type']})")
                            else:
                                st.write("No content scheduled")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")

def show_complete_workflow_page():
    """Complete workflow overview"""
    st.header("🔗 Complete AI Agent Workflow")
    
    st.markdown("""
    ### 🔄 How It All Works Together
    
    1. **👤 Artisan Profile Creation** - Basic information and specialization
    2. **🖼️ Image Upload & Analysis** - AI analyzes craft images using Gemini
    3. **📋 Content Strategy** - Generate platform-specific recommendations
    4. **📱 Social Media Setup** - Configure profiles across platforms
    5. **📖 AI Storytelling** - Create compelling narratives from craft analysis
    6. **📅 Content Calendar** - Integrated scheduling with stories and posts
    7. **📊 Performance Tracking** - Monitor engagement and growth
    
    ### 🎯 Key Benefits
    
    - **AI-Powered Storytelling** - Transform craft analysis into engaging narratives
    - **Cultural Authenticity** - Stories rooted in Indian traditions and values
    - **Platform Optimization** - Content adapted for each social media platform
    - **Marketing Integration** - Stories designed to drive sales and engagement
    - **Complete Management** - All social media activities in one place
    
    ### 🚀 Getting Started
    
    1. Use **Artisan Setup** to onboard new artisans
    2. Upload craft images for AI analysis
    3. Generate stories using **Story Generator**
    4. Plan content with **Content Calendar**
    5. Monitor performance in **Analytics**
    """)
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Setup New Artisan", use_container_width=True):
            st.switch_page("👤 Artisan Setup")
    
    with col2:
        if st.button("📖 Generate Stories", use_container_width=True):
            st.switch_page("📖 Story Generator")
    
    with col3:
        if st.button("📅 Create Calendar", use_container_width=True):
            st.switch_page("📅 Content Calendar")

if __name__ == "__main__":
    main()