from website.content import CONTACT  # noqa: F401

NAV = [
    {'label': 'About us', 'url_name': 'about'},
    {'label': 'About me', 'url_name': 'about_me'},
    {
        'label': 'Our services',
        'url_name': 'services',
        'children': [
            {'label': 'Systems and standards', 'url_name': 'service_detail', 'slug': 'sistemi-i-standardi'},
            {'label': 'ISO standards', 'url_name': 'service_detail', 'slug': 'iso-standardi'},
            {'label': 'Food labelling', 'url_name': 'service_detail', 'slug': 'deklarisanje'},
            {'label': 'Gap analysis', 'url_name': 'service_detail', 'slug': 'gap-analiza'},
            {'label': 'Digitalization', 'url_name': 'service_detail', 'slug': 'digitalizacija'},
        ],
    },
    {'label': 'From idea to shelf', 'url_name': 'journey'},
    {'label': 'Expert support', 'url_name': 'support'},
    {'label': 'News', 'url_name': 'news'},
    {'label': 'Contact', 'url_name': 'contact'},
]

SERVICES = [
    {
        'slug': 'sistemi-i-standardi',
        'title': 'Food safety systems and standards',
        'short': 'HACCP | IFS | FSSC 22000 | BRCGS',
        'standards': ['HACCP', 'IFS', 'FSSC 22000', 'BRCGS'],
        'card': 'Establishing and improving food safety systems in line with international standards.',
        'icon': 'haccp',
        'hero': 'haccp',
        'intro': (
            'Food safety is more than meeting legal requirements. A well-designed system '
            'should be clear, functional and tailored to how the business actually operates.'
        ),
        'lead': (
            'Food Compass supports companies in establishing, improving, verifying and preparing '
            'food safety systems against national regulations and internationally recognized standards.'
        ),
        'items': [
            {
                'title': 'HACCP',
                'text': (
                    'Establishing, reviewing and improving HACCP systems, including hazard identification, '
                    'risk assessment, control measures and system verification.'
                ),
            },
            {
                'title': 'FSSC 22000',
                'text': (
                    'Support in developing and improving a food safety management system to FSSC 22000 '
                    'requirements, and in preparing the organization for certification and audit.'
                ),
            },
            {
                'title': 'IFS',
                'text': (
                    'Support in understanding and applying IFS requirements, assessing conformity, '
                    'improving the system and preparing for an IFS audit.'
                ),
            },
            {
                'title': 'BRC',
                'text': (
                    'Support in establishing and improving systems to BRCGS requirements '
                    'and preparing the organization for certification.'
                ),
            },
        ],
    },
    {
        'slug': 'iso-standardi',
        'title': 'ISO standards',
        'short': 'ISO 9001 | ISO 22000',
        'standards': ['ISO 9001', 'ISO 22000'],
        'card': 'Implementation of quality and food safety management systems tailored to your operations.',
        'icon': 'iso',
        'hero': 'iso',
        'intro': (
            'Support for companies in establishing, improving and verifying management systems '
            'to internationally recognized ISO standards, with a focus on quality and food safety.'
        ),
        'lead': 'From meeting requirements to a system that works in practice.',
        'items': [
            {
                'title': 'ISO 9001 – Quality management system',
                'text': (
                    'Support in establishing, improving and internally auditing a quality management system '
                    'to ISO 9001, and in preparing the organization for certification. '
                    'ISO 9001 Lead Auditor – IRCA/CQI certified training.'
                ),
            },
            {
                'title': 'ISO 22000 – Food safety management system',
                'text': (
                    'Support in establishing, improving and maintaining a food safety management system '
                    'to ISO 22000, linked with HACCP principles and other relevant food safety requirements.'
                ),
            },
        ],
    },
    {
        'slug': 'deklarisanje',
        'title': 'Food product labelling',
        'short': 'From recipe to a compliant label — clear, precise and without unnecessary complexity.',
        'standards': [],
        'card': 'From recipe to a compliant label — clear, precise and without unnecessary complexity.',
        'icon': 'deklarisanje',
        'hero': 'deklarisanje',
        'intro': (
            'A correct label is more than a legal duty — it is a key part of product compliance, '
            'consumer safety and how the product appears on the market.'
        ),
        'lead': (
            'Food Compass provides expert support in drafting, checking and improving food labels, '
            'from recipe and composition analysis to a final check of the information on the pack.'
        ),
        'items': [
            {
                'title': 'Complete label development',
                'text': (
                    'Defining and checking all mandatory label elements, including the product name, '
                    'ingredient list, allergens, net quantity, date of minimum durability, storage conditions, '
                    'responsible operator details and other required information.'
                ),
            },
            {
                'title': 'Nutrition labelling and calculations',
                'text': (
                    'Calculation and verification of nutrition values and preparation of the nutrition '
                    'declaration in line with applicable requirements.'
                ),
            },
            {
                'title': 'Allergens, nutrition and health claims',
                'text': (
                    'Checking the correct declaration and highlighting of allergens, plus expert support '
                    'on the use of nutrition and health claims.'
                ),
            },
            {
                'title': 'Compliance check',
                'text': (
                    'A detailed review of existing labels and packaging against applicable rules, '
                    'identifying potential non-conformities and recommending how to close them.'
                ),
            },
            {
                'title': 'Multilingual labels and export',
                'text': (
                    'Preparing and checking labels for different markets, including aligning the content '
                    'with the destination country’s requirements and an expert review of translations.'
                ),
            },
            {
                'title': 'Updates and ongoing support',
                'text': (
                    'Monitoring relevant regulatory changes and updating labels, with expert support when '
                    'the recipe, packaging, market or legal requirements change.'
                ),
            },
        ],
    },
    {
        'slug': 'gap-analiza',
        'title': 'Gap analysis and audit preparation',
        'short': 'Is your system truly ready for audit?',
        'standards': [],
        'card': 'We assess how ready your system really is for audit and define what needs to improve.',
        'icon': 'gap',
        'hero': 'gap',
        'intro': (
            'Through an expert review of the existing system we determine the level of conformity '
            'with the relevant standard and identify areas to improve before the audit.'
        ),
        'lead': (
            'This support is for companies preparing for an IFS, FSSC 22000, BRCGS, ISO 22000 '
            'or ISO 9001 audit.'
        ),
        'list_title': 'A gap analysis covers:',
        'list_items': [
            'review of documentation and procedures',
            'checking how the system is applied in practice',
            'identification of non-conformities and potential risks',
            'defining required corrective and improvement actions',
            'prioritizing activities and recommendations for audit preparation',
        ],
        'closer': (
            'The aim is not only to pass the audit, but to build a system that is compliant, '
            'functional and sustainable in day-to-day operations.'
        ),
        'items': [],
    },
    {
        'slug': 'digitalizacija',
        'title': 'Digitalization of food safety systems',
        'short': 'Digital HACCP | Digital IFS | Digital FSSC 22000 | Digital BRCGS',
        'standards': ['Digital HACCP', 'Digital IFS', 'Digital FSSC 22000', 'Digital BRCGS'],
        'card': 'Move documentation, checklists and records from paper into a simple, clear digital system.',
        'icon': 'digitalizacija',
        'hero': 'digital',
        'intro': 'Less paper. More control. A better system.',
        'lead': (
            'Digitalization lets food safety systems move from folders, spreadsheets and paper records '
            'into one connected digital environment. Food Compass supports the digitalization of systems '
            'such as HACCP, IFS, FSSC 22000 and BRCGS, so day-to-day food safety management is simpler, '
            'clearer and more efficient.'
        ),
        'items': [
            {
                'title': 'Digital HACCP and management systems',
                'text': (
                    'Digitalization of procedures, plans, records, checklists and other food safety system '
                    'elements, with the option to track completion in real time.'
                ),
            },
            {
                'title': 'Digital records',
                'text': (
                    'Cleaning, disinfection, pest control, maintenance, incoming goods, temperatures '
                    'and other operational controls can be kept digitally, without unnecessary paper admin.'
                ),
            },
            {
                'title': 'Automated monitoring and alerts',
                'text': (
                    'Connecting sensors and other digital devices enables continuous monitoring of key '
                    'parameters, with automatic alerts when values go out of range.'
                ),
            },
            {
                'title': 'Tasks and responsibilities in real time',
                'text': (
                    'Staff receive clear tasks and duties, while responsible persons can track completion '
                    'and respond to deviations without waiting for paper reports.'
                ),
            },
            {
                'title': 'Audit readiness',
                'text': (
                    'Evidence of controls, records, deviations, corrective actions and reports are available '
                    'in one place, which greatly simplifies preparation and delivery of internal and external audits.'
                ),
            },
            {
                'title': 'Traceability and data access',
                'text': (
                    'Digital data tracking improves process and product traceability, faster access to '
                    'information and simpler decisions based on available data.'
                ),
            },
        ],
        'closer': (
            'Digitalization is not just replacing paper with a screen. It is a way to make the food safety '
            'system visible, measurable and manageable in real time.'
        ),
    },
]

JOURNEY = [
    {
        'id': 'od-ideje',
        'title': 'From the idea',
        'lead': 'Defining the product and regulatory requirements',
        'intro': 'The first step is to define the product correctly and establish what is needed to place it on the market.',
        'items': [
            'analysis of the product and its intended use',
            'defining an appropriate product name',
            'preparing the manufacturer specification',
            'identifying relevant regulations and requirements',
            'aligning the product with market requirements',
        ],
        'image': '01-idea',
    },
    {
        'id': 'do-bezbednog-proizvoda',
        'title': '…To a safe product',
        'lead': 'HACCP food safety systems',
        'intro': 'Once the product is defined, a system is needed to ensure its safety during production.',
        'items': [
            'assessment of the premises and processes',
            'defining hygiene and other prerequisites',
            'hazard identification and assessment',
            'analysis of biological, chemical and physical/mechanical hazards',
            'establishing the HACCP system and required documentation',
            'establishing traceability',
            'staff training',
            'support in system digitalization',
        ],
        'image': '02-direction',
    },
    {
        'id': 'do-police',
        'title': 'To the shelf',
        'lead': 'Labelling and a final conformity check',
        'intro': 'Before placing the product on the market we check that the product and its label meet the relevant requirements.',
        'items': [
            'planning the required laboratory analyses',
            'drafting and checking the label',
            'correct allergen labelling',
            'nutrition labelling',
            'checking conformity of the product and documentation',
            'support in preparing for inspections and audits',
        ],
        'image': '03-shelf',
    },
]

ABOUT = {
    'title': 'About us',
    'eyebrow': 'Why choose us?',
    'hero_lead': (
        'Food Compass is an expert consulting concept focused on food safety, '
        'regulatory compliance and improving management systems in food businesses.'
    ),
    'quote': 'If we had known it was needed, we would certainly have done it — but we did not know.',
    'quote_context': (
        'As the founder of Food Compass and a specialist with more than 22 years of experience '
        'in food safety, I have heard this sentence countless times.'
    ),
    'origin': (
        'It was one of the main reasons I started Food Compass — as a clear guide through '
        'everything food safety requires, from idea to shelf.'
    ),
    'what': [
        'Food Compass is an expert consulting concept focused on food safety, '
        'regulatory compliance and improving management systems in food businesses.',
        'Our approach connects expert knowledge, practical experience and modern solutions '
        'so companies can treat food safety requirements not only as an obligation, '
        'but as part of efficient, sustainable and well-organized operations.',
    ],
    'principles': [
        {'title': 'Expertise', 'text': 'Knowledge and experience'},
        {'title': 'Practicality', 'text': 'Solutions that work in day-to-day operations'},
        {'title': 'A modern approach', 'text': 'More efficient and digitalized systems'},
    ],
    'areas_intro': (
        'We support HACCP systems, food safety, regulatory compliance, audit and certification '
        'preparation, and digitalization of food safety management systems.'
    ),
    'areas': [
        {'title': 'HACCP systems', 'icon': 'haccp'},
        {'title': 'Food safety', 'icon': 'food'},
        {'title': 'Regulatory compliance', 'icon': 'iso'},
        {'title': 'Audit preparation', 'icon': 'gap'},
        {'title': 'Certification preparation', 'icon': 'badge'},
        {'title': 'Digitalization of food safety management systems', 'icon': 'digitalizacija'},
    ],
    'value': (
        'The particular value of Food Compass is that we turn complex technical and regulatory '
        'requirements into clear, practical solutions that can be used in everyday operations.'
    ),
    'founder_name': 'Sandra Đukanović Kojić',
    'founder_role': 'Master of Biochemical Engineering and Biotechnology',
    'founder_specialty': 'Food safety specialist',
    'founder_body': [
        'Food Compass was built on more than two decades of practical experience of Sandra Đukanović Kojić, Master of Biochemical Engineering and Biotechnology and food safety specialist, in official controls, HACCP systems, risk assessment and regulatory compliance.',
        'Experience gained in the state food control system, work on international projects and continuous professional development in auditing, certification and international standards form the expert foundation on which Food Compass was developed.',
    ],
    'expertise': [
        {'value': '22+', 'label': 'years of experience'},
        {'value': 'HACCP', 'label': 'systems and risk assessment'},
        {'value': 'Audits', 'label': 'and certification'},
        {'value': 'Regulation', 'label': 'and official food controls'},
        {'value': 'International experience', 'label': 'projects and standards'},
    ],
    'goal_title': 'Food safety should be clear, efficient and easy to manage.',
    'goal': 'Our goal is simple — to make food safety clearer, more efficient and easier to manage.',
    'years_label': 'years of experience',
    'origin_eyebrow': 'Why Food Compass was created',
    'origin_title': 'From complex requirements to a clear direction',
    'what_eyebrow': 'What Food Compass is',
    'what_title': 'Expertise with practical application',
    'areas_eyebrow': 'Areas of support',
    'value_eyebrow': 'Our approach',
    'value_title': 'We turn complex requirements into clear solutions.',
    'founder_eyebrow': 'Founder of Food Compass',
    'goal_eyebrow': 'Our goal',
    'cta_talk': 'Let’s talk about your business →',
    'cta_services': 'See our services',
    'quote_open': '“',
    'quote_close': '”',
}

ABOUT_ME = {
    'title': 'About me',
    'name': 'Sandra Đukanović Kojić',
    'initials': 'SĐK',
    'role': 'Master of Biochemical Engineering and Biotechnology',
    'role_extra': 'Food safety specialist',
    'lead': 'More than 22 years of professional experience, including long-standing work in food safety, official controls, HACCP systems, risk assessment and compliance with national and European regulations.',
    'quote': 'I believe a good food safety system should not be documentation alone.',
    'quote_open': '“',
    'quote_close': '”',
    'facts': [
        {'value': '22+', 'label': 'years of experience'},
        {'value': 'TMF', 'label': 'University of Belgrade'},
        {'value': 'IRCA', 'label': 'ISO 9001 Lead Auditor'},
    ],
    'paragraphs': [
        'I completed my professional education at the Faculty of Technology and Metallurgy, University of Belgrade, with a master’s degree in biochemical engineering and biotechnology and a specialization in food safety.',
        'Throughout my career I have continually developed my knowledge through national and international training in HACCP, food hygiene, auditing, regulatory compliance and food safety management systems.',
        'Most of my professional career was spent at the Ministry of Agriculture, Forestry and Water Management of the Republic of Serbia, as a republican food safety inspector. Work in the official control system allowed me to see food safety in a highly practical way — from risk assessment and control planning, through HACCP verification and interpretation of regulations, to direct work with food business operators and laboratories.',
        'My experience also includes work in agricultural policy and analytics, and participation in numerous national and international projects and programmes, including EU TAIEX and Twinning, USAID, UNEP-GEF, WTO SPS and IPA projects, as well as laboratory-related projects. I also took part in a food safety system development project in cooperation with KPMG.',
        'In the next phase of my professional development I focus on expert consulting, audits, certification and digitalization of food safety systems. I hold an IRCA certificate as ISO 9001 Lead Auditor, and I continually expand my knowledge in ISO/FSSC 22000, IFS and other internationally recognized standards.',
        'I see particular value in connecting expertise, regulation and practical application. Long experience in the state food control system has helped me understand not only what the rules require, but also the concrete challenges companies face when those requirements must be applied in daily operations.',
        'Today I bring that experience into a different form — through Food Compass, to help companies make their food safety systems clearer, more efficient, more transparent and simpler to apply and maintain.',
    ],
    'linkedin': 'LinkedIn profile →',
    'cta_about': 'About us',
    'cta_contact': 'Contact us',
}

SUPPORT = {
    'title': 'Expert support for food safety',
    'eyebrow': 'Ongoing monitoring and assistance',
    'options': [
        {
            'slug': 'redovna',
            'title': 'Regular expert visit',
            'subtitle': 'Be confident that your food safety system works in practice',
            'intro': 'Regular expert support — ongoing monitoring and assistance',
            'body': [
                'In day-to-day operations it is easy to miss important details that, if not spotted in time, can grow into a serious problem.',
                'Through regular expert visits we give you ongoing support in maintaining the HACCP system and keeping operations aligned with food safety requirements and applicable regulations.',
            ],
            'list_title': 'Monthly visits, at an agreed frequency, cover:',
            'list_items': [
                'review of the premises and hygiene conditions',
                'checking how the HACCP system is applied in practice',
                'review of documentation and records',
                'checking product labels',
                'checking alignment with legal requirements',
                'identifying potential non-conformities and recommending timely corrective action',
            ],
            'closer': [
                'Our goal is that you recognize and resolve potential issues before they become real problems.',
                'That way your system stays functional, your operations stay compliant, and you stay ready for inspections, audits and customer requirements — without extra stress.',
            ],
            'cta': 'Request a proposal',
            'icon': 'calendar',
            'highlights': [
                'Periodic expert checks',
                'Monitoring of the system and documentation',
                'Ongoing expert support',
            ],
        },
        {
            'slug': 'vanredna',
            'title': 'Ad hoc expert visit',
            'subtitle': 'When a new opportunity or challenge appears, be ready for the right step.',
            'intro': 'Ad hoc expert support — when a new situation, product, audit or change arises',
            'body': [
                'A new product, a change of premises or production organization, preparation for an external audit or a new business-partner requirement — every change brings requirements and risks.',
                'An ad hoc expert visit lets you see what needs to be done and how to implement the change properly before you make important decisions.',
                'With our consultant you get clear guidance, timely recommendations and confidence in decision-making, so you meet the new situation prepared and with a lower risk of non-conformity.',
            ],
            'closer': ['When the business changes, stay a step ahead.'],
            'cta': 'Book a visit',
            'icon': 'alert',
            'highlights': [
                'Support when you need it most',
                'A fast assessment of the specific situation',
                'Clear recommendations for the next steps',
            ],
        },
    ],
}

SEO_PAGES = {
    'home': {
        'title': 'Food Compass | HACCP, labelling and digitalization',
        'description': (
            'HACCP systems, HACCP digitalization, food labelling and audit preparation. '
            'Food Compass — expert food safety support from idea to shelf.'
        ),
    },
    'about': {
        'title': 'About us',
        'description': (
            'Food Compass is an expert consulting concept focused on HACCP, '
            'HACCP system digitalization and regulatory compliance.'
        ),
    },
    'about_me': {
        'title': 'About me',
        'description': (
            'Sandra Đukanović Kojić — food safety and HACCP specialist '
            'with more than 22 years of experience.'
        ),
    },
    'services': {
        'title': 'Our services',
        'description': (
            'HACCP, HACCP digitalization, ISO standards, food labelling, '
            'gap analysis and certification preparation.'
        ),
    },
    'journey': {
        'title': 'From idea to shelf',
        'description': (
            'Complete expert support for product development: HACCP, '
            'labelling and conformity all the way to the shelf.'
        ),
    },
    'support': {
        'title': 'Expert support',
        'description': (
            'Regular and ad hoc expert visits: ongoing support for the HACCP system, '
            'hygiene and documentation.'
        ),
    },
    'news': {
        'title': 'News',
        'description': (
            'Food Compass news — expert articles on HACCP, '
            'digitalization and food safety.'
        ),
    },
    'contact': {
        'title': 'Contact',
        'description': (
            'Contact Food Compass for HACCP, HACCP digitalization and food labelling. '
            'office@foodcompass.rs, +381 63 7707 319.'
        ),
    },
    'terms': {
        'title': 'Terms of use',
        'description': 'Terms of use for the Food Compass website — rights, obligations and governing law.',
    },
}

SERVICE_SEO = {
    'sistemi-i-standardi': {
        'description': (
            'Establishing, reviewing and improving HACCP, IFS, FSSC 22000 and BRCGS food safety systems, '
            'including preparation for audit and certification.'
        ),
    },
    'iso-standardi': {
        'description': (
            'Implementation of ISO 9001 and ISO 22000, linking with HACCP principles '
            'and preparing the organization for certification.'
        ),
    },
    'deklarisanje': {
        'description': (
            'Drafting and checking labels, allergens, nutrition values and conformity '
            'of food labelling with applicable regulations.'
        ),
    },
    'gap-analiza': {
        'description': (
            'Conformity assessment of HACCP and IFS, FSSC 22000, BRCGS and ISO standards '
            'before a certification audit.'
        ),
    },
    'digitalizacija': {
        'description': (
            'HACCP digitalization: procedures, checklists and records moved from paper '
            'into a clear digital system.'
        ),
    },
}

CRUMB_LABELS = {
    'o-nama': 'About us',
    'o-meni': 'About me',
    'usluge': 'Our services',
    'od-ideje-do-police': 'From idea to shelf',
    'strucna-podrska': 'Expert support',
    'haccp-nadzor': 'Expert support',
    'aktuelnosti': 'News',
    'kontakt': 'Contact',
    'uslovi-koriscenja': 'Terms of use',
}

HOME = {
    'eyebrow': 'Food product labelling',
    'title_main': 'Food safety.',
    'title_sub': 'From idea to shelf.',
    'lead': (
        'We establish food safety systems, prepare you for audit and certification, '
        'create labels and digitize HACCP and other standards.'
    ),
    'cta_consult': 'Book a consultation →',
    'cta_services': 'Our services',
    'journey_eyebrow': 'The product journey',
    'journey_title': 'From idea to shelf',
    'journey_lead': 'Complete expert support for developing and launching a food product.',
    'journey_more': 'Learn more →',
    'services_eyebrow': 'Our services',
    'services_title': 'Expert support in food safety',
    'services_lead': 'Knowledge, experience and modern solutions — all in one place.',
    'service_more': 'View →',
    'support_eyebrow': 'Expert support',
    'support_title_html': 'We give you a<br>choice',
    'support_lead': 'A regular or ad hoc expert visit — tailored to your needs.',
    'support_more': 'Learn more',
    'news_eyebrow': 'News',
    'news_title': 'From professional practice',
    'news_lead': 'Articles on food safety, standards and the path from idea to shelf.',
    'news_empty': 'More articles coming soon.',
    'news_more': 'Read →',
    'news_all': 'All news →',
    'goal_eyebrow': 'Our goal',
    'goal_quote': 'To make food safety clearer, more efficient and easier to manage.',
    'goal_aside': 'You have the idea. We show you the way.',
    'goal_cta': 'Book a meeting',
}

SERVICES_PAGE = {
    'eyebrow': 'Our services',
    'title_light': 'Expert support',
    'title_gold': 'for safe, compliant food operations.',
    'lead': (
        'From implementing standards and preparing for audit to product labelling '
        'and digitalizing food safety systems.'
    ),
    'more': 'Learn more',
}

JOURNEY_PAGE = {
    'intro': [
        'You have an idea for a new food product, but you do not know where to start?',
        (
            'Food Compass guides you through the whole process — from the initial idea and product development, '
            'through regulatory compliance and establishing a food safety system, '
            'to correct labelling and preparing the product for the market.'
        ),
        (
            'You do not have to connect regulatory, food safety, documentation and labelling requirements yourself. '
            'We connect every step into one whole.'
        ),
    ],
    'map_label': 'Three steps from idea to shelf',
    'progress_label': 'Progress through the steps',
    'step_eyebrow': 'Step',
    'close_eyebrow': 'One partner',
    'close_title': 'One partner for the whole journey',
    'close_p1': 'From the first idea to a product ready for the market.',
    'close_p2': (
        'Food Compass connects product development, food safety, regulatory compliance, '
        'documentation and labelling so your product is correctly defined, safe and ready for the market.'
    ),
    'quote': 'You have the idea. We show you the way.',
    'cta_meeting': 'Book a meeting',
    'cta_services': 'Our services',
    'hero_eyebrow': 'From idea to shelf',
    'hero_title': 'From idea to shelf',
    'hero_lead': 'Complete expert support for developing and launching a food product.',
}

CONTACT_PAGE = {
    'eyebrow': 'Contact',
    'direct': 'Direct',
    'title': 'Let’s talk.',
    'lead': 'Write, call or find us on LinkedIn — we will get back to you as soon as possible.',
    'email': 'Email',
    'phone': 'Phone',
    'linkedin': 'LinkedIn',
    'linkedin_cta': 'Open profile →',
    'sent_eyebrow': 'Message sent',
    'sent_title': 'Thank you.',
    'sent_lead': 'Your message has arrived. We will get back to you as soon as possible.',
    'sent_again': 'Send another message',
    'form_eyebrow': 'Enquiry',
    'form_title': 'Send a message',
    'form_lead': 'Tell us briefly about the product, premises or standard — we will propose the next step.',
    'form_error': 'Please fill in your name, email and message.',
    'form_send_error': 'The message was saved, but sending email currently failed. Write to us at',
    'submit': 'Send message →',
}

NEWS_PAGE = {
    'eyebrow': 'News',
    'title': 'From professional practice',
    'lead': 'Advice, regulations and practice in food safety.',
    'empty': 'More articles coming soon.',
    'read_more': 'Read →',
    'pagination': 'News pages',
    'prev': '← Previous',
    'next': 'Next →',
    'all': 'All news',
    'contact': 'Contact us',
}

SERVICE_PAGE = {
    'eyebrow': 'Our services',
    'covers': 'What it covers',
    'next_eyebrow': 'Next step',
    'next_title': 'Want to start this service?',
    'next_lead': 'Get in touch for a consultation and a concrete proposal tailored to your premises and products.',
    'cta_offer': 'Request a proposal',
    'cta_all': 'All services',
}

STRINGS = {
    'skip_link': 'Skip to content',
    'back_to_top': 'Back to top',
    'loading': 'Loading',
    'nav_home': 'Food Compass home',
    'nav_main': 'Main navigation',
    'nav_mobile': 'Mobile navigation',
    'lang_label': 'Choose language',
    'panel': 'Panel',
    'login': 'Sign in',
    'open_menu': 'Open menu',
    'footer_blurb': 'Expert support in food safety management through knowledge, experience and modern solutions.',
    'footer_nav': 'Navigation',
    'footer_services': 'Services',
    'footer_terms': 'Terms of use',
    'footer_credit': 'Website by',
    'seo_title_default': 'Food Compass | HACCP, labelling and digitalization',
    'seo_desc_default': (
        'HACCP systems, HACCP digitalization and food labelling. '
        'Food Compass — expert support in food safety.'
    ),
    'og_image_alt': 'Food Compass — HACCP and HACCP system digitalization',
    'jsonld_description': (
        'Expert support in food safety: HACCP, HACCP digitalization, '
        'labelling and audit preparation.'
    ),
    'crumb_home': 'Home',
    'form_name': 'Full name *',
    'form_email': 'Email *',
    'form_phone': 'Phone',
    'form_message': 'Message *',
    'journey_card_title': 'From idea to shelf',
    'journey_card_desc': 'Complete expert support from the first idea and recipe to a product ready for the market.',
}

TERMS = {
    'title': 'Terms of use',
    'eyebrow': 'Legal notice',
    'updated_label': 'Last updated:',
    'updated': '18 August 2026.',
    'intro': (
        'These terms govern the use of foodcompass.rs. By using the site you are deemed to have '
        'read and accepted them. If you do not agree, please do not use the site.'
    ),
    'sections': [
        {
            'title': '1. Site operator',
            'paragraphs': [
                'The website foodcompass.rs (the “Site”) is operated by Food Compass, an expert consulting '
                'concept in food safety, based in the Republic of Serbia.',
                'Contact: office@foodcompass.rs, phone +381 63 7707 319.',
            ],
        },
        {
            'title': '2. Purpose of the site',
            'paragraphs': [
                'The Site presents the activities, services and expert articles of Food Compass, '
                'and enables contact with interested parties.',
                'Content on the Site is informational. It is not a binding offer, legal, tax or regulatory '
                'advice, and it does not replace a service contract.',
            ],
        },
        {
            'title': '3. Services',
            'paragraphs': [
                'Specific services (HACCP, labelling, ISO and other standards, gap analysis, digitalization, '
                'expert visits and similar) are contracted separately, in writing, after agreeing scope, '
                'deadlines and fees.',
                'Publishing service descriptions on the Site does not create an obligation to provide a service '
                'or to accept every request.',
            ],
        },
        {
            'title': '4. Intellectual property',
            'paragraphs': [
                'Texts, photographs, logo, graphic solutions, structure and other Site content are protected '
                'by copyright and related rights and belong to Food Compass or licensors, unless stated otherwise.',
                'Viewing and sharing public pages with attribution is permitted. Copying, altering, reselling '
                'or using the content for commercial purposes without prior written consent is prohibited.',
            ],
        },
        {
            'title': '5. Accuracy of information and liability',
            'paragraphs': [
                'We strive to keep information on the Site accurate and up to date, but we do not guarantee '
                'completeness, accuracy or suitability of the content for a specific situation. Regulations and '
                'standards change, and each case requires a separate expert assessment.',
                'Food Compass is not liable for damage arising from use or inability to use the Site, including '
                'downtime, display errors, viruses or acts of third parties, except to the extent liability '
                'cannot be excluded by law.',
            ],
        },
        {
            'title': '6. User conduct',
            'paragraphs': [
                'You agree to use the Site in accordance with the law and good practice. It is prohibited to '
                'disrupt the Site, send harmful code, gain unauthorized access, misuse the contact form '
                'or send false or offensive content.',
            ],
        },
        {
            'title': '7. Contact form and personal data',
            'paragraphs': [
                'If you send an enquiry, we process the data you provide (name, email, phone, message content) '
                'solely to reply and, if needed, prepare a proposal. We do not sell data to third parties.',
                'The legal basis is taking steps at your request before concluding a contract, or the legitimate '
                'interest in answering the enquiry. We keep the data only as long as needed for that purpose, '
                'then delete it, unless the law requires a longer retention period.',
                'You have the right of access, rectification, erasure and restriction of processing, and the right '
                'to object. For requests write to office@foodcompass.rs. The Commissioner for Information of '
                'Public Importance and Personal Data Protection is the competent authority in the Republic of Serbia.',
            ],
        },
        {
            'title': '8. Cookies and analytics',
            'paragraphs': [
                'The Site may use technically necessary cookies for page operation, language and security. '
                'If analytics or marketing cookies are introduced later, you will be informed and, where required, '
                'consent will be requested.',
            ],
        },
        {
            'title': '9. Links to other websites',
            'paragraphs': [
                'The Site may contain links to LinkedIn and other external pages. Food Compass does not '
                'control their content or privacy policy and is not liable for damage arising from their use.',
            ],
        },
        {
            'title': '10. Changes to the terms',
            'paragraphs': [
                'We reserve the right to change these terms. Changes take effect when published on this page, '
                'with the update date stated. Continued use of the Site after a change is deemed acceptance '
                'of the new terms.',
            ],
        },
        {
            'title': '11. Governing law',
            'paragraphs': [
                'These terms and use of the Site are governed by the law of the Republic of Serbia. Disputes '
                'fall under the jurisdiction of the courts in the Republic of Serbia, in accordance with applicable rules.',
            ],
        },
        {
            'title': '12. Contact',
            'paragraphs': [
                'For questions about these terms write to office@foodcompass.rs or use the Contact page.',
            ],
        },
    ],
}
