"""Locale management module for internationalization support."""

import os
import yaml
from typing import Dict, Optional


class Locale:
    """Manages application localization and internationalization."""
    
    def __init__(self, locale_dir: str = "Locale"):
        """Initialize the locale manager.
        
        Args:
            locale_dir: Directory containing locale files
        """
        self.locale_dir = locale_dir
        self.current_locale = self._detect_system_locale()
        self.translations: Dict[str, str] = {}
        self.load_translations()
    
    def _detect_system_locale(self) -> str:
        """Detect system locale from environment variables.
        
        Returns:
            Detected locale code (e.g., 'en', 'tr')
        """
        # Try to get locale from environment variables
        lang = os.environ.get('LANG', '').lower()
        lc_all = os.environ.get('LC_ALL', '').lower()
        
        # Check for Turkish locale
        if 'tr' in lang or 'tr' in lc_all:
            return 'tr'
        
        # Default to English
        return 'en'
    
    def load_translations(self) -> None:
        """Load translations for the current locale."""
        locale_file = os.path.join(self.locale_dir, f"{self.current_locale}.yml")
        
        try:
            with open(locale_file, 'r', encoding='utf-8') as file:
                self.translations = yaml.safe_load(file) or {}
        except FileNotFoundError:
            # Fallback to English if locale file not found
            if self.current_locale != 'en':
                self.current_locale = 'en'
                self.load_translations()
            else:
                self.translations = {}
        except Exception as e:
            print(f"Error loading locale file {locale_file}: {e}")
            self.translations = {}
    
    def get(self, key: str, **kwargs) -> str:
        """Get translated text for the given key.
        
        Args:
            key: Translation key
            **kwargs: Variables for string formatting
            
        Returns:
            Translated text
        """
        text = self.translations.get(key, key)
        
        try:
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, ValueError):
            return text
    
    def set_locale(self, locale: str) -> None:
        """Set the application locale.
        
        Args:
            locale: Locale code (e.g., 'en', 'tr')
        """
        if locale != self.current_locale:
            self.current_locale = locale
            self.load_translations()
    
    def get_available_locales(self) -> Dict[str, str]:
        """Get list of available locales.
        
        Returns:
            Dictionary of locale codes and their display names
        """
        locales = {}
        
        if os.path.exists(self.locale_dir):
            for file in os.listdir(self.locale_dir):
                if file.endswith('.yml'):
                    locale_code = file[:-4]  # Remove .yml extension
                    if locale_code == 'en':
                        locales[locale_code] = "English"
                    elif locale_code == 'tr':
                        locales[locale_code] = "Türkçe"
                    else:
                        locales[locale_code] = locale_code.title()
        
        return locales