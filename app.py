from flask import Flask, request, jsonify, render_template
from googletrans import Translator

app = Flask(__name__)

# Initialize the Google Translate API
translator = Translator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    source_language = data.get("source_language", "en").strip()
    target_language = data.get("target_language", "en").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Translate text using Google Translate API
        translated = translator.translate(text, src=source_language, dest=target_language)
        translated_text = translated.text

        # Sentiment analysis (basic keyword-based)
        positive_keywords = [
    "happy", "joy", "love", "awesome", "great", "good", "fantastic", "excellent", 
    "amazing", "wonderful", "excited", "glad", "pleased", "satisfied", "positive", 
    "beautiful", "delightful", "enthusiastic", "cheerful", "grateful", "hopeful", 
    "content", "ecstatic", "elated", "proud", "successful", "uplifting", "radiant", 
    "breathtaking", "charming", "elegant", "outstanding", "spectacular", "graceful", 
    "fabulous", "brilliant", "kind", "friendly", "supportive", "helpful", "joyful", 
    "motivated", "peaceful", "inspired", "victorious", "thrilled", "optimistic", 
    "passionate", "trustworthy", "magnificent", "humble", "remarkable", "adorable", 
    "blissful", "gracious", "vibrant", "cheery", "fun", "playful"
]

        negative_keywords = [
    "sad", "bad", "terrible", "awful", "hate", "angry", "horrible", "die", 
    "death", "ugly", "disgusting", "dislike", "unhappy", "displeased", 
    "dissatisfied", "negative", "worst", "depressing", "gloomy", "hopeless", 
    "miserable", "painful", "fear", "anxiety", "lonely", "regret", "loss", 
    "failure", "betrayal", "heartbroken", "cruel", "disappointing", "nasty", 
    "desperate", "jealous", "ashamed", "embarrassed", "frustrated", "irritated", 
    "panicked", "rejected", "sorrowful", "unforgiving", "angst", "worry", 
    "troubled", "uncomfortable", "hostile", "selfish", "arrogant", "harmful", 
    "aggressive", "mean", "vindictive", "detestable", "vengeful", "unfair", 
    "pessimistic", "annoying", "fearful", "traumatized", "grief", "unfortunate"
]

        neutral_keywords = [
    "okay", "fine", "average", "normal", "ordinary", "regular", "standard", 
    "typical", "common", "routine", "usual", "fair", "adequate", "mediocre", 
    "so-so", "balanced", "moderate", "acceptable", "indifferent", "generic", 
    "middle", "plain", "simple", "unremarkable", "everyday", "reasonable", 
    "neither", "equal", "satisfactory", "midway", "neutral", "objective", 
    "unbiased", "reserved", "conventional", "mild", "stable", "functional", 
    "practical", "level", "calm", "unassuming", "reserved", "unexciting", 
    "predictable", "consistent", "steady", "safe", "tolerable", "nonchalant", 
    "passive", "unconcerned", "routine", "balanced", "average-looking", 
    "unspecified", "uncertain", "ambivalent", "controlled", "formal", "casual", 
    "standardized", "expected"
]


        sentiment = "neutral"
        lower_text = text.lower()
        if any(keyword in lower_text for keyword in positive_keywords):
            sentiment = "positive"
        elif any(keyword in lower_text for keyword in negative_keywords):
            sentiment = "negative"

        return jsonify({
            "translated_text": translated_text,
            "sentiment": sentiment
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
