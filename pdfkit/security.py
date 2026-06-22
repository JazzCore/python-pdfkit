# -*- coding: utf-8 -*-
import warnings

# Safe options allowed in HTML meta tags when parsing untrusted markup.
# Anything not in this allowlist is considered unsafe/untrusted and will be ignored
# unless 'allow_unsafe_meta_tags' is explicitly enabled.
ALLOWED_META_OPTIONS = frozenset([
    # Page size & orientation
    'page-size',
    'page-width',
    'page-height',
    'orientation',

    # Margins
    'margin-top',
    'margin-right',
    'margin-bottom',
    'margin-left',

    # Document properties
    'encoding',
    'dpi',
    'grayscale',
    'lowquality',
    'image-dpi',
    'image-quality',
    'title',
    'no-pdf-compression',
    'quiet',

    # Header options (pure text / formatting, no file or URL loading)
    'header-line',
    'header-spacing',
    'header-center',
    'header-left',
    'header-right',
    'header-font-name',
    'header-font-size',

    # Footer options (pure text / formatting, no file or URL loading)
    'footer-line',
    'footer-spacing',
    'footer-center',
    'footer-left',
    'footer-right',
    'footer-font-name',
    'footer-font-size',

    # Outline options
    'outline',
    'outline-depth',
    'no-outline',

    # TOC formatting options
    'toc-header-text',
    'toc-level-indentation',
    'toc-text-size-shrink',
])


def is_safe_meta_option(option_name):
    """
    Checks if an option is present in the ALLOWED_META_OPTIONS allowlist.
    Normalizes option names by stripping any leading dashes and lowercasing.

    :param option_name: The name of the option to check.
    :return: True if the option is safe, False otherwise.
    """
    if not option_name:
        return False
    normalized = option_name.lower().lstrip('-')
    return normalized in ALLOWED_META_OPTIONS
