from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class positions(models.Model):
    pname = models.CharField(max_length=25)

    def __str__(self):
        return self.pname

    def save(self, *args, **kwargs):
        pvals = positions.objects.all()
        for p in pvals:
            if self.pname == p.pname:
                return f'Position {p} already exists'
        super(positions, self).save(*args, **kwargs)
        return f'{ self.pname } is successfully added to positions'


class candidates(models.Model):
    pname = models.ForeignKey(positions, on_delete=models.CASCADE)
    cname = models.ForeignKey(User, on_delete=models.CASCADE)
    cvotes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pname,self.cname,self.cvotes}'

    def save(self, *args, **kwargs):
        cpval = User.objects.filter(username=self.cname).first()
        cvals = candidates.objects.all()
        for c in cvals:
            if c.cname == self.cname and c.pname == self.pname:
                return f'The candidate { self.cname } is already standing for this position { self.pname }'
        super(candidates, self).save(*args, **kwargs)
        cpval.profile.cpost='Yes'
        cpval.save()
        return f'candidate { self.cname } is competing for the position { self.pname }'


class voted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pname = models.ForeignKey(positions, on_delete=models.CASCADE)

    def __str__(self):
        return f'{ self.user } votes position { self.pname }'

    def save(self,*args, **kwargs):
        vvals = voted.objects.all()
        for v in vvals:
            if v.user == self.user and v.pname == self.pname:
                return f'You { self.user } have already voted for this position: { self.pname }'
        print('vote submitted')
        super(voted, self).save(*args, **kwargs)
        return True