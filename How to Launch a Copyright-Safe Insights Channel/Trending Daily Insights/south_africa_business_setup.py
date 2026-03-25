#!/usr/bin/env python3
"""
South African Business Setup Automation
Trending Daily Insights (Pty) Ltd
Automated company formation, banking, and compliance setup
"""

import json
import requests
from datetime import datetime, timedelta
import os

class SouthAfricaBusinessSetup:
    def __init__(self):
        self.company_name = "Trending Daily Insights (Pty) Ltd"
        self.business_type = "Private Company"
        self.industry = "Media and Information Services"
        self.location = "South Africa"
        
        # South African regulatory bodies
        self.regulatory_bodies = {
            "CIPC": "Companies and Intellectual Property Commission",
            "SARS": "South African Revenue Service", 
            "DOL": "Department of Labour",
            "SARB": "South African Reserve Bank"
        }
        
        # Required registrations
        self.registrations = {
            "company_registration": False,
            "tax_registration": False,
            "vat_registration": False,
            "paye_registration": False,
            "uif_registration": False,
            "workers_comp": False,
            "banking_setup": False
        }

    def generate_company_documents(self):
        """Generate all required company formation documents"""
        
        memorandum_of_incorporation = {
            "company_name": self.company_name,
            "company_type": "Private Company",
            "main_business": "Digital media production and geopolitical analysis",
            "authorized_shares": 1000,
            "share_value": "R1.00",
            "directors": [
                {
                    "name": "[DIRECTOR_NAME]",
                    "id_number": "[ID_NUMBER]",
                    "address": "[DIRECTOR_ADDRESS]",
                    "nationality": "South African"
                }
            ],
            "registered_address": "[BUSINESS_ADDRESS]",
            "postal_address": "[POSTAL_ADDRESS]",
            "business_activities": [
                "Digital content creation",
                "Geopolitical analysis and commentary", 
                "Online media publishing",
                "Educational content production",
                "Consulting services"
            ]
        }
        
        # Save documents
        with open('/home/ubuntu/memorandum_of_incorporation.json', 'w') as f:
            json.dump(memorandum_of_incorporation, f, indent=2)
        
        print("✅ Company formation documents generated")
        return memorandum_of_incorporation

    def cipc_registration_checklist(self):
        """Generate CIPC registration checklist and forms"""
        
        checklist = {
            "step_1_name_reservation": {
                "form": "CoR 9.1 - Application for reservation of name",
                "fee": "R50",
                "processing_time": "1-2 business days",
                "required_documents": [
                    "Proposed company name",
                    "Alternative names (2-3 options)",
                    "Applicant details"
                ]
            },
            "step_2_company_incorporation": {
                "form": "CoR 14.1 - Notice of incorporation",
                "fee": "R175",
                "processing_time": "5-10 business days", 
                "required_documents": [
                    "Memorandum of Incorporation",
                    "Notice of incorporation (CoR 14.1)",
                    "Notice of appointment of directors (CoR 14.2)",
                    "Consent to appointment as director (CoR 14.3)",
                    "Proof of payment"
                ]
            },
            "step_3_post_incorporation": {
                "requirements": [
                    "Obtain company registration certificate",
                    "Open company bank account",
                    "Register for tax with SARS",
                    "Obtain tax clearance certificate"
                ]
            }
        }
        
        with open('/home/ubuntu/cipc_registration_checklist.json', 'w') as f:
            json.dump(checklist, f, indent=2)
        
        print("✅ CIPC registration checklist created")
        return checklist

    def sars_tax_registration(self):
        """Generate SARS tax registration requirements"""
        
        tax_registration = {
            "income_tax": {
                "form": "IT77 - Application for registration",
                "deadline": "Within 21 days of incorporation",
                "required_documents": [
                    "Company registration certificate",
                    "Memorandum of incorporation", 
                    "Banking details",
                    "Director ID copies",
                    "Proof of address"
                ]
            },
            "vat_registration": {
                "threshold": "R1,000,000 annual turnover",
                "form": "VAT101 - Application for VAT registration",
                "voluntary_registration": "Available if turnover < R1M",
                "benefits": [
                    "Claim input VAT on business expenses",
                    "Professional credibility",
                    "Required for many B2B transactions"
                ]
            },
            "paye_registration": {
                "required_if": "Employing staff or paying salaries",
                "form": "EMP101 - Employer registration",
                "deadline": "Before first salary payment",
                "obligations": [
                    "Monthly PAYE submissions",
                    "Annual reconciliation",
                    "Employee tax certificates"
                ]
            },
            "uif_registration": {
                "purpose": "Unemployment Insurance Fund",
                "rate": "2% of gross salary (1% employee, 1% employer)",
                "form": "UI-19 - Application for registration",
                "deadline": "Within 7 days of first employee"
            }
        }
        
        with open('/home/ubuntu/sars_tax_registration.json', 'w') as f:
            json.dump(tax_registration, f, indent=2)
        
        print("✅ SARS tax registration guide created")
        return tax_registration

    def fnb_banking_setup(self):
        """Generate FNB business banking setup guide"""
        
        banking_setup = {
            "account_types": {
                "business_current_account": {
                    "monthly_fee": "R95-R295",
                    "features": [
                        "Online banking",
                        "Debit card",
                        "Cheque book",
                        "Monthly statements"
                    ]
                },
                "business_savings_account": {
                    "interest_rate": "Variable",
                    "minimum_balance": "R1,000",
                    "features": [
                        "Interest earning",
                        "Online access",
                        "Limited transactions"
                    ]
                }
            },
            "required_documents": [
                "Company registration certificate (CM1)",
                "Memorandum of incorporation",
                "CIPC certificate of incorporation",
                "Tax clearance certificate",
                "Director ID documents",
                "Proof of business address",
                "Bank resolution (board resolution)",
                "FICA documents for all directors"
            ],
            "merchant_services": {
                "card_processing": {
                    "setup_fee": "R0-R500",
                    "transaction_fees": "2.5%-3.5%",
                    "settlement": "T+1 or T+2"
                },
                "online_payments": {
                    "payfast_integration": "2.9% + R2.00 per transaction",
                    "fnb_pay": "Integrated payment solution",
                    "recurring_billing": "Available for subscriptions"
                }
            },
            "international_payments": {
                "swift_transfers": "Available for international payments",
                "foreign_exchange": "Competitive rates",
                "multi_currency": "USD, EUR, GBP accounts available"
            }
        }
        
        with open('/home/ubuntu/fnb_banking_setup.json', 'w') as f:
            json.dump(banking_setup, f, indent=2)
        
        print("✅ FNB banking setup guide created")
        return banking_setup

    def payment_processing_solutions(self):
        """Generate comprehensive payment processing setup"""
        
        payment_solutions = {
            "local_south_african": {
                "payfast": {
                    "description": "Leading SA payment gateway",
                    "fees": "2.9% + R2.00 per transaction",
                    "supported_methods": ["Credit cards", "EFT", "Bitcoin"],
                    "integration": "API, plugins available",
                    "settlement": "T+1"
                },
                "fnb_merchant_services": {
                    "description": "Direct bank integration",
                    "fees": "2.5%-3.5% depending on volume",
                    "supported_methods": ["Credit cards", "Debit cards"],
                    "integration": "POS, online gateway",
                    "settlement": "T+1 or T+2"
                },
                "paygate": {
                    "description": "Established payment processor",
                    "fees": "2.8% + R1.50 per transaction",
                    "supported_methods": ["Cards", "EFT", "Mobile payments"],
                    "integration": "API, hosted pages",
                    "settlement": "T+1"
                }
            },
            "international_solutions": {
                "stripe": {
                    "description": "Global payment platform",
                    "fees": "2.9% + $0.30 per transaction",
                    "supported_methods": ["Cards", "Digital wallets", "Bank transfers"],
                    "integration": "Comprehensive API",
                    "settlement": "T+2",
                    "note": "Requires Stripe Atlas for SA businesses"
                },
                "wise_business": {
                    "description": "Multi-currency business account",
                    "fees": "0.5%-2% depending on currency",
                    "supported_currencies": "50+ currencies",
                    "integration": "API, direct transfers",
                    "settlement": "Instant to T+1"
                },
                "payoneer": {
                    "description": "Global payment platform",
                    "fees": "1%-3% depending on method",
                    "supported_methods": ["Bank transfers", "Cards", "Digital wallets"],
                    "integration": "API, mass payouts",
                    "settlement": "T+1 to T+3"
                }
            },
            "cryptocurrency": {
                "luno_business": {
                    "description": "SA-based crypto exchange",
                    "fees": "1% trading fee",
                    "supported_currencies": ["Bitcoin", "Ethereum", "XRP"],
                    "integration": "API available",
                    "compliance": "SARB compliant"
                }
            }
        }
        
        with open('/home/ubuntu/payment_processing_solutions.json', 'w') as f:
            json.dump(payment_solutions, f, indent=2)
        
        print("✅ Payment processing solutions guide created")
        return payment_solutions

    def compliance_calendar(self):
        """Generate compliance calendar for ongoing obligations"""
        
        compliance_calendar = {
            "monthly_obligations": {
                "vat_returns": {
                    "due_date": "25th of following month",
                    "penalty": "10% of tax due",
                    "requirement": "If VAT registered"
                },
                "paye_submissions": {
                    "due_date": "7th of following month", 
                    "penalty": "10% of tax due",
                    "requirement": "If employing staff"
                },
                "uif_contributions": {
                    "due_date": "7th of following month",
                    "penalty": "10% of contribution due",
                    "requirement": "If employing staff"
                }
            },
            "annual_obligations": {
                "annual_return_cipc": {
                    "due_date": "Anniversary of incorporation",
                    "fee": "R350",
                    "penalty": "R50 per month late"
                },
                "income_tax_return": {
                    "due_date": "31 October (companies)",
                    "penalty": "R250 per month late",
                    "requirement": "All companies"
                },
                "financial_statements": {
                    "due_date": "With annual return",
                    "requirement": "All companies",
                    "audit_threshold": "R10 million revenue"
                }
            },
            "quarterly_obligations": {
                "provisional_tax": {
                    "due_dates": ["31 August", "28 February"],
                    "penalty": "20% per annum interest",
                    "requirement": "If tax liability > R1,000"
                }
            }
        }
        
        with open('/home/ubuntu/compliance_calendar.json', 'w') as f:
            json.dump(compliance_calendar, f, indent=2)
        
        print("✅ Compliance calendar created")
        return compliance_calendar

    def generate_setup_timeline(self):
        """Generate detailed setup timeline with deadlines"""
        
        today = datetime.now()
        
        timeline = {
            "week_1": {
                "days_1_2": {
                    "tasks": [
                        "Reserve company name with CIPC",
                        "Prepare incorporation documents",
                        "Gather director information and documents"
                    ],
                    "deadline": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R50"
                },
                "days_3_5": {
                    "tasks": [
                        "Submit incorporation application",
                        "Pay incorporation fees",
                        "Wait for CIPC processing"
                    ],
                    "deadline": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R175"
                },
                "days_6_7": {
                    "tasks": [
                        "Receive company registration certificate",
                        "Begin SARS tax registration",
                        "Prepare banking documents"
                    ],
                    "deadline": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R0"
                }
            },
            "week_2": {
                "days_8_10": {
                    "tasks": [
                        "Complete SARS registration",
                        "Apply for VAT registration (if applicable)",
                        "Schedule FNB banking appointment"
                    ],
                    "deadline": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R0"
                },
                "days_11_14": {
                    "tasks": [
                        "Open FNB business account",
                        "Set up merchant services",
                        "Configure online banking",
                        "Obtain tax clearance certificate"
                    ],
                    "deadline": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R500-R1000"
                }
            },
            "week_3": {
                "days_15_21": {
                    "tasks": [
                        "Set up payment processing",
                        "Configure international payment solutions",
                        "Implement compliance systems",
                        "Begin business operations"
                    ],
                    "deadline": (today + timedelta(days=21)).strftime("%Y-%m-%d"),
                    "estimated_cost": "R1000-R2000"
                }
            }
        }
        
        with open('/home/ubuntu/setup_timeline.json', 'w') as f:
            json.dump(timeline, f, indent=2)
        
        print("✅ Setup timeline created")
        return timeline

    def run_complete_setup(self):
        """Execute complete South African business setup process"""
        
        print("🇿🇦 SOUTH AFRICAN BUSINESS SETUP AUTOMATION")
        print("=" * 60)
        print(f"Company: {self.company_name}")
        print(f"Type: {self.business_type}")
        print(f"Industry: {self.industry}")
        print("=" * 60)
        print()
        
        # Generate all required documents and guides
        print("📋 Generating company formation documents...")
        self.generate_company_documents()
        
        print("🏢 Creating CIPC registration checklist...")
        self.cipc_registration_checklist()
        
        print("💰 Preparing SARS tax registration...")
        self.sars_tax_registration()
        
        print("🏦 Setting up FNB banking guide...")
        self.fnb_banking_setup()
        
        print("💳 Configuring payment processing...")
        self.payment_processing_solutions()
        
        print("📅 Creating compliance calendar...")
        self.compliance_calendar()
        
        print("⏰ Generating setup timeline...")
        self.generate_setup_timeline()
        
        print("\n" + "=" * 60)
        print("✅ SOUTH AFRICAN BUSINESS SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("📁 Generated Files:")
        print("   • memorandum_of_incorporation.json")
        print("   • cipc_registration_checklist.json") 
        print("   • sars_tax_registration.json")
        print("   • fnb_banking_setup.json")
        print("   • payment_processing_solutions.json")
        print("   • compliance_calendar.json")
        print("   • setup_timeline.json")
        print()
        print("🚀 Next Steps:")
        print("   1. Review all generated documents")
        print("   2. Begin CIPC name reservation")
        print("   3. Prepare required documentation")
        print("   4. Follow the 3-week setup timeline")
        print()
        print("💡 Estimated Total Setup Cost: R2,000 - R4,000")
        print("⏱️  Estimated Setup Time: 2-3 weeks")
        
        return {
            "status": "setup_complete",
            "company_name": self.company_name,
            "estimated_cost": "R2,000 - R4,000",
            "estimated_time": "2-3 weeks",
            "files_generated": 7
        }

if __name__ == "__main__":
    setup = SouthAfricaBusinessSetup()
    result = setup.run_complete_setup()

