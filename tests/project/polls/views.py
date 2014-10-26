
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from scenic import all as sc

from .models import Choice, Poll


def create_main_index():

    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/main-index.html', sc.DictContext({})),
                )
            )

main_index = create_main_index()


def create_index():
    context = sc.DictContext({
        'latest_poll_list': sc.LiteralValue(Poll.objects.all().order_by('-pub_date')[:5])
        })
    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/index.html', context),
                )
            )

index = create_index()


def create_detail():
    context = sc.DictContext({
        'poll': sc.SingleObject('poll_id', 'poll', Poll.objects)
        })
    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/detail.html', context),
                )
            )

detail = create_detail()

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))


def create_results():
    context = sc.DictContext({
        'poll': sc.SingleObject('poll_id', 'poll', Poll.objects)
        })
    return sc.View(
            sc.TemplateHandler(
                sc.Template('polls/results.html', context),
                )
            )

results = create_results()

