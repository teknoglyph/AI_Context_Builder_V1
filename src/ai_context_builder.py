#!/usr/bin/env python3
"""
AI Context Template Builder
Creates optimized context files for Q and MCP development
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from tooltip import ToolTip

class ContextTemplateBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Context Template Builder")
        self.root.geometry("1200x800")
        
        self.templates = {
            "app_development": self.get_app_template(),
            "mcp_development": self.get_mcp_template(),
            "bug_report": self.get_bug_template(),
            "feature_request": self.get_feature_template()
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Template Builder Tab
        builder_frame = ttk.Frame(notebook)
        notebook.add(builder_frame, text="Template Builder")
        self.setup_builder_tab(builder_frame)
        
        # Preview Tab
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Preview & Export")
        self.setup_preview_tab(preview_frame)
        
    def setup_builder_tab(self, parent):
        # Template selection
        ttk.Label(parent, text="Template Type:").pack(anchor=tk.W, padx=5, pady=5)
        self.template_var = tk.StringVar(value="app_development")
        template_combo = ttk.Combobox(parent, textvariable=self.template_var, 
                                    values=list(self.templates.keys()), state="readonly")
        template_combo.pack(fill=tk.X, padx=5, pady=5)
        template_combo.bind('<<ComboboxSelected>>', self.load_template)
        
        # Scrollable frame for form fields
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
        self.load_template()
        
    def setup_preview_tab(self, parent):
        # Preview text area
        ttk.Label(parent, text="Generated Context:").pack(anchor=tk.W, padx=5, pady=5)
        self.preview_text = scrolledtext.ScrolledText(parent, height=25, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Generate Preview", 
                  command=self.generate_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to MD", 
                  command=self.export_md).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to TXT", 
                  command=self.export_txt).pack(side=tk.LEFT, padx=5)
        
    def get_app_template(self):
        return {
            "Project Name": {
                "type": "entry", "required": True,
                "tooltip": "Enter a clear, descriptive name for your project (e.g., 'Customer Management System', 'Weather Dashboard')"
            },
            "Project Type": {
                "type": "combo", "values": ["Web App", "Desktop App", "CLI Tool", "API Service"], "required": True,
                "tooltip": "Select the type of application you want to build:\n• Web App: Browser-based application\n• Desktop App: Standalone GUI application\n• CLI Tool: Command-line interface\n• API Service: Backend service with REST/GraphQL API"
            },
            "Programming Language": {
                "type": "combo", "values": ["Python", "JavaScript", "TypeScript", "Java", "C#", "Go"], "required": True,
                "tooltip": "Choose your primary programming language. Consider:\n• Python: Great for rapid development, data processing\n• JavaScript/TypeScript: Web development, Node.js\n• Java/C#: Enterprise applications\n• Go: High-performance services"
            },
            "Framework": {
                "type": "entry", "required": False,
                "tooltip": "Specify the framework or library (e.g., Flask, React, Django, Express, .NET Core). Leave blank if unsure."
            },
            "Requirements": {
                "type": "text", "height": 8, "required": True, 
                "placeholder": "List specific requirements, one per line",
                "tooltip": "List specific, measurable requirements:\n• User can login with email/password\n• System displays real-time data updates\n• Export data to CSV format\n• Support 1000+ concurrent users\n\nBe specific about what the app should DO, not how it should work."
            },
            "Existing Code": {
                "type": "text", "height": 6, "required": False, 
                "placeholder": "Paste existing code or file structure",
                "tooltip": "Include any existing code, file structure, or database schemas that should be considered:\n• Current file organization\n• Existing functions/classes\n• Database tables\n• API endpoints\n\nThis helps AI understand what already exists."
            },
            "Dependencies": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "List dependencies and versions",
                "tooltip": "List required libraries, packages, or external services:\n• Python: flask==2.0.1, sqlalchemy>=1.4\n• Node.js: express@4.18.0, mongoose@6.0\n• External APIs: Stripe, SendGrid, AWS S3\n• Databases: PostgreSQL 13+, Redis"
            },
            "Target Platform": {
                "type": "combo", "values": ["Windows", "Linux", "macOS", "Cross-platform"], "required": True,
                "tooltip": "Select where your application will run:\n• Windows: Windows-specific features\n• Linux: Server deployments, containers\n• macOS: Mac-specific applications\n• Cross-platform: Works on multiple operating systems"
            },
            "UI Requirements": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "Describe UI/UX requirements",
                "tooltip": "Describe the user interface and experience:\n• Layout: Dashboard with sidebar navigation\n• Colors: Corporate blue theme\n• Responsive: Mobile-friendly design\n• Accessibility: Screen reader support\n• Components: Data tables, charts, forms"
            },
            "Testing Requirements": {
                "type": "text", "height": 3, "required": False, 
                "placeholder": "Testing strategy and requirements",
                "tooltip": "Specify testing approach:\n• Unit tests for core functions\n• Integration tests for API endpoints\n• End-to-end tests for user workflows\n• Performance tests for 1000+ users\n• Security testing for authentication"
            }
        }
    
    def get_mcp_template(self):
        return {
            "MCP Server Name": {
                "type": "entry", "required": True,
                "tooltip": "Choose a descriptive name for your MCP server (e.g., 'file-manager', 'database-connector', 'weather-api')"
            },
            "Server Description": {
                "type": "text", "height": 3, "required": True, 
                "placeholder": "What does this MCP server do?",
                "tooltip": "Clearly describe what your MCP server provides:\n• 'Manages local file operations and directory browsing'\n• 'Connects to PostgreSQL databases for data queries'\n• 'Provides weather data from OpenWeatherMap API'\n\nBe specific about the main purpose and capabilities."
            },
            "Tools to Implement": {
                "type": "text", "height": 6, "required": True, 
                "placeholder": "List tools with descriptions, one per line",
                "tooltip": "List each tool your MCP will provide:\n• read_file: Read contents of a text file\n• write_file: Write content to a file\n• list_directory: List files in a directory\n• execute_query: Run SQL queries on database\n\nFormat: tool_name: description of what it does"
            },
            "Resources to Provide": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "List resources (files, data sources, etc.)",
                "tooltip": "Resources are data sources your MCP exposes:\n• file://path/to/config.json\n• database://localhost:5432/mydb\n• api://weather.example.com/current\n\nResources provide read-only access to data."
            },
            "Prompts to Include": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "List prompt templates",
                "tooltip": "Prompt templates help users interact with your MCP:\n• 'Analyze this file for security issues'\n• 'Generate SQL query for customer data'\n• 'Create backup script for database'\n\nThese guide users on how to use your tools effectively."
            },
            "Configuration Options": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "Environment variables, settings, etc.",
                "tooltip": "Configuration your MCP server needs:\n• DATABASE_URL: Connection string\n• API_KEY: Authentication token\n• MAX_FILE_SIZE: File size limit in MB\n• DEBUG_MODE: Enable debug logging\n\nInclude environment variables and settings."
            },
            "Error Handling": {
                "type": "text", "height": 3, "required": False, 
                "placeholder": "Specific error scenarios to handle",
                "tooltip": "Important error cases to handle gracefully:\n• File not found or permission denied\n• Database connection failures\n• API rate limits exceeded\n• Invalid input parameters\n• Network timeouts"
            },
            "Integration Requirements": {
                "type": "text", "height": 3, "required": False, 
                "placeholder": "How should this integrate with other systems?",
                "tooltip": "How your MCP connects to other systems:\n• Authentication with OAuth2\n• Webhook notifications\n• Integration with existing APIs\n• Data synchronization requirements\n• Security and permission models"
            }
        }
    
    def get_bug_template(self):
        return {
            "Bug Title": {
                "type": "entry", "required": True,
                "tooltip": "Write a clear, specific title:\n• Good: 'Login fails with 500 error when password contains special characters'\n• Bad: 'Login broken'\n\nInclude what's broken and key symptoms."
            },
            "Current Behavior": {
                "type": "text", "height": 4, "required": True, 
                "placeholder": "What is happening now?",
                "tooltip": "Describe exactly what happens when the bug occurs:\n• User clicks login button\n• Page shows 500 Internal Server Error\n• No error message displayed to user\n• Browser console shows 'TypeError: Cannot read property...'\n\nBe specific about what you observe."
            },
            "Expected Behavior": {
                "type": "text", "height": 4, "required": True, 
                "placeholder": "What should happen instead?",
                "tooltip": "Describe what should happen in the normal case:\n• User should be logged in successfully\n• Dashboard page should load\n• Welcome message should appear\n• Navigation menu should be visible\n\nExplain the correct behavior clearly."
            },
            "Steps to Reproduce": {
                "type": "text", "height": 6, "required": True, 
                "placeholder": "Step-by-step reproduction",
                "tooltip": "Provide exact steps to reproduce the bug:\n1. Open browser and go to login page\n2. Enter email: test@example.com\n3. Enter password: P@ssw0rd!\n4. Click 'Login' button\n5. Observe error message\n\nNumber each step clearly."
            },
            "Error Messages": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "Exact error messages or logs",
                "tooltip": "Include exact error messages:\n• Browser console errors\n• Server log entries\n• Error dialog text\n• HTTP status codes\n• Stack traces\n\nCopy and paste the exact text."
            },
            "Environment": {
                "type": "text", "height": 3, "required": True, 
                "placeholder": "OS, Python version, dependencies",
                "tooltip": "Specify your environment:\n• Operating System: Windows 10, macOS 12.1, Ubuntu 20.04\n• Browser: Chrome 96.0, Firefox 95.0\n• Python version: 3.9.7\n• Framework versions: Flask 2.0.1\n• Database: PostgreSQL 13.4"
            },
            "Code Context": {
                "type": "text", "height": 6, "required": False, 
                "placeholder": "Relevant code snippets",
                "tooltip": "Include relevant code that might be causing the issue:\n• Function where error occurs\n• Configuration files\n• Database queries\n• API calls\n• Recent changes\n\nHelp identify the root cause."
            }
        }
    
    def get_feature_template(self):
        return {
            "Feature Name": {
                "type": "entry", "required": True,
                "tooltip": "Give your feature a clear, descriptive name:\n• 'User Profile Management'\n• 'Real-time Chat System'\n• 'CSV Data Export'\n\nMake it specific and actionable."
            },
            "Feature Description": {
                "type": "text", "height": 4, "required": True, 
                "placeholder": "What should this feature do?",
                "tooltip": "Describe the feature's purpose and main functionality:\n• Allow users to update their profile information\n• Enable real-time messaging between users\n• Provide data export in multiple formats\n\nExplain the business value and user benefit."
            },
            "User Stories": {
                "type": "text", "height": 6, "required": True, 
                "placeholder": "As a user, I want... (one per line)",
                "tooltip": "Write user stories in this format:\n• As a [user type], I want [goal] so that [benefit]\n• As a customer, I want to update my email address so that I receive notifications\n• As an admin, I want to export user data so that I can analyze usage patterns\n\nFocus on user goals and benefits."
            },
            "Acceptance Criteria": {
                "type": "text", "height": 6, "required": True, 
                "placeholder": "How to verify the feature works",
                "tooltip": "Define specific, testable criteria:\n• Given [context], when [action], then [result]\n• User can successfully update email address\n• System validates email format before saving\n• Confirmation email is sent to new address\n• Old email receives notification of change\n\nMake criteria measurable and testable."
            },
            "Technical Requirements": {
                "type": "text", "height": 4, "required": False, 
                "placeholder": "Technical constraints or requirements",
                "tooltip": "Specify technical considerations:\n• Performance: Page load under 2 seconds\n• Security: Encrypt sensitive data\n• Scalability: Support 10,000 concurrent users\n• Integration: Connect with existing user database\n• Compatibility: Work on mobile devices"
            },
            "Integration Points": {
                "type": "text", "height": 3, "required": False, 
                "placeholder": "How does this integrate with existing code?",
                "tooltip": "Describe how this feature connects to existing systems:\n• Uses existing user authentication system\n• Integrates with current database schema\n• Connects to email service API\n• Updates existing user dashboard\n• Requires changes to user model"
            },
            "Priority": {
                "type": "combo", "values": ["High", "Medium", "Low"], "required": True,
                "tooltip": "Set feature priority:\n• High: Critical for next release, blocks other work\n• Medium: Important but can wait for next sprint\n• Low: Nice to have, can be deferred\n\nConsider business impact and user needs."
            }
        }
    
    def load_template(self, event=None):
        # Clear existing fields
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.form_fields.clear()
        
        template_name = self.template_var.get()
        template = self.templates[template_name]
        
        for field_name, config in template.items():
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Label
            label_text = field_name
            if config.get("required", False):
                label_text += " *"
            label = ttk.Label(frame, text=label_text)
            label.pack(anchor=tk.W)
            
            # Add tooltip to label
            if "tooltip" in config:
                ToolTip(label, config["tooltip"])
            
            # Input widget
            if config["type"] == "entry":
                widget = ttk.Entry(frame)
                widget.pack(fill=tk.X, pady=2)
            elif config["type"] == "combo":
                widget = ttk.Combobox(frame, values=config["values"], state="readonly")
                widget.pack(fill=tk.X, pady=2)
            elif config["type"] == "text":
                widget = scrolledtext.ScrolledText(frame, height=config.get("height", 4), wrap=tk.WORD)
                if "placeholder" in config:
                    widget.insert("1.0", config["placeholder"])
                    widget.bind("<FocusIn>", lambda e, w=widget, p=config["placeholder"]: self.clear_placeholder(w, p))
                widget.pack(fill=tk.X, pady=2)
            
            # Add tooltip to input widget
            if "tooltip" in config:
                ToolTip(widget, config["tooltip"])
            
            self.form_fields[field_name] = {"widget": widget, "config": config}
    
    def clear_placeholder(self, widget, placeholder):
        if widget.get("1.0", tk.END).strip() == placeholder:
            widget.delete("1.0", tk.END)
    
    def generate_preview(self):
        template_name = self.template_var.get()
        context = self.build_context(template_name)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", context)
    
    def build_context(self, template_name):
        timestamp = datetime.now().strftime("%A, %Y-%m-%dT%H:%M:%S.%f")[:-3] + "-07:00"
        
        context = f"""--- CONTEXT ENTRY BEGIN ---
Generated by AI Context Template Builder
Template: {template_name.replace('_', ' ').title()}
Created: {timestamp}
--- CONTEXT ENTRY END ---

--- CONTEXT ENTRY BEGIN ---
"""
        
        # Add template-specific context
        if template_name == "app_development":
            context += self.build_app_context()
        elif template_name == "mcp_development":
            context += self.build_mcp_context()
        elif template_name == "bug_report":
            context += self.build_bug_context()
        elif template_name == "feature_request":
            context += self.build_feature_context()
        
        context += "\n--- CONTEXT ENTRY END ---\n\n--- USER MESSAGE BEGIN ---\n[Your request here]\n--- USER MESSAGE END ---"
        
        return context
    
    def build_app_context(self):
        data = self.get_form_data()
        context = f"PROJECT: {data.get('Project Name', 'Unnamed Project')}\n"
        context += f"TYPE: {data.get('Project Type', 'Not specified')} using {data.get('Programming Language', 'Not specified')}\n"
        
        if data.get('Framework'):
            context += f"FRAMEWORK: {data['Framework']}\n"
        
        context += f"TARGET PLATFORM: {data.get('Target Platform', 'Not specified')}\n\n"
        
        if data.get('Requirements'):
            context += f"REQUIREMENTS:\n{data['Requirements']}\n\n"
        
        if data.get('Existing Code'):
            context += f"EXISTING CODE:\n{data['Existing Code']}\n\n"
        
        if data.get('Dependencies'):
            context += f"DEPENDENCIES:\n{data['Dependencies']}\n\n"
        
        if data.get('UI Requirements'):
            context += f"UI/UX REQUIREMENTS:\n{data['UI Requirements']}\n\n"
        
        if data.get('Testing Requirements'):
            context += f"TESTING REQUIREMENTS:\n{data['Testing Requirements']}\n\n"
        
        return context
    
    def build_mcp_context(self):
        data = self.get_form_data()
        context = f"MCP SERVER: {data.get('MCP Server Name', 'Unnamed Server')}\n"
        context += f"DESCRIPTION: {data.get('Server Description', 'No description provided')}\n\n"
        
        context += "MCP PROTOCOL REQUIREMENTS:\n"
        context += "- Follow MCP specification from https://modelcontextprotocol.io/\n"
        context += "- Implement proper JSON-RPC 2.0 communication\n"
        context += "- Include proper error handling and validation\n"
        context += "- Support standard MCP lifecycle methods\n\n"
        
        if data.get('Tools to Implement'):
            context += f"TOOLS TO IMPLEMENT:\n{data['Tools to Implement']}\n\n"
        
        if data.get('Resources to Provide'):
            context += f"RESOURCES:\n{data['Resources to Provide']}\n\n"
        
        if data.get('Prompts to Include'):
            context += f"PROMPTS:\n{data['Prompts to Include']}\n\n"
        
        if data.get('Configuration Options'):
            context += f"CONFIGURATION:\n{data['Configuration Options']}\n\n"
        
        if data.get('Error Handling'):
            context += f"ERROR HANDLING:\n{data['Error Handling']}\n\n"
        
        if data.get('Integration Requirements'):
            context += f"INTEGRATION:\n{data['Integration Requirements']}\n\n"
        
        return context
    
    def build_bug_context(self):
        data = self.get_form_data()
        context = f"BUG REPORT: {data.get('Bug Title', 'Untitled Bug')}\n\n"
        
        context += f"CURRENT BEHAVIOR:\n{data.get('Current Behavior', 'Not specified')}\n\n"
        context += f"EXPECTED BEHAVIOR:\n{data.get('Expected Behavior', 'Not specified')}\n\n"
        context += f"REPRODUCTION STEPS:\n{data.get('Steps to Reproduce', 'Not provided')}\n\n"
        
        if data.get('Error Messages'):
            context += f"ERROR MESSAGES:\n{data['Error Messages']}\n\n"
        
        context += f"ENVIRONMENT:\n{data.get('Environment', 'Not specified')}\n\n"
        
        if data.get('Code Context'):
            context += f"RELEVANT CODE:\n{data['Code Context']}\n\n"
        
        return context
    
    def build_feature_context(self):
        data = self.get_form_data()
        context = f"FEATURE REQUEST: {data.get('Feature Name', 'Unnamed Feature')}\n"
        context += f"PRIORITY: {data.get('Priority', 'Not specified')}\n\n"
        
        context += f"DESCRIPTION:\n{data.get('Feature Description', 'No description provided')}\n\n"
        context += f"USER STORIES:\n{data.get('User Stories', 'Not provided')}\n\n"
        context += f"ACCEPTANCE CRITERIA:\n{data.get('Acceptance Criteria', 'Not specified')}\n\n"
        
        if data.get('Technical Requirements'):
            context += f"TECHNICAL REQUIREMENTS:\n{data['Technical Requirements']}\n\n"
        
        if data.get('Integration Points'):
            context += f"INTEGRATION POINTS:\n{data['Integration Points']}\n\n"
        
        return context
    
    def get_form_data(self):
        data = {}
        for field_name, field_info in self.form_fields.items():
            widget = field_info["widget"]
            config = field_info["config"]
            
            if config["type"] in ["entry", "combo"]:
                value = widget.get().strip()
            else:  # text
                value = widget.get("1.0", tk.END).strip()
                placeholder = config.get("placeholder", "")
                if value == placeholder:
                    value = ""
            
            if value:
                data[field_name] = value
        
        return data
    
    def export_md(self):
        content = self.preview_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Generate preview first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Exported to {filename}")
    
    def export_txt(self):
        content = self.preview_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Generate preview first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Exported to {filename}")

def main():
    root = tk.Tk()
    app = ContextTemplateBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
