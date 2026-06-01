import nltk
import random
import string
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('punkt_tabular', quiet=True)

# ─── Restaurant Menu ─────────────────────────────────────────────

MENU = {
    "biryani":       {"price": 350, "description": "Mashoor Chicken Biryani, dum style"},
    "karahi":        {"price": 450, "description": "Tasty Chicken Karahi, taza masalay ke sath"},
    "burger":        {"price": 250, "description": "Crispy Chicken Burger with fries"},
    "pizza":         {"price": 550, "description": "Large Pizza, 4 flavors available"},
    "nihari":        {"price": 400, "description": "Beef Nihari, naan ke sath"},
    "chai":          {"price": 80,  "description": "Doodh Patti Chai"},
    "juice":         {"price": 150, "description": "Fresh fruit juice"},
    "ice cream":     {"price": 120, "description": "3 scoops, chocolate/vanilla/strawberry"},
    "pulao":         {"price": 300, "description": "Mutton Pulao, raita ke sath"},
    "sandwich":      {"price": 200, "description": "Club Sandwich with fries"},
}

# ─── Responses ───────────────────────────────────────────────────

GREETINGS = ["hello", "hi", "salam", "assalam", "hey", "helo"]
FAREWELLS  = ["bye", "goodbye", "alvida", "khuda hafiz", "exit", "quit"]
THANKS     = ["thanks", "thank", "shukriya", "شکریہ"]

GREETING_REPLIES = [
    "Salam! Cafe Ammar mein khush aamdeed 🍽️ Kya khaana chahoge?",
    "Hello! Aaj kya order karein? Menu dekhne ke liye 'menu' likhein.",
    "Hi there! Humara menu dekhne ke liye 'menu' type karein 😊",
]

FAREWELL_REPLIES = [
    "Khuda Hafiz! Phir aana 😊",
    "Shukriya visit karne ka! Aapka din acha guzray 🌟",
    "Alvida! Humein umeed hai aapko khana pasand aaya 🍽️",
]

THANKS_REPLIES = [
    "Koi baat nahi! Aur kuch chahiye? 😊",
    "Humare liye khushi ki baat hai! Kuch aur poochna ho toh batao.",
]

# ─── Helper Functions ─────────────────────────────────────────────

def show_menu():
    lines = ["\n📋 HAMARA MENU:\n" + "─"*35]
    for item, info in MENU.items():
        lines.append(f"  🍴 {item.capitalize():<15} Rs. {info['price']}")
    lines.append("─"*35)
    lines.append("Kisi item ki details ke liye naam likhein.")
    return "\n".join(lines)


def get_item_info(tokens):
    for token in tokens:
        if token in MENU:
            item = MENU[token]
            return (f"\n🍴 {token.capitalize()}\n"
                    f"   Description : {item['description']}\n"
                    f"   Price        : Rs. {item['price']}\n")
    return None


def get_price(tokens):
    for token in tokens:
        if token in MENU:
            return f"{token.capitalize()} ki price Rs. {MENU[token]['price']} hai. 💰"
    return None


def chatbot_response(user_input):
    # Lowercase + punctuation remove
    user_input = user_input.lower().translate(
        str.maketrans("", "", string.punctuation)
    )
    tokens = word_tokenize(user_input)

    # Greeting
    if any(t in GREETINGS for t in tokens):
        return random.choice(GREETING_REPLIES)

    # Farewell
    if any(t in FAREWELLS for t in tokens):
        return random.choice(FAREWELL_REPLIES)

    # Thanks
    if any(t in THANKS for t in tokens):
        return random.choice(THANKS_REPLIES)

    # Menu request
    if any(t in ["menu", "list", "kya", "sab", "available"] for t in tokens):
        return show_menu()

    # Price query
    if any(t in ["price", "kitna", "rate", "cost", "daam"] for t in tokens):
        response = get_price(tokens)
        if response:
            return response
        return "Kaunse item ki price jaanni hai? Menu ke liye 'menu' likhein."

    # Item detail
    item_info = get_item_info(tokens)
    if item_info:
        return item_info

    # Order
    if any(t in ["order", "chahiye", "lena", "do", "dena"] for t in tokens):
        item_info = get_item_info(tokens)
        if item_info:
            return f"✅ Order place ho gaya!\n{item_info}\nShukriya! Thodi der mein ready hoga. 🍽️"
        return "Kya order karna chahte ho? Item ka naam batao."

    # Hours / timing
    if any(t in ["time", "timing", "open", "close", "hours", "waqt"] for t in tokens):
        return "⏰ Humara restaurant subah 10 baje se raat 11 baje tak open rehta hai."

    # Location
    if any(t in ["address", "location", "kahan", "where"] for t in tokens):
        return "📍 Hamara address: Main Canteen Road, Sukkur. Google Maps par 'Cafe Ammar' search karein."

    # Default
    return ("Maafi chahta hoon, samjha nahi 😅\n"
            "Aap yeh pooch sakte hain:\n"
            "  • 'menu' — poora menu dekhein\n"
            "  • 'biryani price' — kisi item ki price\n"
            "  • 'burger' — item ki details\n"
            "  • 'timing' — opening hours")


# ─── Main Loop ───────────────────────────────────────────────────

def main():
    print("=" * 40)
    print("   🍽️  CAFE AMMAR - AI Chatbot  🍽️")
    print("=" * 40)
    print("Salam! Main aapka restaurant assistant hoon.")
    print("'bye' likhein exit karne ke liye.\n")

    while True:
        user_input = input("Aap: ").strip()
        if not user_input:
            continue

        response = chatbot_response(user_input)
        print(f"Bot: {response}\n")

        if any(t in user_input.lower() for t in FAREWELLS):
            break


if __name__ == "__main__":
    main()
