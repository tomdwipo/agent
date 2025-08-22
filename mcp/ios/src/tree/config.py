"""
iOS Tree Configuration

Configuration settings for iOS UI tree parsing and element detection.
"""

# Interactive element types that can be automated
INTERACTIVE_ELEMENT_TYPES = {
    'XCUIElementTypeButton',
    'XCUIElementTypeTextField',
    'XCUIElementTypeSecureTextField', 
    'XCUIElementTypeTextView',
    'XCUIElementTypeSwitch',
    'XCUIElementTypeSlider',
    'XCUIElementTypeCell',
    'XCUIElementTypeLink',
    'XCUIElementTypeImage',
    'XCUIElementTypeTab',
    'XCUIElementTypeTabBar',
    'XCUIElementTypeNavigationBar',
    'XCUIElementTypeSearchField',
    'XCUIElementTypeSegmentedControl',
    'XCUIElementTypePicker',
    'XCUIElementTypePickerWheel',
    'XCUIElementTypeCollectionView',
    'XCUIElementTypeTableView',
    'XCUIElementTypeScrollView'
}

# Minimum element size to be considered interactive
MIN_INTERACTIVE_SIZE = {
    'width': 10,
    'height': 10
}

# Default annotation settings
ANNOTATION_SETTINGS = {
    'outline_color': 'red',
    'outline_width': 2,
    'text_color': 'white',
    'text_background': 'red',
    'font_size': 16
}