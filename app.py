import streamlit as st
from datetime import datetime, timedelta
import json

# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="✈️ Trip Planner Bot", layout="wide")

# Comprehensive international destinations database
DESTINATIONS_DATABASE = {
    "paris": {
        "name": "Paris, France",
        "description": "The City of Light with iconic landmarks, world-class museums, and romantic atmosphere",
        "best_time": "April-June, September-October (mild weather, fewer crowds)",
        "budget_range": "$100-200 per day",
        "currency": "Euro (€)",
        "language": "French",
        "activities": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Seine River Cruise", "Montmartre district"],
        "food": ["Croissants", "French onion soup", "Coq au vin", "Macarons", "Wine tasting"],
        "transport": "Metro system, buses, taxis, walking"
    },
    "tokyo": {
        "name": "Tokyo, Japan",
        "description": "A vibrant metropolis blending ultra-modern technology with ancient traditions",
        "best_time": "March-May (cherry blossoms), September-November (autumn colors)",
        "budget_range": "$80-150 per day",
        "currency": "Japanese Yen (¥)",
        "language": "Japanese",
        "activities": ["Senso-ji Temple", "Shibuya Crossing", "Tsukiji Fish Market", "Imperial Palace", "Harajuku district"],
        "food": ["Sushi", "Ramen", "Tempura", "Yakitori", "Matcha tea"],
        "transport": "JR trains, subway, buses, taxis"
    },
    "new york": {
        "name": "New York City, USA",
        "description": "The Big Apple - a bustling metropolis with world-class attractions and Broadway shows",
        "best_time": "April-June, September-November (pleasant weather)",
        "budget_range": "$120-250 per day",
        "currency": "US Dollar ($)",
        "language": "English",
        "activities": ["Central Park", "Broadway shows", "Times Square", "Statue of Liberty", "9/11 Memorial"],
        "food": ["New York pizza", "Bagels", "Cheesecake", "Hot dogs", "Deli sandwiches"],
        "transport": "Subway, taxis, buses, walking, Uber/Lyft"
    },
    "london": {
        "name": "London, UK",
        "description": "Historic capital combining royal heritage with modern culture",
        "best_time": "May-September (warmer weather, longer days)",
        "budget_range": "$110-200 per day",
        "currency": "British Pound (£)",
        "language": "English",
        "activities": ["Big Ben", "Tower of London", "British Museum", "Thames cruise", "Hyde Park"],
        "food": ["Fish and chips", "Afternoon tea", "Bangers and mash", "Shepherd's pie", "Pub food"],
        "transport": "Underground (Tube), buses, taxis, walking"
    },
    "rome": {
        "name": "Rome, Italy",
        "description": "The Eternal City with ancient history, incredible architecture, and amazing cuisine",
        "best_time": "April-June, September-October (mild weather)",
        "budget_range": "$90-160 per day",
        "currency": "Euro (€)",
        "language": "Italian",
        "activities": ["Colosseum", "Vatican City", "Trevi Fountain", "Roman Forum", "Pantheon"],
        "food": ["Pizza", "Pasta", "Gelato", "Carbonara", "Tiramisu"],
        "transport": "Metro, buses, trams, walking, taxis"
    },
    "bangkok": {
        "name": "Bangkok, Thailand",
        "description": "Vibrant capital known for street food, temples, and bustling markets",
        "best_time": "November-February (cool and dry season)",
        "budget_range": "$40-80 per day",
        "currency": "Thai Baht (฿)",
        "language": "Thai",
        "activities": ["Grand Palace", "Wat Pho temple", "Floating markets", "Khao San Road", "Chao Phraya River"],
        "food": ["Pad Thai", "Tom Yum soup", "Green curry", "Mango sticky rice", "Street food"],
        "transport": "BTS Skytrain, MRT, buses, tuk-tuks, boats"
    },
    "sydney": {
        "name": "Sydney, Australia",
        "description": "Stunning harbor city with iconic landmarks and beautiful beaches",
        "best_time": "September-November, March-May (spring/autumn)",
        "budget_range": "$100-180 per day",
        "currency": "Australian Dollar (AUD)",
        "language": "English",
        "activities": ["Opera House", "Harbour Bridge", "Bondi Beach", "Darling Harbour", "Blue Mountains"],
        "food": ["Meat pies", "Seafood", "Lamingtons", "Vegemite", "Barramundi"],
        "transport": "Trains, buses, ferries, taxis, walking"
    },
    "dubai": {
        "name": "Dubai, UAE",
        "description": "Modern desert metropolis with luxury shopping, futuristic architecture",
        "best_time": "November-March (cooler temperatures)",
        "budget_range": "$120-300 per day",
        "currency": "UAE Dirham (AED)",
        "language": "Arabic (English widely spoken)",
        "activities": ["Burj Khalifa", "Dubai Mall", "Desert safari", "Palm Jumeirah", "Gold Souk"],
        "food": ["Shawarma", "Hummus", "Dates", "Arabic coffee", "International cuisine"],
        "transport": "Metro, taxis, buses, Uber/Careem"
    }
}

def create_detailed_itinerary(destination, duration, interests):
    """Create a detailed day-by-day itinerary"""
    dest_key = destination.lower()
    duration = int(duration)
    
    if dest_key in DESTINATIONS_DATABASE:
        dest_info = DESTINATIONS_DATABASE[dest_key]
        
        itinerary = f"""
### 📅 Detailed {duration}-Day Itinerary for {dest_info['name']}

"""
        
        # Day 1 - Arrival
        itinerary += f"""**Day 1: Arrival + City Introduction**
**Morning:**
* ✈️ *Arrival in {dest_info['name']}*
* Check-in to hotel (recommended areas: city center for easy access)
* Local breakfast to start your cultural immersion

**Afternoon:**
* First major attraction: {dest_info['activities'][0] if dest_info['activities'] else 'City center exploration'}
* Lunch at local restaurant
* Walking tour of main district

**Evening:**
* Sunset at scenic viewpoint
* Welcome dinner featuring: {dest_info['food'][0] if dest_info['food'] else 'local cuisine'}
* Early rest to overcome jet lag

"""
        
        # Day 2 - Major attractions
        if duration >= 2:
            itinerary += f"""**Day 2: Major Landmarks & Attractions**
**Morning:**
* Early start to {dest_info['activities'][1] if len(dest_info['activities']) > 1 else 'major landmark'}
* Guided tour or audio guide recommended
* Coffee break at local café

**Afternoon:**
* Visit to {dest_info['activities'][2] if len(dest_info['activities']) > 2 else 'museum or cultural site'}
* Lunch: Try {dest_info['food'][1] if len(dest_info['food']) > 1 else 'signature dish'}
* Shopping at local markets

**Evening:**
* {dest_info['activities'][3] if len(dest_info['activities']) > 3 else 'Cultural performance or local entertainment'}
* Dinner at traditional restaurant
* Night walk through historic district

"""
        
        # Day 3 - Culture & experiences
        if duration >= 3:
            itinerary += f"""**Day 3: Cultural Immersion & Local Experiences**
**Morning:**
* {dest_info['activities'][4] if len(dest_info['activities']) > 4 else 'Local neighborhood exploration'}
* Breakfast at local favorite spot
* Cooking class or cultural workshop

**Afternoon:**
* Food tour featuring: {', '.join(dest_info['food'][:3])}
* Visit local markets and artisan shops
* Relaxation at park or café

**Evening:**
* Traditional entertainment or live music
* Dinner at hidden gem restaurant
* Stroll through nightlife district

"""
        
        # Day 4+ - Extended exploration
        if duration >= 4:
            itinerary += f"""**Day 4+: Extended Exploration & Day Trips**
**For longer stays, consider:**
* Day trips to nearby attractions
* Specialized interest tours (food, history, adventure)
* Relaxation and spa experiences
* Meeting locals and cultural exchange
* Photography tours of hidden gems
* Shopping for authentic souvenirs

"""
        
        return itinerary
    else:
        # Generic itinerary for unlisted destinations
        return f"""
### 📅 Detailed {duration}-Day Itinerary for {destination}

**Day 1: Arrival + City Introduction**
**Morning:**
* ✈️ *Arrival in {destination}*
* Check-in to accommodation
* Local breakfast and orientation

**Afternoon:**
* Main city center exploration
* Visit primary landmark or attraction
* Lunch at recommended local restaurant

**Evening:**
* Sunset viewing at scenic location
* Welcome dinner with local specialties
* Early rest for jet lag recovery

**Day 2: Major Attractions**
**Morning:**
* Early visit to top-rated attraction
* Guided tour of historic district
* Coffee break at local café

**Afternoon:**
* Museum or cultural site visit
* Traditional lunch experience
* Local market exploration

**Evening:**
* Cultural performance or entertainment
* Dinner at traditional restaurant
* Night walk through city center

**Day 3+: Cultural Immersion**
* Cooking classes or workshops
* Food tours and tastings
* Local neighborhood exploration
* Day trips to nearby attractions
* Shopping for authentic souvenirs
* Meeting locals and cultural exchange
"""

def get_trip_suggestions(destination, duration, budget, interests):
    """Generate comprehensive trip suggestions"""
    dest_key = destination.lower()
    
    if dest_key in DESTINATIONS_DATABASE:
        dest_info = DESTINATIONS_DATABASE[dest_key]
        
        # Create detailed itinerary
        itinerary = create_detailed_itinerary(destination, duration, interests)
        
        suggestions = f"""
## 🌟 Complete Trip Plan for {dest_info['name']}

**Duration:** {duration} days
**Budget:** ${budget}
**Interests:** {', '.join(interests)}

### 📍 Destination Overview
{dest_info['description']}

### 🌍 Essential Information
* **Best Time to Visit:** {dest_info['best_time']}
* **Currency:** {dest_info['currency']}
* **Language:** {dest_info['language']}
* **Daily Budget:** {dest_info['budget_range']}
* **Your Budget:** ${budget}

### 🚌 Transportation
{dest_info['transport']}

### 🍽️ Must-Try Local Cuisine
{', '.join(dest_info['food'])}

### 🎯 Top Attractions
{', '.join(dest_info['activities'])}

{itinerary}

### 💡 Pro Tips
* Book accommodations in advance, especially during peak season
* Learn basic phrases in {dest_info['language']}
* Keep copies of important documents
* Research local customs and etiquette
* Consider travel insurance
* Download offline maps and translation apps
"""
        
        return suggestions
    else:
        # Generic suggestions for unlisted destinations
        itinerary = create_detailed_itinerary(destination, duration, interests)
        
        suggestions = f"""
## 🔍 Custom Trip Plan for {destination}

**Duration:** {duration} days
**Budget:** ${budget}
**Interests:** {', '.join(interests)}

### 📍 Destination Information
I'd be happy to help you plan your trip to {destination}! Here's a comprehensive plan:

{itinerary}

### 📝 General Planning Tips
* Research visa requirements well in advance
* Check vaccination requirements
* Book flights and accommodations early
* Learn about local customs and etiquette
* Research local transportation options
* Consider travel insurance
* Download useful apps (translation, maps, currency)

### 🎯 Based on Your Interests
"""
        
        if "Adventure" in interests:
            suggestions += "* Look for outdoor activities, hiking trails, and adventure sports\n"
        if "Culture" in interests:
            suggestions += "* Visit museums, historical sites, and cultural landmarks\n"
        if "Food" in interests:
            suggestions += "* Try local cuisine, take food tours, and visit markets\n"
        if "Relaxation" in interests:
            suggestions += "* Find spas, beaches, or peaceful locations\n"
        if "Nature" in interests:
            suggestions += "* Explore national parks, gardens, and natural attractions\n"
        if "History" in interests:
            suggestions += "* Visit historical sites, museums, and heritage locations\n"
        if "Shopping" in interests:
            suggestions += "* Explore local markets, shopping districts, and artisan shops\n"
        if "Nightlife" in interests:
            suggestions += "* Research bars, clubs, and entertainment venues\n"
        
        return suggestions

def get_budget_tips():
    """Comprehensive international budget tips"""
    return """
## 💰 International Budget Travel Tips

### 🛫 Flight Savings
* **Book 6-8 weeks in advance** for international flights
* **Use flight comparison sites**: Skyscanner, Google Flights, Momondo
* **Be flexible with dates**: Use flexible date search
* **Consider layovers**: Sometimes cheaper than direct flights
* **Budget airlines**: Research local budget carriers
* **Error fares**: Follow deal alert websites

### 🏨 Accommodation Strategies
* **Hostels**: Great for meeting people, especially in Europe
* **Airbnb**: Often cheaper for longer stays
* **Guesthouses**: Local alternatives to hotels
* **Location vs Price**: Stay slightly outside city center
* **Booking timing**: Book refundable rates, cancel if better deals appear
* **Loyalty programs**: Use hotel points and status benefits

### 🍽️ Food & Dining
* **Street food**: Often the best and cheapest local cuisine
* **Local markets**: Fresh produce and authentic experience
* **Cook your own**: If staying in places with kitchens
* **Lunch specials**: Many restaurants offer cheaper lunch menus
* **Avoid tourist areas**: Restaurants near attractions are overpriced
* **Happy hours**: Take advantage of drink specials

### 🚌 Transportation
* **Public transport**: Buy day/week passes instead of individual tickets
* **Walking**: Best way to explore and it's free
* **Ride-sharing**: Often cheaper than taxis
* **Bike rentals**: Many cities have bike-sharing programs
* **Regional trains**: Cheaper than high-speed options
* **Multi-city passes**: For extensive travel (Eurail, etc.)

### 🎫 Activities & Attractions
* **Free walking tours**: Available in most major cities
* **Museum free days**: Many museums have free entry days
* **City tourism cards**: Often include transport + attractions
* **Student discounts**: Get an international student ID
* **Group discounts**: Travel with others for better rates
* **Free attractions**: Parks, beaches, viewpoints, markets

### 💳 Money Management
* **Notify banks**: Avoid card blocks while traveling
* **Multi-currency cards**: Avoid foreign transaction fees
* **ATM strategy**: Use bank ATMs, avoid airport/tourist area ATMs
* **Local currency**: Have some cash for small vendors
* **Budgeting apps**: Track expenses in real-time
* **Emergency fund**: Keep separate emergency money

### 🌍 Regional Specific Tips
* **Southeast Asia**: Street food, local transport, guesthouses
* **Europe**: Hostels, train passes, free walking tours
* **Americas**: National parks, road trips, camping
* **Middle East**: Haggling expected, modest dress savings
* **Africa**: Group tours often better value, local guides
* **Oceania**: Working holiday visas, camping, hitchhiking

### 📱 Technology Savings
* **Free WiFi**: Use instead of international roaming
* **Offline maps**: Download before traveling
* **Translation apps**: Google Translate offline mode
* **Travel apps**: Compare prices, find deals
* **VPN**: Access home country prices for bookings
* **International SIM**: Often cheaper than roaming

### 🎒 Packing Smart
* **Pack light**: Avoid baggage fees
* **Versatile clothing**: Mix and match outfits
* **Travel-sized items**: Buy toiletries locally
* **Universal adapter**: One adapter for all countries
* **Portable charger**: Avoid buying multiple chargers
* **Laundry**: Do laundry instead of overpacking

### 💡 Pro Money-Saving Hacks
* **Shoulder season**: Travel just before/after peak season
* **Slow travel**: Stay longer in fewer places
* **House sitting**: Free accommodation for pet/house sitting
* **Work exchanges**: Hostels, farms, volunteer programs
* **Local friends**: Connect with locals for insider tips
* **Travel insurance**: Cheaper than medical emergencies abroad
"""

def main():
    st.title("✈️ International AI Trip Planner")
    st.markdown("🌍 Plan your perfect international adventure with detailed itineraries and insider tips!")
    
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize session state for button clicks to prevent loops
    if "show_destinations" not in st.session_state:
        st.session_state.show_destinations = False
    if "show_budget" not in st.session_state:
        st.session_state.show_budget = False
    if "show_checklist" not in st.session_state:
        st.session_state.show_checklist = False
    
    # Sidebar for trip planning inputs
    with st.sidebar:
        st.header("🎯 Trip Planning")
        
        destination = st.text_input("Where do you want to go?", placeholder="e.g., Paris, Tokyo, New York, London")
        
        duration = st.selectbox("Trip duration (days)", 
                               options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 21, 30],
                               index=6)
        
        budget = st.number_input("Budget ($)", min_value=100, max_value=10000, value=1000, step=100)
        
        interests = st.multiselect("What are you interested in?", 
                                 options=["Adventure", "Culture", "Food", "Relaxation", "Nature", "History", "Shopping", "Nightlife"],
                                 default=["Culture", "Food"])
        
        if st.button("🚀 Create Detailed Itinerary", type="primary"):
            if destination:
                with st.spinner("Creating your personalized international itinerary..."):
                    suggestions = get_trip_suggestions(destination, duration, budget, interests)
                    
                    # Add to chat history
                    user_message = f"Plan a detailed {duration}-day trip to {destination} with a budget of ${budget}. I'm interested in: {', '.join(interests)}"
                    st.session_state.messages.append({"role": "user", "content": user_message})
                    st.session_state.messages.append({"role": "assistant", "content": suggestions})
            else:
                st.error("Please enter a destination!")
    
    # Main chat interface
    st.header("💬 Chat with International Trip Planner")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about international travel..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            if "budget" in prompt.lower() or "money" in prompt.lower() or "cheap" in prompt.lower():
                response = get_budget_tips()
            else:
                response = f"""
Thanks for your question: "{prompt}"

I'd be happy to help with your international travel planning! Here are some insights:

**For specific destination advice:** Use the sidebar to create a detailed itinerary for any country or city.

**General international travel tips:**
* Research visa requirements well in advance
* Check vaccination and health requirements
* Understand local customs and etiquette
* Learn basic phrases in the local language
* Research local transportation options
* Consider travel insurance
* Keep digital and physical copies of important documents

**Popular international destinations in our database:**
🇫🇷 Paris, France | 🇯🇵 Tokyo, Japan | 🇺🇸 New York, USA | 🇬🇧 London, UK | 🇮🇹 Rome, Italy | 🇹🇭 Bangkok, Thailand | 🇦🇺 Sydney, Australia | 🇦🇪 Dubai, UAE

Feel free to ask about specific countries, budget tips, or use the sidebar for a complete itinerary!
"""
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons with proper state management
    st.header("🌍 Quick International Travel Resources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌍 Popular Destinations"):
            popular_response = """
## 🌍 Top International Destinations

### 🏛️ Europe
* **🇫🇷 Paris, France** - Art, romance, and world-class cuisine
* **🇮🇹 Rome, Italy** - Ancient history and incredible food
* **🇬🇧 London, UK** - Royal heritage and modern culture
* **🇩🇪 Berlin, Germany** - History, nightlife, and culture
* **🇪🇸 Barcelona, Spain** - Architecture, beaches, and tapas

### 🏯 Asia
* **🇯🇵 Tokyo, Japan** - Modern technology meets ancient tradition
* **🇹🇭 Bangkok, Thailand** - Street food and vibrant culture
* **🇸🇬 Singapore** - Clean, modern, and incredibly diverse
* **🇰🇷 Seoul, South Korea** - K-culture and amazing food
* **🇻🇳 Ho Chi Minh City, Vietnam** - History and incredible cuisine

### 🏖️ Americas
* **🇺🇸 New York, USA** - The city that never sleeps
* **🇧🇷 Rio de Janeiro, Brazil** - Beaches, carnival, and culture
* **🇨🇦 Toronto, Canada** - Diversity and natural beauty
* **🇲🇽 Mexico City, Mexico** - Rich culture and amazing food
* **🇦🇷 Buenos Aires, Argentina** - Tango, steaks, and wine

### 🏜️ Middle East & Africa
* **🇦🇪 Dubai, UAE** - Luxury, modern architecture, and shopping
* **🇪🇬 Cairo, Egypt** - Ancient pyramids and rich history
* **🇿🇦 Cape Town, South Africa** - Natural beauty and wine
* **🇹🇷 Istanbul, Turkey** - Where Europe meets Asia

### 🏄 Oceania
* **🇦🇺 Sydney, Australia** - Iconic harbor and laid-back culture
* **🇳🇿 Auckland, New Zealand** - Adventure and natural beauty
"""
            st.session_state.messages.append({"role": "assistant", "content": popular_response})
    
    with col2:
        if st.button("💰 International Budget Tips"):
            budget_response = get_budget_tips()
            st.session_state.messages.append({"role": "assistant", "content": budget_response})
    
    with col3:
        if st.button("📋 International Travel Checklist"):
            checklist_response = """
## 📋 International Travel Checklist

### 📄 Essential Documents
* [ ] **Passport** (valid for 6+ months)
* [ ] **Visa** (research requirements early)
* [ ] **Travel insurance** documentation
* [ ] **Flight confirmations** and itinerary
* [ ] **Hotel reservations** confirmations
* [ ] **International driving permit** (if needed)
* [ ] **Vaccination certificates** (if required)
* [ ] **Emergency contact information**

### 💳 Financial Preparation
* [ ] **Notify banks** of travel dates and destinations
* [ ] **International banking cards** (low foreign transaction fees)
* [ ] **Local currency** (some cash for arrival)
* [ ] **Emergency credit card** (separate from main wallet)
* [ ] **Travel budget** planning and tracking app

### 🎒 Smart Packing
* [ ] **Weather-appropriate clothing** (check forecast)
* [ ] **Comfortable walking shoes** (broken in)
* [ ] **Universal power adapter** and chargers
* [ ] **Medications** in original containers
* [ ] **First aid kit** basics
* [ ] **Copies of documents** (digital and physical)
* [ ] **Travel-sized toiletries** (within liquid limits)

### 📱 Technology & Communication
* [ ] **International phone plan** or local SIM research
* [ ] **Offline maps** downloaded
* [ ] **Translation apps** downloaded
* [ ] **Travel apps** (transport, food, accommodation)
* [ ] **VPN** for secure internet access
* [ ] **Emergency contact apps** and information

### 🏥 Health & Safety
* [ ] **Travel insurance** with medical coverage
* [ ] **Vaccinations** (check requirements 6-8 weeks ahead)
* [ ] **Prescription medications** (extra supply)
* [ ] **Emergency medical information** card
* [ ] **Embassy/consulate contact information**
* [ ] **Local emergency numbers** research

### 🌍 Cultural Preparation
* [ ] **Local customs** and etiquette research
* [ ] **Basic phrases** in local language
* [ ] **Dress code** requirements for religious sites
* [ ] **Tipping customs** understanding
* [ ] **Business hours** and holiday calendar
* [ ] **Cultural sensitivity** awareness
"""
            st.session_state.messages.append({"role": "assistant", "content": checklist_response})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []

if __name__ == "__main__":
    main()