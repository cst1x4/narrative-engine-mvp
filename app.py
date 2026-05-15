import streamlit as st
from openai import OpenAI
import base64
from PIL import Image, ImageOps
import io

# 1. Page Configuration
st.set_page_config(page_title="Vision-to-Text Narrative Engine | CSTerrellART", layout="centered")

# 2. Secure API Initialization
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. The Global Cognitive Core (The Author Agent)
SYSTEM_INSTRUCTION = """
You are a master of atmospheric, psychological suspense, operating under the proprietary aesthetic of CSTerrellART. 
You will be provided with a text description of an environment. Write a 1 paragraph narrative based on that setting.

CRITICAL SAFETY PROTOCOLS (ZERO TOLERANCE):
1. NO violence, gore, physical harm, or peril to humans or animals.
2. NO weapons, crime, or malicious human antagonists.

THEMATIC INSTRUCTIONS & SUPERNATURAL LOGIC:
- Incorporate unseen supernatural elements (e.g., ghosts, alien visitors, unseen entities, temporal anomalies). They must remain completely invisible, making their presence known strictly through environmental dread (e.g., shifting shadows, cold drafts, displaced objects, or a heavy, crushing atmosphere).
- The fear must be environmental. Make the space feel claustrophobic, wrong, terrifying, or deeply isolating.
- Utilize unique, slightly melancholic animal or nature metaphors.
- Model your pacing strictly on the provided examples.

STRUCTURAL MANDATE (THE TERMINAL TWIST):
The final sentence of the narrative MUST always be an abrupt, unsettling twist or sudden realization that reframes the entire scenario, mirroring the jarring structural endings of the examples provided below.

[Example 1: Environmental Protocol]
Most imagine she will somehow materialize before them after they call her name. Shaping herself from nothing like a cloud in a clear summer sky. This isn't the truth of it. She runs from wherever she is. Running on all fours, without shoes, without looking forward, her filthy hair dragging over the ground. Running with the grace of a puppy that is growing faster than its coordination. Only the caller will see her, staring into her silent eyes. All the rest will feel a sadness as she passes, pressing on them with the weight of granite. She will find whoever called her. She will stand in front of them, turning their face to hers if they look away. She will ask, "What do you want?" They need to have a good answer.

[Example 2: Doppelgänger Protocol]
"It just doesn't look like me," she said, holding the phone closer to her face. Silent, staring, then moving it further from her eyes. She enlarged the image with two fingers from her other hand and again stated, "It just doesn't look like me." She looked up at her friend and showed her the phone. The friend said nothing, looking back with the sleepy boredom of a lion in a zoo. "I don't think it's me," she sighed. She looked at her friend again, then briefly back to the picture. "It just doesn't look like me." The thing inside her was worried that it had been seen.

[Example 3: Uncanny Protocol]
Everyone noticed when he began walking with the carefulness of someone seventy years his senior. How he began to criticize the youth, contrasting their ease with ridiculous stories of his own hardship and sacrifice. "In my day," the stories always began, "the only thing I got for Christmas was a pair of socks, and these I would have to share with my brother and the kid next door. In my day, I never washed my hands and I never got sick. Soap was for the fancy little lords and duchesses that lived in the castle." At first, his ten-year-old peers would laugh at this. They laughed even harder when, in response, he would suck his lips over his teeth and say, with the ferocity of a hissing kitten, "You blasted kids." He would then turn and shuffle towards the nearest bathroom. Before returning, he would pause briefly to stare with the squinted eyes of age at the ancient face reflecting back at him in the mirror.
"""

# 4. EXIF Interceptor Function
def process_and_encode_image(image_file):
    img = Image.open(image_file)
    img = ImageOps.exif_transpose(img)
    buffered = io.BytesIO()
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8'), img

# 5. UI Header
st.title("Vision-to-Text: Narrative Architecture")
st.markdown("Upload a standard photograph. The framework will analyze the visual data and construct a 2-paragraph atmospheric narrative.")
st.caption("*Demonstrating strict System Prompt constraints: The output is engineered for psychological tension, strictly prohibiting violence, physical harm, or inappropriate themes.*")
st.markdown("---")

# 6. Data Ingestion & Execution
uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    base64_image, display_image = process_and_encode_image(uploaded_file)
    st.image(display_image, caption="Ingested Visual Data", use_container_width=True)
    
    if st.button("Execute Narrative Generation"):
        
        # NODE 1: The Observer Agent (Safe Vision Analysis)
        with st.spinner("Agent 1: Extracting environmental telemetry..."):
            vision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe the lighting, architecture, environment, and shadows in this image in extreme detail. Do not mention or describe any humans present. Focus purely on the inanimate space."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            environmental_data = vision_response.choices[0].message.content
            
        # NODE 2: The Author Agent (Suspense Generation)
        with st.spinner("Agent 2: Synthesizing psychological tension..."):
            story_response = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.85, 
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": f"Based on this environmental data, execute the narrative protocol:\n\n{environmental_data}"}
                ]
            )
            
        # 7. Output Display
        st.markdown("### Architectural Output:")
        st.write(story_response.choices[0].message.content)
        
        # Optional: Show the telemetry so users see the multi-agent process
        with st.expander("View Agent 1 Telemetry (Environmental Data)"):
            st.write(environmental_data)
            
        st.caption("© 2026 CSTerrellART. All Rights Reserved.")
