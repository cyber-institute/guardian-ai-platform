"""
Document Translation Component with Language Flag Animations
One-click translation for GUARDIAN documents with animated language flags
"""

import streamlit as st
import requests
import time
from datetime import datetime

class DocumentTranslator:
    def __init__(self):
        self.supported_languages = {
            'en': {'name': 'English', 'flag': '🇺🇸', 'code': 'en'},
            'es': {'name': 'Spanish', 'flag': '🇪🇸', 'code': 'es'},
            'fr': {'name': 'French', 'flag': '🇫🇷', 'code': 'fr'},
            'de': {'name': 'German', 'flag': '🇩🇪', 'code': 'de'},
            'zh': {'name': 'Chinese', 'flag': '🇨🇳', 'code': 'zh'},
            'ja': {'name': 'Japanese', 'flag': '🇯🇵', 'code': 'ja'},
            'ko': {'name': 'Korean', 'flag': '🇰🇷', 'code': 'ko'},
            'ru': {'name': 'Russian', 'flag': '🇷🇺', 'code': 'ru'},
            'ar': {'name': 'Arabic', 'flag': '🇸🇦', 'code': 'ar'},
            'pt': {'name': 'Portuguese', 'flag': '🇵🇹', 'code': 'pt'},
            'it': {'name': 'Italian', 'flag': '🇮🇹', 'code': 'it'},
            'nl': {'name': 'Dutch', 'flag': '🇳🇱', 'code': 'nl'},
            'hi': {'name': 'Hindi', 'flag': '🇮🇳', 'code': 'hi'},
            'th': {'name': 'Thai', 'flag': '🇹🇭', 'code': 'th'},
            'vi': {'name': 'Vietnamese', 'flag': '🇻🇳', 'code': 'vi'}
        }
        
    def detect_language(self, text):
        """Detect the language of the input text"""
        # Simple language detection based on common words
        # In production, you would use a proper language detection service
        text_lower = text.lower()
        
        # English indicators
        if any(word in text_lower for word in ['the', 'and', 'of', 'to', 'a', 'in', 'is', 'it', 'you', 'that']):
            return 'en'
        # Spanish indicators
        elif any(word in text_lower for word in ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no']):
            return 'es'
        # French indicators
        elif any(word in text_lower for word in ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir']):
            return 'fr'
        # German indicators
        elif any(word in text_lower for word in ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich']):
            return 'de'
        # Default to English
        else:
            return 'en'
    
    def translate_text_google(self, text, target_lang, source_lang='auto'):
        """Translate text using Google Translate API"""
        api_key = st.secrets.get("GOOGLE_TRANSLATE_API_KEY")
        if not api_key:
            return None, "Google Translate API key not configured"
            
        url = f"https://translation.googleapis.com/language/translate/v2"
        params = {
            'key': api_key,
            'q': text,
            'target': target_lang,
            'source': source_lang
        }
        
        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                detected_lang = result['data']['translations'][0].get('detectedSourceLanguage', source_lang)
                return translated_text, detected_lang
            else:
                return None, f"Translation failed: {response.status_code}"
        except Exception as e:
            return None, f"Translation error: {str(e)}"
    
    def translate_text_libre(self, text, target_lang, source_lang='auto'):
        """Translate text using LibreTranslate (free alternative)"""
        url = "https://libretranslate.de/translate"
        data = {
            'q': text,
            'source': source_lang,
            'target': target_lang,
            'format': 'text'
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                return result['translatedText'], source_lang
            else:
                return None, f"Translation failed: {response.status_code}"
        except Exception as e:
            return None, f"Translation error: {str(e)}"
    
    def render_flag_animation(self, from_flag, to_flag, is_translating=False):
        """Render animated language flags during translation"""
        if is_translating:
            # Animated translation in progress
            animation_html = f"""
            <div style="display: flex; align-items: center; justify-content: center; margin: 10px 0;">
                <div style="font-size: 2em; animation: pulse 1s infinite;">{from_flag}</div>
                <div style="margin: 0 15px;">
                    <div style="font-size: 1.5em; animation: slide 2s infinite;">→</div>
                </div>
                <div style="font-size: 2em; animation: pulse 1s infinite reverse;">{to_flag}</div>
            </div>
            <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.2); opacity: 0.7; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            @keyframes slide {{
                0% {{ transform: translateX(-5px); }}
                50% {{ transform: translateX(5px); }}
                100% {{ transform: translateX(-5px); }}
            }}
            </style>
            """
        else:
            # Static flag display
            animation_html = f"""
            <div style="display: flex; align-items: center; justify-content: center; margin: 10px 0;">
                <div style="font-size: 2em;">{from_flag}</div>
                <div style="margin: 0 15px; font-size: 1.5em;">→</div>
                <div style="font-size: 2em;">{to_flag}</div>
            </div>
            """
        
        return animation_html
    
    def render_translation_interface(self, document_content, document_title="Document"):
        """Render the complete translation interface with flags and animations"""
        st.markdown("### 🌐 Document Translation")
        
        # Detect current language
        detected_lang = self.detect_language(document_content)
        current_lang_info = self.supported_languages.get(detected_lang, self.supported_languages['en'])
        
        st.markdown(f"**Detected Language:** {current_lang_info['flag']} {current_lang_info['name']}")
        
        # Language selection
        st.markdown("**Translate to:**")
        
        # Create language options with flags
        language_options = []
        language_codes = []
        
        for code, info in self.supported_languages.items():
            if code != detected_lang:  # Don't show current language
                language_options.append(f"{info['flag']} {info['name']}")
                language_codes.append(code)
        
        selected_idx = st.selectbox(
            "Choose target language",
            range(len(language_options)),
            format_func=lambda x: language_options[x],
            label_visibility="collapsed"
        )
        
        target_lang_code = language_codes[selected_idx]
        target_lang_info = self.supported_languages[target_lang_code]
        
        # Translation button with animation
        if st.button(f"🔄 Translate to {target_lang_info['name']}", key=f"translate_{document_title}"):
            # Show animation
            animation_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with animation_placeholder.container():
                st.markdown(
                    self.render_flag_animation(
                        current_lang_info['flag'], 
                        target_lang_info['flag'], 
                        is_translating=True
                    ),
                    unsafe_allow_html=True
                )
            
            with status_placeholder:
                st.info(f"🔄 Translating from {current_lang_info['name']} to {target_lang_info['name']}...")
            
            # Perform translation
            # Try Google Translate first, fallback to LibreTranslate
            translated_text, error = self.translate_text_google(
                document_content, target_lang_code, detected_lang
            )
            
            if not translated_text:
                # Fallback to LibreTranslate
                translated_text, error = self.translate_text_libre(
                    document_content, target_lang_code, detected_lang
                )
            
            # Clear animation and status
            animation_placeholder.empty()
            status_placeholder.empty()
            
            if translated_text:
                # Success animation
                st.markdown(
                    self.render_flag_animation(
                        current_lang_info['flag'], 
                        target_lang_info['flag'], 
                        is_translating=False
                    ),
                    unsafe_allow_html=True
                )
                
                st.success(f"✅ Translation completed!")
                
                # Store translation in session state
                translation_key = f"translation_{document_title}_{target_lang_code}"
                st.session_state[translation_key] = {
                    'original_text': document_content,
                    'translated_text': translated_text,
                    'source_lang': detected_lang,
                    'target_lang': target_lang_code,
                    'source_lang_name': current_lang_info['name'],
                    'target_lang_name': target_lang_info['name'],
                    'timestamp': datetime.now().isoformat()
                }
                
                # Display translation
                with st.expander(f"📄 Translated Content ({target_lang_info['flag']} {target_lang_info['name']})", expanded=True):
                    st.markdown(translated_text)
                
                # Download option
                st.download_button(
                    label=f"💾 Download Translation ({target_lang_info['flag']} {target_lang_info['name']})",
                    data=translated_text,
                    file_name=f"{document_title}_{target_lang_code}.txt",
                    mime="text/plain"
                )
                
            else:
                st.error(f"❌ Translation failed: {error}")
                
                # Show setup instructions if API key is missing
                if "API key not configured" in str(error):
                    with st.expander("🔧 Setup Translation Service"):
                        st.markdown("""
                        **To enable document translation, you need to configure a translation API:**
                        
                        **Option 1: Google Translate API (Recommended)**
                        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                        2. Enable the Cloud Translation API
                        3. Create an API key
                        4. Add `GOOGLE_TRANSLATE_API_KEY` to your secrets
                        
                        **Option 2: LibreTranslate (Free)**
                        - Uses the free LibreTranslate service (no API key required)
                        - May have rate limits and lower quality
                        """)
    
    def render_translation_history(self):
        """Display translation history for the current session"""
        translation_keys = [key for key in st.session_state.keys() if isinstance(key, str) and key.startswith("translation_")]
        
        if translation_keys:
            st.markdown("### 📚 Translation History")
            
            for key in sorted(translation_keys, reverse=True):
                translation = st.session_state[key]
                
                with st.expander(
                    f"{self.supported_languages[translation['source_lang']]['flag']} → "
                    f"{self.supported_languages[translation['target_lang']]['flag']} "
                    f"{translation['target_lang_name']} Translation"
                ):
                    st.markdown(f"**Original ({translation['source_lang_name']}):**")
                    st.text_area(
                        "Original", 
                        translation['original_text'][:500] + "...", 
                        height=100,
                        disabled=True,
                        key=f"orig_{key}"
                    )
                    
                    st.markdown(f"**Translation ({translation['target_lang_name']}):**")
                    st.text_area(
                        "Translation", 
                        translation['translated_text'][:500] + "...", 
                        height=100,
                        disabled=True,
                        key=f"trans_{key}"
                    )
                    
                    st.download_button(
                        label=f"💾 Download Full Translation",
                        data=translation['translated_text'],
                        file_name=f"translation_{translation['target_lang']}.txt",
                        mime="text/plain",
                        key=f"download_{key}"
                    )

def render_document_translation_button(document_content, document_title, doc_id):
    """Render a compact translation button for document cards"""
    translator = DocumentTranslator()
    
    # Compact translation button
    if st.button(f"🌐 Translate", key=f"translate_btn_{doc_id}"):
        # Store content for translation modal
        st.session_state[f"translate_content_{doc_id}"] = document_content
        st.session_state[f"translate_title_{doc_id}"] = document_title
        st.session_state[f"show_translation_{doc_id}"] = True
    
    # Show translation interface if requested
    if st.session_state.get(f"show_translation_{doc_id}", False):
        with st.container():
            st.markdown("---")
            translator.render_translation_interface(
                st.session_state[f"translate_content_{doc_id}"],
                st.session_state[f"translate_title_{doc_id}"]
            )
            
            if st.button("❌ Close Translation", key=f"close_translate_{doc_id}"):
                st.session_state[f"show_translation_{doc_id}"] = False
                st.rerun()