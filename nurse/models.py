from django.db import models
from django.utils import timezone

# ═══════════════════════════════════════
# VITAL SIGNS
# ═══════════════════════════════════════
class VitalSign(models.Model):
    date_time = models.DateTimeField(default=timezone.now)
    label = models.CharField(max_length=100, blank=True)
    bp = models.CharField(max_length=20, blank=True)
    hr = models.CharField(max_length=20, blank=True)
    temp = models.CharField(max_length=20, blank=True)
    spo2 = models.CharField(max_length=20, blank=True)
    bgl = models.CharField(max_length=20, blank=True)
    rr = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Vitals {self.label} - {self.date_time}"

# ═══════════════════════════════════════
# HEALTH JOURNAL
# ═══════════════════════════════════════
class JournalEntry(models.Model):
    date = models.DateField(default=timezone.now)
    sleep_hours = models.FloatField(default=7)
    energy = models.CharField(max_length=50, blank=True)
    water_glasses = models.IntegerField(default=8)
    nutrition = models.TextField(blank=True)
    feelings = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Journal - {self.date}"

# ═══════════════════════════════════════
# STRESS LOG
# ═══════════════════════════════════════
class StressLog(models.Model):
    date = models.DateField(default=timezone.now)
    groupmates_level = models.IntegerField(default=0)
    groupmates_note = models.TextField(blank=True)
    overall_level = models.IntegerField(default=3)
    notes = models.TextField(blank=True)
    what_helped = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Stress Log - {self.date}"

# ═══════════════════════════════════════
# SELF CARE
# ═══════════════════════════════════════
class SelfCareLog(models.Model):
    date = models.DateField(default=timezone.now)
    completed_items = models.TextField(blank=True)
    total_completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Self Care - {self.date}"

# ═══════════════════════════════════════
# DAILY ROUTINE
# ═══════════════════════════════════════
class DailyRoutine(models.Model):
    ROUTINE_TYPES = [
        ('morning', '☀️ Morning'),
        ('study', '📚 Study'),
        ('night', '🌙 Night'),
    ]
    routine_type = models.CharField(max_length=20, choices=ROUTINE_TYPES)
    task_name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.routine_type} - {self.task_name}"

# ═══════════════════════════════════════
# LOVE LETTER
# ═══════════════════════════════════════
class LoveLetter(models.Model):
    content = models.TextField()
    unlock_date = models.DateField(default='2026-03-22')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Love Letter - unlocks {self.unlock_date}"
    
    # ═══════════════════════════════════════
# GOALS & ACHIEVEMENTS
# ═══════════════════════════════════════
class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('nursing', '🩺 Nursing'),
        ('personal', '🌸 Personal'),
        ('relationship', '💕 Relationship'),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    target_date = models.DateField(null=True, blank=True)
    total_steps = models.IntegerField(default=5)
    completed_steps = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['target_date', 'created_at']

    def __str__(self):
        return f"{self.category} - {self.title}"

    def progress_percentage(self):
        if self.total_steps == 0:
            return 0
        return int((self.completed_steps / self.total_steps) * 100)

# ═══════════════════════════════════════
# MONTHLY WELLNESS SUMMARY
# ═══════════════════════════════════════
class WellnessSummary(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    avg_sleep = models.FloatField(default=0)
    total_water = models.IntegerField(default=0)
    avg_stress = models.FloatField(default=0)
    selfcare_rate = models.FloatField(default=0)
    vitals_count = models.IntegerField(default=0)
    journal_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-month']

    def __str__(self):
        return f"Wellness {self.month}/{self.year}"