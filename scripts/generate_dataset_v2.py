import json
import os
import time
import re
import ollama

# Configuration
MODEL = "metacraft"
OUTPUT_PATH = "data/organic_ads_dataset.json"

# Massive Synthetic Expansion (100+ Seeds)
# Covering multiple industries: Food, FMCG, Tech, Banking, Travel, Sports
SEEDS = [
    # --- HINDI (25 Seeds) ---
    {"brand": "Maggi", "tagline": "2-Minute Noodles", "theme": "Late night study, hostel life", "language": "Hindi"},
    {"brand": "Thums Up", "tagline": "Taste the Thunder", "theme": "Action, bravery, summer", "language": "Hindi"},
    {"brand": "Amul Macho", "tagline": "Bade Aaram Se", "theme": "Comfort, masculinity", "language": "Hindi"},
    {"brand": "Dhara Oil", "tagline": "Shuddhata ki Pehchan", "theme": "Family dinner, Jalebi", "language": "Hindi"},
    {"brand": "PolicyBazaar", "tagline": "Ullu Mat Bano", "theme": "Insurance, smart saving", "language": "Hindi"},
    {"brand": "Lenskart", "tagline": "Specsy is Sexy", "theme": "Fashion, vision, youth", "language": "Hindi"},
    {"brand": "Asian Paints", "tagline": "Har Ghar Kuch Kehta Hai", "theme": "Home renovation, emotions", "language": "Hindi"},
    {"brand": "Surf Excel", "tagline": "Daag Acche Hain", "theme": "Kids playing, kindness", "language": "Hindi"},
    {"brand": "Cadbury Celebrations", "tagline": "Kuch Meetha Ho Jaaye", "theme": "Diwali, gifting", "language": "Hindi"},
    {"brand": "Ariel", "tagline": "Share The Load", "theme": "Equality, household chores", "language": "Hindi"},
    {"brand": "Zomato", "tagline": "Har Craving ka Cure", "theme": "Late night food, delivery", "language": "Hindi"},
    {"brand": "Blinkit", "tagline": "Everything in 10 minutes", "theme": "Last minute, kitchen essentials", "language": "Hindi"},
    {"brand": "PhonePe", "tagline": "Karte Ja. Badhte Ja.", "theme": "Universal payment, trust", "language": "Hindi"},
    {"brand": "Cred", "tagline": "Not for Everyone", "theme": "Exclusivity, rewards, irony", "language": "Hindi"},
    {"brand": "Maruti Suzuki", "tagline": "Kitna Deti Hai?", "theme": "Mileage, common man, middle class", "language": "Hindi"},
    {"brand": "Royal Enfield", "tagline": "Made Like a Gun", "theme": "Vibration, road trip, masculinity", "language": "Hindi"},
    {"brand": "FabIndia", "tagline": "Celebrate India", "theme": "Ethic wear, culture, Diwali", "language": "Hindi"},
    {"brand": "Fevikwik", "tagline": "Chutki mein chipkaye", "theme": "Humor, fixing things, instant", "language": "Hindi"},
    {"brand": "Jio", "tagline": "Digital India", "theme": "Connectivity, family, technology", "language": "Hindi"},
    {"brand": "Pepsi", "tagline": "Yeh Dil Maange More", "theme": "Youth, thirst, cricket", "language": "Hindi"},
    {"brand": "Amul", "tagline": "The Taste of India", "theme": "Dairy, Nation, Happiness", "language": "Hindi"},
    {"brand": "Tata Salt", "tagline": "Desh ka Namak", "theme": "Trust, purity, patriotism", "language": "Hindi"},
    {"brand": "Mountain Dew", "tagline": "Darr Ke Aage Jeet Hai", "theme": "Adventure, overcoming fear", "language": "Hindi"},
    {"brand": "Tanishq", "tagline": "Beautiful Together", "theme": "Wedding, jewelry, tradition", "language": "Hindi"},
    {"brand": "Frooti", "tagline": "Live the Frooti Life", "theme": "Mango fun, youth, summer", "language": "Hindi"},

    # --- TAMIL (25 Seeds) ---
    {"brand": "Aachi Masala", "tagline": "The Taste of South India", "theme": "Traditional cooking, Grandmother", "language": "Tamil"},
    {"brand": "Sun Direct", "tagline": "Direct to Heart", "theme": "Movies, family entertainment", "language": "Tamil"},
    {"brand": "Cooptex", "tagline": "Handloom Heritage", "theme": "Cotton sarees, summer comfort", "language": "Tamil"},
    {"brand": "Medimix", "tagline": "Nothing better than Natural", "theme": "Skin care, herbal heritage", "language": "Tamil"},
    {"brand": "Preethi Mixer", "tagline": "Perfect Results Everytime", "theme": "Kitchen efficiency, Chutney", "language": "Tamil"},
    {"brand": "Hatsun Curd", "tagline": "Purity Guaranteed", "theme": "Healthy breakfast, cool curd", "language": "Tamil"},
    {"brand": "GRT Jewellers", "tagline": "Gold with Trust", "theme": "Akshaya Tritiya, investment", "language": "Tamil"},
    {"brand": "Tamil Nadu Tourism", "tagline": "Enchanting Tamil Nadu", "theme": "Temples, Mahabalipuram", "language": "Tamil"},
    {"brand": "Saravana Stores", "tagline": "Low price, high quality", "theme": "Shopping, variety", "language": "Tamil"},
    {"brand": "Chennai Super Kings", "tagline": "Whistle Podu", "theme": "Sports, fans, yellow pride", "language": "Tamil"},
    {"brand": "Aravind Eye Care", "tagline": "Vision for all", "theme": "Healthcare, compassion, service", "language": "Tamil"},
    {"brand": "Ramraj Cotton", "tagline": "Spirit of tradition", "theme": "Dhotis, men's pride, white", "language": "Tamil"},
    {"brand": "Pothys", "tagline": "Aalayam of Silks", "theme": "Wedding collection, grand shopping", "language": "Tamil"},
    {"brand": "Arusuvai Arasu", "tagline": "King of Catering", "theme": "Mouth watering food, rituals", "language": "Tamil"},
    {"brand": "MTR", "tagline": "Authentic Taste", "theme": "Ready to eat, Rava Idli", "language": "Tamil"},
    {"brand": "Horlicks", "tagline": "Taller, Stronger, Sharper", "theme": "Exam time, morning energy", "language": "Tamil"},
    {"brand": "Fair & Lovely", "tagline": "Glow & Lovely", "theme": "Confidence, skin glow", "language": "Tamil"},
    {"brand": "Boost", "tagline": "Secret of my energy", "theme": "Cricket training, kids", "language": "Tamil"},
    {"brand": "Santoor", "tagline": "Young skin", "theme": "Mom mistaken for sister", "language": "Tamil"},
    {"brand": "Cinthol", "tagline": "Alive is Awesome", "theme": "Morning bath, freshness", "language": "Tamil"},
    {"brand": "Clinic Plus", "tagline": "Strong Hair", "theme": "Mother daughter bond", "language": "Tamil"},
    {"brand": "Hamam", "tagline": "Go Safe Outside", "theme": "Protection, nature, soap", "language": "Tamil"},
    {"brand": "Gold Winner", "tagline": "Healthy Heart", "theme": "Cooking oil, family care", "language": "Tamil"},
    {"brand": "Parachute", "tagline": "Nurture with Love", "theme": "Coconut oil, tradition", "language": "Tamil"},
    {"brand": "Bru Coffee", "tagline": "A lot can happen", "theme": "Rainy day, bonding", "language": "Tamil"},

    # --- MALAYALAM (25 Seeds) ---
    {"brand": "Manappuram Finance", "tagline": "Make Life Easy", "theme": "Gold loan, business dreams", "language": "Malayalam"},
    {"brand": "Elite Foods", "tagline": "Experience Goodness", "theme": "Bread, breakfast, kids", "language": "Malayalam"},
    {"brand": "Manorama News", "tagline": "Truth First", "theme": "Breaking news, credibility", "language": "Malayalam"},
    {"brand": "Milma", "tagline": "The Spirit of Kerala", "theme": "Milk, early morning, village", "language": "Malayalam"},
    {"brand": "Eastern Spices", "tagline": "The Masters of Kerala Spices", "theme": "Sambar, Onam Sadhya", "language": "Malayalam"},
    {"brand": "South Indian Bank", "tagline": "Next Generation Banking", "theme": "NRI services, family support", "language": "Malayalam"},
    {"brand": "Kalyan Silks", "tagline": "Tradition in every thread", "theme": "Saree, wedding, festive", "language": "Malayalam"},
    {"brand": "Jos Alukkas", "tagline": "Gold for generations", "theme": "Jewellery, trust, inheritance", "language": "Malayalam"},
    {"brand": "Kerala Tourism", "tagline": "God's Own Country", "theme": "Nature, backwaters, peace", "language": "Malayalam"},
    {"brand": "Asianet", "tagline": "The heart of Kerala", "theme": "Media, news, entertainment", "language": "Malayalam"},
    {"brand": "Nirapara", "tagline": "Quality you can trust", "theme": "Rice, traditional meal", "language": "Malayalam"},
    {"brand": "Double Horse", "tagline": "Authentic Kerala Taste", "theme": "Palada Payasam, feast", "language": "Malayalam"},
    {"brand": "Federal Bank", "tagline": "Your perfect banking partner", "theme": "Digital banking, simplicity", "language": "Malayalam"},
    {"brand": "Oxygen Digital Shop", "tagline": "Smart Choice", "theme": "Electronics, gadgets, deals", "language": "Malayalam"},
    {"brand": "Bismi", "tagline": "Connect with Trust", "theme": "Home appliances, shopping", "language": "Malayalam"},
    {"brand": "Mathrubhumi", "tagline": "The silent revolution", "theme": "Reading habit, culture", "language": "Malayalam"},
    {"brand": "Paragon Footwear", "tagline": "Walk with Style", "theme": "Durability, monsoon, office", "language": "Malayalam"},
    {"brand": "Lunar", "tagline": "Step into comfort", "theme": "School shoes, kids", "language": "Malayalam"},
    {"brand": "Preethi Mixer", "tagline": "Kitchen expert", "theme": "Fast cooking, busy morning", "language": "Malayalam"},
    {"brand": "Peevees", "tagline": "Sweet dreams", "theme": "Mattress, comfort, sleep", "language": "Malayalam"},
    {"brand": "V-Guard", "tagline": "Protects for life", "theme": "Voltage stabilizer, safety", "language": "Malayalam"},
    {"brand": "Malayala Manorama", "tagline": "The daily companion", "theme": "Morning ritual, coffee", "language": "Malayalam"},
    {"brand": "Joyalukkas", "tagline": "World's favorite jeweler", "theme": "Diamonds, elegance", "language": "Malayalam"},
    {"brand": "Aline", "tagline": "Fashion for you", "theme": "Textile, dress, youth", "language": "Malayalam"},
    {"brand": "Mazzone", "tagline": "Tasty treats", "theme": "Cakes, pastries, celebration", "language": "Malayalam"},

    # --- MARATHI (25 Seeds) ---
    {"brand": "Vasu Bar", "tagline": "Swadeshi Shuddhata", "theme": "Village soap, purity", "language": "Marathi"},
    {"brand": "Chitale Bandhu", "tagline": "Taste of Pune", "theme": "Bakarwadi, snacks", "language": "Marathi"},
    {"brand": "Mala's Juices", "tagline": "Nature in a Bottle", "theme": "Mahabaleshwar, fruit juice", "language": "Marathi"},
    {"brand": "Jio", "tagline": "Digital Life", "theme": "Connectivity in villages", "language": "Marathi"},
    {"brand": "Su hana Masala", "tagline": "Zanzanit Taste", "theme": "Kolhapuri Misal, spice", "language": "Marathi"},
    {"brand": "Parle-G", "tagline": "G Maane Genius", "theme": "Childhood memory, tea time", "language": "Marathi"},
    {"brand": "Asian Paints", "tagline": "Har Ghar Kuch Kehta Hai", "theme": "Home, colors, emotional", "language": "Marathi"},
    {"brand": "Maharashtra Tourism", "tagline": "Unlimited", "theme": "Travel, heritage, pride", "language": "Marathi"},
    {"brand": "Saraswat Bank", "tagline": "Service to the common man", "theme": "Trust, local banking", "language": "Marathi"},
    {"brand": "Kansai Nerolac", "tagline": "Colours of Life", "theme": "Ganpati festival decoration", "language": "Marathi"},
    {"brand": "Idea", "tagline": "An idea can change your life", "theme": "Connectivity, sharing", "language": "Marathi"},
    {"brand": "Bajaj Auto", "tagline": "The World's Favorite Indian", "theme": "Pulsar, youth, speed", "language": "Marathi"},
    {"brand": "Mahindra", "tagline": "Rise", "theme": "Tractors, farming, progress", "language": "Marathi"},
    {"brand": "Amul Ice Cream", "tagline": "Real Milk", "theme": "Family outings, summer", "language": "Marathi"},
    {"brand": "Fevicol", "tagline": "Mazboot Jodd", "theme": "Strong bond, humor", "language": "Marathi"},
    {"brand": "Dettol", "tagline": "Dettol Dettol Ho", "theme": "Hygiene, protection", "language": "Marathi"},
    {"brand": "Colgate", "tagline": "Strong Teeth", "theme": "Confidence, smile", "language": "Marathi"},
    {"brand": "Lifebuoy", "tagline": "Help a Child Reach 5", "theme": "Handwash, health", "language": "Marathi"},
    {"brand": "Lux", "tagline": "Star Glow", "theme": "Beauty, elegance", "language": "Marathi"},
    {"brand": "Pears", "tagline": "Pure and Gentle", "theme": "Soft skin, kids", "language": "Marathi"},
    {"brand": "Cadbury Dairy Milk", "tagline": "Kuch Meetha Ho Jaaye", "theme": "Small joys, celebration", "language": "Marathi"},
    {"brand": "Kitkat", "tagline": "Have a break", "theme": "Work stress, relaxation", "language": "Marathi"},
    {"brand": "Google India", "tagline": "Helping India Progress", "theme": "Education, search, village", "language": "Marathi"},
    {"brand": "Samsung", "tagline": "Innovating for India", "theme": "Smartphone, camera, family", "language": "Marathi"},
    {"brand": "Amazon India", "tagline": "Apni Dukaan", "theme": "Delivery, variety, trust", "language": "Marathi"},

    # --- TELUGU (25 Seeds) ---
    {"brand": "Freedom Oil", "tagline": "Eat Healthy, Live Healthy", "theme": "Cooking, fitness", "language": "Telugu"},
    {"brand": "Maaza", "tagline": "Har Mausam Aam", "theme": "Mango love, summer", "language": "Telugu"},
    {"brand": "Apollo Hospitals", "tagline": "Touching Lives", "theme": "Healthcare, family care", "language": "Telugu"},
    {"brand": "Heritage Milk", "tagline": "Fresh and Healthy", "theme": "Milk, calcium, growth", "language": "Telugu"},
    {"brand": "Ramoji Film City", "tagline": "World of Wonder", "theme": "Tourism, cinema magic", "language": "Telugu"},
    {"brand": "Asian Paints", "tagline": "Beautiful Homes", "theme": "Festive colors", "language": "Telugu"},
    {"brand": "Tanishq", "tagline": "Jewelry of trust", "theme": "Marriage rituals", "language": "Telugu"},
    {"brand": "Kalyan Jewellers", "tagline": "Buy with trust", "theme": "Family heirloom", "language": "Telugu"},
    {"brand": "GRT Jewellers", "tagline": "Purity of Gold", "theme": "Traditional wear", "language": "Telugu"},
    {"brand": "South Indian Bank", "tagline": "Local support", "theme": "Small business loan", "language": "Telugu"},
    {"brand": "Andhra Bank", "tagline": "Service for decades", "theme": "Farmers support", "language": "Telugu"},
    {"brand": "Eenadu", "tagline": "Heart of Telugu", "theme": "News, culture", "language": "Telugu"},
    {"brand": "Gemini TV", "tagline": "Entertainment at home", "theme": "Soap opera, family", "language": "Telugu"},
    {"brand": "Swayam Krushi", "tagline": "Hard work pays", "theme": "Inspiration", "language": "Telugu"},
    {"brand": "Maha Cements", "tagline": "Strong build", "theme": "Hardness, home foundation", "language": "Telugu"},
    {"brand": "Ultratech Cement", "tagline": "Engineers choice", "theme": "Solid building", "language": "Telugu"},
    {"brand": "Vicco Turmeric", "tagline": "Ayurvedic care", "theme": "Natural beauty", "language": "Telugu"},
    {"brand": "Priya Pickles", "tagline": "Taste of tradition", "theme": "Spicy mango pickle", "language": "Telugu"},
    {"brand": "Bhimavaram Pickles", "tagline": "Pure homemade", "theme": "Authentic spice", "language": "Telugu"},
    {"brand": "Dr. Reddy's", "tagline": "Health for all", "theme": "Medicine, trust", "language": "Telugu"},
    {"brand": "Airtel", "tagline": "Fastest network", "theme": "Streaming, video call", "language": "Telugu"},
    {"brand": "Vivo India", "tagline": "Perfect Selfie", "theme": "Camera, youth", "language": "Telugu"},
    {"brand": "Oppo India", "tagline": "Flash charge", "theme": "Speed, battery", "language": "Telugu"},
    {"brand": "Rapido", "tagline": "Fast ride", "theme": "Traffic, bike taxi", "language": "Telugu"},
    {"brand": "Swiggy", "tagline": "Order food online", "theme": "Hunger, quick delivery", "language": "Telugu"},

    # --- KANNADA (25 Seeds) ---
    {"brand": "Nandini Milk", "tagline": "Pure and Healthy", "theme": "Morning routine, coffee", "language": "Kannada"},
    {"brand": "Mysore Sandal Soap", "tagline": "The Fragrance of Karnataka", "theme": "Heritage, sandalwood", "language": "Kannada"},
    {"brand": "KSIC Mysore Silk", "tagline": "The Royal Silk", "theme": "Wedding, elegance", "language": "Kannada"},
    {"brand": "Karnataka Bank", "tagline": "Your Family Bank", "theme": "Trust, rural banking", "language": "Kannada"},
    {"brand": "MTR", "tagline": "Authentic Taste", "theme": "Breakfast, tradition, Rava Idli", "language": "Kannada"},
    {"brand": "Zepto", "tagline": "Quick Commerce", "theme": "Bangalore traffic, fast delivery", "language": "Kannada"},
    {"brand": "BigBasket", "tagline": "Freshness delivered", "theme": "Convenience, grocery, home", "language": "Kannada"},
    {"brand": "KRS Cements", "tagline": "Strength of KRS", "theme": "Solid dam, construction", "language": "Kannada"},
    {"brand": "Brigade Group", "tagline": "Building trust", "theme": "Real estate, apartement", "language": "Kannada"},
    {"brand": "VRL Travels", "tagline": "Service with safely", "theme": "Road trip, bus travel", "language": "Kannada"},
    {"brand": "Airavata AC Bus", "tagline": "Comfort journey", "theme": "Luxury travel", "language": "Kannada"},
    {"brand": "Namma Metro", "tagline": "Life in Bangalore", "theme": "Connectivity, traffic solution", "language": "Kannada"},
    {"brand": "Karnataka Tourism", "tagline": "One State, Many Worlds", "theme": "Hampi, heritage", "language": "Kannada"},
    {"brand": "Udayavani", "tagline": "Voice of People", "theme": "News, reliability", "language": "Kannada"},
    {"brand": "Prajavani", "tagline": "Truth in every word", "theme": "Morning news", "language": "Kannada"},
    {"brand": "Sangeetha Mobiles", "tagline": "Trust of decades", "theme": "Mobile shopping", "language": "Kannada"},
    {"brand": "Poorvika Mobiles", "tagline": "Best deals", "theme": "Gadgets, offers", "language": "Kannada"},
    {"brand": "Incredible India", "tagline": "Explore", "theme": "Jog falls, nature", "language": "Kannada"},
    {"brand": "Himalaya Wellness", "tagline": "Pure happiness", "theme": "Face wash, natural", "language": "Kannada"},
    {"brand": "Wildcraft", "tagline": "Adventure awaits", "theme": "Backpacks, trekking", "language": "Kannada"},
    {"brand": "PhonePe", "tagline": "Easy payment", "theme": "Vendor payment, scan QR", "language": "Kannada"},
    {"brand": "Ola Cabs", "tagline": "Chalo Ola", "theme": "City travel, apps", "language": "Kannada"},
    {"brand": "Dunzo", "tagline": "Get it done", "theme": "Pick and drop", "language": "Kannada"},
    {"brand": "Cult.fit", "tagline": "Fitness made fun", "theme": "Workout, health", "language": "Kannada"},
    {"brand": "Kosh", "tagline": "Grain goodness", "theme": "Healthy food", "language": "Kannada"},

    # --- BENGALI (25 Seeds) ---
    {"brand": "Senco Gold", "tagline": "The Karigari of Bengal", "theme": "Durga Puja, jewellery", "language": "Bengali"},
    {"brand": "Boroline", "tagline": "The Magic Cream", "theme": "Winter protection, tradition", "language": "Bengali"},
    {"brand": "Sunrise Masala", "tagline": "The Taste of Bengal", "theme": "Fish curry, spices", "language": "Bengali"},
    {"brand": "Britannia Marie Gold", "tagline": "Teatime partner", "theme": "Evening adda, biscuits", "language": "Bengali"},
    {"brand": "Flipkart", "tagline": "Fashion Hub", "theme": "Durga Puja fashion, savings", "language": "Bengali"},
    {"brand": "Tata Tea", "tagline": "Jaago Re", "theme": "Morning habits, social talk", "language": "Bengali"},
    {"brand": "Wow! Momo", "tagline": "Wow in every bite", "theme": "Indulgence, street food, youth", "language": "Bengali"},
    {"brand": "East India Pharmaceutical", "tagline": "Health for generations", "theme": "BoroPlus, safety", "language": "Bengali"},
    {"brand": "Anandabazar Patrika", "tagline": "The daily guide", "theme": "News, literature", "language": "Bengali"},
    {"brand": "ABP Ananda", "tagline": "Truth First", "theme": "Live news, debate", "language": "Bengali"},
    {"brand": "Bikaji", "tagline": "Amit Ji ka favorite", "theme": "Chanachur, snacks", "language": "Bengali"},
    {"brand": "Pran Foods", "tagline": "Natural taste", "theme": "Juice, snacks", "language": "Bengali"},
    {"brand": "Bandhan Bank", "tagline": "Hope for all", "theme": "Micro finance, success", "language": "Bengali"},
    {"brand": "UCO Bank", "tagline": "Honors your trust", "theme": "Old heritage banking", "language": "Bengali"},
    {"brand": "Biswa Bangla", "tagline": "Brand of Bengal", "theme": "Handloom, pride", "language": "Bengali"},
    {"brand": "Aakash Institute", "tagline": "Path to success", "theme": "Education, coaching", "language": "Bengali"},
    {"brand": "Zomato", "tagline": "Food cravings", "theme": "Rainy afternoon, khichuri", "language": "Bengali"},
    {"brand": "Coca-Cola", "tagline": "Open happiness", "theme": "Puja celebration, friends", "language": "Bengali"},
    {"brand": "Horlicks", "tagline": "Health drink", "theme": "Student life", "language": "Bengali"},
    {"brand": "Pantaloons", "tagline": "Fresh fashion", "theme": "New clothes for Puja", "language": "Bengali"},
    {"brand": "Shoppers Stop", "tagline": "Premium style", "theme": "Grand shopping", "language": "Bengali"},
    {"brand": "ITC Yippee", "tagline": "Long Noodles", "theme": "Kids fun", "language": "Bengali"},
    {"brand": "Kitchen Treasures", "tagline": "Authentic spice", "theme": "Cooking", "language": "Bengali"},
    {"brand": "Amul Milk", "tagline": "Taste of India", "theme": "Early morning delivery", "language": "Bengali"},
    {"brand": "Life Insurance", "tagline": "Zindagi ke saath bhi", "theme": "Future security", "language": "Bengali"},

    # --- GUJARATI (25 Seeds) ---
    {"brand": "Wagh Bakri", "tagline": "Hamesha Rishto Ki Garmahat", "theme": "Family tea time, bonding", "language": "Gujarati"},
    {"brand": "Astral Pipes", "tagline": "Strong and Durable", "theme": "Strength, trust", "language": "Gujarati"},
    {"brand": "Fortune Oil", "tagline": "Ghar ka Khana", "theme": "Health, taste, Gujarati snacks", "language": "Gujarati"},
    {"brand": "Amul Ice Cream", "tagline": "Real Milk. Real Ice Cream.", "theme": "Summer, happiness, family", "language": "Gujarati"},
    {"brand": "Gopal Namkeen", "tagline": "Taste of Gujarat", "theme": "Evening snack, Gathiya", "language": "Gujarati"},
    {"brand": "Balaji Wafers", "tagline": "Always Fresh", "theme": "Crispy chips, youth", "language": "Gujarati"},
    {"brand": "Reliance Industries", "tagline": "Growth is Life", "theme": "Legacy, business pride", "language": "Gujarati"},
    {"brand": "Adani Group", "tagline": "Nation Building", "theme": "Infrastructure, power", "language": "Gujarati"},
    {"brand": "Harsiddhi Cements", "tagline": "Strong as Rock", "theme": "Home building", "language": "Gujarati"},
    {"brand": "Ajanta Clocks", "tagline": "Keep Moving", "theme": "Punctuality, family time", "language": "Gujarati"},
    {"brand": "Sandesh News", "tagline": "Fastest news", "theme": "Regional news, events", "language": "Gujarati"},
    {"brand": "Divya Bhaskar", "tagline": "Knowledge is power", "theme": "Daily reading habit", "language": "Gujarati"},
    {"brand": "Gujarat Tourism", "tagline": "Khushboo Gujarat Ki", "theme": "Rann Utsav, Gir Lions", "language": "Gujarati"},
    {"brand": "Sardar Sarovar", "tagline": "Lifeline of Gujarat", "theme": "Water, prosperity", "language": "Gujarati"},
    {"brand": "Tata Motors", "tagline": "Connecting Aspirations", "theme": "Tiago, safe cars", "language": "Gujarati"},
    {"brand": "Maruti Suzuki", "tagline": "Trusted by millions", "theme": "Alto, middle class dream", "language": "Gujarati"},
    {"brand": "Havmor Ice Cream", "tagline": "Heart's delight", "theme": "Dessert, flavor", "language": "Gujarati"},
    {"brand": "Cadbury Celebrations", "tagline": "Kuch Meetha Ho Jaaye", "theme": "Raksha Bandhan", "language": "Gujarati"},
    {"brand": "Ariel", "tagline": "Share the load", "theme": "Equal household", "language": "Gujarati"},
    {"brand": "Vim Bar", "tagline": "Clean and Shiny", "theme": "Vessels cleaning", "language": "Gujarati"},
    {"brand": "Dettol", "tagline": "Be 100% sure", "theme": "Health and hygiene", "language": "Gujarati"},
    {"brand": "Loreal India", "tagline": "Because you're worth it", "theme": "Skin care", "language": "Gujarati"},
    {"brand": "Nykaa", "tagline": "Beauty at doorstep", "theme": "Cosmetics shopping", "language": "Gujarati"},
    {"brand": "Urban Company", "tagline": "Service at home", "theme": "AC repair, salon", "language": "Gujarati"},
    {"brand": "Yatra.com", "tagline": "Create memories", "theme": "Family vacation", "language": "Gujarati"},

    # --- PUNJABI (25 Seeds) ---
    {"brand": "Verka", "tagline": "Taste of Punjab", "theme": "Lassi, tradition, energy", "language": "Punjabi"},
    {"brand": "Hershey's India", "tagline": "Moments of Happiness", "theme": "Chocolate, love, celebration", "language": "Punjabi"},
    {"brand": "Ambuja Cement", "tagline": "Giant Compressive Strength", "theme": "Strength, home building", "language": "Punjabi"},
    {"brand": "Hero MotoCorp", "tagline": "Hum Mein Hai Hero", "theme": "Pride, riding, friendship", "language": "Punjabi"},
    {"brand": "Bonn Bread", "tagline": "Health and Taste", "theme": "Healthy breakfast", "language": "Punjabi"},
    {"brand": "Markfed Sohna", "tagline": "Purity of Punjab", "theme": "Pure Honey, Ghee", "language": "Punjabi"},
    {"brand": "Chandigarh Tourism", "tagline": "City Beautiful", "theme": "Rock garden, clean city", "language": "Punjabi"},
    {"brand": "Jagbani", "tagline": "Voice of Punjab", "language": "Punjabi", "theme": "Local news"},
    {"brand": "Ajit Newspaper", "tagline": "Truth above all", "theme": "Morning routine", "language": "Punjabi"},
    {"brand": "Royal Enfield", "tagline": "Made Like a Gun", "theme": "Bullet, swagger, pride", "language": "Punjabi"},
    {"brand": "Mahindra Thar", "tagline": "Explore the Impossible", "theme": "Off-roading, style", "language": "Punjabi"},
    {"brand": "JCB India", "tagline": "Innovation at work", "theme": "Construction sites", "language": "Punjabi"},
    {"brand": "Coca-Cola", "tagline": "Thanda Matlab", "theme": "Wedding party, fun", "language": "Punjabi"},
    {"brand": "Pepsi", "tagline": "Yeh Dil Maange More", "theme": "Youth, college life", "language": "Punjabi"},
    {"brand": "Sprite", "tagline": "Clear hai", "theme": "Direct talk, honesty", "language": "Punjabi"},
    {"brand": "Nike India", "tagline": "Just Do It", "theme": "Running in fields, sports", "language": "Punjabi"},
    {"brand": "Adidas India", "tagline": "Impossible is Nothing", "theme": "Training hard", "language": "Punjabi"},
    {"brand": "Puma India", "tagline": "Fastest", "theme": "Athletic spirit", "language": "Punjabi"},
    {"brand": "Skechers India", "tagline": "Comfort always", "theme": "Walking, daily wear", "language": "Punjabi"},
    {"brand": "Bata India", "tagline": "Surprisingly Bata", "theme": "Formal shoes, style", "language": "Punjabi"},
    {"brand": "Raymond", "tagline": "Complete Man", "theme": "Elegant suit, wedding", "language": "Punjabi"},
    {"brand": "Peter England", "tagline": "Honest price", "theme": "Office wear, youth", "language": "Punjabi"},
    {"brand": "Louis Philippe", "tagline": "Upper Crest", "theme": "Premium lifestyle", "language": "Punjabi"},
    {"brand": "Van Heusen", "tagline": "Power dressing", "theme": "Success, confidence", "language": "Punjabi"},
    {"brand": "Pantaloons", "tagline": "Play with fashion", "theme": "Festive sale", "language": "Punjabi"},

    # --- ODIA (25 Seeds) ---
    {"brand": "Asian Paints", "tagline": "Har Ghar Kuch Kehta Hai", "theme": "Home, pride", "language": "Odia"},
    {"brand": "Odisha Tourism", "tagline": "Scenic Odisha", "theme": "Jagannath Puri, coastline", "language": "Odia"},
    {"brand": "Falcon Marine", "tagline": "Quality Seafood", "theme": "Freshness, exports", "language": "Odia"},
    {"brand": "OTDC", "tagline": "Delicious Odisha", "theme": "Pakhala Bhata, tradition", "language": "Odia"},
    {"brand": "Boyanika", "tagline": "Heritage of Odisha", "theme": "Sambalpuri Saree, handloom", "language": "Odia"},
    {"brand": "Nalco India", "tagline": "Aluminum of pride", "theme": "Industrial growth", "language": "Odia"},
    {"brand": "OMFED", "tagline": "Milk of Odisha", "theme": "Morning tea, healthy milk", "language": "Odia"},
    {"brand": "Sambad", "tagline": "First and Best", "theme": "Credible news", "language": "Odia"},
    {"brand": "Dharitri", "tagline": "Voice of people", "theme": "Authentic info", "language": "Odia"},
    {"brand": "Kalinga TV", "tagline": "Fearless news", "theme": "Current affairs", "language": "Odia"},
    {"brand": "Odia Film", "tagline": "Ollywood magic", "theme": "Family drama", "language": "Odia"},
    {"brand": "Ruchi Masala", "tagline": "Kitchen partner", "theme": "Spicy curry", "language": "Odia"},
    {"brand": "Bhagirathi Masala", "tagline": "Taste of home", "theme": "Traditional spices", "language": "Odia"},
    {"brand": "Utkal Cements", "tagline": "Strong Odisha", "theme": "Building home", "language": "Odia"},
    {"brand": "Biju Swasthya Kalyan", "tagline": "Health for all", "theme": "Medical support", "language": "Odia"},
    {"brand": "Mission Shakti", "tagline": "Empowering women", "theme": "SHG success stories", "language": "Odia"},
    {"brand": "Zomato India", "tagline": "Hungry?", "theme": "Late night Biryani", "language": "Odia"},
    {"brand": "Uber India", "tagline": "Ride with safety", "theme": "Easy travel", "language": "Odia"},
    {"brand": "V-Guard India", "tagline": "Smart protecting", "theme": "Inverter, power cut", "language": "Odia"},
    {"brand": "Syska LED", "tagline": "Save energy", "theme": "Bright lights", "language": "Odia"},
    {"brand": "Orient Fans", "tagline": "Live fresh", "theme": "Cool air", "language": "Odia"},
    {"brand": "Havells India", "tagline": "Shock laga?", "theme": "Safe wiring", "language": "Odia"},
    {"brand": "Bajaj Electricals", "tagline": "Inspiring trust", "theme": "Home devices", "language": "Odia"},
    {"brand": "Phillips India", "tagline": "Innovation for you", "theme": "Beard trimmer, styling", "language": "Odia"},
    {"brand": "Gillette India", "tagline": "Best a man can get", "theme": "Smooth shave, confidence", "language": "Odia"},
]

EXAMPLES = {
    "Hindi": """Input: Brand: Amul | Theme: Trust
Output: [CONTEXT]: A middle-class kitchen.
[VISUAL]: Mom making paratha, putting Amul butter.
[AUDIO/DIALOGUE]: माँ: "असली स्वाद तो अमूल में ही है!"
[TAGLINE]: Amul - The Taste of India.""",
    "Tamil": """Input: Brand: Swiggy | Theme: Hunger
Output: [CONTEXT]: Late night study room.
[VISUAL]: Student hungry, opening Swiggy app.
[AUDIO/DIALOGUE]: மாணவன்: "பசிக்குதா? ஸ்விக்கி இருக்கு!"
[TAGLINE]: Swiggy - Order Now.""",
    "Malayalam": """Input: Brand: Kalyan Jewellers | Theme: Wedding
Output: [CONTEXT]: Wedding hall in Kerala.
[VISUAL]: Bride wearing gold jewellery.
[AUDIO/DIALOGUE]: അച്ഛൻ: "ഇത് കല്യാണിന്റെ വിശ്വാസം."
[TAGLINE]: Kalyan Jewellers - Trust is Everything.""",
    "Marathi": """Input: Brand: Chitale | Theme: Snacks
Output: [CONTEXT]: Pune street scene.
[VISUAL]: Friends eating Bakarwadi.
[AUDIO/DIALOGUE]: मित्र: "चितळेंची बाकरवडी, सर्वात भारी!"
[TAGLINE]: Chitale Bandhu - Tradition of Taste.""",
    "Telugu": """Input: Brand: Heritage | Theme: Health
Output: [CONTEXT]: Early morning home.
[VISUAL]: Kid drinking milk, looking strong.
[AUDIO/DIALOGUE]: తల్లి: "హెరిటేజ్ పాలు, ఆరోగ్యం మెండు!"
[TAGLINE]: Heritage - Fresh and Healthy.""",
    "Bengali": """Input: Brand: Senco Gold | Theme: Festive
Output: [CONTEXT]: Durga Puja Pandal.
[VISUAL]: Woman in red saree with gold jewellery.
[AUDIO/DIALOGUE]: নারী: "পুজোর সাজ, সেঙ্কো গোল্ডের সাথে।"
[TAGLINE]: Senco Gold - The Art of Karigari.""",
    "Kannada": """Input: Brand: Nandini | Theme: Morning
Output: [CONTEXT]: Coffee shop in Bangalore.
[VISUAL]: Steam rising from Kaapi.
[AUDIO/DIALOGUE]: ಗ್ರಾಹಕ: "ನಂದಿನಿ ಹಾಲು, ಕಾಫಿ ಅದ್ಭುತ!"
[TAGLINE]: Nandini - Pure and Healthy.""",
    "Gujarati": """Input: Brand: Fortune | Theme: Snack
Output: [CONTEXT]: Gujarati kitchen setting.
[VISUAL]: Frying hot Gathiya.
[AUDIO/DIALOGUE]: નાસ્તો: "ફોર્ચ્યુન તેલ, સ્વાદમાં બેસ્ટ!"
[TAGLINE]: Fortune - Ab Har Ghar Banega Restaurant.""",
    "Punjabi": """Input: Brand: Verka | Theme: Energy
Output: [CONTEXT]: Punjab fields in afternoon.
[VISUAL]: Farmer drinking Lassi.
[AUDIO/DIALOGUE]: ਕਿਸਾਨ: "ਵੇਰਕਾ ਲੱਸੀ, ਪੰਜਾਬ ਦੀ ਸ਼ਾਨ!"
[TAGLINE]: Verka - Taste of Punjab.""",
    "Odia": """Input: Brand: Asian Paints | Theme: Home
Output: [CONTEXT]: Cuttack household.
[VISUAL]: Painting walls for Bali Jatra.
[AUDIO/DIALOGUE]: ବୋହୂ: "ଏସିଆନ୍ ପେଣ୍ଟସ୍, ଘରର ଚମକ!"
[TAGLINE]: Asian Paints - Har Ghar Kuch Kehta Hai."""
}

def is_native_script(text, language):
    """Simple regex check for native scripts"""
    patterns = {
        "Hindi": r'[\u0900-\u097F]',
        "Marathi": r'[\u0900-\u097F]',
        "Tamil": r'[\u0B80-\u0BFF]',
        "Malayalam": r'[\u0D00-\u0D7F]',
        "Telugu": r'[\u0C00-\u0C7F]',
        "Kannada": r'[\u0C80-\u0CFF]',
        "Bengali": r'[\u0980-\u09FF]',
        "Gujarati": r'[\u0A80-\u0AFF]',
        "Punjabi": r'[\u0A00-\u0A7F]',
        "Odia": r'[\u0B00-\u0B7F]'
    }
    return bool(re.search(patterns.get(language, r'.'), text))

def generate_script(seed):
    lang = seed['language']
    example = EXAMPLES.get(lang, EXAMPLES["Hindi"])
    
    prompt = f"""You are a top-tier Indian Ad Agency Creative Lead.
Write a cinematic, high-impact organic ad script for {seed['brand']}.

REFERENCE STYLE:
{example}

TASK:
Brand: {seed['brand']}
Tagline: {seed['tagline']}
Theme: {seed['theme']}
Language: {lang}

STRICT REQUIREMENTS:
1. DIALOGUE MUST be in the native {lang} script.
2. The script MUST strictly focus on {seed['brand']}.
3. Format MUST include exactly these headers: [CONTEXT], [VISUAL], [AUDIO/DIALOGUE], and [TAGLINE].
4. The tagline "{seed['tagline']}" MUST be included under the [TAGLINE] section.
5. Do NOT include any introductory or concluding remarks. Just the structured script.
"""

    try:
        response = ollama.generate(
            model=MODEL, 
            prompt=prompt, 
            options={
                "temperature": 0.3,
                "num_predict": 500,
                "top_p": 0.9
            }
        )
        content = response['response'].strip()
        has_tagline = "[TAGLINE]" in content
        is_native = is_native_script(content, lang)
        
        if has_tagline and is_native:
            return content
        else:
            print(f"  Fail Details - Tagline: {has_tagline}, Native Script: {is_native}")
            if not is_native:
                print(f"  Snippet: {content[:100]}...")
    except Exception as e:
        print(f"  Error: {e}")
    return None

def main():
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    else:
        dataset = []

    # Count existing per language to see gaps
    lang_counts = {}
    for item in dataset:
        l = item['response']['Language']
        lang_counts[l] = lang_counts.get(l, 0) + 1
    
    print(f"Current stats: {lang_counts}")

    existing_keys = [f"{item['response']['Brand']}_{item['response']['Language']}" for item in dataset]

    for seed in SEEDS:
        key = f"{seed['brand']}_{seed['language']}"
        if key in existing_keys:
            continue
            
        print(f"[{seed['language']}] Generating for {seed['brand']}...")
        script = generate_script(seed)
        
        if script:
            entry = {
                "instruction": f"Write an organic advertisement for {seed['brand']} in {seed['language']} with theme {seed['theme']}.",
                "response": {
                    "Brand": seed['brand'],
                    "Language": seed['language'],
                    "Theme": seed['theme'],
                    "Content": script
                }
            }
            dataset.append(entry)
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print(f"  Success.")
            time.sleep(1)
        else:
            print(f"  Failed (Format/Language check).")

    print(f"Final Dataset Size: {len(dataset)}")

if __name__ == "__main__":
    main()
