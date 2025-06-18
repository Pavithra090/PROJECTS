class EnhancedRadarVisualizer(RadarVisualizer):
    def __init__(self):
        super().__init__()
        self.figsize = (12, 12)
        self.font_size = 14
        self.colors = plt.cm.viridis(np.linspace(0, 1, 8))  # More color options
        self.background_color = '#f5f5f5'
        self.grid_color = '#dddddd'
        
    def create_individual_radar(self, resume_path, skills, output_path, proficiency_levels=None):
        """Generate enhanced single candidate radar chart with proficiency levels"""
        candidate = os.path.basename(resume_path).replace('.txt', '').replace('_', ' ').title()
        
        # Use provided proficiency levels or extract binary skills
        if proficiency_levels:
            values = proficiency_levels
        else:
            values = self._extract_skills(resume_path, skills)
        
        theta = np.linspace(0, 2*np.pi, len(skills), endpoint=False)
        theta = np.concatenate((theta, [theta[0]]))
        values = np.concatenate((values, [values[0]]))
        
        fig = plt.figure(figsize=self.figsize, facecolor=self.background_color)
        ax = fig.add_subplot(111, projection='radar', facecolor=self.background_color)
        
        # Plot main area
        ax.plot(theta, values, color=self.colors[2], linewidth=3, marker='o', markersize=8)
        ax.fill(theta, values, color=self.colors[2], alpha=0.25)
        
        # Add skill value annotations
        for i, (angle, value) in enumerate(zip(theta[:-1], values[:-1])):
            ax.annotate(f"{value:.1f}", 
                       xy=(angle, value), 
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=self.font_size-2)
        
        # Customize appearance
        ax.set_varlabels([s.title() for s in skills])
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=0)
        ax.spines['polar'].set_visible(True)
        ax.spines['polar'].set_color(self.grid_color)
        ax.grid(color=self.grid_color, linestyle='--', linewidth=0.5)
        
        # Add metadata
        ax.set_title(f"{candidate}\nSkill Assessment", pad=25, 
                    fontsize=self.font_size+4, fontweight='bold')
        
        # Add legend and description
        ax.text(0.5, -0.15, "Proficiency levels: 0 (None) to 1 (Expert)", 
               transform=ax.transAxes, ha='center', fontsize=self.font_size-2)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        
    def create_comparison_chart(self, resume_dir, skills, output_path, proficiency_data=None):
        """Generate enhanced comparison radar chart"""
        fig = plt.figure(figsize=(14, 14), facecolor=self.background_color)
        ax = fig.add_subplot(111, projection='radar', facecolor=self.background_color)
        
        theta = np.linspace(0, 2*np.pi, len(skills), endpoint=False)
        theta = np.concatenate((theta, [theta[0]]))
        
        # If proficiency data is provided, use that instead of binary extraction
        if proficiency_data:
            for idx, (candidate, values) in enumerate(proficiency_data.items()):
                values = np.concatenate((values, [values[0]]))
                ax.plot(theta, values, color=self.colors[idx], 
                       linewidth=2.5, label=candidate, marker='o', markersize=7)
                ax.fill(theta, values, color=self.colors[idx], alpha=0.1)
        else:
            for idx, filename in enumerate([f for f in os.listdir(resume_dir) if f.endswith('.txt')]):
                resume_path = os.path.join(resume_dir, filename)
                values = self._extract_skills(resume_path, skills)
                values = np.concatenate((values, [values[0]]))
                
                candidate = filename.replace('.txt', '').replace('_', ' ').title()
                ax.plot(theta, values, color=self.colors[idx], 
                       linewidth=2.5, label=candidate, marker='o', markersize=7)
                ax.fill(theta, values, color=self.colors[idx], alpha=0.1)
        
        # Enhanced styling
        ax.set_varlabels([s.title() for s in skills], fontsize=self.font_size)
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=0, fontsize=self.font_size-2)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), 
                 fontsize=self.font_size, framealpha=0.9)
        
        ax.spines['polar'].set_visible(True)
        ax.spines['polar'].set_color(self.grid_color)
        ax.grid(color=self.grid_color, linestyle='--', linewidth=0.5)
        
        plt.title("Candidate Skill Comparison\n", pad=40, 
                 fontsize=self.font_size+6, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
