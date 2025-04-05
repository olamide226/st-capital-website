#!/usr/bin/env python3
"""
Script to update all HTML pages with the new modern template.
This script will apply the new header, navigation, and footer to all HTML files in the src directory.
"""

import os
import re
import glob
from bs4 import BeautifulSoup

# Define the template parts
HEADER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | St. Stephen's Capital</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="business development, business consulting, sales management, business development consultants, sales force, sales force management, sales force training">
    
    <!-- Favicon -->
    <link rel="icon" href="sitebuildercontent/sitebuilderpictures/icon2.jpg" type="image/jpeg">
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="css/styles.css" rel="stylesheet">
</head>
<body>
"""

NAVIGATION_TEMPLATE = """    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.html">
                <img src="sitebuildercontent/sitebuilderpictures/icon2.jpg" alt="St. Stephen's Capital" height="50">
                <span class="ms-2">St. Stephen's Capital</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="about_us.html">About Us</a></li>
                    <li class="nav-item"><a class="nav-link" href="agency.html">Business Development Agency</a></li>
                    <li class="nav-item"><a class="nav-link" href="academy.html">Business Development Academy</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Services</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="briefing.html">Client Enquiry & Briefing</a></li>
                            <li><a class="dropdown-item" href="aux.html">Auxiliary Services</a></li>
                            <li><a class="dropdown-item" href="refer.html">Referrals</a></li>
                        </ul>
                    </li>
                    <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
                    <li class="nav-item"><a class="nav-link btn btn-primary text-white ms-lg-3 px-4" href="pay.html">Payment Portal</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Page Header -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8 mx-auto text-center fade-in">
                    <h1 class="company-title">{page_title}</h1>
                    <p class="lead mb-0">{page_subtitle}</p>
                </div>
            </div>
        </div>
    </section>
"""

FOOTER_TEMPLATE = """    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-4 mb-lg-0">
                    <h5>About Us</h5>
                    <p>St. Stephen's Capital is an enterprise consulting firm providing outstanding Business Development services since 2005.</p>
                    <p>"we want to be part of your success story"</p>
                </div>
                <div class="col-lg-2 col-md-6 mb-4 mb-md-0">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled footer-links">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about_us.html">About Us</a></li>
                        <li><a href="agency.html">Agency</a></li>
                        <li><a href="academy.html">Academy</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6 mb-4 mb-md-0">
                    <h5>Resources</h5>
                    <ul class="list-unstyled footer-links">
                        <li><a href="privacy_policy.html">Privacy Policy</a></li>
                        <li><a href="disclaimer.html">Disclaimer</a></li>
                        <li><a href="green.html">Green Policy</a></li>
                        <li><a href="vacancies.html">Current Opportunities</a></li>
                        <li><a href="refer.html">Referrals</a></li>
                    </ul>
                </div>
                <div class="col-lg-3">
                    <h5>Contact Us</h5>
                    <p><i class="fas fa-phone me-2"></i> +44 (0)20 8638 6093</p>
                    <p><i class="fas fa-phone me-2"></i> +234 (0)80 3691 0800</p>
                    <p><i class="fas fa-envelope me-2"></i> <a href="mailto:info@saintstephenscapital.com">info@saintstephenscapital.com</a></p>
                    <div class="social-links mt-3">
                        <a href="http://www.linkedin.com/groups?gid=2914570" target="_blank"><i class="fab fa-linkedin-in"></i></a>
                        <a href="http://www.facebook.com/pages/St-Stephens-Capital-Business-Growth/111623372200938" target="_blank"><i class="fab fa-facebook-f"></i></a>
                        <a href="http://twitter.com/stephenscapital" target="_blank"><i class="fab fa-twitter"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom text-center">
                <p>&copy; 2005-2024 St. Stephen's Capital Ltd. All Rights Reserved.</p>
                <p class="small">St. Stephen's Capital Limited (CH: 14273578 & RC: 1564353)</p>
                <p class="small">Leaders in Sustainable Entrepreneurial Development</p>
                <p class="small">"global presence through regional offices network"</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="js/main.js"></script>
</body>
</html>
"""

# Pages that have already been updated
UPDATED_PAGES = ['index.html', 'about_us.html', 'pay.html']

# Page titles and descriptions
PAGE_INFO = {
    'academy.html': {
        'title': 'Business Development Academy',
        'description': 'St. Stephen\'s Capital Business Development Academy offers training and development programs to equip your team with the skills needed for sustainable business growth.',
        'subtitle': 'Equipping your team with the skills needed for sustainable business growth'
    },
    'agency.html': {
        'title': 'Business Development Agency',
        'description': 'St. Stephen\'s Capital Business Development Agency provides strategic business development services to help your organization grow and thrive.',
        'subtitle': 'Strategic business development services for organizational growth'
    },
    'aux.html': {
        'title': 'Auxiliary Services',
        'description': 'St. Stephen\'s Capital provides additional support services to complement our core offerings and ensure comprehensive business solutions.',
        'subtitle': 'Additional support services to complement our core offerings'
    },
    'briefing.html': {
        'title': 'Client Enquiry & Briefing',
        'description': 'Submit your business development enquiry and briefing to St. Stephen\'s Capital to get started with our services.',
        'subtitle': 'Tell us about your business needs and challenges'
    },
    'contact.html': {
        'title': 'Contact Us',
        'description': 'Contact St. Stephen\'s Capital for business development services and consultancy. Get in touch with our team today.',
        'subtitle': 'Get in touch with our team'
    },
    'disclaimer.html': {
        'title': 'Disclaimer',
        'description': 'Legal disclaimer for St. Stephen\'s Capital website and services.',
        'subtitle': 'Legal information about our website and services'
    },
    'green.html': {
        'title': 'Green Policy',
        'description': 'St. Stephen\'s Capital\'s commitment to environmental sustainability and green business practices.',
        'subtitle': 'Our commitment to environmental sustainability'
    },
    'privacy_policy.html': {
        'title': 'Privacy Policy',
        'description': 'St. Stephen\'s Capital\'s privacy policy explaining how we collect, use, and protect your personal information.',
        'subtitle': 'How we protect your personal information'
    },
    'refer.html': {
        'title': 'Referrals',
        'description': 'Refer businesses to St. Stephen\'s Capital and help them benefit from our business development services.',
        'subtitle': 'Recommend our services to others'
    },
    'vacancies.html': {
        'title': 'Current Opportunities',
        'description': 'Explore current job opportunities and vacancies at St. Stephen\'s Capital.',
        'subtitle': 'Join our team of business development professionals'
    }
}

def extract_main_content(html_content):
    """Extract the main content from the old HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find the main content
    main_content = ""
    
    # Look for content in the main area
    main_area = soup.find('div', {'class': 'user main'})
    if main_area:
        main_content += str(main_area.decode_contents())
    
    # Look for content in the subhead area
    subhead_area = soup.find('div', {'class': 'user subhead'})
    if subhead_area:
        # Skip the search form
        for element in subhead_area.find_all(['p', 'div']):
            if not element.find('form', {'id': 'websearch1'}):
                main_content += str(element)
    
    # Look for content in area_a, area_b, area_c
    for area in ['area_a', 'area_b', 'area_c']:
        area_div = soup.find('div', {'class': f'user {area}'})
        if area_div and area_div.decode_contents().strip():
            main_content += str(area_div.decode_contents())
    
    return main_content

def create_modern_page(filename, main_content):
    """Create a modern page with the extracted content."""
    page_info = PAGE_INFO.get(filename, {
        'title': os.path.splitext(filename)[0].replace('_', ' ').title(),
        'description': f'St. Stephen\'s Capital - {os.path.splitext(filename)[0].replace("_", " ").title()}',
        'subtitle': 'Business Development Services'
    })
    
    # Create the header
    header = HEADER_TEMPLATE.format(
        title=page_info['title'],
        description=page_info['description']
    )
    
    # Create the navigation
    navigation = NAVIGATION_TEMPLATE.format(
        page_title=page_info['title'],
        page_subtitle=page_info['subtitle']
    )
    
    # Create the main content section
    content_section = f"""    <!-- Main Content -->
    <section class="py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    <div class="card shadow-sm">
                        <div class="card-body p-4 p-md-5">
                            {main_content}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto text-center">
                    <h2 class="mb-4">Ready to work with us?</h2>
                    <p class="lead mb-4">Contact us today to discuss how we can help you achieve your business development goals.</p>
                    <a href="contact.html" class="btn btn-primary btn-lg">Contact Us</a>
                </div>
            </div>
        </div>
    </section>
"""
    
    # Combine all parts
    modern_page = header + navigation + content_section + FOOTER_TEMPLATE
    
    return modern_page

def update_pages():
    """Update all HTML pages in the src directory."""
    html_files = glob.glob('*.html')
    
    for filename in html_files:
        if filename in UPDATED_PAGES:
            print(f"Skipping {filename} (already updated)")
            continue
        
        print(f"Updating {filename}...")
        
        try:
            # Read the original file
            with open(filename, 'r', encoding='utf-8') as file:
                original_content = file.read()
            
            # Extract the main content
            main_content = extract_main_content(original_content)
            
            # Create the modern page
            modern_page = create_modern_page(filename, main_content)
            
            # Create a backup of the original file
            backup_filename = f"{filename}.bak"
            with open(backup_filename, 'w', encoding='utf-8') as file:
                file.write(original_content)
            
            # Write the new content
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(modern_page)
            
            print(f"✅ Updated {filename} (backup saved as {backup_filename})")
            
        except Exception as e:
            print(f"❌ Error updating {filename}: {str(e)}")

if __name__ == "__main__":
    # Change to the src directory if not already there
    if not os.path.basename(os.getcwd()) == 'src':
        os.chdir('src')
    
    update_pages()
    print("Done! All pages have been updated with the modern template.")
