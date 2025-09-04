#!/usr/bin/env python3
"""
App Context Builder
Specialized tool for creating application development contexts
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime
from tooltip import ToolTip

class AppContextBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("App Development Context Builder")
        self.root.geometry("1000x700")
        
        # App-specific styling
        style = ttk.Style()
        style.configure("App.TLabel", foreground="#28A745")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(header_frame, text="🚀 App Development Context Builder", 
                               font=("Arial", 16, "bold"), style="App.TLabel")
        title_label.pack(side=tk.LEFT)
        
        info_label = ttk.Label(header_frame, text="Create optimized contexts for application development", 
                              font=("Arial", 10))
        info_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Main notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # App Builder Tab
        builder_frame = ttk.Frame(notebook)
        notebook.add(builder_frame, text="🏗️ App Specification")
        self.setup_builder_tab(builder_frame)
        
        # Preview Tab
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="📋 Context Preview")
        self.setup_preview_tab(preview_frame)
        
        # Templates Tab
        templates_frame = ttk.Frame(notebook)
        notebook.add(templates_frame, text="📝 App Templates")
        self.setup_templates_tab(templates_frame)
        
    def setup_builder_tab(self, parent):
        # App type selection
        type_frame = ttk.LabelFrame(parent, text="Application Type")
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.app_type_var = tk.StringVar(value="web_app")
        app_types = [
            ("🌐 Web Application", "web_app"),
            ("🖥️ Desktop Application", "desktop_app"),
            ("⚡ CLI Tool", "cli_tool"),
            ("🔌 API Service", "api_service"),
            ("📱 Mobile App", "mobile_app")
        ]
        
        for text, value in app_types:
            ttk.Radiobutton(type_frame, text=text, variable=self.app_type_var, 
                           value=value, command=self.on_type_change).pack(anchor=tk.W, padx=10, pady=2)
        
        # Scrollable form
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        self.form_fields = {}
        self.load_app_form()
        
    def setup_preview_tab(self, parent):
        ttk.Label(parent, text="Generated Application Context:", 
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(parent, height=25, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="🔄 Generate App Context", 
                  command=self.generate_preview).pack(side=tk.LEFT, padx=5)
        
        # XML tags option
        self.xml_tags_var = tk.BooleanVar(value=False)
        xml_check = ttk.Checkbutton(button_frame, text="Include XML Tags", 
                                   variable=self.xml_tags_var)
        xml_check.pack(side=tk.LEFT, padx=5)
        ToolTip(xml_check, "Add XML tags for better AI comprehension\n(Recommended for Claude and advanced AI models)")
        
        ttk.Button(button_frame, text="💾 Export Context", 
                  command=self.export_context).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
    def setup_templates_tab(self, parent):
        ttk.Label(parent, text="Application Development Templates", 
                 font=("Arial", 14, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        
        templates_text = scrolledtext.ScrolledText(parent, height=25, wrap=tk.WORD)
        templates_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        templates_content = """# Application Development Templates

## Web Application Template
Perfect for browser-based applications with user interfaces.

**Common Requirements:**
• User authentication and authorization
• Responsive design for mobile/desktop
• Database integration (PostgreSQL, MySQL)
• RESTful API endpoints
• Real-time features (WebSocket, SSE)
• File upload and management
• Email notifications
• Search functionality

**Tech Stack Examples:**
• Frontend: React, Vue.js, Angular, HTML/CSS/JS
• Backend: Node.js, Python (Django/Flask), Ruby on Rails
• Database: PostgreSQL, MySQL, MongoDB
• Deployment: AWS, Heroku, Vercel, Netlify

## Desktop Application Template
For native applications running on Windows, macOS, or Linux.

**Common Requirements:**
• Native OS integration (file system, notifications)
• Offline functionality
• Local data storage
• System tray integration
• Auto-updates
• Cross-platform compatibility
• Performance optimization

**Tech Stack Examples:**
• Electron (JavaScript/TypeScript)
• Python (Tkinter, PyQt, Kivy)
• C# (.NET, WPF)
• Java (Swing, JavaFX)
• C++ (Qt, GTK)

## CLI Tool Template
Command-line interfaces for automation and developer tools.

**Common Requirements:**
• Command parsing and validation
• Configuration file support
• Progress indicators
• Error handling and logging
• Help documentation
• Piping and redirection support
• Cross-platform compatibility

**Tech Stack Examples:**
• Python (Click, argparse)
• Node.js (Commander.js, Yargs)
• Go (Cobra, CLI)
• Rust (Clap)
• Shell scripting (Bash, PowerShell)

## API Service Template
Backend services providing data and functionality via APIs.

**Common Requirements:**
• RESTful or GraphQL endpoints
• Authentication and authorization
• Rate limiting and throttling
• Data validation and sanitization
• Database operations (CRUD)
• Caching strategies
• API documentation
• Monitoring and logging

**Tech Stack Examples:**
• Node.js (Express, Fastify, NestJS)
• Python (FastAPI, Django REST, Flask)
• Java (Spring Boot)
• C# (ASP.NET Core)
• Go (Gin, Echo)

## Mobile App Template
Native or cross-platform mobile applications.

**Common Requirements:**
• Touch-friendly interface design
• Offline data synchronization
• Push notifications
• Camera and media access
• Location services
• App store compliance
• Performance optimization
• Device-specific features

**Tech Stack Examples:**
• React Native (JavaScript/TypeScript)
• Flutter (Dart)
• Native iOS (Swift)
• Native Android (Kotlin/Java)
• Xamarin (C#)

## Best Practices for All App Types

### Requirements Gathering
1. Define clear user stories
2. Specify acceptance criteria
3. Identify technical constraints
4. Plan for scalability
5. Consider security requirements

### Development Process
1. Set up version control (Git)
2. Implement CI/CD pipelines
3. Write comprehensive tests
4. Document APIs and code
5. Plan deployment strategy

### Quality Assurance
1. Unit testing for core logic
2. Integration testing for APIs
3. End-to-end testing for workflows
4. Performance testing under load
5. Security testing for vulnerabilities
"""
        
        templates_text.insert("1.0", templates_content)
        templates_text.config(state=tk.DISABLED)
        
    def on_type_change(self):
        self.load_app_form()
        
    def load_app_form(self):
        # Clear existing fields
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.form_fields.clear()
        
        app_type = self.app_type_var.get()
        
        # Common fields for all app types
        common_fields = {
            "Project Name": {
                "type": "entry", "required": True,
                "tooltip": f"Enter a clear, descriptive name for your {app_type.replace('_', ' ')}:\n• Be specific: 'Task Manager Pro' not 'My App'\n• Avoid generic terms like 'System' or 'Tool'\n• Consider branding and user recognition"
            },
            "Project Description": {
                "type": "text", "height": 3, "required": True,
                "tooltip": "Describe what your application does and why it's valuable:\n• Focus on user benefits and problems solved\n• Mention key features and capabilities\n• Keep it concise but comprehensive"
            },
            "Target Users": {
                "type": "text", "height": 2, "required": True,
                "tooltip": "Who will use this application?\n• Primary users: 'Small business owners managing inventory'\n• Secondary users: 'Employees tracking daily tasks'\n• User personas help guide design decisions"
            },
            "Core Features": {
                "type": "text", "height": 6, "required": True,
                "tooltip": "List the main features your application must have:\n• User authentication and profiles\n• Data visualization with charts\n• Export functionality (PDF, CSV)\n• Real-time notifications\n• Search and filtering\n\nPrioritize essential features first."
            }
        }
        
        # Type-specific fields
        if app_type == "web_app":
            specific_fields = {
                "Frontend Framework": {
                    "type": "combo", "values": ["React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", "Vanilla JavaScript", "TypeScript", "jQuery"], "required": False,
                    "tooltip": "Choose your frontend technology:\n• React: Large ecosystem, component-based\n• Vue.js: Gentle learning curve, flexible\n• Angular: Full framework, TypeScript-first\n• Svelte: Compile-time optimization\n• Next.js: React with SSR/SSG\n• Nuxt.js: Vue with SSR/SSG\n• Vanilla JavaScript: No framework dependencies\n• TypeScript: Type-safe JavaScript\n• jQuery: Legacy support, simple DOM manipulation"
                },
                "Backend Framework": {
                    "type": "combo", "values": ["Python (Django)", "Python (Flask)", "Python (FastAPI)", "Node.js (Express)", "Node.js (NestJS)", "Ruby on Rails", "PHP (Laravel)", "Java (Spring Boot)", "C# (ASP.NET Core)", "Go (Gin)", "Rust (Actix)"], "required": True,
                    "tooltip": "Select your backend framework:\n• Django: Python, batteries included, rapid development\n• Flask: Python, lightweight, flexible\n• FastAPI: Python, modern, automatic API docs\n• Express: Node.js, minimal, flexible\n• NestJS: Node.js, TypeScript, enterprise-grade\n• Rails: Ruby, convention over configuration\n• Laravel: PHP, elegant syntax, full-featured\n• Spring Boot: Java, enterprise, microservices\n• ASP.NET Core: C#, high performance, cross-platform\n• Gin: Go, fast, minimal\n• Actix: Rust, extremely fast, safe"
                },
                "Database": {
                    "type": "combo", "values": ["PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", "Cassandra", "DynamoDB", "Firebase"], "required": True,
                    "tooltip": "Choose your database:\n• PostgreSQL: Advanced features, JSON support, ACID\n• MySQL: Reliable, widely supported, fast\n• MongoDB: Document-based, flexible schema\n• SQLite: Lightweight, serverless, embedded\n• Redis: In-memory, caching, pub/sub\n• Cassandra: Distributed, high availability\n• DynamoDB: AWS NoSQL, serverless\n• Firebase: Google, real-time, easy setup"
                },
                "Authentication": {
                    "type": "text", "height": 2, "required": False,
                    "tooltip": "Specify authentication requirements:\n• Email/password with verification\n• OAuth (Google, GitHub, Facebook, Apple)\n• Two-factor authentication (2FA)\n• Role-based access control (RBAC)\n• JWT tokens with refresh\n• Session management\n• Single Sign-On (SSO)"
                },
                "Styling/CSS": {
                    "type": "combo", "values": ["Tailwind CSS", "Bootstrap", "Material-UI", "Ant Design", "Chakra UI", "Styled Components", "CSS Modules", "SCSS/Sass", "Vanilla CSS"], "required": False,
                    "tooltip": "Choose your styling approach:\n• Tailwind CSS: Utility-first, highly customizable\n• Bootstrap: Component library, responsive\n• Material-UI: Google's Material Design\n• Ant Design: Enterprise-class UI language\n• Chakra UI: Modular, accessible components\n• Styled Components: CSS-in-JS\n• CSS Modules: Scoped CSS\n• SCSS/Sass: CSS preprocessor\n• Vanilla CSS: Pure CSS, no dependencies"
                }
            }
        elif app_type == "desktop_app":
            specific_fields = {
                "Desktop Framework": {
                    "type": "combo", "values": ["Electron", "Python (Tkinter)", "Python (PyQt/PySide)", "Python (Kivy)", "C# (WPF)", "C# (WinUI)", "Java (Swing)", "Java (JavaFX)", "C++ (Qt)", "Rust (Tauri)", "Go (Fyne)"], "required": True,
                    "tooltip": "Choose your desktop framework:\n• Electron: Web technologies, cross-platform, large apps\n• Tkinter: Python built-in, simple GUIs\n• PyQt/PySide: Professional Python GUIs, native look\n• Kivy: Python, touch-friendly, mobile support\n• WPF: Modern Windows applications, XAML\n• WinUI: Latest Windows UI framework\n• Swing: Cross-platform Java GUIs, mature\n• JavaFX: Modern Java UI, rich graphics\n• Qt: C++, native performance, cross-platform\n• Tauri: Rust backend, web frontend, small size\n• Fyne: Go, simple, cross-platform"
                },
                "Target OS": {
                    "type": "combo", "values": ["Windows", "macOS", "Linux", "Cross-platform"], "required": True,
                    "tooltip": "Select target operating systems:\n• Windows: Largest desktop market, .NET ecosystem\n• macOS: Premium user base, App Store\n• Linux: Developer and enterprise users\n• Cross-platform: Maximum reach, consistent experience"
                },
                "Installation Method": {
                    "type": "text", "height": 2, "required": False,
                    "tooltip": "How will users install your app?\n• Installer package (.msi, .dmg, .deb, .rpm)\n• Portable executable (no installation)\n• App store distribution (Microsoft Store, Mac App Store)\n• Package managers (Chocolatey, Homebrew, apt)\n• Auto-updater integration\n• Silent/enterprise deployment"
                },
                "UI Library": {
                    "type": "combo", "values": ["Native OS", "Material Design", "Fluent Design", "Custom Theme"], "required": False,
                    "tooltip": "Choose your UI design approach:\n• Native OS: Platform-specific look and feel\n• Material Design: Google's design language\n• Fluent Design: Microsoft's design system\n• Custom Theme: Branded, unique appearance"
                }
            }
        elif app_type == "cli_tool":
            specific_fields = {
                "CLI Framework": {
                    "type": "combo", "values": ["Python (Click)", "Python (argparse)", "Python (Typer)", "Node.js (Commander)", "Node.js (Yargs)", "Go (Cobra)", "Rust (Clap)", "C# (System.CommandLine)", "Java (Picocli)"], "required": True,
                    "tooltip": "Choose your CLI framework:\n• Click: Python, decorator-based, powerful features\n• argparse: Python built-in, standard library\n• Typer: Python, modern, type hints, FastAPI style\n• Commander: Node.js, feature-rich, popular\n• Yargs: Node.js, flexible, interactive\n• Cobra: Go, used by Docker, Kubernetes\n• Clap: Rust, performance-focused, derive macros\n• System.CommandLine: C#, modern .NET CLI\n• Picocli: Java, annotation-based, GraalVM ready"
                },
                "Command Structure": {
                    "type": "text", "height": 3, "required": True,
                    "tooltip": "Define your command structure:\n• mytool init --config config.json\n• mytool process --input file.txt --output result.txt\n• mytool status --verbose\n• mytool deploy --env production\n\nInclude subcommands, options, and arguments."
                },
                "Configuration": {
                    "type": "text", "height": 2, "required": False,
                    "tooltip": "How will your CLI be configured?\n• Configuration files (JSON, YAML, TOML, INI)\n• Environment variables\n• Command-line flags and options\n• Interactive setup wizard\n• Config file auto-generation\n• Profile/workspace support"
                },
                "Output Format": {
                    "type": "combo", "values": ["Plain Text", "JSON", "YAML", "Table", "Progress Bars", "Interactive"], "required": False,
                    "tooltip": "Choose output formatting:\n• Plain Text: Simple, readable output\n• JSON: Machine-readable, structured\n• YAML: Human-readable, structured\n• Table: Tabular data display\n• Progress Bars: Long-running operations\n• Interactive: Menus, prompts, TUI"
                }
            }
        elif app_type == "api_service":
            specific_fields = {
                "API Framework": {
                    "type": "combo", "values": ["Python (FastAPI)", "Python (Django REST)", "Python (Flask-RESTful)", "Node.js (Express)", "Node.js (NestJS)", "Java (Spring Boot)", "C# (ASP.NET Core)", "Go (Gin)", "Go (Echo)", "Rust (Actix)", "Ruby (Rails API)"], "required": True,
                    "tooltip": "Choose your API framework:\n• FastAPI: Python, automatic docs, type hints, async\n• Django REST: Python, batteries included, serializers\n• Flask-RESTful: Python, lightweight, flexible\n• Express: Node.js, minimal, middleware-based\n• NestJS: Node.js, TypeScript, decorator-based\n• Spring Boot: Java, enterprise-grade, microservices\n• ASP.NET Core: C#, high performance, cross-platform\n• Gin: Go, fast HTTP router, minimal\n• Echo: Go, high performance, middleware\n• Actix: Rust, extremely fast, actor-based\n• Rails API: Ruby, convention over configuration"
                },
                "API Type": {
                    "type": "combo", "values": ["REST", "GraphQL", "gRPC", "WebSocket", "Server-Sent Events"], "required": True,
                    "tooltip": "Select your API type:\n• REST: Standard HTTP methods, widely supported\n• GraphQL: Flexible queries, single endpoint, type-safe\n• gRPC: High performance, binary protocol, streaming\n• WebSocket: Real-time, bidirectional communication\n• Server-Sent Events: Real-time, server-to-client"
                },
                "Authentication": {
                    "type": "combo", "values": ["JWT", "OAuth 2.0", "API Keys", "Basic Auth", "Bearer Token", "mTLS"], "required": True,
                    "tooltip": "Choose authentication method:\n• JWT: Stateless, scalable tokens, claims-based\n• OAuth 2.0: Industry standard, secure, delegated auth\n• API Keys: Simple, good for service-to-service\n• Basic Auth: Simple but less secure, base64 encoded\n• Bearer Token: Token-based, stateless\n• mTLS: Mutual TLS, certificate-based, high security"
                },
                "Documentation": {
                    "type": "combo", "values": ["OpenAPI/Swagger", "GraphQL Playground", "Postman", "Insomnia", "Custom Docs"], "required": False,
                    "tooltip": "API documentation approach:\n• OpenAPI/Swagger: Standard, interactive docs\n• GraphQL Playground: GraphQL schema explorer\n• Postman: Collection-based, team collaboration\n• Insomnia: REST client with documentation\n• Custom Docs: Tailored documentation site"
                }
            }
        else:  # mobile_app
            specific_fields = {
                "Mobile Framework": {
                    "type": "combo", "values": ["React Native", "Flutter", "Native iOS (Swift)", "Native Android (Kotlin)", "Xamarin", "Ionic", "Cordova/PhoneGap", "Unity (Games)", "Expo"], "required": True,
                    "tooltip": "Choose your mobile framework:\n• React Native: JavaScript, code sharing, large community\n• Flutter: Dart, high performance, single codebase\n• Native iOS: Swift, platform-specific, best performance\n• Native Android: Kotlin, platform-specific, Material Design\n• Xamarin: C#, Microsoft ecosystem, native performance\n• Ionic: Web technologies, hybrid apps, plugins\n• Cordova/PhoneGap: HTML/CSS/JS, web-based\n• Unity: Game development, 3D/2D, cross-platform\n• Expo: React Native with managed workflow"
                },
                "Target Platforms": {
                    "type": "combo", "values": ["iOS only", "Android only", "Both iOS and Android", "Web Progressive App"], "required": True,
                    "tooltip": "Select target platforms:\n• iOS only: Premium market, consistent hardware, App Store\n• Android only: Larger market share, diverse devices, Google Play\n• Both: Maximum reach, more development effort\n• Web Progressive App: Web-based, app-like experience"
                },
                "Device Features": {
                    "type": "text", "height": 3, "required": False,
                    "tooltip": "What device features will you use?\n• Camera for photo/video capture\n• GPS for location services and mapping\n• Push notifications for engagement\n• Biometric authentication (Face ID, Touch ID)\n• Offline data storage and sync\n• Accelerometer/Gyroscope for motion\n• Bluetooth for device connectivity\n• NFC for payments/data transfer\n• Background processing"
                },
                "App Store Strategy": {
                    "type": "text", "height": 2, "required": False,
                    "tooltip": "Distribution and monetization:\n• Free app with ads\n• Paid app (one-time purchase)\n• Freemium with in-app purchases\n• Subscription model\n• Enterprise distribution\n• Beta testing strategy (TestFlight, Play Console)\n• App Store Optimization (ASO)"
                },
                "Backend Services": {
                    "type": "combo", "values": ["Firebase", "AWS Amplify", "Supabase", "Custom API", "Parse", "Back4App"], "required": False,
                    "tooltip": "Choose backend services:\n• Firebase: Google, real-time database, auth, hosting\n• AWS Amplify: Amazon, full-stack, GraphQL\n• Supabase: Open source Firebase alternative\n• Custom API: Your own backend service\n• Parse: Open source, self-hosted\n• Back4App: Parse hosting service"
                }
            }
        
        # Combine common and specific fields
        all_fields = {**common_fields, **specific_fields}
        
        # Add remaining common fields
        all_fields.update({
            "Technical Requirements": {
                "type": "text", "height": 4, "required": False,
                "tooltip": "Specify technical constraints and requirements:\n• Performance: Load time under 2 seconds\n• Scalability: Support 10,000 concurrent users\n• Security: Encrypt sensitive data\n• Compatibility: Support modern browsers/OS versions\n• Accessibility: WCAG 2.1 compliance"
            },
            "Dependencies": {
                "type": "text", "height": 3, "required": False,
                "tooltip": "List external dependencies:\n• Third-party libraries and versions\n• External APIs and services\n• Database requirements\n• System dependencies\n• Development tools"
            },
            "Testing Strategy": {
                "type": "text", "height": 3, "required": False,
                "tooltip": "Define your testing approach:\n• Unit tests for core business logic\n• Integration tests for API endpoints\n• End-to-end tests for user workflows\n• Performance tests for load handling\n• Security tests for vulnerabilities"
            },
            "Deployment": {
                "type": "text", "height": 2, "required": False,
                "tooltip": "How will you deploy your application?\n• Cloud platforms: AWS, Azure, Google Cloud\n• Containerization: Docker, Kubernetes\n• CI/CD pipelines: GitHub Actions, Jenkins\n• Monitoring: Application performance monitoring\n• Backup and recovery strategies"
            }
        })
        
        # Create form fields
        for field_name, config in all_fields.items():
            frame = ttk.LabelFrame(self.scrollable_frame, text=field_name + (" *" if config.get("required") else ""))
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            if config["type"] == "entry":
                widget = ttk.Entry(frame)
                widget.pack(fill=tk.X, padx=10, pady=5)
            elif config["type"] == "combo":
                widget = ttk.Combobox(frame, values=config["values"], state="readonly")
                widget.pack(fill=tk.X, padx=10, pady=5)
            elif config["type"] == "text":
                widget = scrolledtext.ScrolledText(frame, height=config.get("height", 4), wrap=tk.WORD)
                widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            if "tooltip" in config:
                ToolTip(widget, config["tooltip"])
            
            self.form_fields[field_name] = {"widget": widget, "config": config}
    
    def generate_preview(self):
        use_xml = self.xml_tags_var.get()
        if use_xml:
            context = self.build_xml_context()
        else:
            context = self.build_app_context()
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", context)
    
    def build_xml_context(self):
        data = self.get_form_data()
        app_type = self.app_type_var.get().replace('_', ' ').title()
        timestamp = datetime.now().strftime("%A, %Y-%m-%dT%H:%M:%S.%f")[:-3] + "-07:00"
        
        context = f"""--- CONTEXT ENTRY BEGIN ---
<metadata>
<generated_by>App Development Context Builder</generated_by>
<application_type>{app_type}</application_type>
<created>{timestamp}</created>
<xml_enhanced>true</xml_enhanced>
</metadata>
--- CONTEXT ENTRY END ---

--- CONTEXT ENTRY BEGIN ---
<application_specification>

<project_info>
<name>{data.get('Project Name', 'Unnamed Application')}</name>
<type>{app_type}</type>
<description>{data.get('Project Description', 'No description provided')}</description>
</project_info>

<target_audience>
{data.get('Target Users', 'Not specified')}
</target_audience>

<core_features>
{self.format_xml_list(data.get('Core Features', 'No features specified'))}
</core_features>

"""
        
        # Add technical stack in XML format
        if any(key in data for key in ['Frontend Framework', 'Backend Framework', 'Database']):
            context += "<technical_stack>\n"
            if 'Frontend Framework' in data:
                context += f"<frontend framework=\"{data['Frontend Framework']}\"/>\n"
            if 'Backend Framework' in data:
                context += f"<backend framework=\"{data['Backend Framework']}\"/>\n"
            if 'Database' in data:
                context += f"<database type=\"{data['Database']}\"/>\n"
            if 'Styling/CSS' in data:
                context += f"<styling framework=\"{data['Styling/CSS']}\"/>\n"
            context += "</technical_stack>\n\n"
        
        # Add requirements in XML format
        if data.get('Technical Requirements'):
            context += f"<technical_requirements>\n{self.format_xml_requirements(data['Technical Requirements'])}\n</technical_requirements>\n\n"
        
        if data.get('Dependencies'):
            context += f"<dependencies>\n{self.format_xml_list(data['Dependencies'])}\n</dependencies>\n\n"
        
        if data.get('Testing Strategy'):
            context += f"<testing_strategy>\n{self.format_xml_list(data['Testing Strategy'])}\n</testing_strategy>\n\n"
        
        if data.get('Deployment'):
            context += f"<deployment_plan>\n{data['Deployment']}\n</deployment_plan>\n\n"
        
        context += """<development_checklist>
<task status="pending">Set up development environment</task>
<task status="pending">Initialize version control (Git)</task>
<task status="pending">Create project structure</task>
<task status="pending">Implement core features</task>
<task status="pending">Add user authentication</task>
<task status="pending">Set up database/data storage</task>
<task status="pending">Implement error handling</task>
<task status="pending">Add logging and monitoring</task>
<task status="pending">Write comprehensive tests</task>
<task status="pending">Create deployment pipeline</task>
<task status="pending">Document APIs and usage</task>
<task status="pending">Perform security review</task>
<task status="pending">Optimize performance</task>
<task status="pending">Plan maintenance strategy</task>
</development_checklist>

<quality_assurance>
<test_type>Unit tests for business logic</test_type>
<test_type>Integration tests for components</test_type>
<test_type>End-to-end user workflow tests</test_type>
<test_type>Performance and load testing</test_type>
<test_type>Security vulnerability assessment</test_type>
<test_type>Accessibility compliance check</test_type>
<test_type>Cross-platform compatibility</test_type>
<test_type>User acceptance testing</test_type>
</quality_assurance>
</application_specification>
--- CONTEXT ENTRY END ---

--- USER MESSAGE BEGIN ---
<request>
Build me this application based on the specification above
</request>
--- USER MESSAGE END ---"""
        
        return context
    
    def format_xml_list(self, text):
        if not text:
            return ""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(f"<item>{line}</item>" for line in lines)
    
    def format_xml_requirements(self, text):
        if not text:
            return ""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(f"<requirement>{line}</requirement>" for line in lines)
    
    def build_app_context(self):
        data = self.get_form_data()
        app_type = self.app_type_var.get().replace('_', ' ').title()
        timestamp = datetime.now().strftime("%A, %Y-%m-%dT%H:%M:%S.%f")[:-3] + "-07:00"
        
        context = f"""--- CONTEXT ENTRY BEGIN ---
Generated by App Development Context Builder
Application Type: {app_type}
Created: {timestamp}
--- CONTEXT ENTRY END ---

--- CONTEXT ENTRY BEGIN ---
APPLICATION SPECIFICATION

PROJECT: {data.get('Project Name', 'Unnamed Application')}
TYPE: {app_type}
DESCRIPTION: {data.get('Project Description', 'No description provided')}

TARGET USERS:
{data.get('Target Users', 'Not specified')}

CORE FEATURES:
{data.get('Core Features', 'No features specified')}

"""
        
        # Add type-specific information
        if 'Frontend Framework' in data:
            context += f"FRONTEND: {data['Frontend Framework']}\n"
        if 'Backend Framework' in data:
            context += f"BACKEND: {data['Backend Framework']}\n"
        if 'Database' in data:
            context += f"DATABASE: {data['Database']}\n"
        if 'Desktop Framework' in data:
            context += f"FRAMEWORK: {data['Desktop Framework']}\n"
        if 'CLI Framework' in data:
            context += f"CLI FRAMEWORK: {data['CLI Framework']}\n"
        if 'API Framework' in data:
            context += f"API FRAMEWORK: {data['API Framework']}\n"
        if 'Mobile Framework' in data:
            context += f"MOBILE FRAMEWORK: {data['Mobile Framework']}\n"
        
        context += "\n"
        
        # Add additional sections
        for field in ['Authentication', 'Target OS', 'Command Structure', 'API Type', 'Target Platforms', 'Device Features', 'Styling/CSS', 'UI Library', 'Output Format', 'Documentation', 'App Store Strategy', 'Backend Services']:
            if field in data:
                context += f"{field.upper().replace(' ', '_')}:\n{data[field]}\n\n"
        
        if data.get('Technical Requirements'):
            context += f"TECHNICAL REQUIREMENTS:\n{data['Technical Requirements']}\n\n"
        
        if data.get('Dependencies'):
            context += f"DEPENDENCIES:\n{data['Dependencies']}\n\n"
        
        if data.get('Testing Strategy'):
            context += f"TESTING STRATEGY:\n{data['Testing Strategy']}\n\n"
        
        if data.get('Deployment'):
            context += f"DEPLOYMENT:\n{data['Deployment']}\n\n"
        
        context += """DEVELOPMENT CHECKLIST:
□ Set up development environment
□ Initialize version control (Git)
□ Create project structure
□ Implement core features
□ Add user authentication
□ Set up database/data storage
□ Implement error handling
□ Add logging and monitoring
□ Write comprehensive tests
□ Create deployment pipeline
□ Document APIs and usage
□ Perform security review
□ Optimize performance
□ Plan maintenance strategy

QUALITY ASSURANCE:
□ Unit tests for business logic
□ Integration tests for components
□ End-to-end user workflow tests
□ Performance and load testing
□ Security vulnerability assessment
□ Accessibility compliance check
□ Cross-platform compatibility
□ User acceptance testing
--- CONTEXT ENTRY END ---

--- USER MESSAGE BEGIN ---
Build me this application based on the specification above
--- USER MESSAGE END ---"""
        
        return context
    
    def get_form_data(self):
        data = {}
        for field_name, field_info in self.form_fields.items():
            widget = field_info["widget"]
            
            if isinstance(widget, ttk.Entry):
                value = widget.get().strip()
            elif isinstance(widget, ttk.Combobox):
                value = widget.get().strip()
            else:  # ScrolledText
                value = widget.get("1.0", tk.END).strip()
            
            if value:
                data[field_name] = value
        
        return data
    
    def export_context(self):
        content = self.preview_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Generate context first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Save App Context"
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"App context exported to {filename}")
    
    def copy_to_clipboard(self):
        content = self.preview_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Generate context first!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "Context copied to clipboard!")

def main():
    root = tk.Tk()
    app = AppContextBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
