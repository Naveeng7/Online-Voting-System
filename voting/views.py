from django.shortcuts import render, redirect
from voting.models import positions
from voting.models import candidates
from django.contrib.auth.models import User
from voting.models import voted
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from news.models import Post

# Create your views here.
@login_required()
def voting(request):
    pval = None
    ceval = None
    if request.method == 'POST':
        if 'posval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
        if 'canval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['canval']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates.objects.filter(pname=pval, cname=cval).first()
            voter = request.POST['voter']
            voter = User.objects.filter(username=voter).first()

            v1 = voted(user=voter, pname=pval)
            yo = v1.save()
            if yo == True:
                candidates.objects.filter(id=ceval.id).update(cvotes=ceval.cvotes + 1)
                messages.info(request, f'You have successfully voted { cval } for the posistion { pval }')
            else:
                messages.info(request, f'You have already voted for the posistion { pval }')

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval
    }
    return render(request, 'voting/v_base.html', context)



@user_passes_test(lambda u: u.is_superuser)
def mpos(request):
    if request.method == 'POST':
        if 'posval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            try:
                pval.delete()
            except Exception:
                messages.info(request, f'Please Try Again')
                return redirect('addndel')
            messages.info(request, f'{pval} removed form voting system ')
        if 'posadd' in request.POST:
            pval = request.POST['posadd']
            if len(pval) == 0:
                return redirect('addndel')
            pval = pval.capitalize()
            pval = positions(pname=pval)
            pval.save()
            messages.info(request, f'{pval} has successfully added to positions')

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'voting/mpos.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cadd(request):
    msg = ''
    if request.method == 'POST':
        if 'canadd' in request.POST:
            try:
                pval = request.POST['canadd']
                pval = positions.objects.filter(pname=pval).first()
                cval = request.POST['candadd']
                cval = User.objects.filter(username=cval).first()
                ceval = candidates(pname=pval, cname=cval)
                msg = ceval.save()
            except Exception:
                messages.info(request, f'Please select both position and candidate')
                return redirect('addcand')
    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'users': User.objects.all(),
        'msg': msg
    }
    return render(request, 'voting/cadd.html', context)



@user_passes_test(lambda u: u.is_superuser)
def cdel(request):
    pval = None
    ceval = None
    if request.method == 'POST':
        if 'candel' in request.POST:
            pval = request.POST['candel']
            pval = positions.objects.filter(pname=pval).first()
        if 'canval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['canval']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates.objects.filter(pname=pval, cname=cval).first()
            try:
                ceval.delete()
            except Exception:
                messages.info(request, f'The selected candidate doesn\'t exist')
                return redirect('delcand')
            messages.info(request, f'{ cval } is removed from the position { pval }')

            flag = 0
            for val in candidates.objects.all():
                if val.cname.id == cval.id:
                    flag = 1
            if flag == 1:
                cval.profile.cpost='Yes'
                cval.save()
            else:
                cval.profile.cpost='No'
                cval.save()

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval
    }

    return render(request, 'voting/cdel.html', context)



@user_passes_test(lambda u: u.is_superuser)
def cres(request):
    canpos = None
    msg = ''
    str = ''
    if request.method == 'POST':
        if 'canpos' in request.POST:
            canpos = request.POST['canpos']
            canpos = positions.objects.filter(pname=canpos).first()

            mv = 0
            str = str + 'The candidates '
            for can in candidates.objects.all():
                if canpos.id == can.pname.id:
                    str = str + f' {can.cname}'
                    if mv < can.cvotes:
                        mv = can.cvotes
                        id = can.cname
            if mv > 0:
                str = str +f' were competing for the position {canpos} and the winner is {id} with total number of votes is {mv}'

        if 'title' in request.POST:
            title = request.POST['title']
            content = request.POST['content']
            if len(title) == 0 or len(content) <= 16:
                messages.info(request, f'Noting to Post')
                return redirect('rescand')
            p = Post(title=title, content=content, author=request.user)
            p.save()
            return redirect('home')

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'canpos': canpos,
        'msg': msg,
        'str': str
    }

    return render(request, 'voting/cres.html', context)
