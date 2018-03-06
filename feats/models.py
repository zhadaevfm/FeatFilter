from django.db import models


class FeatType(models.Model):
    name = models.CharField(null=False, max_length=32)


class Race(models.Model):
    name = models.CharField(null=False, max_length=32)


class Trait(models.Model):
    name = models.CharField(null=False, max_length=32)


class Skill(models.Model):
    name = models.CharField(null=False, max_length=32)


class ClassFeature(models.Model):
    name = models.CharField(null=False, max_length=32)


class Class(models.Model):
    name = models.CharField(null=False, max_length=32)
    features = models.ManyToManyField(ClassFeature)


class Feat(models.Model):
    ARCANE = "A"
    DIVINE = "D"
    MAGIC_TYPES = (
        (ARCANE, "Arcane"),
        (DIVINE, "Divine"),
    )
    name = models.CharField(null=False, max_length=64)
    feat_type = models.ForeignKey(FeatType, on_delete=models.CASCADE)
    benefit = models.TextField()
    normal = models.TextField()
    special = models.CharField(max_length=64, blank=True)
    note = models.TextField()
    full_text = models.TextField()
    goal = models.TextField()
    completion_benefit = models.TextField()
    suggested_traits = models.ManyToManyField(Trait, blank=True)

    req_dex = models.IntegerField(null=True, default=None)
    req_str = models.IntegerField(null=True, default=None)
    req_con = models.IntegerField(null=True, default=None)
    req_int = models.IntegerField(null=True, default=None)
    req_wis = models.IntegerField(null=True, default=None)
    req_cha = models.IntegerField(null=True, default=None)

    req_bab = models.IntegerField(null=True, default=None)
    req_lvl = models.IntegerField(null=True, default=None)

    req_feats = models.ManyToManyField("self", blank=True, symmetrical=False)
    req_races = models.ManyToManyField(Race, blank=True)
    req_skills = models.ManyToManyField(Skill, through="RequiredSkill")
    req_classes = models.ManyToManyField(Class, blank=True)
    req_class_features = models.ManyToManyField(ClassFeature, blank=True)
    req_traits = models.ManyToManyField(Trait, blank=True)

    caster_lvl = models.IntegerField(null=True, default=None)
    caster_type = models.CharField(max_length=1, choices=MAGIC_TYPES,
                                   blank=True)
    spell_lvl = models.IntegerField(null=True, default=None)
    spell_type = models.CharField(max_length=1, choices=MAGIC_TYPES,
                                  blank=True)

    teamwork = models.BooleanField(null=False, default=False)
    critical = models.BooleanField(null=False, default=False)
    grit = models.BooleanField(null=False, default=False)
    style = models.BooleanField(null=False, default=False)
    performance = models.BooleanField(null=False, default=False)
    racial = models.BooleanField(null=False, default=False)
    companion_familiar = models.BooleanField(null=False, default=False)
    multiples = models.BooleanField(null=False, default=False)


class RequiredSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,
                              related_name='+')
    feat = models.ForeignKey(Feat, on_delete=models.CASCADE)
    ranks = models.IntegerField(default=0, null=False)
