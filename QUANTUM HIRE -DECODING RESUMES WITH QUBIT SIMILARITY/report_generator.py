import os
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


class ReportGenerator:
    def __init__(self, logo_path=None):
        """Initialize the report generator with optional logo"""
        self.logo_path = logo_path
        self.styles = self._init_styles()

    def _init_styles(self):
        """Initialize fresh stylesheet with custom styles"""
        styles = StyleSheet1()
        
        # Base styles
        styles.add(ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=10,
            leading=12
        ))
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='ReportTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        styles.add(ParagraphStyle(
            name='SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#003366"),
            spaceBefore=12,
            spaceAfter=8
        ))
        
        styles.add(ParagraphStyle(
            name='BodyTextJustify',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY
        ))
        
        return styles

    def _add_header_footer(self, canvas, doc):
        """Add consistent header/footer to all pages"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        # Add QuantumHire branding
        canvas.drawCentredString(
            letter[0]/2.0, 
            letter[1]-0.5*inch, 
            "QuantumHire Talent Analytics"
        )
        canvas.drawCentredString(
            letter[0]/2.0, 
            0.5*inch, 
            "Confidential - For Internal Use Only"
        )
        canvas.drawRightString(
            letter[0]-0.5*inch, 
            0.5*inch, 
            f"Page {doc.page}"
        )
        canvas.restoreState()

    def _create_summary_table(self, analysis_data):
        """Create the executive summary table with actual data"""
        summary_data = [
            ["Total Candidates Analyzed:", str(analysis_data.get('total_candidates', 0))],
            ["Shortlisted Candidates:", str(analysis_data.get('shortlisted_count', 0))],
            ["Requested Team Size:", str(analysis_data.get('requested_team_size', 0))],
            ["Team Skill Coverage:", f"{analysis_data.get('team_coverage', 0)}%"],
            ["Key Required Skills:", ", ".join(analysis_data.get('required_skills', []))],
            ["Critical Missing Skills:", ", ".join(analysis_data.get('missing_skills', []))]
        ]
        
        table = Table(summary_data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f5f5f5")),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return table

    def _create_candidate_table(self, candidates):
        """Create the top candidates table with actual ranking data"""
        if not candidates or not isinstance(candidates, list):
            return None
            
        candidate_data = [["Rank", "Name", "Score", "Matched Skills"]]
        for idx, candidate in enumerate(candidates[:10], 1):  # Show top 10 candidates
            candidate_data.append([
                str(idx),
                candidate.get('name', 'N/A'),
                f"{candidate.get('score', 0):.1f}%",
                ", ".join(candidate.get('matched_skills', []))
            ])
            
        table = Table(candidate_data, colWidths=[0.5*inch, 1.5*inch, 0.8*inch, 3.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e3f2fd")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.darkblue),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        return table

    def _create_skill_gap_table(self, skill_gaps):
        """Create detailed skill gap analysis table"""
        if not skill_gaps or not isinstance(skill_gaps, list):
            return None
            
        gap_data = [["Candidate", "Missing Skills", "Gap Score"]]
        for gap in skill_gaps[:10]:  # Show top 10 gaps
            gap_data.append([
                gap.get('Candidate', 'N/A'),
                ", ".join(gap.get('missing_skills', [])),
                f"{gap.get('gap_score', 0):.1f}%"
            ])
            
        table = Table(gap_data, colWidths=[1.5*inch, 3*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#fff3e0")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.darkorange),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        return table

    def generate(self, analysis_data, output_dir="outputs/reports"):
        """
        Main method to generate PDF report
        Returns path to generated PDF file
        """
        try:
            # Validate input data
            if not analysis_data:
                raise ValueError("No analysis data provided")
                
            if not isinstance(analysis_data, dict):
                raise ValueError("Analysis data must be a dictionary")
                
            # Create output directory if needed
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Talent_Report_{timestamp}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            # Initialize document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Build story content
            story = []
            
            # Add logo if available
            if self.logo_path and os.path.exists(self.logo_path):
                logo = Image(self.logo_path, width=2*inch, height=0.5*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 12))
            
            # Report title
            story.append(Paragraph(
                "Talent Acquisition Executive Report", 
                self.styles['ReportTitle']
            ))
            story.append(Paragraph(
                f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
                self.styles['Normal']
            ))
            story.append(Spacer(1, 24))
            
            # 1. Executive Summary
            story.append(Paragraph(
                "1. Executive Summary", 
                self.styles['SectionTitle']
            ))
            story.append(self._create_summary_table(analysis_data))
            story.append(Spacer(1, 24))
            
            # 2. Top Candidates
            candidates = analysis_data.get('top_candidates', [])
            if candidates:
                story.append(Paragraph(
                    "2. Top Candidates", 
                    self.styles['SectionTitle']
                ))
                candidate_table = self._create_candidate_table(candidates)
                if candidate_table:
                    story.append(candidate_table)
                    story.append(Spacer(1, 24))
            
            # 3. Skill Gap Analysis
            skill_gaps = analysis_data.get('skill_gaps', [])
            if skill_gaps:
                story.append(Paragraph(
                    "3. Skill Gap Analysis", 
                    self.styles['SectionTitle']
                ))
                gap_table = self._create_skill_gap_table(skill_gaps)
                if gap_table:
                    story.append(gap_table)
                    story.append(Spacer(1, 24))
            
            # 4. Recommendations
            story.append(Paragraph(
                "4. Strategic Recommendations", 
                self.styles['SectionTitle']
            ))
            
            recommendations = [
                "✅ <b>Hiring Focus:</b> Prioritize candidates strong in " + 
                ", ".join(analysis_data.get('required_skills', ['key technologies'])),
                
                "📚 <b>Training Needs:</b> Develop programs for " + 
                ", ".join(analysis_data.get('missing_skills', ['critical skill gaps'])),
                
                "🔄 <b>Team Composition:</b> Balance skills across " + 
                f"{analysis_data.get('requested_team_size', 'the team')} members",
                
                "📈 <b>Development:</b> Create personalized learning paths for skill gaps"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(rec, self.styles['BodyTextJustify']))
                story.append(Spacer(1, 8))
            
            # Build the PDF document
            doc.build(
                story, 
                onFirstPage=self._add_header_footer, 
                onLaterPages=self._add_header_footer
            )
            
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF report: {str(e)}")
            raise

    # Alias for compatibility
    create_pdf = generate
