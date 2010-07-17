from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.conf import settings
from web.nodes.models import Node
from web.generator.models import Profile
from web.generator.queue import queue_generator_job
from web.generator.forms import GenerateImageForm

@login_required
def request(request, node):
  """
  Displays a confirmation form.
  """
  node = get_object_or_404(Node, pk = node)
  if node.owner != request.user and not request.user.is_staff:
    raise Http404

  try:
    profile = node.profile
  except Profile.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = GenerateImageForm(request.POST)
    if form.is_valid():

      if getattr(settings, 'ENABLE_IMAGE_GENERATOR', None) and not getattr(settings, 'IMAGE_GENERATOR_SUSPENDED', None):
        email_user = form.save(node)
        queue_generator_job(node, email_user, form.cleaned_data['config_only'])

      return render_to_response('generator/please_wait.html',
        { 'node' : node,
          'image_generator_enabled' : getattr(settings, 'ENABLE_IMAGE_GENERATOR', None),
          'image_generator_suspended' : getattr(settings, 'IMAGE_GENERATOR_SUSPENDED', None) },
        context_instance = RequestContext(request)
      )
  else:
    form = GenerateImageForm(initial = {
      'email_user'  : node.owner.id
    })

  return render_to_response('generator/generate.html',
    { 'node'  : node,
      'form'  : form },
    context_instance = RequestContext(request)
  )
