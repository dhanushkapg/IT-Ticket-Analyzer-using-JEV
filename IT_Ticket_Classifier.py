import os

from dotenv import load_dotenv
from typesafe_sdk import Choice, Score, TypeSafeClient


# Load environment variables
load_dotenv()

api_key = os.getenv("TYPESAFE_API_KEY")

if not api_key:
    raise ValueError(
        "TYPESAFE_API_KEY environment variable not set"
    )


def analyze_ticket(ticket_text):

    with TypeSafeClient() as client:

        response = client.system_one(

            state={
                "ticket": ticket_text
            },

            questions={

                # Category
                "category": Choice(
                    instructions="What type of IT issue is this?",
                    criteria={
                        "network": "VPN or network issue",
                        "hardware": "Physical hardware issue",
                        "software": "Application or software issue",
                        "account": "Login or password issue",
                        "other": "Other IT issue"
                    }
                ),

                # Urgency
                "urgency": Score(
                    instructions="How urgent is this IT support ticket?",
                    criteria=[
                        "Low - little or no immediate impact.",
                        "Medium - issue affects work but a workaround may exist.",
                        "High - significant impact on the user's work.",
                        "Critical - major business impact or critical service unavailable."
                    ]
                )
            }
        )

    # Get answers
    category = response.answers["category"]
    urgency = response.answers["urgency"]

    # Urgency labels
    urgency_levels = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    # Find highest probability urgency
    probabilities = urgency.probabilities

    most_likely_level = max(
        probabilities,
        key=probabilities.get
    )

    urgency_label = urgency_levels[
        int(most_likely_level)
    ]











    

    # Return results to Streamlit
    results = {
        "ticket": ticket_text.strip(),

        "category": category.choice,

        "category_confidence":
            category.confidence,

        "category_probabilities":
            category.probabilities,

        "urgency_score":
            urgency.score,

        "urgency_label":
            urgency_label,

        "urgency_confidence":
            urgency.confidence,

        "urgency_probabilities":
            urgency.probabilities
    }

    print("\n" + "=" * 50)
    print("       IT SUPPORT TICKET ANALYSIS")
    print("=" * 50)
    print(f"\n🎫 Ticket: {results['ticket']}")
    print(f"📂 Category: {results['category']}")
    print(f"🚨 Urgency: {results['urgency_label']}")
    print(f"📈 Urgency Score: {results['urgency_score']:.2f}")
    print(f"🎯 Category Confidence: {results['category_confidence']:.2%}")
    print(f"🎯 Urgency Confidence: {results['urgency_confidence']:.2%}")
    print("=" * 50)

    return results



