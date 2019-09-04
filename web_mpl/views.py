from django.shortcuts import render
from matplotlib._pylab_helpers import Gcf
import matplotlib.pyplot as plt
from .models import MplFigure

def example(request):
	# fig, ax = plt.subplots(num="test")
	fig = plt.figure(num="test")
	fig_id = fig.canvas.manager.num
	plt.savefig('fig_at_views.png')


	context = {
		'mpl_fig_id': fig_id,
	}

	return render(request, 'example.html', context)
