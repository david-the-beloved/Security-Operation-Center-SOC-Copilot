from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Corporate Security & IT Policy - 2026', 0, 1, 'C')
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

policy_text = """
1. VENDOR COMPLIANCE: All external cloud vendors must be pre-approved by the IT Risk Management team.

2. SHADOW IT: Any network traffic originating from unauthorized IP addresses must be immediately flagged as a Critical Shadow IT violation.

3. PHISHING PROTOCOL: If an employee clicks a link matching a known malicious domain in the enterprise database, their Okta SSO session must be revoked immediately.

4. ALLOWED TOOLS: Employees are only permitted to use GitHub Enterprise, Microsoft Office 365, and approved AWS environments. Personal Notion or ChatGPT accounts are strictly prohibited on company networks to prevent data exfiltration.
"""

pdf.multi_cell(0, 10, policy_text)
pdf.output('corporate_policy.pdf')
print("corporate_policy.pdf generated successfully!")