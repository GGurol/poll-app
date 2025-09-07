from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from django.http import HttpResponse

@login_required
def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = request.GET.get('search', '')

    # Apply filtering and sorting
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')
    elif 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')
    elif 'vote' in request.GET:
        all_polls = all_polls.annotate(vote_count=Count('vote')).order_by('vote_count')

    if search_term:
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)
    page_number = request.GET.get('page')
    polls = paginator.get_page(page_number)

    # Preserve search/filter parameters during pagination
    params = request.GET.copy()
    if 'page' in params:
        del params['page']

    context = {
        'polls': polls,
        'params': params.urlencode(),
        'search_term': search_term,
    }
    return render(request, 'polls/polls_list.html', context)

@login_required
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)
    page_number = request.GET.get('page')
    polls = paginator.get_page(page_number)
    return render(request, 'polls/polls_list.html', {'polls': polls})

@login_required
def polls_add(request):
    if not request.user.has_perm('polls.add_poll'):
        return HttpResponse("Sorry, you don't have permission to do that!", status=403)

    if request.method == 'POST':
        form = PollAddForm(request.POST)
        # CORRECTED: is_valid is a method, must be called with ()
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            # Create choices from the form
            Choice.objects.create(poll=poll, choice_text=form.cleaned_data['choice1'])
            Choice.objects.create(poll=poll, choice_text=form.cleaned_data['choice2'])
            messages.success(request, "Poll and Choices added successfully.")
            return redirect('polls:list')
    else:
        form = PollAddForm()
        
    return render(request, 'polls/add_poll.html', {'form': form})

@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, owner=request.user)
    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        # CORRECTED: is_valid is a method
        if form.is_valid():
            form.save()
            messages.success(request, "Poll updated successfully.")
            return redirect("polls:list")
    else:
        form = EditPollForm(instance=poll)
    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})

@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, owner=request.user)
    # CORRECTED (Security): Only delete on POST request
    if request.method == 'POST':
        poll.delete()
        messages.success(request, "Poll deleted successfully.")
        return redirect("polls:list")
    # For GET request, show a confirmation page
    return render(request, "polls/poll_confirm_delete.html", {'poll': poll})

@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, owner=request.user)
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        # CORRECTED: is_valid is a method
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, "Choice added successfully.")
            return redirect('polls:edit', poll_id=poll.id)
    else:
        form = ChoiceAddForm()
    return render(request, 'polls/add_choice.html', {'form': form, 'poll': poll})

@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        # CORRECTED: is_valid is a method
        if form.is_valid():
            form.save()
            messages.success(request, "Choice updated successfully.")
            return redirect('polls:edit', poll_id=poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)

@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')
    # CORRECTED (Security): Only delete on POST request
    if request.method == 'POST':
        choice.delete()
        messages.success(request, "Choice deleted successfully.")
        return redirect('polls:edit', poll_id=poll.id)
    # For GET request, show a confirmation page
    return render(request, "polls/choice_confirm_delete.html", {'choice': choice})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})

    # Kullanıcının bu anket için oyunu veritabanından bulmaya çalış
    user_vote = None
    if request.user.is_authenticated:
        # get() metodu bir kayıt bulamazsa DoesNotExist hatası verir, bunu yakalıyoruz
        try:
            user_vote = Vote.objects.get(user=request.user, poll=poll)
        except Vote.DoesNotExist:
            user_vote = None # Eğer oy yoksa, değişken None olarak kalır

    context = {
        'poll': poll,
        'user_vote': user_vote, # Kullanıcının oyunu (veya None) şablona gönder
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')

    if not poll.user_can_vote(request.user):
        messages.error(request, "You have already voted on this poll!")
        return redirect("polls:list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        Vote.objects.create(user=request.user, poll=poll, choice=choice)
        # CORRECTED (Best Practice): Redirect after a successful POST
        return redirect('polls:result', poll_id=poll.id)
    else:
        messages.error(request, "No choice selected!")
        return redirect("polls:detail", poll_id=poll_id)

# It's good practice to have a separate view for results
def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/poll_result.html', {'poll': poll})

@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, owner=request.user)
    if poll.active:
        poll.active = False
        poll.save()
    # CORRECTED (Best Practice): Redirect after the action
    return redirect('polls:result', poll_id=poll.id)