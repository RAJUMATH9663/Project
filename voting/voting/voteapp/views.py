from django.shortcuts import render, redirect
from .models import Candidate

def vote(request):
    candidates = Candidate.objects.all()

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')

        try:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.votes += 1
            candidate.save()
            return redirect('result')
        except Candidate.DoesNotExist:
            return render(request, 'vote.html', {
                'candidates': candidates,
                'error': 'Invalid candidate selected'
            })

    return render(request, 'vote.html', {'candidates': candidates})


def result(request):
    candidates = Candidate.objects.all()
    return render(request, 'result.html', {'candidates': candidates})